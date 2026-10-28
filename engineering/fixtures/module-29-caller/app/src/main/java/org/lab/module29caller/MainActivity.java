package org.lab.module29caller;

import android.app.Activity;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Process;
import android.widget.TextView;

public class MainActivity extends Activity {
    private static final Uri ADDRESSES_URI = Uri.parse(
            "content://com.bugbazaar.provider.addresses/addresses");
    private static final String NICKNAME = "LAB29-PILOT-20261028-7F3A";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        TextView result = new TextView(this);
        result.setTextSize(18);
        result.setPadding(32, 48, 32, 32);
        setContentView(result);

        StringBuilder text = new StringBuilder()
                .append("Module 29 Provider Caller\n\n")
                .append("Caller package: ").append(getPackageName()).append('\n')
                .append("Caller UID: ").append(Process.myUid()).append('\n')
                .append("URI: ").append(ADDRESSES_URI).append('\n')
                .append("Operation: read-only query\n")
                .append("Filter: nickname = ").append(NICKNAME).append("\n\n")
                .append("Result:\n");

        try (Cursor cursor = getContentResolver().query(
                ADDRESSES_URI,
                new String[]{"nickname", "address"},
                "nickname = ?",
                new String[]{NICKNAME},
                null)) {
            if (cursor == null || !cursor.moveToFirst()) {
                text.append("No matching row returned.");
            } else {
                int nicknameColumn = cursor.getColumnIndexOrThrow("nickname");
                int addressColumn = cursor.getColumnIndexOrThrow("address");
                do {
                    text.append(cursor.getString(nicknameColumn)).append('\n')
                            .append(cursor.getString(addressColumn)).append('\n');
                } while (cursor.moveToNext());
            }
        } catch (Exception error) {
            text.append("Query failed: ")
                    .append(error.getClass().getSimpleName())
                    .append(": ")
                    .append(error.getMessage());
        }

        result.setText(text.toString());
    }
}
