# Lab 27 local Storage emulator

Run these scripts from the extracted LabKit directory after `./setup.sh` has installed the pinned Firebase CLI.

```bash
cd lab27
./reset.sh   # stop, clear only the LabKit emulator workspace, start and seed
./start.sh   # start the emulator only
./seed.sh    # re-upload the synthetic fixture files
./stop.sh    # stop the emulator
```

The Storage emulator and UI bind to host loopback at `127.0.0.1:9199` and `127.0.0.1:4000`; the Android emulator reaches Storage through `10.0.2.2:9199`. Keep those ports inside the disposable lab. The included `storage.rules` are intentionally permissive and must never be deployed to a cloud project. Use synthetic data only.

The prebuilt Lab 27 APK is at `apk/bugbazaar-lab27-emulator.apk`. `./install-apk.sh bugbazaar-lab27-emulator.apk` installs it only when that exact package is absent; an existing package with a different APK hash causes the command to stop without replacing or clearing it.
