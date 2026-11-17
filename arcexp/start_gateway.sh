#!/bin/bash
# Idempotently start the budget gateway (root). Usage: bash arcexp/start_gateway.sh
cd "$(dirname "$0")/.."
mkdir -p exp/logs /run/arcgw
exec 9>/run/arcgw.start.lock
flock 9   # one starter at a time
if [ -f /run/arcgw/gateway.pid ] && kill -0 "$(cat /run/arcgw/gateway.pid)" 2>/dev/null \
   && pgrep -f "python3 -m arcexp.gateway" >/dev/null; then
  echo "gateway already running (pid $(cat /run/arcgw/gateway.pid))"; exit 0
fi
pkill -f "python3 -m arcexp.gateway" 2>/dev/null; sleep 1
rm -f /run/arcgw/gateway.pid /run/arcgw/admin.sock /run/arcgw/gw.sock
setsid nohup python3 -m arcexp.gateway >> exp/logs/gateway.log 2>&1 < /dev/null 9>&- &
for i in $(seq 1 100); do [ -S /run/arcgw/gw.sock ] && [ -f /run/arcgw/gateway.pid ] && break; sleep 0.2; done
echo "gateway started (pid $(cat /run/arcgw/gateway.pid))"
