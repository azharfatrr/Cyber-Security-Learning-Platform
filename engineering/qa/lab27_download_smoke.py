#!/usr/bin/env python3
"""Check the downloaded Lab 27 host service with loopback-only networking.

Run on Linux with user/network namespaces, iproute2, Java and Node available:
python3 engineering/qa/lab27_download_smoke.py docs/assets/labkit/LabKit-linux-x86_64.zip
This does not exercise the Android app or replace its end-to-end evidence.
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--inside":
        root = Path(sys.argv[2])
        runtime = root / "lab27/emulators/cloud-storage-rules-runtime-v1.1.3.jar"
        assert runtime.is_file(), runtime
        subprocess.run(["ip", "link", "set", "lo", "up"], check=True)
        # There is no default route or external interface in this namespace.
        assert not subprocess.check_output(["ip", "route", "show", "default"])
        try:
            subprocess.run(["./lab27/reset.sh"], cwd=root, check=True, timeout=90)
            listing = subprocess.check_output([
                "curl", "--fail", "--silent", "http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o",
            ], text=True)
            names = {item["name"] for item in json.loads(listing)["items"]}
            assert names == {"alice-lab27/userinfo.txt", "bob-lab27/userinfo.txt"}, names
            body = subprocess.check_output([
                "curl", "--fail", "--silent",
                "http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o/alice-lab27%2Fuserinfo.txt?alt=media",
            ], text=True)
            assert "LAB27-ALICE-SYNTHETIC" in body
            subprocess.run(["curl", "--fail", "--silent", "--output", "/dev/null", "http://127.0.0.1:4000"], check=True)
        finally:
            debug_log = root / "lab27/firebase-debug.log"
            if sys.exc_info()[0] is not None and debug_log.exists():
                print(debug_log.read_text()[-16000:])
            subprocess.run(["./lab27/stop.sh"], cwd=root, check=True, timeout=15)
            for port in (9199, 4000):
                stopped = subprocess.run([
                    "curl", "--silent", "--max-time", "2", f"http://127.0.0.1:{port}",
                ], capture_output=True)
                assert stopped.returncode != 0, f"service still listening after stop on {port}"
        print("PASS: extracted download started Storage and UI with no external network; both fixtures, credential-free read and closed ports after stop verified.")
        return

    archive_path = Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory(prefix="lab27-download-", dir="/tmp/opencode") as temp:
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(temp)
            for info in archive.infolist():
                Path(temp, info.filename).chmod((info.external_attr >> 16) & 0o777)
        root = Path(temp, "LabKit")
        assert not (root / "lab27/node_modules").exists()
        subprocess.run([
            "unshare", "--user", "--map-root-user", "--net", "--pid", "--fork", "--mount-proc", sys.executable,
            str(Path(__file__).resolve()), "--inside", str(root),
        ], check=True, timeout=120)


if __name__ == "__main__":
    main()
