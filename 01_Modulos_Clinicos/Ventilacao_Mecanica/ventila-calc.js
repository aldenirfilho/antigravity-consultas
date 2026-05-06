// Lógica Clínica - Ventila-Calc
// Arquivo gerado para a Enciclopédia Antigravity

// 1. Peso Corporal Ideal (Devine)
function calcularPCI() {
    const sexo = document.querySelector('input[name="pci_sexo"]:checked').value;
    const altura = parseFloat(document.getElementById('pci_altura').value);

    if (!altura || altura < 100 || altura > 250) {
        document.getElementById('out_pci').innerText = "--";
        document.getElementById('out_vt4').innerText = "--";
        document.getElementById('out_vt6').innerText = "--";
        document.getElementById('out_vt8').innerText = "--";
        return;
    }

    const base = sexo === 'M' ? 50 : 45.5;
    const pci = base + 0.91 * (altura - 152.4);

    document.getElementById('out_pci').innerText = pci.toFixed(1);
    document.getElementById('out_vt4').innerText = (pci * 4).toFixed(0);
    document.getElementById('out_vt6').innerText = (pci * 6).toFixed(0);
    document.getElementById('out_vt8').innerText = (pci * 8).toFixed(0);
}

// 2. Mecânica Respiratória
function calcularMecanica() {
    const vt = parseFloat(document.getElementById('mec_vt').value);
    const ppico = parseFloat(document.getElementById('mec_pico').value);
    const pplat = parseFloat(document.getElementById('mec_plat').value);
    const peep = parseFloat(document.getElementById('mec_peep').value);

    const alertDp = document.getElementById('alert_dp');
    const alertCst = document.getElementById('alert_cst');
    const alertPlat = document.getElementById('alert_plat');
    
    // Reset
    alertDp.style.display = 'none'; alertCst.style.display = 'none'; alertPlat.style.display = 'none';
    document.getElementById('out_dp').innerText = '--';
    document.getElementById('out_cst').innerText = '--';
    document.getElementById('out_plat_status').innerText = pplat ? pplat : '--';

    if (pplat && peep) {
        const dp = pplat - peep;
        document.getElementById('out_dp').innerText = dp.toFixed(0);
        
        alertDp.style.display = 'block';
        if (dp > 15) {
            alertDp.className = 'alert-box alert-danger';
            alertDp.innerText = '🔴 REDUZIR Vt! ΔP > 15 (Risco VILI)';
        } else {
            alertDp.className = 'alert-box alert-success';
            alertDp.innerText = '✅ Protetor (≤ 15)';
        }

        if (vt) {
            const cst = vt / dp;
            document.getElementById('out_cst').innerText = cst.toFixed(0);
            
            alertCst.style.display = 'block';
            if (cst < 25) {
                alertCst.className = 'alert-box alert-danger';
                alertCst.innerText = '🔴 SARA GRAVE (< 25)';
            } else if (cst < 40) {
                alertCst.className = 'alert-box alert-warning';
                alertCst.innerText = '🟠 SARA Leve/Mod (25-40)';
            } else {
                alertCst.className = 'alert-box alert-success';
                alertCst.innerText = '✅ Normal (> 40)';
            }
        }
    }

    if (pplat) {
        alertPlat.style.display = 'block';
        if (pplat > 30) {
            alertPlat.className = 'alert-box alert-danger';
            alertPlat.innerText = '🔴 ALTO! Reduzir Vt. Alvo ≤ 30';
        } else {
            alertPlat.className = 'alert-box alert-success';
            alertPlat.innerText = '✅ Seguro (≤ 30)';
        }
    }
}

// 3. Índice ROX
function calcularROX() {
    const spo2 = parseFloat(document.getElementById('rox_spo2').value);
    let fio2 = parseFloat(document.getElementById('rox_fio2').value);
    const fr = parseFloat(document.getElementById('rox_fr').value);
    const alertRox = document.getElementById('alert_rox');

    if (!spo2 || !fio2 || !fr) return;

    if (fio2 > 1) fio2 = fio2 / 100; // Converte % para fração se o usuário botar > 1
    
    const rox = (spo2 / fio2) / fr;
    document.getElementById('out_rox').innerText = rox.toFixed(2);
    
    alertRox.style.display = 'block';
    if (rox >= 4.88) {
        alertRox.className = 'alert-box alert-success !block';
        alertRox.innerText = '✅ Sucesso Provável de OAF/VNI. Evita IOT.';
    } else if (rox >= 3.85) {
        alertRox.className = 'alert-box alert-warning !block';
        alertRox.innerText = '🟠 Zona Cinzenta. Avaliar clínica e repetir.';
    } else {
        alertRox.className = 'alert-box alert-danger !block';
        alertRox.innerText = '🔴 Risco de Falha. Preparar material de IOT imediata.';
    }
}

// 4. Relação P/F SARA
function calcularPF() {
    const pao2 = parseFloat(document.getElementById('pf_pao2').value);
    let fio2 = parseFloat(document.getElementById('pf_fio2').value);
    const alertPf = document.getElementById('alert_pf');

    if (!pao2 || !fio2) return;
    if (fio2 > 1) fio2 = fio2 / 100;

    const pf = (pao2 / fio2).toFixed(0);
    
    alertPf.style.display = 'block';
    if (pf >= 300) {
        alertPf.className = 'alert-box alert-success';
        alertPf.innerHTML = `P/F = <strong>${pf}</strong>. Sem SARA clássica.`;
    } else if (pf >= 200) {
        alertPf.className = 'alert-box alert-warning';
        alertPf.innerHTML = `P/F = <strong>${pf}</strong>. 🟡 SARA Leve.`;
    } else if (pf >= 100) {
        alertPf.className = 'alert-box alert-warning';
        alertPf.innerHTML = `P/F = <strong>${pf}</strong>. 🟠 SARA Moderada. Otimizar PEEP/Sedação.`;
    } else {
        alertPf.className = 'alert-box alert-danger';
        alertPf.innerHTML = `P/F = <strong>${pf}</strong>. 🔴 SARA GRAVE! Indicação formal de Pronação (16h) + BNM (48h) se < 150.`;
    }
}
