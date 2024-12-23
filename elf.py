#!/usr/bin/env python3
import os
import subprocess
import sys
import glob
import readline

# Function to find subcommands dynamically
def discover_commands(base_dir):
    commands = {}
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            # Look for valid implementations in the subdirectory
            impl_files = glob.glob(f"{subdir_path}/impl*")
            for impl_file in impl_files:
                if impl_file.endswith((".py", ".o", ".so")) or os.access(impl_file, os.X_OK):
                    commands[str(subdir).replace("elf-","")] = impl_file
                    break
    return commands

# Function to list available commands
def list_commands(commands):
    print("Available commands:")
    for cmd in sorted(commands):
        print(f"  {cmd}")

# Function to execute a command
def execute_command(command_name, commands, args):
    if command_name not in commands:
        print(f"Error: Command '{command_name}' not found.")
        return

    impl_path = commands[command_name]
    if impl_path.endswith(".py"):
        # Run Python implementation
        subprocess.run([sys.executable, impl_path] + args)
    elif impl_path.endswith((".o", ".so")) or os.access(impl_path, os.X_OK):
        # Run compiled binary or shared object
        subprocess.run([impl_path] + args)
    else:
        try:
            subprocess.run([impl_path] + args)
        except subprocess.CalledProcessError as e:
            print(f"Error: running file type for command '{command_name}'. Exception: {e}")

# Main interactive terminal
def interactive_terminal(commands):
    print("Welcome to ELF Interactive Terminal.")
    print("Type 'help' for available commands or press Tab for suggestions.")

    # Maintain a list of matches for cycling
    matches = []
    match_index = -1

    # Define a completer function for readline
    def completer(text, state):
        nonlocal matches, match_index
        if state == 0:  # First Tab press
            # Find matching commands
            matches = [cmd for cmd in commands if cmd.startswith(text)]
            match_index = 0

        # Cycle through matches on subsequent Tab presses
        if matches:
            suggestion = matches[match_index % len(matches)]
            match_index += 1
            return suggestion
        return None

    # Attach the completer to readline
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")  # Bind Tab key to auto-completion

    while True:
        try:
            user_input = input("elf> ").strip()
            if not user_input:
                continue
            if user_input == "exit":
                print("Goodbye!")
                break
            elif user_input == "help":
                print("Core commands:")
                print("  list-commands  - List all available ELF commands")
                print("  help           - Show this help menu")
                print("  exit           - Exit the ELF terminal")
            elif user_input == "list-commands":
                list_commands(commands)
            else:
                parts = user_input.split()
                command_name = parts[0]
                args = parts[1:]
                execute_command(command_name, commands, args)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

# Main function
def main():
    base_dir = os.getcwd()  # Look for subcommands in the current directory
    commands = discover_commands(base_dir)

    # If no arguments are provided, open the interactive terminal
    if len(sys.argv) == 1:
        interactive_terminal(commands)
    else:
        # Run the specified command
        command_name = sys.argv[1]
        args = sys.argv[2:]
        execute_command(command_name, commands, args)

if __name__ == "__main__":
    main()
