# Lab 1 Measurements — fonsifdez

## Machine
Machine details are recorded in machine.txt.

## Task 3 — Auditing

Command:
DATA=~/data/sales_2025_sample.csv /usr/bin/time -f "$T" python3 steps/audit.py

Dataset: 100,000 orders

Results:
- Elapsed time: 0.57 seconds
- User CPU time: 1.65 seconds
- System CPU time: 0.14 seconds
- Peak memory: 129,048 KB
- Output: 100,000 lines written

## Worker Experiment

Command:
bash tools/sweep.sh fonsifdez

Tested 1, 2, 4, 8, and 16 workers, three times each.

Results saved in members/fonsifdez/sweep.csv.

## Output Verification

Command:
python3 tools/check.py

Results:
- Revenue by region and month: FAIL (missing)
- Regional extracts: FAIL (six empty files)
- Audit: PASS
- Segments: PASS
- Statistics: PASS

These results describe the state of the pipeline at the time of testing.
