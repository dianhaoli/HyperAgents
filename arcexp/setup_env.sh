#!/bin/bash
# One-time (idempotent) VM setup. Re-run after a VM rebuild. Usage: bash arcexp/setup_env.sh
set -e
cd "$(dirname "$0")/.."
pip install -q GitPython==3.1.44 backoff docker matplotlib scipy numpy pandas requests networkx 2>&1 | grep -v WARNING || true
id arcagent >/dev/null 2>&1 || useradd -M -u 30033 -d /nonexistent -s /usr/sbin/nologin arcagent
chmod 700 /home/user /root
mkdir -p /opt/arc_private && chmod 700 /opt/arc_private
if [ ! -d /opt/arc_private/ARC-AGI-2 ]; then
  git clone -q https://github.com/arcprize/ARC-AGI-2.git /opt/arc_private/ARC-AGI-2
  git -C /opt/arc_private/ARC-AGI-2 checkout -q f3283f727488ad98fe575ea6a5ac981e4a188e49
fi
mkdir -p /opt/arc_runner && cp arcexp/runner/*.py /opt/arc_runner/ && chown -R root:root /opt/arc_runner && chmod 755 /opt/arc_runner && chmod 644 /opt/arc_runner/*.py
mkdir -p /hyperagents && chmod 755 /hyperagents
git config --global --unset-all safe.directory || true
sysctl -q fs.protected_symlinks=1 fs.protected_hardlinks=1 fs.protected_fifos=1 fs.protected_regular=1 || true
git config --global user.name "arc-exp"; git config --global user.email "arc-exp@localhost"
echo setup ok
