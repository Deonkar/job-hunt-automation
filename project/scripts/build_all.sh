#!/usr/bin/env bash
# Rebuild every role variant and every country resume, then render PDFs and print page counts.
# Countries without "base_variant" use the first variant.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUTF8=1
stem=$(py -3 -c "import json,re;print(re.sub(r'\W+','_',json.load(open('data/profile.json',encoding='utf-8'))['name']).strip('_').lower())")
first=$(ls variants/*.json | head -1)
docs=()
for v in variants/*.json; do
  out="out/variants/${stem}_$(basename "$v" .json).docx"
  mkdir -p out/variants
  py -3 scripts/build_resume.py "$v" "$out" >/dev/null; docs+=("$out")
done
for c in countries/*.json; do
  base=$(py -3 -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('base_variant') or '')" "$c")
  v=${base:+variants/$base.json}; v=${v:-$first}
  out="out/countries/${stem}_$(basename "$c" .json).docx"
  mkdir -p out/countries
  py -3 scripts/build_resume.py "$v" "$out" --country "$c" >/dev/null; docs+=("$out")
done
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/to_pdf.ps1 "${docs[@]}"
