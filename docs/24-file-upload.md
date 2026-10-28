# 24 — Unrestricted file upload

**Target:** Devom. Source-inspected; not runtime-tested. Complete [common setup](00-common-setup.md).

## Objective and challenge
Check whether the profile picture upload validates file type and ownership. First upload a harmless image. Then try a small text file with a different declared type or extension, and check whether you can retrieve it. Do not upload executable code or real data.

## Before you begin

Follow [common setup](00-common-setup.md). Obtain a disposable user ID, a harmless image and a small text file containing a unique synthetic marker. These steps are source-based and have not been piloted.

## Guided walkthrough

**Tools:** Bash, `curl` and two harmless files. Create the text sample in an instructor-approved working directory, using a new filename so you do not overwrite an existing file:

```bash
printf '%s\n' 'LAB_UPLOAD_MARKER' > lab-marker.txt
BASE='http://127.0.0.1:8443'
USER_ID='LAB_USER_ID'
curl -i -F "user_id=$USER_ID" -F 'file=@lab-marker.txt;type=text/plain' "$BASE/upload_profile_pic"
```

Replace the ID with your assigned user. Repeat with an instructor-provided image by changing the file path and MIME type. The command is derived from the handler and has not been piloted; inspect the returned filename before attempting retrieval. Do not upload an executable file.

1. Send a multipart `POST /upload_profile_pic` with the assigned `user_id` and the image in field `file`. Record the response, including its returned filename.
2. Retrieve the returned filename from `/view_upload/<filename>` and record the response status and content type. This is your normal-file baseline.
3. Repeat the upload using the harmless text file. Record its actual content, filename, declared multipart content type and server response. Use only an instructor-approved test user ID.
4. If a filename is returned, request it through `/view_upload/<filename>`. Check whether the synthetic marker is present and compare the response headers with the baseline.
5. Inspect the handler for file-type and ownership checks. Explain what the results demonstrate and what they do not: storage or retrieval of text does not establish code execution.

## Troubleshooting

Use the returned filename rather than assuming the server preserves your original name. If retrieval fails, record the response and check whether upload succeeded.

<details markdown="1">
<summary>Hints</summary>

1. Compare content, filename and multipart content type.
2. Inspect `/upload_profile_pic` and `/view_upload`; saving a file alone is not proof of server-side code execution.

</details>

## Evidence
Provide sanitized request metadata, returned filename, retrieval response, actual content type, impact limits and an allowlist/storage/access-control remediation.

## Cleanup and review

Ask the instructor to remove the two test uploads at reset. Where should content validation and access control be enforced, and why should uploaded content be stored separately from executable application code?
