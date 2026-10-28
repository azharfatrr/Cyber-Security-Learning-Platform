# Common setup

**Status:** Repository configuration inspected; setup and exercises have not been run. Provision an isolated disposable lab with an instructor before assigning these exercises. Do not expose intentionally vulnerable services to the internet or corporate networks.

## Reference versions

- [Devom](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161): `af4290ce8d2178765bfc2bd96cf233f6d3d03161`.
- [BugBazaar](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9): `fef6a899a684245eb70b2ab4be926f62be849ed9`.
- Review each project's license before internal distribution; Devom's README references a custom educational license and a LICENSE file that was not visible in the repository listing. Confirm permission where unclear.

## Environment

Use a disposable VM and Android emulator with synthetic data, Docker Engine/Compose, Git, Android SDK/ADB, Android Studio and a debugging proxy. Labs 29–30 may require a compatible instrumentable emulator and Frida tooling; configure those only on the lab device. Restrict network egress, particularly for BugBazaar, whose build includes Firebase and other external SDKs. A local Android emulator may need controlled access to the local backend; prevent access by unrelated hosts. Do not forward the proxy or service publicly.

## Devom

Clone the correct repository and pin the reviewed revision:

```bash
git clone https://github.com/memohk/Devom.git
cd Devom
git checkout af4290ce8d2178765bfc2bd96cf233f6d3d03161
```

The provided Compose file publishes `8443:8080` on all host interfaces by default. **Before starting**, change that mapping in the disposable copy to `127.0.0.1:8443:8080`, and verify the effective configuration with `docker compose config`. For a remote emulator, use an instructor-approved isolated network configuration instead; loopback is not reachable from a separate host. Start with `docker compose up --build`; check `http://127.0.0.1:8443/`, `/docs`, and `/admin`. Port 8443 is **HTTP**, not HTTPS. Compose bind-mounts persistent `usersdb`, `uploads`, and `jwt_keys` directories: keep them inside the disposable lab and do not reset or delete existing data without permission.

Install `Dvom.apk` from the pinned checkout on the lab emulator using `adb install Dvom.apk`. The README describes long-pressing the login logo to configure the backend URL; for the Android Studio emulator, `http://10.0.2.2:8443` commonly reaches the host loopback, but confirm with your emulator and firewall. The default mobile user is `cala` / `cala123`; admin portal is `admin` / `admin123`. These are lab-only credentials.

The server accepts ordinary JSON requests and, unless the `User-Agent` contains `Postman`, encrypts JSON responses using application-layer AES. For API investigation use an instructor-approved local proxy/client; `User-Agent: Postman` causes plaintext responses in the inspected server version. Do not assume TLS or encryption protects this environment.

## BugBazaar

Clone and pin as above, using `https://github.com/payatu/BugBazaar.git` and revision `fef6a899a684245eb70b2ab4be926f62be849ed9`. The repository contains Android source; `app/build.gradle` specifies compile SDK 34, min SDK 24, target SDK 32, and CMake 3.22.1. Import into Android Studio and have the instructor verify SDK, Gradle, native dependencies, Firebase configuration and the debug build before installation. Build dependencies may require network access during provisioning; disconnect or restrict egress for exercises. Do not use a real phone or real contacts. A working build and login have not been confirmed.

## Troubleshooting and evidence

If the backend fails, inspect `docker compose logs` and port availability. If ADB fails, verify `adb devices`, emulator status, and the SDK platform-tools path. If API responses look opaque, check the User-Agent and encryption behavior described above. Keep sanitized requests, responses and screenshots with timestamps; redact tokens and sensitive fields. Stop and ask the instructor if an endpoint points outside the approved environment.

## Command conventions

The examples use Bash and `curl` on Linux. They assume the server is on the same host. Set the base URL in your terminal:

```bash
BASE='http://127.0.0.1:8443'
curl -i "$BASE/"
```

The source returns `DVOM SERVER LIVE` at `/`; that expected response has not been verified in a running lab. For JSON API requests, `User-Agent: Postman` selects plaintext responses in the inspected server. `-i` includes response headers. Keep output containing tokens or synthetic personal information private.

Check the Android device connection:

```bash
adb devices
```

An authorized emulator should appear with the status `device`. If it does not, start the emulator and follow your organization's Android SDK setup. Install APKs only on the disposable lab device. Examples using variables such as `$TOKEN` and `$USER_ID` require values from your own lab session; do not paste placeholder values unchanged.
