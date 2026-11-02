#!/bin/bash
# AI assistance: ChatGPT (OpenAI) suggested CPU-aware worker
# selection and signal handling for background processes.

set -euo pipefail

WORKERS=${WORKERS:-$(nproc)}
OUT=${OUT:-$HOME/data/out}
pids=()

cleanup() {
    trap - INT TERM
    for pid in "${pids[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    wait 2>/dev/null || true
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

python3 steps/stats_prepare.py

mkdir -p "$OUT/stats"
rm -f "$OUT"/stats/part_*.csv

for k in $(seq 0 $((WORKERS - 1))); do
    python3 steps/stats_worker.py "$k" "$WORKERS" &
    pids+=("$!")
done

for pid in "${pids[@]}"; do
    wait "$pid"
done

cat "$OUT"/stats/part_*.csv | sort > "$OUT/stats.csv"

echo "stats: done with $WORKERS workers"
