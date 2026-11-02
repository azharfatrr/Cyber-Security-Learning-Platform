import unittest
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from unittest.mock import patch

import labkit.build as labkit_builder


class SiteTest(unittest.TestCase):
    def test_required_documentation_and_lab_images_exist(self):
        root = Path(__file__).parent
        required_files = (
            "docs/index.md",
            "docs/00-common-setup.md",
            "docs/01-devom-setup.md",
            "docs/02-bugbazaar-setup.md",
            "docs/29-components.md",
            "docs/30-runtime-bypass.md",
            "labkit/input/apk/module-29-caller.apk",
            "docs/images/lab-29/bugbazaar-synthetic-address.png",
            "docs/images/lab-29/ordinary-app-provider-result.png",
            "docs/images/lab-30/passcode-rejected.png",
            "docs/images/lab-30/passcode-correct.png",
            "docs/images/lab-30/passcode-hook-success.png",
        )

        for required_file in required_files:
            with self.subTest(path=required_file):
                self.assertTrue((root / required_file).is_file())

    def test_labkit_build_is_deterministic_and_contains_verified_apks(self):
        root = Path(__file__).parent
        expected_hashes = {
            "BugBazaar_v1.2.1.apk": "c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c",
            "Dvom.apk": "afec11d202a4069880469274200bb377a9f1cb2205bad52c3f0f906c705cf409",
            "module-29-caller.apk": "5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc",
            "bugbazaar-lab27-emulator.apk": "b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604",
        }
        apk_dir = root / "labkit/input/apk"
        missing_apks = [filename for filename in expected_hashes if not (apk_dir / filename).is_file()]
        self.assertEqual(missing_apks, [])
        if missing_apks:
            return
        for filename, digest in expected_hashes.items():
            with self.subTest(apk=filename):
                self.assertEqual(hashlib.sha256((apk_dir / filename).read_bytes()).hexdigest(), digest)

        expected_members = {
            "LabKit/README.md",
            "LabKit/manifest.sha256",
            *(f"LabKit/apk/{filename}" for filename in expected_hashes),
            "LabKit/setup.sh",
            "LabKit/install-apk.sh",
            "LabKit/backend/requirements.lock",
            "LabKit/hooks/lab30-hook.js",
            "LabKit/tools/frida-requirements.lock",
            "LabKit/tools/versions.env",
            "LabKit/lab27/README.md",
            "LabKit/lab27/firebase.json",
            "LabKit/lab27/google-services.json",
            "LabKit/lab27/package.json",
            "LabKit/lab27/package-lock.json",
            "LabKit/lab27/storage.rules",
            "LabKit/lab27/reset.sh",
            "LabKit/lab27/seed.sh",
            "LabKit/lab27/start.sh",
            "LabKit/lab27/stop.sh",
            "LabKit/lab27/process.sh",
            "LabKit/lab27/fixtures/alice-userinfo.txt",
            "LabKit/lab27/fixtures/bob-userinfo.txt",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first.zip"
            second = Path(temp_dir) / "second.zip"
            for output in (first, second):
                result = subprocess.run(
                    [sys.executable, str(root / "labkit/build.py"), "--output", str(output)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            archive_digest = hashlib.sha256(first.read_bytes()).hexdigest()
            downloads = (root / "docs/downloads.md").read_text()
            release_report = (root / "engineering/qa/release-readiness.md").read_text()
            for document in (downloads, release_report):
                published_digest = re.search(r"LabKit SHA-256: `([0-9a-f]{64})`", document)
                if published_digest is None:
                    published_digest = re.search(r"SHA-256:\s*`([0-9a-f]{64})`", document)
                self.assertIsNotNone(published_digest, "published LabKit checksum is missing")
                self.assertEqual(published_digest.group(1), archive_digest)
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()), expected_members)
                self.assertTrue(archive.getinfo("LabKit/setup.sh").external_attr >> 16 & 0o111)
                self.assertTrue(archive.getinfo("LabKit/lab27/reset.sh").external_attr >> 16 & 0o111)
                for line in archive.read("LabKit/manifest.sha256").decode().splitlines():
                    digest, member = line.split("  ", 1)
                    self.assertEqual(hashlib.sha256(archive.read(f"LabKit/{member}")).hexdigest(), digest)

            checked = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--check", str(first)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_labkit_builder_rejects_payload_shadowing_pinned_apk(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kit_root = Path(temp_dir) / "labkit"
            apk_dir = kit_root / "input/apk"
            payload_apk_dir = kit_root / "payload/apk"
            apk_dir.mkdir(parents=True)
            payload_apk_dir.mkdir(parents=True)
            pinned_apk = apk_dir / "pinned.apk"
            pinned_apk.write_bytes(b"pinned APK")
            (kit_root / "README.md").write_text("LabKit test\n")
            (kit_root / "manifest.sha256").write_text(
                f"{hashlib.sha256(pinned_apk.read_bytes()).hexdigest()}  pinned.apk\n"
            )
            (payload_apk_dir / "pinned.apk").write_bytes(b"replacement payload")

            with patch.multiple(
                labkit_builder,
                KIT_ROOT=kit_root,
                APK_DIR=apk_dir,
                PINNED_MANIFEST=kit_root / "manifest.sha256",
                README=kit_root / "README.md",
            ):
                with self.assertRaisesRegex(labkit_builder.LabKitError, "Duplicate LabKit source path"):
                    labkit_builder.source_files()

    def test_lab27_host_commands_are_labeled_from_extracted_kit(self):
        root = Path(__file__).parent
        guide = (root / "docs/27-cloud-database.md").read_text()
        self.assertNotIn("**Where:** host shell, repository root.", guide)
        self.assertEqual(guide.count("**Where:** host shell, extracted LabKit directory."), 6)

    def test_labkit_setup_preflight_fails_closed_and_checks_the_emulator(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as empty_path:
            archive = Path(empty_path) / "LabKit.zip"
            built = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--output", str(archive)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive) as kit:
                kit.extractall(empty_path)
            setup = Path(empty_path) / "LabKit/setup.sh"
            self.assertTrue(setup.is_file())

            missing_tools = subprocess.run(
                ["/usr/bin/bash", str(setup), "--check"],
                env={"PATH": empty_path},
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing_tools.returncode, 1)
            self.assertIn("adb", missing_tools.stderr)

        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "LabKit.zip"
            built = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--output", str(archive)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive) as kit:
                kit.extractall(temp_dir)
            setup = Path(temp_dir) / "LabKit/setup.sh"
            fake_bin = Path(temp_dir) / "bin"
            fake_bin.mkdir()
            adb = Path(fake_bin) / "adb"
            adb.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in\n"
                "  *devices*) printf 'List of devices attached\\nemulator-5554\\tdevice\\n' ;;\n"
                "  *ro.build.version.sdk*) printf '34\\n' ;;\n"
                "  *ro.product.cpu.abi*) printf 'x86_64\\n' ;;\n"
                "  *ro.kernel.qemu*) printf '%s\\n' \"${FAKE_QEMU:-1}\" ;;\n"
                "  *) exit 0 ;;\n"
                "esac\n"
            )
            adb.chmod(0o755)
            checked = subprocess.run(
                ["/usr/bin/bash", str(setup), "--check"],
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("emulator-5554", checked.stdout)

            non_emulator = subprocess.run(
                ["/usr/bin/bash", str(setup), "--check"],
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}", "FAKE_QEMU": "0"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(non_emulator.returncode, 1)
            self.assertIn("Android emulator is required", non_emulator.stderr)

    def test_labkit_setup_checks_venv_support_before_creating_workspace(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "LabKit.zip"
            built = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--output", str(archive)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive) as kit:
                kit.extractall(temp_dir)
            kit_root = Path(temp_dir) / "LabKit"
            fake_bin = Path(temp_dir) / "bin"
            fake_bin.mkdir()

            python3 = fake_bin / "python3"
            python3.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in *'import ensurepip, venv'*) exit 1 ;; esac\n"
                f"exec '{sys.executable}' \"$@\"\n"
            )
            adb = fake_bin / "adb"
            adb.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in\n"
                "  *devices*) printf 'List of devices attached\\nemulator-5554\\tdevice\\n' ;;\n"
                "  *ro.kernel.qemu*) printf '1\\n' ;;\n"
                "  *ro.build.version.sdk*) printf '34\\n' ;;\n"
                "  *ro.product.cpu.abi*) printf 'x86_64\\n' ;;\n"
                "esac\n"
            )
            node = fake_bin / "node"
            node.write_text("#!/bin/sh\nprintf 'v20.0.0\\n'\n")
            java = fake_bin / "java"
            java.write_text("#!/bin/sh\nprintf 'openjdk version \"17.0.0\"\\n' >&2\n")
            git = fake_bin / "git"
            git.write_text("#!/bin/sh\nprintf 'git was reached before the venv check\\n' >&2; exit 1\n")
            for executable in (python3, adb, node, java, git):
                executable.chmod(0o755)

            result = subprocess.run(
                ["/usr/bin/bash", str(kit_root / "setup.sh")],
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Python venv support is required", result.stderr)
            self.assertFalse((kit_root / ".labkit").exists())

    def test_python_bootstrap_dependencies_are_hash_verified(self):
        root = Path(__file__).parent
        setup = (root / "labkit/setup.sh").read_text()
        self.assertEqual(setup.count("--require-hashes"), 2)

        for lock_path in (
            root / "labkit/payload/backend/requirements.lock",
            root / "labkit/payload/tools/frida-requirements.lock",
        ):
            lock = lock_path.read_text()
            entries = list(re.finditer(r"(?m)^[A-Za-z0-9_.-]+==[^\s\\]+", lock))
            self.assertTrue(entries, f"no pinned packages in {lock_path}")
            for index, entry in enumerate(entries):
                end = entries[index + 1].start() if index + 1 < len(entries) else len(lock)
                with self.subTest(lock=lock_path.name, package=entry.group(0)):
                    self.assertRegex(lock[entry.start():end], r"--hash=sha256:[0-9a-f]{64}")

    def test_labkit_installer_does_not_replace_an_unverified_package(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "LabKit.zip"
            built = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--output", str(archive)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive) as kit:
                kit.extractall(temp_dir)

            fake_bin = Path(temp_dir) / "bin"
            fake_bin.mkdir()
            install_marker = Path(temp_dir) / "adb-install-was-called"
            adb = fake_bin / "adb"
            adb.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in\n"
                "  *devices*) printf 'List of devices attached\\nemulator-5554\\tdevice\\n' ;;\n"
                "  *ro.kernel.qemu*) printf '1\\n' ;;\n"
                "  *ro.build.version.sdk*) printf '34\\n' ;;\n"
                "  *ro.product.cpu.abi*) printf 'x86_64\\n' ;;\n"
                "  *'pm path com.example.vulnappowasp'*) printf 'package:/data/app/base.apk\\n' ;;\n"
                "  *'sha256sum /data/app/base.apk'*) printf '0000000000000000000000000000000000000000000000000000000000000000  /data/app/base.apk\\n' ;;\n"
                f"  *install*) touch '{install_marker}' ;;\n"
                "esac\n"
            )
            adb.chmod(0o755)
            result = subprocess.run(
                ["/usr/bin/bash", str(Path(temp_dir) / "LabKit/install-apk.sh"), "Dvom.apk"],
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("not replaced or cleared", result.stderr)
            self.assertFalse(install_marker.exists())

    def test_labkit_installer_refuses_a_non_emulator_android_device(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "LabKit.zip"
            built = subprocess.run(
                [sys.executable, str(root / "labkit/build.py"), "--output", str(archive)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive) as kit:
                kit.extractall(temp_dir)

            fake_bin = Path(temp_dir) / "bin"
            fake_bin.mkdir()
            install_marker = Path(temp_dir) / "adb-install-was-called"
            adb = fake_bin / "adb"
            adb.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in\n"
                "  *devices*) printf 'List of devices attached\\nemulator-5554\\tdevice\\n' ;;\n"
                "  *ro.kernel.qemu*) printf '0\\n' ;;\n"
                "  *ro.build.version.sdk*) printf '34\\n' ;;\n"
                "  *ro.product.cpu.abi*) printf 'x86_64\\n' ;;\n"
                f"  *install*) touch '{install_marker}' ;;\n"
                "esac\n"
            )
            adb.chmod(0o755)
            result = subprocess.run(
                ["/usr/bin/bash", str(Path(temp_dir) / "LabKit/install-apk.sh"), "Dvom.apk"],
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Android emulator is required", result.stderr)
            self.assertFalse(install_marker.exists())

    def test_lab27_stop_does_not_kill_an_unrelated_reused_pid(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_dir = Path(temp_dir) / "LabKit/lab27"
            runtime = lab_dir / ".runtime"
            runtime.mkdir(parents=True)
            stop_script = lab_dir / "stop.sh"
            stop_script.write_bytes((root / "labkit/payload/lab27/stop.sh").read_bytes())
            (lab_dir / "process.sh").write_bytes((root / "labkit/payload/lab27/process.sh").read_bytes())
            pid_file = runtime / "emulator.pid"
            child_pid_file = Path(temp_dir) / "unrelated.pid"
            parent = subprocess.Popen(
                ["/usr/bin/bash", "-c", 'sleep 60 & echo $! > "$1"; wait', "test", str(child_pid_file)]
            )
            try:
                for _ in range(100):
                    if child_pid_file.exists():
                        break
                    time.sleep(0.01)
                self.assertTrue(child_pid_file.exists())
                unrelated_pid = int(child_pid_file.read_text())
                pid_file.write_text(f"{unrelated_pid}\n")

                result = subprocess.run(
                    ["/usr/bin/bash", str(stop_script)], capture_output=True, text=True, timeout=5
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("leaving that process untouched", result.stdout)
                self.assertIsNone(parent.poll(), "unrelated process was terminated")
                self.assertFalse(pid_file.exists())
            finally:
                try:
                    os.kill(int(child_pid_file.read_text()), 15)
                except (ProcessLookupError, FileNotFoundError, ValueError):
                    pass
                parent.wait(timeout=5)

    def test_lab27_start_and_stop_match_the_running_emulator(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_dir = Path(temp_dir) / "LabKit/lab27"
            runtime = lab_dir / ".runtime"
            runtime.mkdir(parents=True)
            start_script = lab_dir / "start.sh"
            start_script.write_bytes((root / "labkit/payload/lab27/start.sh").read_bytes())
            stop_script = lab_dir / "stop.sh"
            stop_script.write_bytes((root / "labkit/payload/lab27/stop.sh").read_bytes())
            (lab_dir / "process.sh").write_bytes((root / "labkit/payload/lab27/process.sh").read_bytes())
            pid_file = runtime / "emulator.pid"
            invoked_marker = Path(temp_dir) / "firebase-was-restarted"
            firebase = lab_dir / "node_modules/.bin/firebase"
            firebase.parent.mkdir(parents=True)
            firebase.write_text(f"#!/bin/sh\ntouch '{invoked_marker}'\n")
            firebase.chmod(0o755)
            fake_bin = Path(temp_dir) / "bin"
            fake_bin.mkdir()
            curl = fake_bin / "curl"
            curl.write_text("#!/bin/sh\nexit 0\n")
            curl.chmod(0o755)

            command_line = (
                "node ./node_modules/.bin/firebase emulators:start --only storage "
                "--project lab27-local --config firebase.json"
            )
            emulator = subprocess.Popen(
                [
                    "/usr/bin/bash",
                    "-c",
                    'cd "$1"; exec -a "$2" sleep 60',
                    "test",
                    str(lab_dir),
                    command_line,
                ]
            )
            try:
                pid_file.write_text(f"{emulator.pid}\n")
                result = subprocess.run(
                    ["/usr/bin/bash", str(start_script)],
                    env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("already running", result.stdout)
                self.assertEqual(pid_file.read_text(), f"{emulator.pid}\n")
                self.assertFalse(invoked_marker.exists())

                stopped = subprocess.run(
                    ["/usr/bin/bash", str(stop_script)],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(stopped.returncode, 0, stopped.stderr)
                self.assertIn("Lab 27 emulator stopped", stopped.stdout)
                self.assertFalse(pid_file.exists())
                self.assertIsNotNone(emulator.poll(), "matching emulator process was not terminated")
            finally:
                try:
                    os.kill(emulator.pid, 15)
                except ProcessLookupError:
                    pass
                emulator.wait(timeout=5)

    def test_learner_setup_uses_labkit_instead_of_manual_artifact_installs(self):
        root = Path(__file__).parent
        common = (root / "docs/00-common-setup.md").read_text()
        devom = (root / "docs/01-devom-setup.md").read_text()
        bugbazaar = (root / "docs/02-bugbazaar-setup.md").read_text()
        lab27 = (root / "docs/27-cloud-database.md").read_text()

        self.assertIn("./setup.sh --check", common)
        self.assertIn("./setup.sh", common)
        self.assertIn("./install-apk.sh Dvom.apk", devom)
        self.assertNotIn("git clone", devom.lower())
        self.assertNotIn("pip install", devom.lower())
        self.assertIn("./install-apk.sh BugBazaar_v1.2.1.apk", bugbazaar)
        self.assertIn("./install-apk.sh module-29-caller.apk", bugbazaar)
        self.assertIn("./install-apk.sh bugbazaar-lab27-emulator.apk", bugbazaar)
        self.assertNotIn("npm install", lab27.lower())
        self.assertNotIn("docs/assets/apk/", "\n".join((devom, bugbazaar, lab27)))

    def test_download_page_has_one_labkit_link_and_no_individual_apk_links(self):
        root = Path(__file__).parent
        downloads = (root / "docs/downloads.md").read_text()
        links = re.findall(r"\[[^\]]+\]\(assets/labkit/LabKit-linux-x86_64\.zip\)", downloads)
        self.assertEqual(len(links), 1)
        self.assertIsNotNone(re.search(r"LabKit SHA-256:\s*`?[a-f0-9]{64}`?", downloads))
        self.assertNotRegex(downloads, r"\]\([^)]*\.apk\)")
        for digest in (
            "c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c",
            "afec11d202a4069880469274200bb377a9f1cb2205bad52c3f0f906c705cf409",
            "5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc",
            "b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604",
        ):
            with self.subTest(apk_hash=digest):
                self.assertIn(digest, downloads)

    def test_lab_downloads_follow_common_prerequisites_in_setup_navigation(self):
        config = (Path(__file__).parent / "mkdocs.yml").read_text()
        pages = (
            "Common prerequisites: 00-common-setup.md",
            "Lab downloads: downloads.md",
            "Devom setup: 01-devom-setup.md",
            "BugBazaar setup: 02-bugbazaar-setup.md",
        )
        positions = [config.index(page) for page in pages]
        self.assertEqual(positions, sorted(positions))

    def test_maintainer_contract_is_not_published_and_license_404_are_present(self):
        root = Path(__file__).parent
        config = (root / "mkdocs.yml").read_text()
        self.assertFalse((root / "docs/lab-structure.md").exists())
        self.assertNotIn("lab-structure.md", config)
        self.assertIn("MIT License", (root / "LICENSE").read_text())
        self.assertIn("project-owned", (root / "LICENSE").read_text().lower())
        self.assertIn("404", (root / "docs/404.md").read_text())

        self.assertIn("site_url: https://azharfatrr.github.io/Cyber-Security-Learning-Platform/", config)
        self.assertIn("custom_dir: overrides", config)
        not_found = (root / "overrides/404.html").read_text()
        self.assertIn("Page not found", not_found)
        self.assertIn("config.site_url", not_found)
        self.assertIn("downloads/", not_found)

        notice = (root / "NOTICE").read_text().lower()
        self.assertIn("public educational redistribution", notice)
        self.assertIn("labkit/input/apk/", notice)

    def test_repository_guides_point_to_the_single_labkit_download(self):
        root = Path(__file__).parent
        readme = (root / "README.md").read_text()
        publishing = (root / "PUBLISHING.txt").read_text()

        self.assertIn("docs/downloads.md", readme)
        self.assertIn("one labkit", readme.lower())
        self.assertIn("python3 labkit/build.py", publishing)
        self.assertIn("before", publishing.lower())
        self.assertIn("mkdocs build --strict", publishing)

    def test_rendered_site_link_checker_validates_targets_fragments_and_labkit(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            site = Path(temp_dir) / "site"
            (site / "assets/labkit").mkdir(parents=True)
            (site / "assets/logo.png").parent.mkdir(parents=True, exist_ok=True)
            (site / "assets/logo.png").write_bytes(b"image")
            (site / "assets/labkit/LabKit-linux-x86_64.zip").write_bytes(b"archive")
            (site / "guide.html").write_text('<h1 id="start">Guide</h1>')
            index = site / "index.html"
            index.write_text(
                '<a href="guide.html#start">Guide</a>'
                '<a href="/Cyber-Security-Learning-Platform/guide.html#start">Pages-base guide</a>'
                '<a href="https://azharfatrr.github.io/Cyber-Security-Learning-Platform/guide.html#start">Absolute Pages guide</a>'
                '<img src="assets/logo.png">'
                '<a href="assets/labkit/LabKit-linux-x86_64.zip">LabKit</a>'
                '<a href="https://example.test/page">External</a>'
            )

            checked = subprocess.run(
                [sys.executable, str(root / "scripts/check_site_links.py"), str(site)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertIn("external", checked.stdout.lower())
            self.assertIn("https://example.test/page", checked.stdout)
            self.assertNotIn("https://azharfatrr.github.io/Cyber-Security-Learning-Platform/guide.html", checked.stdout)

            index.write_text(
                '<a href="guide.html#missing">Guide</a>'
                '<img src="assets/missing.png">'
                '<a href="assets/labkit/LabKit-linux-x86_64.zip">LabKit</a>'
            )
            broken = subprocess.run(
                [sys.executable, str(root / "scripts/check_site_links.py"), str(site)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(broken.returncode, 1)
            self.assertIn("missing fragment", broken.stdout.lower())
            self.assertIn("missing target", broken.stdout.lower())

            (site / "assets/labkit/LabKit-linux-x86_64.zip").unlink()
            missing_archive = subprocess.run(
                [sys.executable, str(root / "scripts/check_site_links.py"), str(site)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing_archive.returncode, 1)
            self.assertIn("labkit", missing_archive.stdout.lower())

    def test_workflow_validates_pull_requests_and_only_deploys_main(self):
        root = Path(__file__).parent
        workflow = (root / ".github/workflows/deploy.yml").read_text()

        self.assertRegex(workflow, r"(?m)^\s+pull_request:\s*$")
        self.assertRegex(workflow, r"(?ms)^\s+push:\s*\n\s+branches:\s*\n\s+-\s+main\s*$")
        self.assertIn("  validate:", workflow)
        ordered_steps = (
            "python3 labkit/build.py",
            "python -m unittest -v test_site",
            "python -m mkdocs build --strict",
            "python3 scripts/check_site_links.py site",
            "node engineering/qa/accessibility_audit.mjs site",
        )
        positions = [workflow.find(step) for step in ordered_steps]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))
        self.assertRegex(
            workflow,
            r"(?ms)^\s+deploy:\s*\n(?:(?!^\s+\w+:).)*?\s+needs: validate\s*\n"
            r"\s+if:.*github\.event_name\s*==\s*'push'.*github\.ref\s*==\s*'refs/heads/main'",
        )

    def test_labkit_validator_rejects_unsafe_and_duplicate_members(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as temp_dir:
            for index, names in enumerate(
                (("LabKit/../outside",), ("LabKit/README.md", "LabKit/README.md"))
            ):
                bad_archive = Path(temp_dir) / f"bad-{index}.zip"
                with zipfile.ZipFile(bad_archive, "w") as archive:
                    for name in names:
                        archive.writestr(name, b"not a valid LabKit")
                checked = subprocess.run(
                    [sys.executable, str(root / "labkit/build.py"), "--check", str(bad_archive)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(checked.returncode, 1, checked.stderr)

    def test_user_facing_pages_do_not_mark_labs_as_pilots(self):
        root = Path(__file__).parent
        pages = [root / "README.md", root / "lab-expansion-plan.md"]
        pages.extend(
            path
            for path in (root / "docs").rglob("*.md")
            if "superpowers" not in path.parts
        )

        for page in pages:
            with self.subTest(path=str(page.relative_to(root))):
                self.assertNotIn("pilot", page.read_text().lower())

    def test_each_lab_has_a_key_observation_callout(self):
        root = Path(__file__).parent
        lab_pages = (
            "09-jwt-account-state.md",
            "10-otp-bypass.md",
            "14-command-injection.md",
            "24-file-upload.md",
            "25-path-traversal.md",
            "26-transactions.md",
            "27-cloud-database.md",
            "28-bola.md",
            "29-components.md",
            "30-runtime-bypass.md",
        )

        for lab_page in lab_pages:
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text()
                self.assertIn('!!! important "Key observation"', content)

    def test_key_observation_callouts_use_orange_in_both_themes(self):
        root = Path(__file__).parent
        stylesheet = (root / "docs/stylesheets/extra.css").read_text()

        self.assertIn(".md-typeset .admonition.important", stylesheet)
        self.assertIn("#a75a07", stylesheet)
        self.assertIn('[data-md-color-scheme="slate"] .md-typeset .admonition.important', stylesheet)
        self.assertIn("#ffae54", stylesheet)

    def test_hints_are_nested_under_evidence_on_every_lab_page(self):
        root = Path(__file__).parent
        lab_pages = (
            "09-jwt-account-state.md",
            "10-otp-bypass.md",
            "14-command-injection.md",
            "24-file-upload.md",
            "25-path-traversal.md",
            "26-transactions.md",
            "27-cloud-database.md",
            "28-bola.md",
            "29-components.md",
            "30-runtime-bypass.md",
        )

        for lab_page in lab_pages:
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text()
                evidence = content.index("## Evidence")
                hints = content.index("<summary>Hints</summary>")
                vulnerability = content.index("## Vulnerability and Impact")
                self.assertLess(evidence, hints)
                self.assertLess(hints, vulnerability)

    def test_target_setup_guides_use_restricted_egress_not_airplane_mode(self):
        root = Path(__file__).parent
        devom_setup = (root / "docs/01-devom-setup.md").read_text().lower()
        bugbazaar_setup = (root / "docs/02-bugbazaar-setup.md").read_text().lower()

        self.assertIn("network egress", devom_setup)
        self.assertIn("network egress", bugbazaar_setup)
        self.assertNotIn("airplane mode", bugbazaar_setup)
        self.assertNotIn("offline", bugbazaar_setup)

        for lab_page in ("27-cloud-database.md", "29-components.md", "30-runtime-bypass.md"):
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text().lower()
                self.assertNotIn("keep the emulator offline", content)


if __name__ == "__main__":
    unittest.main()
