#!/bin/bash
# Launch a resumable job detached, logging to exp/logs/<name>.log. Usage: bash arcexp/run_bg.sh <name> <cmd...>
cd "$(dirname "$0")/.."
bash arcexp/start_gateway.sh >/dev/null
name=$1; shift
if pgrep -f "ARCJOB=$name " >/dev/null; then echo "$name already running"; exit 0; fi
setsid nohup bash -c "ARCJOB=$name ; $*" >> exp/logs/$name.log 2>&1 < /dev/null &
echo "launched $name"
