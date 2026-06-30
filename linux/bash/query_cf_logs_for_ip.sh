#!/bin/bash
# Query all gzipped CloudFront logs in S3 for a specific IP pattern
# Usage: ./query_all_cf_logs.sh [s3-path] <ip-pattern>
# Example: ./query_all_cf_logs.sh 108.165
#          ./query_all_cf_logs.sh s3://bucket/path 108.165

BUCKET_PATH="${1}"
IP_PATTERN="${2}"
START_DATE="${3}"
END_DATE="${4}"

# Default bucket path 
DEFAULT_BUCKET="s3://web-production-web-ui-cloudfront-logs/web-ui-cloudfront"

# Number of parallel downloads/processes
CONCURRENCY=8

# Handle arguments shifts if custom bucket isn't provided
if [[ ! "$BUCKET_PATH" =~ ^s3:// ]]; then
    END_DATE="$START_DATE"
    START_DATE="$IP_PATTERN"
    IP_PATTERN="$BUCKET_PATH"
    BUCKET_PATH="$DEFAULT_BUCKET"
fi

if [ -z "$IP_PATTERN" ]; then
    echo "Usage: $0 [s3-path] <ip-pattern> [start-date: YYYY-MM-DD] [end-date: YYYY-MM-DD]"
    exit 1
fi

# Keep logs on stderr so they don't mix with your terminal data stream
exec 3>&1
exec 1>&2

echo "🔍 Querying CloudFront logs for IP: $IP_PATTERN"
echo "📂 Bucket path: $BUCKET_PATH"
[ -n "$START_DATE" ] && echo "📅 Start Date: $START_DATE"
[ -n "$END_DATE" ] && echo "📅 End Date:   $END_DATE"
echo "⚡ Parallelism: $CONCURRENCY workers"
echo ""

echo "📋 Listing log files..."
RAW_LOG_FILES=$(aws s3 ls "$BUCKET_PATH" --recursive | awk '{print $4}' | grep "\.gz$")

# Filter files down to the exact day range
LOG_FILES=$(echo "$RAW_LOG_FILES" | awk -v start="$START_DATE" -v end="$END_DATE" '
    BEGIN {
        gsub("-", "", start)
        gsub("-", "", end)
    }
    {
        match($0, /[0-9]{4}-[0-9]{2}-[0-9]{2}/)
        if (RSTART > 0) {
            file_date = substr($0, RSTART, RLENGTH)
            gsub("-", "", file_date)

            if (start != "" && file_date < start) next
            if (end != "" && file_date > end) next
        } else if (start != "" || end != "") {
            next
        }
        print $0
    }
')

FILE_COUNT=$(echo "$LOG_FILES" | tr -d ' ' | wc -l)

if [ -z "$LOG_FILES" ] || [ "$FILE_COUNT" -eq 0 ]; then
    echo "❌ No log files found matching those dates at $BUCKET_PATH"
    exit 1
fi

echo "✅ Found $FILE_COUNT log files matching date criteria"
echo "Processing downloads in parallel..."
echo ""

BUCKET_NAME=$(echo "$BUCKET_PATH" | cut -d'/' -f3)

export BUCKET_NAME
export IP_PATTERN

# Restore stdout for the pure data dump
exec 1>&3

# Process files concurrently and output standard space-padded counts
echo "$LOG_FILES" | xargs -P "$CONCURRENCY" -I {} sh -c '
    aws s3 cp "s3://${BUCKET_NAME}/{}" - 2>/dev/null | \
    gunzip | \
    grep "^[^#]" | \
    awk -F"\t" "\$5 ~ /^${IP_PATTERN}/ {print \$5}"
' | sort | uniq -c | sort -rn

# Redirect logging output back to stderr for the final confirmation
exec 1>&2
echo ""
echo "✅ Query complete"
