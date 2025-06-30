#######################################################################
# Author: Lehlohonolo Matobakele 
# Email: lehlohonolo.matobakele@gov.ls
# Contacxt: 00266 62320704
#######################################################################


import os            # For directory and file handling
import random
import itertools    # Used for creating combinations of characters

# Character set: full printable charset with letters, digits, and symbols
charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"

# Constants
SPLIT_SIZE = 10 * 1024 * 1024 * 1024  # 10 GB  Define max size of each wordlist file: 10 GB (in bytes)
BUFFER_SIZE = 1024 * 1024             # 1MB buffer
OUTPUT_DIR = "wordlists"              # Output directory to store wordlist files

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)     # Create the directory if it doesn't exist

def prompt_length():
    min_len = int(input("Enter minimum word length: "))
    max_len = int(input("Enter maximum word length: "))
    if min_len > max_len:
        min_len, max_len = max_len, min_len
    return min_len, max_len

def write_to_file(base_name, content_generator):     # File tracking variables
    file_index = 1      # Index for naming files like wordlist_1.txt, wordlist_2.txt, ...
    file_size = 0       # Track size of current file
    filename = f"{OUTPUT_DIR}/{base_name}_{file_index}.txt"     # Initial file name
    output_file = open(filename, "w", buffering=BUFFER_SIZE)
    print(f"[+] Writing to {filename}")

    try:
        for word in content_generator:
            line = word + "\n"
            encoded = line.encode()
            output_file.write(line)
            file_size += len(encoded)

            if file_size >= SPLIT_SIZE:
                output_file.close()
                file_index += 1
                file_size = 0
                filename = f"{OUTPUT_DIR}/{base_name}_{file_index}.txt"
                output_file = open(filename, "w", buffering=BUFFER_SIZE)
                print(f"[+] Switched to {filename}")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")

    finally:
        output_file.close()
        print("[✓] Wordlist generation complete.")

# Option 1: Random wordlist generator
def random_wordlist():
    min_len, max_len = prompt_length()
    print("[+] Starting random wordlist generation...")

    def random_generator():
        while True:
            length = random.randint(min_len, max_len)
            yield ''.join(random.choices(charset, k=length))

    write_to_file("random_wordlist", random_generator())

# Option 2: Full wordlist generator (brute-force)
def full_wordlist():
    min_len, max_len = prompt_length()
    print("[+] Starting full wordlist generation (this may be huge!)")

    def full_generator():
        for length in range(min_len, max_len + 1):
            print(f"[+] Generating combinations of length {length}...")
            for combo in itertools.product(charset, repeat=length):
                yield ''.join(combo)

    write_to_file("general_wordlist", full_generator())

# Menu
def menu():
    while True:
        print("\n========== Wordlist Generator ==========")
        print("1. Generate RANDOM wordlist (infinite, random)")
        print("2. Generate FULL wordlist (all combinations)")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            random_wordlist()
        elif choice == '2':
            full_wordlist()
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
