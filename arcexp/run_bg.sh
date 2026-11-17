#!/bin/bash
# Launch a resumable job detached, logging to exp/logs/<name>.log, pid in exp/logs/<name>.pid.
# Usage: bash arcexp/run_bg.sh <name> <cmd...>     (no-op if that job is already running)
cd "$(dirname "$0")/.."
bash arcexp/start_gateway.sh >/dev/null
name=$1; shift
pf=exp/logs/$name.pid
if [ -f $pf ] && kill -0 $(cat $pf) 2>/dev/null; then echo "$name already running"; exit 0; fi
setsid nohup bash -c "$*" >> exp/logs/$name.log 2>&1 < /dev/null &
echo $! > $pf
echo "launched $name"
