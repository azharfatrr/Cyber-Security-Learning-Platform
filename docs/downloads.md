# Lab downloads

These four APKs are hosted in this repository under `docs/assets/apk/`. Install them only in the disposable lab described in [Common prerequisites](00-common-setup.md). Do not download lab targets from third-party APK sites.

Verify every file before installing it. Run this on the host from a checkout of this repository:

```bash title="Verify all published APKs"
cd docs/assets/apk
sha256sum --check <<'EOF'
c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c  BugBazaar_v1.2.1.apk
afec11d202a4069880469274200bb377a9f1cb2205bad52c3f0f906c705cf409  Dvom.apk
5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc  module-29-caller.apk
b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604  bugbazaar-lab27-emulator.apk
EOF
```

!!! success "Expected"
    Every line reports `OK`. A `FAILED` line means the file does not match this page; stop and obtain a fresh copy from the same repository revision.

## Files

| File | Package and version | SHA-256 | Source |
| --- | --- | --- | --- |
| [BugBazaar_v1.2.1.apk](assets/apk/BugBazaar_v1.2.1.apk) | `com.BugBazaar` 1.0 (version code 1) | `c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c` | Official [BugBazaar v1.2.1 release](https://github.com/payatu/BugBazaar/releases/tag/v1.2.1) built from source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9) |
| [Dvom.apk](assets/apk/Dvom.apk) | `com.example.vulnappowasp` 1.0 | `afec11d202a4069880469274200bb377a9f1cb2205bad52c3f0f906c705cf409` | Prebuilt APK at Devom revision [`af4290ce8d2178765bfc2bd96cf233f6d3d03161`](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161) |
| [module-29-caller.apk](assets/apk/module-29-caller.apk) | `org.lab.module29caller` 1.0 | `5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc` | Project-built fixture for [Lab 29](29-components.md) |
| [bugbazaar-lab27-emulator.apk](assets/apk/bugbazaar-lab27-emulator.apk) | `com.BugBazaar.lab27` 1.0 (version code 1) | `b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604` | Project-built Lab 27 variant of the pinned BugBazaar source revision `fef6a899a684245eb70b2ab4be926f62be849ed9`, configured for the local emulator in `engineering/lab27/` |

The official BugBazaar file is byte-for-byte the upstream release. The Lab 27 file is not the official app: it has its own application ID, points only at the local Firebase Storage emulator, and must not be used as a substitute for the official APK in Labs 29 or 30.

## Attribution and license status

These are third-party or third-party-derived works. Any license for this repository's own material does not relicense them.

- **BugBazaar** is by Payatu. At the pinned release and source revision, the repository contains no license file and no license statement in its README, and its GitHub metadata declares no license. Redistribution permission has therefore not been established. The binary is mirrored for the authorized training use described on this site, and all upstream rights remain with the authors.
- **Devom** is by `memohk`. Its README at the pinned revision states that DVOM is provided under a custom "Educational Use License" for personal learning, internal training, academic labs, authorized workshops, and ethical security research, and prohibits commercial redistribution, resale, and unauthorized use. The referenced `LICENSE` file is absent at that revision, so the full terms could not be read. The prebuilt `Dvom.apk` is mirrored unchanged for that educational use, and all upstream rights remain with the author.
- **module-29-caller.apk** is built by this project for the Lab 29 exercise and is project-owned material.
- **bugbazaar-lab27-emulator.apk** is built by this project from the pinned BugBazaar source. Because it is a derivative of BugBazaar, the BugBazaar provenance and rights statement above also applies to it.

If you need to redistribute any of these files outside an authorized educational setting, obtain permission from the upstream author first.

## Before installing

Each target setup page owns installation and verification:

- [Devom setup](01-devom-setup.md) for Labs 9, 10, 14, 24–26, and 28.
- [BugBazaar setup](02-bugbazaar-setup.md) for Labs 27, 29, and 30.

BugBazaar's official APK and its Lab 27 variant can be installed side by side because they use different application IDs. Do not uninstall or clear an existing package to force an installation.
