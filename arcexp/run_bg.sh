#!/bin/bash
# Launch a resumable job detached, logging to exp/logs/<name>.log, pid in exp/logs/<name>.pid.
# The job is recorded in exp/logs/jobs.tsv; "__JOB_DONE__" is logged when it exits successfully, so
# `python3 -m arcexp.orchestrate resume` can relaunch unfinished jobs after a VM restart.
# Usage: bash arcexp/run_bg.sh <name> <cmd...>     (no-op if that job is already running)
cd "$(dirname "$0")/.."
bash arcexp/start_gateway.sh >/dev/null
name=$1; shift
pf=exp/logs/$name.pid
# alive = pid exists AND its command line is this job's command (pids are reused after a reboot)
if [ -f $pf ] && kill -0 $(cat $pf) 2>/dev/null && tr '\0' ' ' < /proc/$(cat $pf)/cmdline 2>/dev/null | grep -qF -- "$*"; then
  echo "$name already running"; exit 0; fi
grep -q "^$name	" exp/logs/jobs.tsv 2>/dev/null || printf '%s\t%s\t%s\n' "$name" "${ARC_WORKERS:-}" "$*" >> exp/logs/jobs.tsv
ARC_WORKERS=${ARC_WORKERS:-16} setsid nohup bash -c "$* && echo __JOB_DONE__" >> exp/logs/$name.log 2>&1 < /dev/null &
echo $! > $pf
echo "launched $name"
