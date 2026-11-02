# Devom setup

Complete [Common prerequisites](00-common-setup.md) first and run the LabKit bootstrap once. The LabKit prepares the pinned Devom checkout and isolated Python environment; the Android app is supplied as a verified prebuilt APK.

**Verification:** The backend and API steps on this page were tested again on 2 November 2026 over loopback, using Python 3.14 and Flask 3.1.3. The optional Android app steps depend on your emulator and certificate setup.

## Pinned version and safety

Use the reviewed [Devom revision](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161): `af4290ce8d2178765bfc2bd96cf233f6d3d03161`. The LabKit checks out this exact commit into `.labkit/Devom` and installs the dependencies from its bundled, fully pinned lock file rather than the upstream unpinned `requirements.txt`. Python 3.12 matches the pinned Dockerfile; the tested loopback run used Python 3.14 with Flask 3.1.3.

!!! danger "Run only in an isolated disposable lab"
    The pinned server starts Flask with `debug=True`, binds to `0.0.0.0`, and enables an ad-hoc TLS certificate. The debug server can expose sensitive server internals and is reachable on every host interface unless the host firewall restricts it. Use a disposable VM with an approved firewall. Restrict network egress, block public and corporate access, and allow only the local host/emulator path required by the selected lab. Do not run this service on a personal workstation with sensitive files.

The server uses HTTPS with a generated, ad-hoc certificate. Certificate trust and the prebuilt Android app's behavior with that certificate depend on your environment. Do not switch to HTTP or disable certificate checks globally just to make a connection work; if the client rejects the certificate, use the API workflow in the labs or stop.

## Primary path: Python backend

After completing the LabKit bootstrap, start the backend from the LabKit directory:

```bash title="Start the pinned Devom backend"
cd .labkit/Devom
source .venv/bin/activate
python server.py
```

The server listens on port `8080` and creates its SQLite database and runtime directories under this checkout on first launch. Keep the checkout and all generated data inside the disposable lab. Stop the server with `Ctrl+C`; do not delete or reset generated data unless your lab policy approves the cleanup procedure.

Leave the server running in this terminal. Open a second terminal at the checkout root to check the local server. Return to the LabKit directory for APK installation. The source defines the response `DVOM SERVER LIVE` at `/`; check it with this loopback-only request:

```bash title="03 · Check the local HTTPS endpoint"
curl --insecure -i https://127.0.0.1:8080/
```

!!! info "Expected"
    The source-defined response is `DVOM SERVER LIVE`. `--insecure` skips certificate validation for this one local request. It does not establish trust in the ad-hoc certificate; do not use it as a general client setting.

## Install and configure the prebuilt Android app

The verified `Dvom.apk` is included in the LabKit; see [Lab downloads](downloads.md) for its provenance and hash. From the LabKit directory, install it on the selected disposable emulator:

```bash title="04 · Verify and install the supplied Android APK"
./install-apk.sh Dvom.apk
```

!!! success "Expected"
    The installer verifies the bundled hash before using ADB. It installs only when the package is absent, or reports that the identical verified APK is already installed. If another version is present, stop and use a fresh disposable emulator; the installer will not replace it or clear app data.

The project README describes long-pressing the login logo to set the backend URL. For an Android Studio emulator running on the same host, `https://10.0.2.2:8080` commonly routes to the host service; for another emulator, use only the approved address and firewall path. If the app cannot connect, use the API workflow in the labs rather than weakening network or certificate protections.

Lab-only default credentials in the inspected source:

- Mobile user: `cala` / `cala123`.
- Admin portal: `admin` / `admin123`.

Never reuse these credentials outside the disposable lab. Do not treat the ad-hoc TLS or application-layer encryption as a production security boundary.

For API exercises, the server returns encrypted JSON responses unless the request's `User-Agent` contains `Postman`. A local API client can use `User-Agent: Postman` to select plaintext responses in the inspected version. Keep any captured tokens and synthetic data private.

## URL for the Devom lab examples

The lab examples use the manual backend by default. If you chose the optional Compose path, replace port `8080` with `8443` in the `BASE` value. The server's ad-hoc certificate is not trusted by default, so the examples use `curl --insecure` on each individual loopback request only. Never use that option for a remote endpoint or disable certificate validation globally.

```bash title="Manual backend · default for lab examples"
BASE='https://127.0.0.1:8080'
```

For a local API client or proxy, configure trust only for the local lab certificate. If it rejects the generated certificate and cannot be configured safely, use `curl --insecure` for loopback requests as shown, or stop.

## Optional alternative: Docker Compose

Docker is optional; the manual Python path above is the primary setup. The pinned Compose file maps container port `8080` to host port `8443` on all host interfaces by default. In the disposable checkout, change the mapping to loopback before starting:

```yaml title="Optional · Bind Compose to host loopback"
ports:
  - "127.0.0.1:8443:8080"
```

Verify the effective configuration, then start the backend:

```bash title="Start the optional Compose backend"
docker compose config
docker compose up --build
```

Compose bind-mounts `usersdb`, `uploads`, `jwt_keys`, and `templates`; keep these inside the disposable checkout. Do not remove or reset existing data without approval. The service uses HTTPS on `https://127.0.0.1:8443/` with the same ad-hoc certificate. A remote emulator needs a separately approved isolated network configuration; loopback is not reachable from another host. The Compose path was not part of the tested loopback run.
