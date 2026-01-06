#!/bin/bash
#
# Claude Router - Uninstall Script
# https://github.com/0xrdan/claude-router
#
# Removes Claude Router files installed via install.sh
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════╗"
echo "║        Claude Router Uninstaller              ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Determine uninstall location
echo -e "${YELLOW}Where did you install Claude Router?${NC}"
echo "  1) Current project (./.claude/)"
echo "  2) Global install (~/.claude/)"
echo ""
read -p "Choose (1 or 2): " choice

case $choice in
    1)
        INSTALL_PATH="./.claude"
        ;;
    2)
        INSTALL_PATH="$HOME/.claude"
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

if [ ! -d "$INSTALL_PATH" ]; then
    echo -e "${RED}Directory $INSTALL_PATH does not exist.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}This will remove:${NC}"
echo "  - $INSTALL_PATH/hooks/classify-prompt.py"
echo "  - $INSTALL_PATH/hooks/venv/ (if exists)"
echo "  - $INSTALL_PATH/agents/fast-executor/"
echo "  - $INSTALL_PATH/agents/standard-executor/"
echo "  - $INSTALL_PATH/agents/deep-executor/"
echo "  - $INSTALL_PATH/skills/route/"
echo "  - $INSTALL_PATH/skills/router-stats/"
echo "  - UserPromptSubmit hook from settings.json"
echo ""
read -p "Continue? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo -e "${YELLOW}Aborted.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Removing files...${NC}"

# Remove classifier and venv
rm -f "$INSTALL_PATH/hooks/classify-prompt.py"
rm -rf "$INSTALL_PATH/hooks/venv"

# Remove agents
rm -rf "$INSTALL_PATH/agents/fast-executor"
rm -rf "$INSTALL_PATH/agents/standard-executor"
rm -rf "$INSTALL_PATH/agents/deep-executor"

# Remove skills
rm -rf "$INSTALL_PATH/skills/route"
rm -rf "$INSTALL_PATH/skills/router-stats"

# Clean up empty directories
rmdir "$INSTALL_PATH/agents" 2>/dev/null || true
rmdir "$INSTALL_PATH/skills" 2>/dev/null || true

# Update settings.json to remove UserPromptSubmit hook
SETTINGS_FILE="$INSTALL_PATH/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo -e "${BLUE}Updating settings.json...${NC}"

    if command -v jq &> /dev/null; then
        # Use jq to remove the hook
        jq 'del(.hooks.UserPromptSubmit)' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"

        # If hooks object is now empty, remove it too
        jq 'if .hooks == {} then del(.hooks) else . end' "$SETTINGS_FILE.tmp" > "$SETTINGS_FILE"
        rm -f "$SETTINGS_FILE.tmp"

        echo -e "${GREEN}Removed UserPromptSubmit hook from settings.json${NC}"
    else
        echo -e "${YELLOW}jq not installed. Please manually remove UserPromptSubmit from:${NC}"
        echo "  $SETTINGS_FILE"
    fi
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Uninstall Complete!                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Note: Start a new Claude Code session for changes to take effect.${NC}"
