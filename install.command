#!/bin/bash
# Sky Knowledge Base — one-click installer for macOS
# Double-click this file to install or update.

set -e

REPO_URL="https://github.com/arcniko/sky-kb.git"
INSTALL_DIR="$HOME/sky-kb"

echo ""
echo "=== Sky Knowledge Base Installer ==="
echo ""

# Clone or pull
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing install..."
    git -C "$INSTALL_DIR" pull --ff-only
else
    if [ -d "$INSTALL_DIR" ]; then
        echo "Error: $INSTALL_DIR exists but is not a git repo."
        echo "Remove it first and re-run this installer."
        echo ""
        read -n 1 -s -r -p "Press any key to close..."
        exit 1
    fi
    echo "Cloning to $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

echo ""

# Sync content
echo "Syncing content..."
python3 "$INSTALL_DIR/scripts/sync.py"

echo ""

# Configure Claude Desktop
echo "Configuring Claude Desktop..."
python3 "$INSTALL_DIR/scripts/configure_claude_desktop.py" --content-dir "$INSTALL_DIR/content"

echo ""
echo "=== Done! ==="
echo ""
echo "Restart Claude Desktop to activate the sky-knowledge tool."
echo ""
read -n 1 -s -r -p "Press any key to close..."
