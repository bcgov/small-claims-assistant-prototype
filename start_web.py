"""Launch the BC Small Claims Assistant web app dev server on port 5173."""

from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path


PORT = 5173
WEB_DIR = Path(__file__).resolve().parent / "web"


def free_port(port: int) -> None:
    """Kill any process currently listening on the given port (Windows + Unix)."""
    if sys.platform == "win32":
        # Find PIDs using the port then terminate them
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True
        )
        pids: set[str] = set()
        for line in result.stdout.splitlines():
            if f":{port}" in line and ("LISTENING" in line or "ESTABLISHED" in line):
                parts = line.split()
                if parts:
                    pids.add(parts[-1])
        for pid in pids:
            if pid.isdigit() and pid != "0":
                subprocess.run(
                    ["taskkill", "/PID", pid, "/F"],
                    capture_output=True
                )
                print(f"  Freed port {port} (killed PID {pid})")
    else:
        # macOS / Linux
        result = subprocess.run(
            ["lsof", "-ti", f"tcp:{port}"],
            capture_output=True, text=True
        )
        for pid in result.stdout.strip().splitlines():
            if pid.isdigit():
                subprocess.run(["kill", "-9", pid], capture_output=True)
                print(f"  Freed port {port} (killed PID {pid})")


def check_node() -> bool:
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Node.js is not installed or not on PATH.")
        print("  Download it from https://nodejs.org/")
        return False
    print(f"  Node {result.stdout.strip()}")
    return True


def install_deps() -> bool:
    node_modules = WEB_DIR / "node_modules"
    if not node_modules.exists():
        print("  node_modules not found — running npm install...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=WEB_DIR,
            shell=(sys.platform == "win32"),
        )
        if result.returncode != 0:
            print("ERROR: npm install failed.")
            return False
    return True


def main() -> None:
    print("=" * 55)
    print("  BC Small Claims Assistant — Web App")
    print("=" * 55)

    print("\n[1/3] Checking Node.js...")
    if not check_node():
        sys.exit(1)

    print(f"\n[2/3] Freeing port {PORT} if in use...")
    free_port(PORT)

    print("\n[3/3] Checking dependencies...")
    if not install_deps():
        sys.exit(1)

    print(f"\nStarting dev server at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.\n")

    npm_cmd = ["npm", "run", "dev", "--", "--port", str(PORT)]
    try:
        subprocess.run(
            npm_cmd,
            cwd=WEB_DIR,
            shell=(sys.platform == "win32"),
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
