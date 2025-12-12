# security_vulnerability_framework.py
import os
import time
import psutil
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import dns.resolver
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# ====================================================================
# 🔐 LOGGING CONFIGURATION
# ====================================================================
logging.basicConfig(filename="security_framework_logs.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_alert(msg, severity="MEDIUM"):
    logging.warning(f"{severity} ALERT → {msg}")
    print(f"\n🔴 {severity} ALERT → {msg}")

# ====================================================================
# 🧱 MODULE 1: BUFFER OVERFLOW DETECTION
# ====================================================================
class BufferOverflowDetector:
    MAX_LENGTH = 15  # threshold length

    def test_input(self, user_input):
        if len(user_input) > self.MAX_LENGTH:
            log_alert("Buffer Overflow Attempt Detected", "HIGH")
            self.recovery()
        else:
            print("✔ Buffer Input Safe")

    def recovery(self):
        print("🛠 FIX → Implement input sanitization & bounds checking in C/C++.")
        print("💡 Use strncpy(), fgets(), safe stack guards, and ASLR.\n")

# ====================================================================
# 🧱 MODULE 2: TRAPDOOR / HIDDEN BACKDOOR FILE MONITORING
# ====================================================================
TRAPDOOR_KEYWORDS = ["backdoor", "rootkit", "trapdoor", "hidden_user", "secret_admin"]

class TrapdoorFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if any(k in event.src_path.lower() for k in TRAPDOOR_KEYWORDS):
            log_alert(f"Trapdoor/Backdoor File Found: {event.src_path}", "CRITICAL")
            print("🛠 FIX → Delete file, audit user accounts, run antivirus scan.\n")

def monitor_trapdoor(path="."):
    observer = Observer()
    event_handler = TrapdoorFileHandler()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("🔍 Trapdoor Monitor Activated...")
    return observer

# ====================================================================
# 🧱 MODULE 3: IMPROVED CACHE & DNS POISONING DETECTION
# ====================================================================
DNS_WHITELIST = {
    "google.com": ["142.250.", "172.217.", "74.125.", "216.58."],
    "github.com": ["140.82.", "20.205."]
}

class CachePoisoningDetector:
    def check_dns(self):
        for domain, valid_prefixes in DNS_WHITELIST.items():
            try:
                ip = str(dns.resolver.resolve(domain, "A")[0])
                if not any(ip.startswith(prefix) for prefix in valid_prefixes):
                    log_alert(f"DNS Cache Poisoning Detected for {domain}: {ip}", "HIGH")
                    self.recovery()
                else:
                    print(f"✔ DNS Safe → {domain} resolved to {ip}")
            except Exception as e:
                print(f"⚠ DNS Lookup Failed for {domain}: {e}")

    def recovery(self):
        print("🛠 FIX → Flush DNS & enable DNSSEC.")
        print("💡 Windows: ipconfig /flushdns | Linux: systemd-resolve --flush-caches\n")

# ====================================================================
# 🧱 MODULE 4: MALICIOUS PROCESS DETECTION
# ====================================================================
SUSPICIOUS_PROCESS = ["nc", "ncat", "hydra", "airmon", "meterpreter", "msfconsole", "john"]

def monitor_processes():
    for proc in psutil.process_iter(["pid", "name", "username"]):
        try:
            if any(s in proc.info["name"].lower() for s in SUSPICIOUS_PROCESS):
                log_alert(f"Malicious Process Detected: {proc.info}", "CRITICAL")
                print("🛠 FIX → Kill process & inspect network ports.\n")
        except:
            pass

# ====================================================================
# 🧠 MODULE 5: ML‑BASED SYSTEM ANOMALY DETECTION
# ====================================================================
class MLAnomalyDetector:

    def __init__(self):
        self.model = None

    def collect_system_features(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        return [cpu, mem, disk, net.bytes_sent, net.bytes_recv]

    def create_training_data(self, n_samples=40):
        data = []
        for _ in range(n_samples):
            data.append(self.collect_system_features())
            time.sleep(0.3)
        return pd.DataFrame(data, columns=["CPU","Memory","Disk","Bytes_Sent","Bytes_Recv"])

    def train(self):
        print("🧠 Collecting Normal System Data for ML Training...")
        df = self.create_training_data()
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(df)
        print("🎯 ML Model Trained Successfully!\n")

    def detect(self):
        features = self.collect_system_features()
        df = pd.DataFrame([features], columns=["CPU","Memory","Disk","Bytes_Sent","Bytes_Recv"])
        pred = self.model.predict(df)
        if pred[0] == -1:
            log_alert(f"Anomaly Detected via ML: {df.iloc[0].to_dict()}", "HIGH")
            print("🛠 FIX → Check running processes, network usage, disk spikes.\n")
        else:
            print("✔ ML System Status → Normal")

# ====================================================================
# 🎯 MAIN REAL-TIME SECURITY EXECUTION ENGINE
# ====================================================================
if __name__ == "__main__":
    print("\n🛡 Starting ADVANCED Security Framework...\n")

    # Initialize Modules
    buffer_detector = BufferOverflowDetector()
    cache_detector = CachePoisoningDetector()
    ml_detector = MLAnomalyDetector()

    # Train ML Model
    ml_detector.train()

    # Start trapdoor monitor
    monitor = monitor_trapdoor(".")

    try:
        while True:
            # Buffer simulation input
            user_input = input("\n💻 Enter Input to Test Buffer Overflow: ")
            buffer_detector.test_input(user_input)

            # Real-time scans
            monitor_processes()
            cache_detector.check_dns()
            ml_detector.detect()

            time.sleep(2)

    except KeyboardInterrupt:
        monitor.stop()
        monitor.join()
        print("\n🛑 Framework Stopped Safely.")
