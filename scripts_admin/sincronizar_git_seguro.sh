#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
EXPECTED_REPOSITORY="aldenirfilho/antigravity-consultas"

finish() {
  local exit_code=$?
  if [[ -t 0 ]]; then
    printf '\nPressione Enter para fechar.'
    read -r _
  fi
  exit "${exit_code}"
}
trap finish EXIT

cd "${PROJECT_ROOT}"

printf '🔄 Antigravity · sincronização Git segura\n'
printf '📁 Pasta: %s\n\n' "${PROJECT_ROOT}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '❌ Esta pasta não é um repositório Git.\n' >&2
  exit 10
fi

remote_url="$(git remote get-url origin 2>/dev/null || true)"
if [[ "${remote_url}" != *"${EXPECTED_REPOSITORY}"* ]]; then
  printf '❌ O remote origin não corresponde ao projeto esperado.\n' >&2
  printf '   Encontrado: %s\n' "${remote_url:-ausente}" >&2
  exit 11
fi

if [[ -n "$(git status --porcelain=v1)" ]]; then
  printf '⛔ Sincronização interrompida: existem mudanças locais.\n'
  printf '   Revise, faça commit ou peça ajuda antes de atualizar.\n\n'
  git status --short --branch
  exit 20
fi

current_branch="$(git branch --show-current)"
if [[ -z "${current_branch}" ]]; then
  printf '❌ O repositório está sem uma branch ativa (detached HEAD).\n' >&2
  exit 21
fi

printf '🌿 Branch atual: %s\n' "${current_branch}"
printf '📡 Buscando atualizações do GitHub…\n'
git fetch --prune origin

if [[ "${current_branch}" == "main" ]]; then
  printf '⬇️ Atualizando main somente por fast-forward…\n'
  git pull --ff-only origin main
  read -r local_only remote_only < <(
    git rev-list --left-right --count HEAD...origin/main
  )
  if [[ "${local_only}" != "0" || "${remote_only}" != "0" ]]; then
    printf '❌ A main ainda diverge da origin/main. Peça uma revisão.\n' >&2
    exit 30
  fi
  printf '\n✅ main sincronizada com o GitHub.\n'
  printf '➡️ Próximo passo: crie uma branch própria antes de editar.\n'
else
  read -r local_only remote_only < <(
    git rev-list --left-right --count HEAD...origin/main
  )
  printf '\nℹ️ Branch de trabalho preservada; nenhuma integração automática foi feita.\n'
  printf '   Commits exclusivos desta branch: %s\n' "${local_only}"
  printf '   Commits novos existentes na main: %s\n' "${remote_only}"
  printf '➡️ Faça commit/push ou peça ajuda para atualizar a branch com segurança.\n'
fi
