#!/usr/bin/env python3
import os
import shutil
import sys
import stat

# Function to get the correct bin directory
def get_bin_dir():
    if os.name == "posix":  # Unix or MacOS
        return "/usr/local/bin"
    elif os.name == "nt":  # Windows
        return os.path.join(os.getenv("APPDATA"), "elf-bin")
    else:
        raise OSError("Unsupported operating system")

# Function to make a file executable
def make_executable(file_path):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)

# Main function
def main():
    elf_dir = os.getcwd()  # Current working directory (where ELF suite is located)
    bin_dir = get_bin_dir()

    print(f"Installing ELF suite to {bin_dir}...")

    # Ensure the bin directory exists
    os.makedirs(bin_dir, exist_ok=True)

    # Copy the main ELF command
    main_elf_command = os.path.join(elf_dir, "elf")
    if not os.path.isfile(main_elf_command):
        print("Error: Main 'elf' command not found in the current directory.")
        sys.exit(1)

    shutil.copy(main_elf_command, bin_dir)
    make_executable(os.path.join(bin_dir, "elf"))
    print("Installed main 'elf' command.")

    # Dynamically detect and copy subcommands
    for entry in os.listdir(elf_dir):
        subcommand_path = os.path.join(elf_dir, entry)
        if (
            os.path.isfile(subcommand_path)  # Ensure it's a file
            and entry != "elf"               # Exclude the main command
            and not entry.endswith(".py")    # Exclude the compile script itself
        ):
            target_name = f"elf-{entry}"
            target_path = os.path.join(bin_dir, target_name)
            shutil.copy(subcommand_path, target_path)
            make_executable(target_path)
            print(f"Installed subcommand: {target_name}")

    print("ELF suite installation complete!")
    print(f"You can now run 'elf' or 'elf-<subcommand>' from any terminal.")

if __name__ == "__main__":
    main()