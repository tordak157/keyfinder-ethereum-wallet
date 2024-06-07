# keyfinder-ethereum-wallet
This script generates random Ethereum private keys with high entropy using secrets.token_bytes(32). For each key generated, it creates the corresponding Ethereum address and checks its balance via the Alchemy API. If a positive balance is detected, the address, private key and balance are saved to a file, and the script stops.
