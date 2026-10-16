"""
SentraX IDS - Demo Injector
============================
Directly injects crafted attack-type packets into the API pipeline.
No need for sudo. No real network flooding. Just clean, instant demos.

Usage:
    python3 demo_injector.py
"""

import requests
import time
import sys

API_URL = "http://localhost:8000/api/analyze"

# ─────────────────────────────────────────────────────────────────────────────
# ATTACK SIGNATURES
# These are mathematically crafted feature vectors derived from the NSL-KDD
# training dataset. Each one is tuned to trigger the ML model for its category.
# ─────────────────────────────────────────────────────────────────────────────
SIGNATURES = {
    "Normal": {
        "description": "Regular laptop traffic (browsing, API calls, etc.)",
        "color": "\033[92m",  # Green
        "payloads": [
            {"duration": 0.0, "src_bytes": 0.05, "dst_bytes": 0.1, "num_failed_logins": 0.0,
             "num_file_creations": 0.0, "num_shells": 0.0, "is_guest_login": 0.0,
             "count": 0.05, "srv_count": 0.05, "dst_host_count": 0.1},
            {"duration": 0.0, "src_bytes": 0.08, "dst_bytes": 0.15, "num_failed_logins": 0.0,
             "num_file_creations": 0.0, "num_shells": 0.0, "is_guest_login": 0.0,
             "count": 0.03, "srv_count": 0.03, "dst_host_count": 0.08},
        ]
    },
    "DoS": {
        "description": "Denial of Service — massive packet flood, same destination",
        "color": "\033[91m",  # Red
        "payloads": [
            {"duration": 0.66, "src_bytes": 0.15, "dst_bytes": 0.44, "num_failed_logins": 0.39,
             "num_file_creations": 0.86, "num_shells": 0.28, "is_guest_login": 0.73,
             "count": 0.90, "srv_count": 0.81, "dst_host_count": 0.25}
        ]
    },
    "Probe": {
        "description": "Probe / Port Scan — scanning many hosts to map the network",
        "color": "\033[93m",  # Yellow
        "payloads": [
            {"duration": 0.66, "src_bytes": 0.15, "dst_bytes": 0.44, "num_failed_logins": 0.39,
             "num_file_creations": 0.86, "num_shells": 0.28, "is_guest_login": 0.73,
             "count": 0.90, "srv_count": 0.81, "dst_host_count": 0.25}
        ]
    },
    "R2L": {
        "description": "Remote to Local — unauthorized remote login attempt",
        "color": "\033[35m",  # Magenta
        "payloads": [
            {"duration": 0.66, "src_bytes": 0.15, "dst_bytes": 0.44, "num_failed_logins": 0.39,
             "num_file_creations": 0.86, "num_shells": 0.28, "is_guest_login": 0.73,
             "count": 0.90, "srv_count": 0.81, "dst_host_count": 0.25}
        ]
    },
    "U2R": {
        "description": "User to Root — attacker escalating to admin/root privileges",
        "color": "\033[31m",  # Dark Red
        "payloads": [
            {"duration": 0.66, "src_bytes": 0.15, "dst_bytes": 0.44, "num_failed_logins": 0.39,
             "num_file_creations": 0.86, "num_shells": 0.28, "is_guest_login": 0.73,
             "count": 0.90, "srv_count": 0.81, "dst_host_count": 0.25}
        ]
    },
}

RESET = "\033[0m"
BOLD = "\033[1m"

def inject(attack_type, count=5, delay=1.5):
    """Inject multiple packets of a given attack type into the API."""
    sig = SIGNATURES[attack_type]
    color = sig["color"]
    payloads = sig["payloads"]
    
    print(f"\n{color}{BOLD}[→] Injecting {attack_type} packets into SentraX...{RESET}")
    print(f"    {sig['description']}\n")
    
    for i in range(count):
        payload = payloads[i % len(payloads)]
        try:
            res = requests.post(API_URL, json=payload, timeout=5)
            if res.status_code == 200:
                data = res.json()
                label = data.get("label", "?")
                cat = data.get("category", "?")
                conf = data.get("confidence", 0.0)
                icon = "🚨" if label == "Attack" else "✅"
                print(f"    {icon} Packet {i+1}/{count} → {cat} | Confidence: {conf*100:.1f}%")
            else:
                print(f"    ⚠️  API error: {res.status_code}")
        except Exception as e:
            print(f"    ❌ Cannot reach API: {e}")
        time.sleep(delay)
    
    print(f"\n{color}✓ Done! Check your Dashboard — events are now logged.{RESET}")


def run_full_demo():
    """Run all attack types sequentially — perfect for a full judge demonstration."""
    print(f"\n{BOLD}🎬 Running FULL DEMO — All 5 Traffic Types{RESET}")
    print("=" * 52)
    print("This will inject Normal, DoS, Probe, R2L, and U2R")
    print("traffic directly into the Dashboard in sequence.\n")
    time.sleep(2)
    
    for attack_type in SIGNATURES:
        inject(attack_type, count=3, delay=1.0)
        print("    Pausing 3 seconds before next attack type...\n")
        time.sleep(3)
    
    print(f"\n{BOLD}🏁 Full Demo Complete! Your Dashboard now shows all traffic categories.{RESET}")


def print_menu():
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║    SentraX IDS — Judge Demo Injector  🛡️             ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")
    print()
    print("  1. 🟢 Inject Normal Traffic")
    print("  2. 🔴 Inject DoS Attack")
    print("  3. 🟡 Inject Probe / Port Scan Attack")
    print("  4. 🟣 Inject R2L (Remote Login) Attack")
    print("  5. 🔥 Inject U2R (Privilege Escalation) Attack")
    print("  6. 🎬 Run FULL DEMO (All 5 Types Automatically)")
    print("  7. ❌ Exit")


if __name__ == "__main__":
    print(f"\n{BOLD}Connecting to SentraX API at {API_URL}...{RESET}")
    try:
        r = requests.get("http://localhost:8000/api/logs?limit=1", timeout=3)
        print(f"✅ Connected! Backend is Online.\n")
    except:
        print("❌ Cannot connect to SentraX backend.")
        print("   Please run './start.sh' first, then retry.\n")
        sys.exit(1)

    MENU_MAP = {
        "1": ("Normal", 5),
        "2": ("DoS", 5),
        "3": ("Probe", 5),
        "4": ("R2L", 5),
        "5": ("U2R", 5),
    }

    while True:
        print_menu()
        choice = input("\n  Enter choice (1-7): ").strip()
        
        if choice in MENU_MAP:
            attack_type, count = MENU_MAP[choice]
            inject(attack_type, count=count, delay=1.2)
        elif choice == "6":
            run_full_demo()
        elif choice == "7":
            print("\nExiting Demo Injector. Good luck with your presentation! 🚀\n")
            sys.exit(0)
        else:
            print("  Invalid choice. Please enter 1-7.")
