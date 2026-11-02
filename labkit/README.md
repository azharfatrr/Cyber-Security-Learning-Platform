# Cyber Security Learning Platform LabKit

This archive contains the verified Android targets and lab-owned support files for all ten labs. It is a single Linux x86_64 download. Start with the public Lab Downloads guide for host/emulator prerequisites and safety requirements, then run these commands from the extracted `LabKit` directory:

```bash
./setup.sh --check  # read-only host and emulator preflight
./setup.sh          # fetch the pinned dependencies and tools
```

The setup does not launch apps, change app data, or install APKs. Install only the target needed for a lab, for example `./install-apk.sh Dvom.apk` or `./install-apk.sh BugBazaar_v1.2.1.apk`. An existing package is left untouched; installation stops if its APK hash is different.

The LabKit requires Linux x86_64, Bash, Python 3.12+, Git, curl, Node.js 20+, npm, Java 17+, ADB, and an already booted Android 14/API 34 x86_64 instrumentable emulator. It does not contain Android SDK components or emulator images. First-time setup retrieves pinned dependencies and tools from their documented upstream sources; the kit is not an offline bundle.

The setup pins Devom to its reviewed source commit, installs the bundled Python lock and Firebase CLI npm lock, prefetches the local Storage emulator, and installs matching Frida 17.4.2 and JADX 1.5.1 host tools. It does not copy or start `frida-server` on the emulator; follow Lab 30's explicit ADB commands when you choose to do that exercise.

Use only a disposable lab environment with synthetic data. Keep vulnerable services and emulator endpoints isolated, and follow each lab's documented egress restrictions.
