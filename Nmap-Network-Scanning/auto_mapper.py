#!/usr/bin/env python3

import subprocess
import shutil
import os
import re
from datetime import datetime

# Colors
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
M = "\033[95m"
W = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

# AUTO-MAPPER Banner
def banner():
    os.system("clear")
    print(f"""{C}{BOLD}
     █████╗ ██╗   ██╗████████╗ ██████╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
    ███████║██║   ██║   ██║   ██║   ██║
    ██╔══██║██║   ██║   ██║   ██║   ██║
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝

    ███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗
    ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝

              {M}>>> NMAP AUTOMATION TOOL <<<
              {Y}>>> KALI LINUX EDITION <<<
    {RESET}""")

    print(f"{G}{BOLD}    [ AUTO-MAPPER | NETWORK SCANNER ]{RESET}")
    print(f"{B}    ---------------------------------------{RESET}")
    print(f"{Y}    Use only on authorized targets!{RESET}\n")


# Check Nmap
def check_nmap():
    if shutil.which("nmap") is None:
        print(f"{R}[!] Nmap is not installed!{RESET}")
        print(f"{Y}Install it using: sudo apt install nmap{RESET}")
        exit()


# Get target
def get_target():
    while True:
        target = input(f"\n{C}[+] Enter Target IP/Hostname: {W}").strip()

        if re.fullmatch(r"[A-Za-z0-9.-]+", target):
            return target

        print(f"{R}[!] Invalid target format!{RESET}")


# Scan Menu
def scan_menu():
    print(f"""
{C}{BOLD}========== SCAN OPTIONS =========={RESET}

{G}[1]{W} Ping Scan
{G}[2]{W} TCP SYN Scan
{G}[3]{W} TCP Connect Scan
{G}[4]{W} UDP Scan
{G}[5]{W} Service Version Detection
{G}[6]{W} OS Detection
{G}[7]{W} Aggressive Scan
{G}[8]{W} Top 1000 Ports Scan
{G}[9]{W} Full TCP Port Scan
{G}[10]{W} Custom Port Scan
{G}[0]{W} Exit

{C}================================={RESET}
""")


# Execute scan
def run_scan(target, scan_type):

    commands = {
        "1": ["-sn"],
        "2": ["-sS", "-T3"],
        "3": ["-sT", "-T3"],
        "4": ["-sU", "-T3"],
        "5": ["-sV", "-T3"],
        "6": ["-O", "-T3"],
        "7": ["-A", "-T3"],
        "8": ["-sS", "-T3"],
        "9": ["-sS", "-p-", "-T3"]
    }

    scan_names = {
        "1": "Ping Scan",
        "2": "TCP SYN Scan",
        "3": "TCP Connect Scan",
        "4": "UDP Scan",
        "5": "Service Version Detection",
        "6": "OS Detection",
        "7": "Aggressive Scan",
        "8": "Top 1000 Ports Scan",
        "9": "Full TCP Port Scan"
    }

    if scan_type == "10":
        ports = input(
            f"{Y}[+] Enter ports (example: 22,80,443 or 1-1000): {W}"
        ).strip()

        if not re.fullmatch(r"[0-9,-]+", ports):
            print(f"{R}[!] Invalid port format!{RESET}")
            return

        for part in ports.split(","):
            nums = part.split("-")
            if (len(nums) > 2 or
                any(not n.isdigit() for n in nums) or
                any(int(n) < 1 or int(n) > 65535 for n in nums) or
                (len(nums) == 2 and int(nums[0]) > int(nums[1]))):
                print(f"{R}[!] Invalid port range!{RESET}")
                return

        args = ["-sS", "-T3", "-p", ports]
        name = "Custom Port Scan"

    elif scan_type in commands:
        args = commands[scan_type]
        name = scan_names[scan_type]

    else:
        print(f"{R}[!] Invalid selection!{RESET}")
        return

    # Create output folder
    folder = "AUTO_MAPPER_RESULTS"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = re.sub(r"[^A-Za-z0-9_.-]", "_", target)
    output_file = f"{folder}/{safe_target}_{timestamp}"

    command = [
        "nmap",
        *args,
        "-oN", output_file + ".txt",
        "-oX", output_file + ".xml",
        target
    ]

    print(f"\n{G}[+] Selected Scan: {name}{RESET}")
    print(f"{B}[+] Target: {target}{RESET}")
    print(f"{Y}[+] Command: {' '.join(command)}{RESET}")

    confirm = input(
        f"\n{Y}[?] Start scan? (y/n): {W}"
    ).lower().strip()

    if confirm != "y":
        print(f"{R}[!] Scan cancelled.{RESET}")
        return

    print(f"\n{G}[+] Scan Starting...{RESET}\n")

    try:
        subprocess.run(command, check=False)

        print(f"\n{G}[+] Scan Finished!{RESET}")
        print(f"{C}[+] TXT Report: {output_file}.txt{RESET}")
        print(f"{C}[+] XML Report: {output_file}.xml{RESET}")

    except KeyboardInterrupt:
        print(f"\n{R}[!] Scan Interrupted!{RESET}")

    except Exception as error:
        print(f"{R}[!] Error: {error}{RESET}")


# Main Program
def main():

    check_nmap()

    while True:

        banner()
        scan_menu()

        choice = input(
            f"{Y}[AUTO-MAPPER] Select Option: {W}"
        ).strip()

        if choice == "0":
            print(f"\n{G}[+] Exiting AUTO-MAPPER. Goodbye!{RESET}")
            break

        if choice not in [
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10"
        ]:
            print(f"{R}[!] Invalid option!{RESET}")
            input("Press Enter to continue...")
            continue

        target = get_target()

        run_scan(target, choice)

        input(f"\n{C}Press Enter to return to menu...{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] AUTO-MAPPER Terminated.{RESET}")
