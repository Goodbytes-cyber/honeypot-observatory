"""Checks the downloaded files before they are committed: valid JSON with the expected keys,
a period end newer than or equal to the one already in the repository, a CSV with the expected
header, and no IPv4 address in either file (the observatory publishes aggregates only)."""
import csv
import json
import re
import sys

new_json, old_json, new_csv = sys.argv[1:4]
d = json.load(open(new_json))
for k in ("version", "generated", "period", "totals"):
    if k not in d:
        sys.exit(f"missing key: {k}")
try:
    old_end = json.load(open(old_json))["period"]["end"]
except (OSError, ValueError, KeyError):
    old_end = ""
if d["period"]["end"] < old_end:
    sys.exit("period end is older than the one in the repository")
rows = list(csv.reader(open(new_csv)))
if not rows or rows[0] != ["section", "rank", "label", "value"]:
    sys.exit("unexpected CSV header")
ipv4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
for f in (new_json, new_csv):
    if ipv4.search(open(f).read()):
        sys.exit(f"IPv4 address found in {f}")
print("ok", d["period"]["end"])
