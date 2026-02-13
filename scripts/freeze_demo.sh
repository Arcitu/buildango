#!/usr/bin/env bash
set -euo pipefail

# Example: create a local "frozen" run artifact folder.
RUN_ID="${1:-demo_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "frozen_runs/$RUN_ID"
echo '{"parcel_id":"P-123","jurisdiction":"DemoCity"}' > "frozen_runs/$RUN_ID/input.json"
echo '{"ir":"placeholder"}' > "frozen_runs/$RUN_ID/ir.json"
echo '{"output":"placeholder"}' > "frozen_runs/$RUN_ID/output.json"
echo "Frozen run created: frozen_runs/$RUN_ID"
