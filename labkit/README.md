# Cyber Security Learning Platform LabKit

This optional archive contains the verified Android targets and support files for all ten labs. Start with the public Common prerequisites guide for point-by-point host/emulator requirements and safety boundaries. You can prepare only your chosen lab's tools independently, or run the convenience bootstrap from the extracted `LabKit` directory:

```bash
./setup.sh --check  # read-only host and emulator preflight
./setup.sh          # fetch the pinned dependencies and tools
```

The setup does not launch apps, change app data, or install APKs. Install only the target needed for a lab, for example `./install-apk.sh Dvom.apk` or `./install-apk.sh BugBazaar_v1.2.1.apk`. An existing package is left untouched; installation stops if its APK hash is different.

The full bootstrap requires Linux x86_64, Bash, Python 3.12+ with venv/ensurepip, Git, curl, Node.js 20+, npm, Java 17+, ADB and an already booted Android 14/API 34 x86_64 emulator. Only Lab 30 requires instrumentation support. The archive does not contain Android SDK components or emulator images.

Lab 27 includes its pinned Linux Firebase CLI executable, Storage runtime, emulator UI, APK, configuration and fixtures. With the host tools and Android emulator ready, follow BugBazaar setup to install the variant, then run `./lab27/reset.sh`. This archive path needs no npm installation, Firebase account or separate Lab 27 dependency fetch. The repository-only path still uses the included npm lock to prepare its CLI independently.

Other labs are not a fully disconnected environment. The optional bootstrap downloads the reviewed Devom source and hash-locked Python dependencies, matching Frida 17.4.2 and JADX 1.5.1 tools. It does not copy or start `frida-server` on Android; follow Lab 30's explicit ADB commands.

Use only a disposable lab environment with synthetic data. Keep vulnerable services and emulator endpoints isolated, and follow each lab's documented egress restrictions.
