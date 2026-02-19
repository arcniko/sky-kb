"""Configure Claude Desktop to use the sky-knowledge MCP filesystem server.

Called by install.command (macOS) and install.bat (Windows).
Merges the sky-knowledge entry into the existing config without touching other servers.
"""

import argparse
import json
import os
import platform
import sys


def get_config_path():
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser(
            "~/Library/Application Support/Claude/claude_desktop_config.json"
        )
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        return os.path.join(appdata, "Claude", "claude_desktop_config.json")
    else:
        print(f"Unsupported platform: {system}")
        sys.exit(1)


def configure(content_dir):
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # Read existing config or start fresh
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        print(f"  Updating {config_path}")
    else:
        config = {}
        os.makedirs(config_dir, exist_ok=True)
        print(f"  Creating {config_path}")

    # Merge sky-knowledge server entry
    servers = config.setdefault("mcpServers", {})
    servers["sky-knowledge"] = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", content_dir],
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print(f"  Added sky-knowledge MCP server -> {content_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-dir", required=True, help="Path to content directory")
    args = parser.parse_args()

    content_dir = os.path.abspath(args.content_dir)
    configure(content_dir)


if __name__ == "__main__":
    main()
