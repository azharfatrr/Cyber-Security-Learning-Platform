# Lab downloads

## Download once for all ten labs

The LabKit archive contains all four verified APKs plus the lab-owned setup scripts, Lab 27 Firebase configuration and synthetic fixtures, the Lab 30 hook, pinned dependency locks, and checksum manifest.

[Download LabKit-linux-x86_64.zip](assets/labkit/LabKit-linux-x86_64.zip)

LabKit SHA-256: `7d5042d8978f27b963ad4b28ce40f2111af6319b7dcd533e3a714340f98692cf`

Verify the downloaded archive before extracting it:

```bash
sha256sum --check <<'EOF'
7d5042d8978f27b963ad4b28ce40f2111af6319b7dcd533e3a714340f98692cf  LabKit-linux-x86_64.zip
EOF
```

After extraction, use the [Common prerequisites](00-common-setup.md) and run `./setup.sh` from the `LabKit` directory. The kit targets Linux x86_64 and requires an already installed Android 14 / API 34 x86_64 emulator. It does not bundle an Android SDK or emulator image and is not an offline package: its first-time bootstrap downloads pinned dependencies and analysis tools from documented upstream sources.

## Included APK inventory

The APKs are inside the LabKit archive under `apk/`. Use the package details and hashes here to verify each file. The site does not offer individual APK downloads.

| APK in LabKit | Package and version | SHA-256 | Source and provenance |
| --- | --- | --- | --- |
| `BugBazaar_v1.2.1.apk` | `com.BugBazaar` 1.0 (version code 1) | `c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c` | Official [BugBazaar v1.2.1 release](https://github.com/payatu/BugBazaar/releases/tag/v1.2.1), byte-for-byte unchanged; source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9) |
| `Dvom.apk` | `com.example.vulnappowasp` 1.0 | `afec11d202a4069880469274200bb377a9f1cb2205bad52c3f0f906c705cf409` | Prebuilt APK at Devom revision [`af4290ce8d2178765bfc2bd96cf233f6d3d03161`](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161) |
| `module-29-caller.apk` | `org.lab.module29caller` 1.0 | `5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc` | Project-built fixture for [Lab 29](29-components.md) |
| `bugbazaar-lab27-emulator.apk` | `com.BugBazaar.lab27` 1.0 (version code 1) | `b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604` | Project-built Lab 27 variant of the pinned BugBazaar source, configured for the local Firebase emulator |

The official BugBazaar file is byte-for-byte the upstream release. The Lab 27 file is a separate derived variant with its own application ID and local emulator endpoint; it is not a substitute for the official APK in Labs 29 or 30.

## Attribution and authorization

The repository owner has confirmed authorization to publicly redistribute the four verified APKs in this LabKit for educational lab use. This is separate from upstream licensing, does not change upstream ownership or license terms, and does not make third-party material MIT-licensed. See the repository `NOTICE` for the verified details.

- **BugBazaar** is by Payatu. The pinned repository revision has no license file or README license statement, and GitHub metadata declares no license. The public educational redistribution here relies on the separate repository-owner authorization, not an upstream open-source license.
- **Devom** is by `memohk`. Its pinned README describes a custom "Educational Use License" for personal learning, internal training, academic labs, authorized workshops, and ethical security research, and prohibits commercial redistribution, resale, and unauthorized use. The referenced `LICENSE` file is absent, so its full terms could not be read. All upstream rights remain with the author.
- **`module-29-caller.apk`** is project-built material; the root MIT license covers project-owned materials only.
- **`bugbazaar-lab27-emulator.apk`** is built from BugBazaar and remains a derivative; BugBazaar provenance and rights apply.

## Before installing

Use the kit installer only on the disposable emulator described in [Common prerequisites](00-common-setup.md). The installer verifies the archive's APK hashes and refuses to replace an existing package with a different APK. Review the target-specific steps before launching an app:

- [Devom setup](01-devom-setup.md) for Labs 09, 10, 14, 24–26, and 28.
- [BugBazaar setup](02-bugbazaar-setup.md) for Labs 27, 29, and 30.
