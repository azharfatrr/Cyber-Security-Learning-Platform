# Lab 27 local Storage emulator

The download includes Firebase CLI 15.34.2 as `firebase-tools-linux`, Storage runtime 1.1.3 and emulator UI 1.15.0 in the workspace cache. Verify the archive and manifest first. With your Linux x86_64 host tools and Java ready, no npm installation or separate Lab 27 dependency download is needed. The repository-only preparation path uses `node_modules/.bin/firebase` instead; the lifecycle scripts accept either path.

From the extracted LabKit directory:

```bash
cd lab27
./reset.sh   # stop, clear only the LabKit emulator workspace, start and seed
./start.sh   # start the emulator only
./seed.sh    # re-upload the synthetic fixture files
./stop.sh    # stop the emulator
```

The Storage emulator and UI bind to host loopback at `127.0.0.1:9199` and `127.0.0.1:4000`; the Android emulator reaches Storage through `10.0.2.2:9199`. Keep those ports inside the disposable lab. The included `storage.rules` are intentionally permissive and must never be deployed to a cloud project. Use synthetic data only.

The prebuilt Lab 27 APK is at `apk/bugbazaar-lab27-emulator.apk`. `./install-apk.sh bugbazaar-lab27-emulator.apk` installs it only when that exact package is absent; an existing package with a different APK hash causes the command to stop without replacing or clearing it.
