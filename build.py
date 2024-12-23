#!/usr/bin/env python3
import os
import subprocess
import shutil

# Function to compile Rust files using Cargo
def compile_rust_with_cargo(subdir: str):
    try:
        print(subdir)
        spl = subdir.split(os.sep)
        bin = spl[-2] if subdir.endswith("src") else None
        projdir = os.sep.join(spl[0:-1]) if subdir.endswith("src") else None
        print(f"Compiling Rust project in: {projdir}")
        subprocess.run(["cargo", "build", "--release"], cwd=subdir, check=True)
        # Move the compiled binary to the subdirectory as `impl`
        print(bin)
        binary_name = os.path.join(projdir, f"target/release/{bin}")
        output_path = os.path.join(projdir, "impl")
        shutil.copy(binary_name, output_path)
        print(f"Successfully compiled: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Rust project in {subdir}: {e}")

# Function to compile C files
def compile_c(source_file, output_file):
    try:
        print(f"Compiling C file: {source_file} -> {output_file}")
        subprocess.run(["gcc", "-o", output_file, source_file], check=True)
        print(f"Successfully compiled: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling C file {source_file}: {e}")

# Main function to traverse subdirectories and compile
def main():
    base_dir = os.getcwd()  # Current directory
    print(f"Scanning for source files in {base_dir}...")

    for subdir, _, files in os.walk(base_dir):
        for file in files:
            source_file = os.path.join(subdir, file)
            if file.endswith(".rs"):
                if "release" in subdir:
                    print(f"Skipping rust build directory {subdir}")
                    continue
                compile_rust_with_cargo(subdir)
            elif file == "impl.c":
                output_file = os.path.join(subdir, "impl")
                compile_c(source_file, output_file)

    print("Compilation process complete.")

if __name__ == "__main__":
    main()