# keyfinder-ethereum-wallet
This script generates random Ethereum private keys with high entropy using secrets.token_bytes(32). For each key generated, it creates the corresponding Ethereum address and checks its balance via the Alchemy API. If a positive balance is detected, the address, private key and balance are saved to a file, and the script stops.
Initialization:

The script starts by importing the necessary modules, initializes colorama for color management in the console and configures logging to record events in a log file.
Generating an Ethereum address:

The generate_eth_address function uses secrets.token_bytes(32) to generate a random private key with high entropy (32 bytes, or 256 bits).
It derives the public key from the private key using the ECDSA algorithm with the SECP256k1 curve.
It uses the SHA-3 algorithm to obtain the hash of the public key, the last 40 characters of which are used to form the Ethereum address.
Balance check:

The check_balance function sends a POST request to the Alchemy API to get the Ethereum address balance.
It returns the balance in Wei (the base unit of Ethereum) in a JSON response.
Address processing:

The process_address function generates an Ethereum address and its private key.
It displays the generated private key and address.
It checks the balance of the address using the check_balance function.
If the balance is positive (above a small threshold), it saves the address, private key and ETH balance in a data.txt file and terminates the script.
Main Loop:

The main function contains an infinite loop that generates and processes Ethereum addresses until an address with a positive balance is found.
A 0.4 second pause is added between iterations to avoid exceeding the Alchemy or etherscan API request limits. YOU NEED TO ADD YOUR API KEY TO THE SCRYPT
TO THIS LINE OF CODE
 api_key = 'sMlNfnJdFt5OM*****************'
