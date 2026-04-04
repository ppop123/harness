#!/usr/bin/env bash
# init.sh — Environment setup & baseline verification for TypeScript + Next.js
#
# Run this at the start of every AI agent session to ensure:
# 1. Dependencies are installed
# 2. Dev server starts successfully
# 3. Baseline tests pass
#
# Usage: bash scripts/init.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔧 [TypeScript + Next.js] Initializing environment..."

# Step 1: Check required tools
echo -e "\n${YELLOW}[1/4] Checking tools...${NC}"
MISSING=0
for cmd in node npm npx; do
  if ! command -v "$cmd" &>/dev/null; then
    echo -e "${RED}  ✗ $cmd not found${NC}"
    MISSING=1
  else
    echo "  ✓ $cmd $(command -v "$cmd")"
  fi
done
[[ $MISSING -eq 1 ]] && echo -e "${RED}Install missing tools before continuing.${NC}" && exit 1

# Step 2: Install dependencies
echo -e "\n${YELLOW}[2/4] Installing dependencies...${NC}"
npm install

# Step 3: Run baseline checks (lint + typecheck)
echo -e "\n${YELLOW}[3/4] Running lint & type checks...${NC}"
npm run lint && tsc --noEmit

# Step 4: Run tests
echo -e "\n${YELLOW}[4/4] Running tests...${NC}"
npx vitest run

echo -e "\n${GREEN}✅ Environment verified. All checks passed. Ready to code.${NC}"
