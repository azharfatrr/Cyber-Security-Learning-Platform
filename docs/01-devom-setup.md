# Devom setup

Complete [Common prerequisites](00-common-setup.md) first. This page prepares the Devom Android app and its backend; the app is supplied as a prebuilt APK. Learners do not build it from source.

**Status:** Instructions are based on the pinned repository and have not been runtime-validated as a manual setup. Have an instructor pilot them in the intended disposable environment before assigning labs.

## Pinned version and safety

Use the reviewed [Devom revision](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161): `af4290ce8d2178765bfc2bd96cf233f6d3d03161`. This checkout contains `server.py`, `requirements.txt`, and the prebuilt `Dvom.apk` at its root. Python dependencies in `requirements.txt` are not version-pinned; Python 3.12 matches the pinned Dockerfile, but compatibility of the manual setup has not been tested.

!!! danger "Run only in an isolated disposable lab"
    The pinned server starts Flask with `debug=True`, binds to `0.0.0.0`, and enables an ad-hoc TLS certificate. The debug server can expose sensitive server internals and is reachable on every host interface unless the host firewall restricts it. Use a disposable VM with an instructor-approved firewall/network policy. Do not run this service on a personal workstation with sensitive files, or expose it to public or corporate networks.

The server uses HTTPS with a generated, ad-hoc certificate. Certificate trust and the prebuilt Android app's behavior with that certificate are environment-specific and have not been verified here. Do not switch to HTTP or disable certificate checks globally just to make a connection work; stop and ask the instructor if the client rejects the certificate.

## Primary path: manual Python backend

Clone and pin the checkout in the disposable VM:

```bash title="01 · Clone and pin the reviewed checkout"
git clone https://github.com/memohk/Devom.git
cd Devom
git checkout af4290ce8d2178765bfc2bd96cf233f6d3d03161
```

Create an isolated Python environment, install the pinned checkout's requirements, and start the server from the repository root:

```bash title="02 · Create the Python environment and start the backend"
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python server.py
```

The server listens on port `8080` and creates its SQLite database and runtime directories under this checkout on first launch. Keep the checkout and all generated data inside the disposable lab. Stop the server with `Ctrl+C`; do not delete or reset generated data unless the instructor has approved the cleanup procedure.

The command occupies this terminal; leave it running. Open a second terminal at the checkout root for the local diagnostic and APK installation. The source defines `DVOM SERVER LIVE` at `/`. A loopback-only diagnostic can check that the local server responds:

```bash title="03 · Check the local HTTPS endpoint"
curl --insecure -i https://127.0.0.1:8080/
```

!!! info "Expected"
    The source-defined response is `DVOM SERVER LIVE`. `--insecure` applies only to this one request to the local ad-hoc certificate; it does not validate certificate trust and is not a recommended general client setting. This expected response is source-derived, not a claim that this setup has been run successfully.

## Install and configure the prebuilt Android app

With the emulator connected, install the APK from the pinned checkout in that second terminal:

```bash title="04 · Install the supplied Android APK"
adb devices
adb install Dvom.apk
```

!!! success "Expected"
    ADB reports `Success`. If installation fails because another app version is present, stop and ask the instructor; do not uninstall or clear app data to force it through.

The project README describes long-pressing the login logo to set the backend URL. For an Android Studio emulator running on the same host, `https://10.0.2.2:8080` commonly routes to the host service; for another emulator, use only the instructor-approved address and firewall path. The app's ability to trust the generated certificate is unverified; stop if it cannot connect rather than weakening network or certificate protections.

Lab-only default credentials in the inspected source:

- Mobile user: `cala` / `cala123`.
- Admin portal: `admin` / `admin123`.

Never reuse these credentials outside the disposable lab. Do not treat the ad-hoc TLS or application-layer encryption as a production security boundary.

For API exercises, the server returns encrypted JSON responses unless the request's `User-Agent` contains `Postman`. An instructor-approved local API client can use `User-Agent: Postman` to select plaintext responses in the inspected version. Keep any captured tokens and synthetic data private.

## URL for the Devom lab examples

The lab examples use the manual backend by default. If you chose the optional Compose path, replace port `8080` with `8443` in the `BASE` value. The server's ad-hoc certificate is not trusted by default, so the examples use `curl --insecure` on each individual loopback request only. Never use that option for a remote endpoint or disable certificate validation globally.

```bash title="Manual backend · default for lab examples"
BASE='https://127.0.0.1:8080'
```

For an instructor-approved API client or proxy, configure trust only for the local lab certificate. If it rejects the generated certificate and cannot be configured safely, stop and ask the instructor.

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

Compose bind-mounts `usersdb`, `uploads`, `jwt_keys`, and `templates`; keep these inside the disposable checkout. Do not remove or reset existing data without instructor approval. The service uses HTTPS on `https://127.0.0.1:8443/` with the same ad-hoc certificate. A remote emulator needs a separately approved isolated network configuration; loopback is not reachable from another host. The pinned Compose configuration and app connection have not been runtime-validated here.
