#!/bin/bash
# Idempotently start the budget gateway (root). Usage: bash arcexp/start_gateway.sh
cd "$(dirname "$0")/.."
if [ -S /run/arcgw/gw.sock ] && [ -f /run/arcgw/gateway.pid ] && kill -0 $(cat /run/arcgw/gateway.pid) 2>/dev/null; then
  echo "gateway already running (pid $(cat /run/arcgw/gateway.pid))"; exit 0
fi
mkdir -p exp/logs
setsid nohup python3 -m arcexp.gateway >> exp/logs/gateway.log 2>&1 < /dev/null &
for i in $(seq 1 50); do [ -S /run/arcgw/admin.sock ] && break; sleep 0.2; done
echo "gateway started (pid $(cat /run/arcgw/gateway.pid))"
