# 25 — Server-side file retrieval traversal

**Target:** Devom. Source-inspected; not runtime-tested. Complete [Common prerequisites](00-common-setup.md) and [Devom setup](01-devom-setup.md). Instructor must place an innocuous, uniquely marked text file inside the disposable container outside its uploads directory and provide its path.

## Objective and challenge
Retrieve an uploaded file or contract normally, then test whether the same endpoint can reach the instructor's marker outside the uploads directory. Access only that marker; do not retrieve secrets or system files. Record the exact request and compare it with the normal retrieval.

## Before you begin

Get the marker's approved path and contents from the instructor. The marker must be inside the isolated container but outside its uploads directory. This exercise has not been piloted.

## Guided walkthrough

**Tools:** Bash and `curl`. A normal request can be inspected with the following command after replacing the filename with a known lab upload:

```bash
BASE='https://127.0.0.1:8080'
curl --insecure -i --path-as-is "$BASE/view_upload/LAB_FILENAME"
```

`--path-as-is` asks curl not to normalize path segments; other intermediaries may still alter them. Only attempt traversal to the instructor's approved marker. The exact marker path depends on the provisioned environment.

1. Retrieve a known lab upload or generated contract using its normal endpoint. Record the request and successful response as a baseline.
2. Inspect `/view_upload/<path:filename>` or `/download_pdf/<path:filename>` in the pinned server source. Note how the server combines the requested filename with the uploads directory.
3. Construct a request that references only the approved marker outside that directory. Send it through a client that lets you inspect the raw request path. Do not request system files or credentials.
4. Compare the response with the instructor's marker and the baseline. If the marker is returned, record the request path and the trust boundary crossed. If it is not, check the raw path for client or proxy normalization and report the result without claiming success.

## Troubleshooting

Some clients normalize path segments before transmission. Check the request actually sent and ask the instructor to confirm the marker exists in the container.

<details markdown="1">
<summary>Hints</summary>

1. The server implements `/download_pdf/<path:filename>` and `/view_upload/<path:filename>`.
2. Consider URL normalization and the difference between joining paths and enforcing a canonical directory boundary.

</details>

## Evidence
Submit the sanitized request, marker-only response, comparison with the normal retrieval, impact and a canonical-path containment remedy. Explain if your client or proxy normalized the request before it reached the server.

## Cleanup and review

Ask the instructor to remove the marker through the lab reset procedure. How does a canonical path check prevent access outside the intended directory? Why is joining two paths alone insufficient?
