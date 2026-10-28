# 14 — Command injection through file input

**Target:** Devom. Source-inspected; not runtime-tested. Complete [common setup](00-common-setup.md). Use a disposable container and a harmless text file only.

## Objective and challenge
Follow a profile picture upload from the app or API through server-side processing. Check whether characters in the filename affect the processing command. Use a harmless output marker, with no external callbacks, and compare the debug output with a normal upload.

## Before you begin

Follow [common setup](00-common-setup.md). Obtain an assigned disposable user ID and a small harmless file. The instructor must confirm that the container and its mounts are isolated. Source-based expectations below are unverified.

## Guided walkthrough

**Tools:** an HTTP proxy with a request editor, or an API client that can edit multipart filenames, and a harmless local file. The relevant request is `POST /upload_profile_pic` with multipart fields `user_id` and `file`; the response includes `server_debug` in the inspected source. Use the instructor's assigned ID and retain the original request as the control. A specific marker payload has not been tested, so ask the instructor to approve one before testing.

1. Create a normal multipart `POST /upload_profile_pic` request with fields `user_id` and `file`. Send it to the lab server and record the returned filename and `server_debug` field.
2. Inspect the upload handler in the pinned Devom source. Trace how the submitted filename becomes part of the server's processing command. Identify where input crosses into the shell.
3. With instructor approval, change only the multipart filename to include a harmless marker-producing test. Do not change files, launch network requests or access unrelated data. Send the test and record the exact filename as transmitted.
4. Compare `server_debug` with the normal upload. A distinct marker in command output may indicate that the filename affected shell processing; confirm the marker is not merely echoed as literal text.
5. If the upload fails before processing, inspect how the client, server and filesystem handled the filename. Do not assume injection succeeded from an HTTP status alone.

## Troubleshooting

Some filename characters may be rejected or normalized before the shell is reached. Ask the instructor for a permitted benign test if your client cannot preserve them.

<details markdown="1">
<summary>Hints</summary>

1. Examine multipart file metadata, not just file contents.
2. Inspect `/upload_profile_pic` and the way the filename is incorporated into a shell command.

</details>

## Evidence
Submit sanitized requests and the observed marker, expected versus actual behavior, affected trust boundary, and remediation using safe APIs without shell interpolation. Do not execute destructive commands or access unrelated files.

## Cleanup and review

Ask the instructor to remove the uploaded lab files during the normal reset. Which data entered the shell command, and how could the same processing be implemented without a shell?
