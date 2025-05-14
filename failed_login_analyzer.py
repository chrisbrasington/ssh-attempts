import re
import sys
import gzip
import glob
from datetime import datetime
from collections import defaultdict


class FailedLoginAnalyzer:
    def __init__(self, log_glob="/var/log/auth.log*"):
        self.log_glob = log_glob
        self.failed_attempts = defaultdict(int)
        self.success_attempts = defaultdict(int)
        self.success_lines = []  # Store raw success lines
        self.dates = []
        self.total_failed = 0
        self.total_success = 0

        # Match failed (valid and invalid users)
        self.failed_pattern = re.compile(
            r"^([A-Z][a-z]{2} +\d+ \d{2}:\d{2}:\d{2}) .*sshd.*Failed password for (invalid user )?(\w+)"
        )
        # Match successful login
        self.success_pattern = re.compile(
            r"^([A-Z][a-z]{2} +\d+ \d{2}:\d{2}:\d{2}) .*sshd.*Accepted \w+ for (\w+)"
        )

    def parse_logs(self):
        log_files = sorted(glob.glob(self.log_glob))
        for file in log_files:
            try:
                if file.endswith(".gz"):
                    with gzip.open(file, "rt", encoding="utf-8", errors="ignore") as f:
                        self._parse_file(f)
                else:
                    with open(file, "r", encoding="utf-8", errors="ignore") as f:
                        self._parse_file(f)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    def _parse_file(self, file_obj):
        for line in file_obj:
            # Check for failed login
            failed_match = self.failed_pattern.search(line)
            if failed_match:
                date_str, _, user = failed_match.groups()
                self.failed_attempts[user] += 1
                self.total_failed += 1
                try:
                    self.dates.append(self._parse_date(date_str))
                except ValueError:
                    pass
                continue

            # Check for successful login
            success_match = self.success_pattern.search(line)
            if success_match:
                date_str, user = success_match.groups()
                self.success_attempts[user] += 1
                self.total_success += 1
                self.success_lines.append(line.strip())  # Store raw line for successes
                try:
                    self.dates.append(self._parse_date(date_str))
                except ValueError:
                    pass

    def _parse_date(self, date_str):
        current_year = datetime.now().year
        return datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")

    def print_summary(self):
        # Print failed attempts
        print("\n❌ Failed Login Attempts")
        if not self.failed_attempts:
            print("  No failed login attempts found.")
        else:
            print(f"\n{'User':<20} {'Attempts':>8}")
            print("-" * 30)
            for user, count in sorted(self.failed_attempts.items(), key=lambda x: x[1], reverse=True):
                print(f"{user:<20} {count:>8}")
            print("-" * 30)
            print(f"{'Total':<20} {self.total_failed:>8}")

        # Print successful attempts
        print("\n✅ Successful Logins")
        if not self.success_attempts:
            print("  No successful login attempts found.")
        else:
            print(f"\n{'User':<20} {'Logins':>8}")
            print("-" * 30)
            for user, count in sorted(self.success_attempts.items(), key=lambda x: x[1], reverse=True):
                print(f"{user:<20} {count:>8}")
            print("-" * 30)
            print(f"{'Total':<20} {self.total_success:>8}")

        # Date range
        if self.dates:
            first = min(self.dates)
            last = max(self.dates)
            print("\n📅 Date range:")
            print(f"  First: {first.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Last : {last.strftime('%Y-%m-%d %H:%M:%S')}")

        # Print raw successful login data
        print("\n📋 Raw Successful Login Data:")
        for line in self.success_lines:
            print(line)


if __name__ == "__main__":
    analyzer = FailedLoginAnalyzer()
    analyzer.parse_logs()
    analyzer.print_summary()

