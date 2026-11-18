#!/bin/bash
# One-command resume after a VM/worker restart.  Usage: bash arcexp/resume.sh
cd "$(dirname "$0")/.."
bash arcexp/setup_env.sh >/dev/null
bash arcexp/start_gateway.sh
if ! pgrep -f "arcexp.run_loop|arcexp.phases" >/dev/null; then rm -rf exp/stage/*; fi
python3 -m arcexp.orchestrate resume 2>&1 | grep -v "already running"
echo "gateways: $(pgrep -fc 'python3 -m arcexp.gateway')"
