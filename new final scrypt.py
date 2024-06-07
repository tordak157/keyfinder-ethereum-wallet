import os
import binascii
import ecdsa
import hashlib
import sys
import time
import requests
from colorama import Fore, init
import logging
import secrets  # Ajout du module secrets

# Initialisation de colorama
init(autoreset=True)

# Configuration du logging
logging.basicConfig(filename='eth_search.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_eth_address():
    # Utilisation de secrets pour une meilleure entropie
    private_key = secrets.token_bytes(32)
    private_key_hex = binascii.hexlify(private_key).decode()
    
    public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = b'\x04' + public_key.to_string()
    
    keccak = hashlib.sha3_256()
    keccak.update(public_key_bytes)
    address = "0x" + keccak.hexdigest()[-40:]
    
    return private_key_hex, address

def check_balance(address, api_key):
    url = f'https://eth-mainnet.alchemyapi.io/v2/{api_key}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result

def process_address(api_key):
    eth_private_key, eth_address = generate_eth_address()
    
    print(Fore.GREEN + f"Private Key: {eth_private_key}")
    print(Fore.WHITE + f"Address: {eth_address}")
    
    try:
        data = check_balance(eth_address, api_key)
        
        if 'result' in data:
            balance_wei = int(data['result'], 16)
            balance_ether = balance_wei / 10 ** 18
            print(Fore.RED + f"Balance {eth_address}: {balance_ether} ETH")
            
            if balance_ether > 0.000000000001:
                with open("data.txt", "a") as file:  # Change 'w' to 'a' to append to the file
                    file.write(f"Address: {eth_address}\n")
                    file.write(f"Private Key: {eth_private_key}\n")
                    file.write(f"Balance: {balance_ether} ETH\n")
                return eth_address, eth_private_key, balance_ether
        else:
            logging.error(f"Error: {data['error']['message']}")
    except requests.RequestException as e:
        logging.error(f"Error: Failed to retrieve data from Alchemy API - {e}")
    
    return None

def main():
    api_key = 'sMlNfnJdFt5OMVr***************'
    while True:
        result = process_address(api_key)
        if result:
            eth_address, eth_private_key, balance_ether = result
            print(Fore.GREEN + f"Found non-zero balance!")
            print(Fore.GREEN + f"Address: {eth_address}")
            print(Fore.GREEN + f"Private Key: {eth_private_key}")
            print(Fore.GREEN + f"Balance: {balance_ether} ETH")
            sys.exit()
        
        time.sleep(0)  # Réduire la vitesse pour éviter de dépasser les limites de requêtes

if __name__ == '__main__':
    main()
