# ELFS Suite
Modular framework for cryptographic functions and secure communication with a terminal interface to interact with the suite in a seamless way. The network operates on the basis
that daily share passphrases will be communicated and used to initialize cryptographic function. Servers that run with out of date passphrases will be 
clipped from the visible network.

## Ideaology

The idea is that eventually modern cryptography will be broken by quantum computing and most of current cryptography can be broken by brute force.
This project combines an old idea of rotating passphrases to make cryptogrphic artifacts unique every set period determined in advance. 
Users of the network and tool would rotate the passphrase they use at the beginning of the working period before starting their work. 
Idea is to make something simple and extensible that could eventually be replaced with quantum resistant algorithms but in the short term 
would be safe as long as users don't compromise the list of passphrases. The target audience would be for individuals working on a short term 
project that need a way to securely communicate with one another.

## Elegant Layered Framework for Security

The purpose of Elfs is to allow for modular enhancement for crpytographic processes, the core uses python to create the terminal the 
modules are fleshed out in different languages. The tooling is built in typical *nix style, which modular subcommands being combined to
do more sophisticated functionality.


## Roadmap
1. config - configuration used by the rest of the suite.
2. terminal - the primary user interface for elf.
3. seed - creates a unique seed address that can be used to register peer with other peers and perform cryptographic functionality of the project.
4. hash - hashing algorithm that will be used in other crypto functionality.
5. key - command to create public private key pairs that are used in encryption.
6. pulse - secure random number generator based on peer seed and passphrase.
7. crypt - the base encryption and decryption commands, handles cryptographic functions that make communication secure over elf-net
8. peer - acts as a server and client that will allow for other commands to propogate over the public internet
10. mail - P2P email which is stored locally
11. file - P2P file sharing that allows pushing files to different nodes on the elf net
12. chat  - a P2P chat system that would allow realtime communication