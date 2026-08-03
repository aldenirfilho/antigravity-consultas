"use strict";

const assert = require("assert");
const path = require("path");

const root = path.resolve(__dirname, "..");
const moduleRoot = path.join(root, "01_Modulos_Clinicos", "Sepse_Choque_Septico");
require(path.join(moduleRoot, "data", "acra-bundle.js"));
require(path.join(moduleRoot, "assets", "acra-runtime.js"));
require(path.join(moduleRoot, "assets", "acra-controller.js"));

const bundle = global.SEPSE_ACRA_BUNDLE;
const runtime = global.SepsisAcraRuntime;
const controllerApi = global.SepsisAcraController;

const valid = runtime.validateBundle(bundle);
assert.strictEqual(valid.ok, true);
assert.strictEqual(valid.artifacts.length, 10);
assert.strictEqual(new Set(valid.artifacts.map((item) => item.id)).size, 10);
assert(Object.isFrozen(bundle));
assert(Object.isFrozen(bundle.entries));

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

const badVersion = clone(bundle);
badVersion.entries[0].artifact.version = "2.0";
assert.strictEqual(runtime.validateBundle(badVersion).ok, false);

const badComponent = clone(bundle);
badComponent.entries[0].artifact.components[0].type = "remoteClinicalWidget";
assert.strictEqual(runtime.validateBundle(badComponent).ok, false);

const badUrl = clone(bundle);
badUrl.entries[0].artifact.sources[0].url = "http://example.test/fonte";
assert.strictEqual(runtime.validateBundle(badUrl).ok, false);

const badAction = clone(bundle);
badAction.entries[0].artifact.actions[0].requiresPreview = false;
assert.strictEqual(runtime.validateBundle(badAction).ok, false);

const unknownProperty = clone(bundle);
unknownProperty.entries[0].artifact.remotePrompt = "executar";
assert.strictEqual(runtime.validateBundle(unknownProperty).ok, false);

const duplicateId = clone(bundle);
duplicateId.entries[0].artifact.components[0].id = duplicateId.entries[0].artifact.id;
assert.strictEqual(runtime.validateBundle(duplicateId).ok, false);

assert.strictEqual(runtime.safeHttpsUrl("javascript:alert(1)"), "");
assert.strictEqual(runtime.safeHttpsUrl("http://example.test"), "");
assert.strictEqual(runtime.safeHttpsUrl("https://example.test/path"), "https://example.test/path");

class FakeNode {
  constructor(dataset = {}) {
    this.dataset = { ...dataset };
    this.hidden = false;
    this.disabled = false;
    this.open = false;
    this.textContent = "";
    this.listeners = new Map();
    this.attributes = new Map();
    this.parentNode = null;
  }

  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, new Set());
    this.listeners.get(type).add(listener);
  }

  removeEventListener(type, listener) {
    if (this.listeners.has(type)) this.listeners.get(type).delete(listener);
  }

  dispatch(type, event = {}) {
    Array.from(this.listeners.get(type) || []).forEach((listener) => listener(event));
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  getAttribute(name) {
    return this.attributes.has(name) ? this.attributes.get(name) : null;
  }

  showModal() {
    this.open = true;
    this.hidden = false;
  }

  close() {
    this.open = false;
  }

  remove() {
    this.removed = true;
  }
}

class FakeScope extends FakeNode {
  constructor(nodes) {
    super();
    this.nodes = nodes;
  }

  querySelectorAll(selector) {
    const map = {
      "[data-acra-mode]": this.nodes.modeButtons,
      ".acra-slot[data-acra-id], .acra-slot[data-artifact-id]": this.nodes.slots,
      "[data-acra-open]": this.nodes.openButtons,
      "[data-acra-clear]": this.nodes.clearButtons,
      "[data-acra-close]": this.nodes.closeButtons,
      '[data-acra-generated="true"]': []
    };
    return map[selector] || [];
  }

  querySelector(selector) {
    if (selector === "[data-acra-status]") return this.nodes.status;
    if (selector === "[data-acra-stage]") return this.nodes.stage;
    return null;
  }
}

class FakeObserver {
  static instances = [];

  constructor(callback, options) {
    this.callback = callback;
    this.options = options;
    this.observed = new Set();
    this.disconnected = false;
    FakeObserver.instances.push(this);
  }

  observe(node) {
    this.observed.add(node);
  }

  unobserve(node) {
    this.observed.delete(node);
  }

  disconnect() {
    this.disconnected = true;
    this.observed.clear();
  }

  intersect(node) {
    this.callback([{ isIntersecting: true, target: node }]);
  }
}

function makeStorage(initial = {}) {
  const values = new Map(Object.entries(initial));
  return {
    values,
    getItem(key) { return values.has(key) ? values.get(key) : null; },
    setItem(key, value) { values.set(key, String(value)); },
    removeItem(key) { values.delete(key); }
  };
}

function makeFixture() {
  const artifactId = valid.artifacts[0].id;
  const nodes = {
    clearButtons: [new FakeNode()],
    closeButtons: [new FakeNode()],
    modeButtons: [
      new FakeNode({ acraMode: "sem-acra" }),
      new FakeNode({ acraMode: "parcial" }),
      new FakeNode({ acraMode: "auto" })
    ],
    openButtons: [new FakeNode({ acraId: artifactId })],
    slots: [new FakeNode({ acraId: artifactId })],
    stage: new FakeNode(),
    status: new FakeNode()
  };
  return { artifactId, nodes, scope: new FakeScope(nodes) };
}

const fixture = makeFixture();
const storage = makeStorage();
const mountCalls = [];
let unmounts = 0;
const runtimePort = {
  validateBundle: runtime.validateBundle,
  mount(request) {
    mountCalls.push(request);
    return {
      ok: true,
      handle: {
        unmount() { unmounts += 1; return true; }
      }
    };
  }
};
const controller = controllerApi.create({
  bundle,
  document: {},
  IntersectionObserver: FakeObserver,
  runtime: runtimePort,
  scope: fixture.scope,
  storage
});
controller.start();
assert.strictEqual(controller.getMode(), "PARCIAL");
assert.strictEqual(mountCalls.length, 0, "montagem deve aguardar interseção");
assert.strictEqual(FakeObserver.instances.length, 1);
FakeObserver.instances.at(-1).intersect(fixture.nodes.slots[0]);
assert.strictEqual(mountCalls.length, 1);
assert.strictEqual(mountCalls[0].variant, "partial");

const savedProgress = JSON.parse(storage.values.get(controllerApi.progressKey));
assert.deepStrictEqual(Object.keys(savedProgress).sort(), ["answeredIds", "checkedIds", "visitedIds"]);
assert(savedProgress.visitedIds.includes(fixture.artifactId));
assert(!storage.values.get(controllerApi.progressKey).includes(valid.artifacts[0].title));

assert.strictEqual(controller.setMode("AUTO"), false, "AUTO programático deve falhar fechado");
assert.strictEqual(controller.getMode(), "PARCIAL");
assert.strictEqual(controller.setMode("AUTO", { persist: true, userInitiated: true }), true);
assert.strictEqual(storage.values.get(controllerApi.modeKey), "AUTO");
assert.strictEqual(controller.getMode(), "AUTO");
assert(unmounts >= 1);
FakeObserver.instances.at(-1).intersect(fixture.nodes.slots[0]);
assert.strictEqual(mountCalls.at(-1).variant, "full");

assert.strictEqual(controller.setMode("OFF", { persist: true, userInitiated: true }), true);
assert.strictEqual(controller.getMode(), "OFF");
assert.strictEqual(storage.values.get(controllerApi.modeKey), "OFF");
assert.strictEqual(fixture.nodes.slots[0].hidden, true);
assert.strictEqual(FakeObserver.instances.at(-1).disconnected, true);

controller.clearProgress();
assert.strictEqual(storage.values.has(controllerApi.progressKey), false);
controller.stop();

const restoredFixture = makeFixture();
const restoredStorage = makeStorage({ [controllerApi.modeKey]: "AUTO" });
const restored = controllerApi.create({
  bundle,
  document: {},
  IntersectionObserver: FakeObserver,
  runtime: runtimePort,
  scope: restoredFixture.scope,
  storage: restoredStorage
});
restored.start();
assert.strictEqual(restored.getMode(), "AUTO", "AUTO persistido representa opt-in anterior");
restored.stop();

const fallbackFixture = makeFixture();
const fallback = controllerApi.create({
  bundle: {},
  document: {},
  IntersectionObserver: FakeObserver,
  runtime,
  scope: fallbackFixture.scope,
  storage: makeStorage()
});
fallback.start();
assert.strictEqual(fallback.isFallback(), true);
assert.strictEqual(fallback.getMode(), "OFF");
assert(fallbackFixture.nodes.status.textContent.includes("conteúdo convencional"));
assert.strictEqual(fallbackFixture.nodes.modeButtons[2].disabled, true);
fallback.stop();

assert.strictEqual(controllerApi.normalizeMode("sem-acra"), "OFF");
assert.strictEqual(controllerApi.normalizeMode("parcial"), "PARCIAL");
assert.strictEqual(controllerApi.normalizeMode("auto"), "AUTO");
assert.deepStrictEqual(
  controllerApi.sanitizeProgress({ visitedIds: [fixture.artifactId], freeText: "paciente" }),
  {
    answeredIds: [],
    checkedIds: [],
    visitedIds: []
  },
  "propriedade fora da allowlist deve limpar o progresso"
);

process.stdout.write("PASS sepsis-acra-offline-smoke\n");
