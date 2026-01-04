#!/bin/bash
#
# Claude Router - Intelligent model routing for Claude Code
# https://github.com/0xrdan/claude-router
#
# This script installs Claude Router to your project or globally.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════╗"
echo "║         Claude Router Installer               ║"
echo "║   Intelligent model routing for Claude Code   ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Determine install location
echo -e "${YELLOW}Where would you like to install Claude Router?${NC}"
echo "  1) Current project (./.claude/) - Recommended for project-specific use"
echo "  2) Global install (~/.claude/) - Applies to all Claude Code sessions"
echo ""
read -p "Choose (1 or 2): " choice

case $choice in
    1)
        INSTALL_PATH="./.claude"
        echo -e "${GREEN}Installing to current project...${NC}"
        ;;
    2)
        INSTALL_PATH="$HOME/.claude"
        echo -e "${GREEN}Installing globally...${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p "$INSTALL_PATH/hooks"
mkdir -p "$INSTALL_PATH/agents/fast-executor"
mkdir -p "$INSTALL_PATH/agents/standard-executor"
mkdir -p "$INSTALL_PATH/agents/deep-executor"
mkdir -p "$INSTALL_PATH/skills/route"

# Copy files
echo -e "${BLUE}Copying router files...${NC}"

# Check if running from cloned repo or via curl
if [ -f "$SCRIPT_DIR/.claude/hooks/classify-prompt.py" ]; then
    # Running from cloned repo
    cp "$SCRIPT_DIR/.claude/hooks/classify-prompt.py" "$INSTALL_PATH/hooks/"
    cp "$SCRIPT_DIR/.claude/agents/fast-executor/AGENT.md" "$INSTALL_PATH/agents/fast-executor/"
    cp "$SCRIPT_DIR/.claude/agents/standard-executor/AGENT.md" "$INSTALL_PATH/agents/standard-executor/"
    cp "$SCRIPT_DIR/.claude/agents/deep-executor/AGENT.md" "$INSTALL_PATH/agents/deep-executor/"
    cp "$SCRIPT_DIR/.claude/skills/route/SKILL.md" "$INSTALL_PATH/skills/route/"
else
    # Running via curl - download files from GitHub
    BASE_URL="https://raw.githubusercontent.com/0xrdan/claude-router/main"
    curl -sL "$BASE_URL/.claude/hooks/classify-prompt.py" -o "$INSTALL_PATH/hooks/classify-prompt.py"
    curl -sL "$BASE_URL/.claude/agents/fast-executor/AGENT.md" -o "$INSTALL_PATH/agents/fast-executor/AGENT.md"
    curl -sL "$BASE_URL/.claude/agents/standard-executor/AGENT.md" -o "$INSTALL_PATH/agents/standard-executor/AGENT.md"
    curl -sL "$BASE_URL/.claude/agents/deep-executor/AGENT.md" -o "$INSTALL_PATH/agents/deep-executor/AGENT.md"
    curl -sL "$BASE_URL/.claude/skills/route/SKILL.md" -o "$INSTALL_PATH/skills/route/SKILL.md"
fi

# Make classifier executable
chmod +x "$INSTALL_PATH/hooks/classify-prompt.py"

# Set up Python virtual environment for hybrid classification
echo -e "${BLUE}Setting up Python environment...${NC}"
if [ ! -d "$INSTALL_PATH/hooks/venv" ]; then
    python3 -m venv "$INSTALL_PATH/hooks/venv"
fi
"$INSTALL_PATH/hooks/venv/bin/pip" install --quiet --upgrade pip
"$INSTALL_PATH/hooks/venv/bin/pip" install --quiet anthropic

# Update shebang to use the venv Python
VENV_PYTHON="$INSTALL_PATH/hooks/venv/bin/python"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "1s|.*|#!$VENV_PYTHON|" "$INSTALL_PATH/hooks/classify-prompt.py"
else
    # Linux
    sed -i "1s|.*|#!$VENV_PYTHON|" "$INSTALL_PATH/hooks/classify-prompt.py"
fi

# Handle settings.json
SETTINGS_FILE="$INSTALL_PATH/settings.json"
HOOK_PATH="$INSTALL_PATH/hooks/classify-prompt.py"

# Convert to absolute path for the hook command
HOOK_PATH_ABS="$(cd "$(dirname "$HOOK_PATH")" && pwd)/$(basename "$HOOK_PATH")"

if [ -f "$SETTINGS_FILE" ]; then
    echo -e "${YELLOW}Existing settings.json found.${NC}"

    # Check if UserPromptSubmit hook already exists
    if grep -q "UserPromptSubmit" "$SETTINGS_FILE"; then
        echo -e "${YELLOW}UserPromptSubmit hook already configured.${NC}"
        echo -e "${YELLOW}Please manually add the Claude Router hook if needed.${NC}"
        echo ""
        echo "Add this to your UserPromptSubmit hooks array:"
        echo -e "${BLUE}{"
        echo '  "type": "command",'
        echo "  \"command\": \"$HOOK_PATH_ABS\","
        echo '  "timeout": 15'
        echo -e "}${NC}"
    else
        # Add UserPromptSubmit hook to existing settings
        echo -e "${BLUE}Adding UserPromptSubmit hook to settings...${NC}"
        # This is a simplified approach - for complex merging, use jq
        if command -v jq &> /dev/null; then
            jq ".hooks.UserPromptSubmit = [{\"hooks\": [{\"type\": \"command\", \"command\": \"$HOOK_PATH_ABS\", \"timeout\": 15}]}]" "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"
            mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
        else
            echo -e "${YELLOW}jq not found. Please manually add the hook.${NC}"
        fi
    fi
else
    # Create new settings.json
    echo -e "${BLUE}Creating settings.json...${NC}"
    cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOOK_PATH_ABS",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
EOF
fi

# Set up CLAUDE.md for routing enforcement
CLAUDE_MD_CONTENT='## Claude Router Enforcement

When you receive a `[Claude Router] MANDATORY ROUTING DIRECTIVE`, you MUST:

1. Use the Task tool IMMEDIATELY to spawn the specified subagent
2. Do NOT respond to the user directly - delegate to the subagent
3. Pass the user'"'"'s original query in the prompt parameter

Subagent mapping:
- fast → `claude-router:fast-executor`
- standard → `claude-router:standard-executor`
- deep → `claude-router:deep-executor`

Exceptions: Slash commands (`/route`, `/router-stats`) and questions about the router itself.'

# Determine CLAUDE.md location based on install type
if [ "$choice" = "1" ]; then
    CLAUDE_MD_PATH="./CLAUDE.md"
else
    CLAUDE_MD_PATH="$HOME/CLAUDE.md"
fi

echo -e "${BLUE}Setting up routing enforcement...${NC}"

if [ -f "$CLAUDE_MD_PATH" ]; then
    # Check if already contains router enforcement
    if grep -q "Claude Router Enforcement" "$CLAUDE_MD_PATH"; then
        echo -e "${YELLOW}CLAUDE.md already contains router enforcement.${NC}"
    else
        # Append to existing CLAUDE.md
        echo -e "${BLUE}Adding router enforcement to existing CLAUDE.md...${NC}"
        echo "" >> "$CLAUDE_MD_PATH"
        echo "$CLAUDE_MD_CONTENT" >> "$CLAUDE_MD_PATH"
    fi
else
    # Create new CLAUDE.md
    echo -e "${BLUE}Creating CLAUDE.md with router enforcement...${NC}"
    echo "$CLAUDE_MD_CONTENT" > "$CLAUDE_MD_PATH"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Installation Complete!                ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Claude Router is now installed at: $INSTALL_PATH${NC}"
echo ""
echo -e "${YELLOW}How it works:${NC}"
echo "  - Every prompt is automatically classified"
echo "  - Simple queries -> Haiku (98% cost savings)"
echo "  - Standard coding -> Sonnet (balanced)"
echo "  - Complex tasks -> Opus (full power)"
echo ""
echo -e "${YELLOW}Optional:${NC}"
echo "  - Set ANTHROPIC_API_KEY for hybrid LLM classification"
echo "  - Use /route manually: /route <your query>"
echo ""
echo -e "${GREEN}Start a new Claude Code session to begin routing!${NC}"
