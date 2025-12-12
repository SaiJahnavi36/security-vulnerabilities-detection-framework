function scanSystem() {
    let input = document.getElementById("userInput").value;
    let output = document.getElementById("outputBox");

    output.innerHTML = "<h3>🧪 Scan Results</h3>";

    // ===============================
    // BUFFER OVERFLOW CHECK
    // ===============================
    if (input.length > 15) {
        output.innerHTML += "<p>🔴 HIGH ALERT → Buffer Overflow Detected</p>";
    } else {
        output.innerHTML += "<p>✔ Buffer Input Safe</p>";
    }

    // ===============================
    // DNS SIMULATION
    // ===============================
    let googleIPs = ["142.250.", "172.217.", "74.125.", "216.58."];
    let randomIP = "74.125." + Math.floor(Math.random() * 200) + "." + Math.floor(Math.random() * 200);

    let safe = googleIPs.some(prefix => randomIP.startsWith(prefix));

    if (safe) {
        output.innerHTML += `<p>✔ DNS Safe → google.com → ${randomIP}</p>`;
    } else {
        output.innerHTML += `<p>🔴 DNS Cache Poisoning Detected → google.com → ${randomIP}</p>`;
    }

    // ===============================
    // ML ANOMALY SIMULATION
    // ===============================
    let cpu = Math.floor(Math.random() * 100);

    if (cpu > 80) {
        output.innerHTML += `<p>🔴 ML ALERT → High CPU Usage Detected (${cpu}%)</p>`;
    } else {
        output.innerHTML += `<p>✔ ML System Status → Normal (${cpu}%)</p>`;
    }
}
