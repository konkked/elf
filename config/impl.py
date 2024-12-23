#!/usr/bin/env python3
import os
import json
import sys

# Determine the configuration directory based on the operating system
def get_config_dir():
    if os.name == "posix":  # Linux or macOS
        return os.path.expanduser("~/.config/elf")
    elif os.name == "nt":  # Windows
        return os.path.join(os.getenv("APPDATA"), "elf")
    else:
        raise OSError("Unsupported operating system")

# Ensure the configuration directory exists
def ensure_config_dir():
    config_dir = get_config_dir()
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    return config_dir

# Get the path to the configuration file
def get_config_file():
    config_dir = ensure_config_dir()
    return os.path.join(config_dir, "config.json")

# Load the configuration from the file
def load_config():
    config_file = get_config_file()
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

# Save the configuration to the file
def save_config(config):
    config_file = get_config_file()
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

# Handle the command-line arguments
def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage:")
        print("  config set <key> <value>  - Set a configuration key-value pair")
        print("  config get <key>          - Get a configuration value by key")
        print("  config list               - List all configuration key-value pairs")
        sys.exit(1)

    command = args[0]

    if command == "set":
        if len(args) != 3:
            print("Usage: config set <key> <value>")
            sys.exit(1)
        key, value = args[1], args[2]
        config = load_config()
        config[key] = value
        save_config(config)
        print(f"Configuration set: {key} = {value}")
    elif command == "get":
        if len(args) != 2:
            print("Usage: config get <key>")
            sys.exit(1)
        key = args[1]
        config = load_config()
        if key in config:
            print(f"{key} = {config[key]}")
        else:
            print(f"Configuration key '{key}' not found.")
    elif command == "list":
        config = load_config()
        if config:
            print("Current configuration:")
            for key, value in config.items():
                print(f"  {key}: {value}")
        else:
            print("No configuration found.")
    else:
        print(f"Unknown command: {command}")
        print("Usage: config set <key> <value>, config get <key>, config list")
        sys.exit(1)

if __name__ == "__main__":
    main()
