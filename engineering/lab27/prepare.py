#!/usr/bin/env python3
"""Apply the Lab 27 emulator configuration to the pinned BugBazaar source."""

from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
here = Path(__file__).resolve().parent

app_gradle = root / "app/build.gradle"
text = app_gradle.read_text()
assert "    namespace 'com.BugBazaar'\n" in text
text = text.replace(
    "    namespace 'com.BugBazaar'\n",
    "    namespace 'com.BugBazaar'\n    ndkVersion '26.1.10909125'\n",
    1,
)
assert '        applicationId "com.BugBazaar"\n' in text
text = text.replace(
    '        applicationId "com.BugBazaar"\n',
    '        applicationId "com.BugBazaar.lab27"\n',
    1,
)
app_gradle.write_text(text)

root_gradle = root / "build.gradle"
text = root_gradle.read_text()
assert "        jcenter()\n" in text
text = text.replace(
    "        maven { url 'https://jitpack.io' }\n        jcenter()\n",
    "        google()\n        mavenCentral()\n        maven { url 'https://jitpack.io' }\n",
    1,
)
root_gradle.write_text(text)

manifest = root / "app/src/main/AndroidManifest.xml"
text = manifest.read_text()
service = """        <service
            android:name=".MyFirebaseInstanceIDService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.INSTANCE_ID_EVENT" />
            </intent-filter>
        </service>
"""
assert service in text
text = text.replace(service, "", 1)
for old, new in (
    ("com.BugBazaar.permission.contacts", "com.BugBazaar.lab27.permission.contacts"),
    ("com.BugBazaar.permission.contact", "com.BugBazaar.lab27.permission.contact"),
    ("com.BugBazaar.UserProfile", "com.BugBazaar.lab27.UserProfile"),
    ("com.bugbazaar.mycontacts", "com.bugbazaar.lab27.mycontacts"),
    ("com.bugbazaar.provider.addresses", "com.bugbazaar.lab27.provider.addresses"),
):
    assert old in text, old
    text = text.replace(old, new)
manifest.write_text(text)

source_replacements = {
    "app/src/main/java/com/BugBazaar/ui/addresses/AddressContract.java": (
        "content://com.bugbazaar.provider.addresses/addresses",
        "content://com.bugbazaar.lab27.provider.addresses/addresses",
    ),
    "app/src/main/java/com/BugBazaar/provider/UserProfileProvider.java": (
        'AUTHORITY = "com.BugBazaar.UserProfile"',
        'AUTHORITY = "com.BugBazaar.lab27.UserProfile"',
    ),
    "app/src/main/java/com/BugBazaar/provider/UserProfileContract.java": (
        'CONTENT_AUTHORITY = "com.BugBazaar.UserProfile"',
        'CONTENT_AUTHORITY = "com.BugBazaar.lab27.UserProfile"',
    ),
    "app/src/main/java/com/BugBazaar/provider/MyContactsProvider.java": (
        'AUTHORITY = "com.bugbazaar.mycontacts"',
        'AUTHORITY = "com.bugbazaar.lab27.mycontacts"',
    ),
    "app/src/main/res/values/strings.xml": (
        '<string name="app_name">BugBazaar</string>',
        '<string name="app_name">BugBazaar Lab 27</string>',
    ),
}
for relative, (old, new) in source_replacements.items():
    path = root / relative
    content = path.read_text()
    assert old in content, relative
    path.write_text(content.replace(old, new, 1))

profile = root / "app/src/main/java/com/BugBazaar/ui/MyProfile.java"
text = profile.read_text()
needle = "        firebaseStorage = FirebaseStorage.getInstance();\n"
assert needle in text
text = text.replace(
    needle,
    needle + '        firebaseStorage.useEmulator("10.0.2.2", 9199);\n',
    1,
)
profile.write_text(text)

shutil.copyfile(here / "google-services.json", root / "app/google-services.json")
print("Lab 27 source prepared")
