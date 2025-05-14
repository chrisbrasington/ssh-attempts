### `failed_login_analyzer.py`

#### Overview

This Python script analyzes SSH login logs (`auth.log*`) to gather statistics about **failed** and **successful login attempts**, and identifies **bad actor IPs** associated with failed attempts. The script also prints the **date range** of the log entries and raw **successful login data**.

#### Features

* Tracks **failed login attempts** by **user**.
* Tracks **successful login attempts** by **user**.
* Identifies **bad actor IPs** based on failed logins.
* Prints the **date range** for the logs.
* Outputs raw **successful login** entries.
* Displays total counts for failed and successful attempts.

#### Requirements

* Python 3.x
* Access to `/var/log/auth.log*` (typically requires sudo)

#### Usage

1. Clone or download the script to your system.
2. Run the script:

   ```bash
   python failed_login_analyzer.py
   ```

#### Example Output

```plaintext
❌ Failed Login Attempts

User                 Attempts
------------------------------
root                       12
admin                       5
test                        3
------------------------------
Total                      20

✅ Successful Logins

User                 Logins
------------------------------
user1                      4
------------------------------
Total                      4

📅 Date range:
  First: 2025-05-10 01:22:13
  Last : 2025-05-14 11:17:44

📋 Raw Successful Login Data:
May 11 01:47:52 sshd[1990726]: Accepted publickey for user1 from 192.168.0.53 port 46026 ssh2
May 11 02:25:10 sshd[1991345]: Accepted password for user1 from 192.168.0.53 port 46028 ssh2

🚨 Bad Actor IPs (Failed Login Attempts):
x.x.x.x, y.y.y.y, z.z.z.z
```

#### Notes

* The script scans all available `auth.log*` files, including rotated logs (`.gz`).
* It aggregates failed login attempts by user and IP, showing the **most frequent offenders**.
* The script outputs **date ranges** for log entries.

#### License

MIT License.
