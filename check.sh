#!/bin/bash

# Default log file (can be overridden with an argument)
LOGFILE="${1:-/var/log/auth.log}"

# Extract usernames from both "for" and "invalid user" patterns
grep "Failed password" "$LOGFILE" \
    | awk '
        /invalid user/ {
            for (i=1; i<=NF; i++) {
                if ($i == "user") {
                    print $(i+1)
                    break
                }
            }
        }
        !/invalid user/ {
            for (i=1; i<=NF; i++) {
                if ($i == "for") {
                    print $(i+1)
                    break
                }
            }
        }
    ' | sort | uniq -c | sort -nr

