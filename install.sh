#!/usr/bin/env bash
# Install or update job-hunt into ~/.claude. Safe to re-run: it only copies code, prompts and
# examples, never touches your data (~/.claude/job-hunt/data, state, out, variants, .env).
set -euo pipefail
cd "$(dirname "$0")"
C="${CLAUDE_HOME:-$HOME/.claude}"
mkdir -p "$C/skills" "$C/agents" "$C/job-hunt"
rm -rf "$C/skills/job-hunt" && cp -r skills/job-hunt "$C/skills/job-hunt"
cp agents/jd-matcher.md "$C/agents/jd-matcher.md"
for d in scripts examples countries; do rm -rf "$C/job-hunt/$d" && cp -r "project/$d" "$C/job-hunt/$d"; done
cp project/CLAUDE.md "$C/job-hunt/CLAUDE.md"
rm -rf "$C/job-hunt/scheduled-tasks" && cp -r scheduled-tasks "$C/job-hunt/scheduled-tasks"
mkdir -p "$C/job-hunt/data" "$C/job-hunt/state" "$C/job-hunt/out" "$C/job-hunt/variants"
echo "Installed to $C. Open Claude Code and say: set up job-hunt"
