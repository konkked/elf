use chrono::Utc;
use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;

// Configuration structure
#[derive(Serialize, Deserialize, Default)]
struct Config {
    seed: Option<String>,
}

// Determine the config directory based on the operating system
fn get_config_dir() -> PathBuf {
    if cfg!(target_os = "windows") {
        dirs::config_dir().unwrap().join("elf")
    } else {
        dirs::home_dir().unwrap().join(".config/elf")
    }
}

// Ensure the configuration directory exists
fn ensure_config_dir() -> io::Result<PathBuf> {
    let config_dir = get_config_dir();
    if !config_dir.exists() {
        fs::create_dir_all(&config_dir)?;
    }
    Ok(config_dir)
}

// Load the configuration from a JSON file
fn load_config() -> io::Result<Config> {
    let config_file = ensure_config_dir()?.join("config.json");
    if config_file.exists() {
        let data = fs::read_to_string(config_file)?;
        let config: Config = serde_json::from_str(&data)?;
        Ok(config)
    } else {
        Ok(Config::default())
    }
}

// Save the configuration to a JSON file
fn save_config(config: &Config) -> io::Result<()> {
    let config_file = ensure_config_dir()?.join("config.json");
    let data = serde_json::to_string_pretty(config)?;
    fs::write(config_file, data)
}

// Get the device fingerprint
fn get_device_fingerprint() -> String {
    if cfg!(target_os = "linux") {
        fs::read_to_string("/etc/machine-id").unwrap_or_else(|_| "unknown-device".to_string())
    } else if cfg!(target_os = "macos") {
        fs::read_to_string("/Library/Preferences/SystemConfiguration/com.apple.smb.server.plist")
            .unwrap_or_else(|_| "unknown-device".to_string())
    } else if cfg!(target_os = "windows") {
        sys_info::os_release().unwrap_or_else(|_| "unknown-device".to_string())
    } else {
        "unsupported-os".to_string()
    }
}

// Generate the seed
fn generate_seed(phrase: &str) -> String {
    if phrase.len() != 16 {
        eprintln!("Expected: The phrase must be exactly 16 characters.\nActual: {}", phrase.len());

        std::process::exit(1);
    }

    let phrase_hash = Sha256::digest(phrase.as_bytes());
    let utc_time = Utc::now().timestamp();
    let device_fingerprint = get_device_fingerprint();

    let seed_input = format!("{:x}{}{}", phrase_hash, utc_time, device_fingerprint);
    let seed_hash = Sha256::digest(seed_input.as_bytes());

    format!("{:x}", seed_hash)
}

fn main() {
    // Parse command-line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: seed <16-character-phrase>");
        std::process::exit(1);
    }

    let phrase = &args[1];
    let seed = generate_seed(phrase);

    // Save the seed to the configuration
    let mut config = load_config().unwrap_or_default();
    config.seed = Some(seed.clone());
    save_config(&config).expect("Failed to save configuration.");

    println!("Seed generated and stored: {}", seed);
}
