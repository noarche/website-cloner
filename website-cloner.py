import os
import subprocess
from colorama import Fore, Style, init
import time

init(autoreset=True)

def get_directory_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # convert to MB

def download_website(url):
    save_dir = "website_clone"
    print(f"{Fore.YELLOW}Starting website clone...{Style.RESET_ALL}")
    
    # Command to download website with wget and save it in the specified directory
    command = f'wget -mpEk {save_dir} "{url}"'

    # Run the wget command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    files_saved = 0
    last_update_time = time.time()

    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            if "saved" in output:
                files_saved += 1

            # Update every second to avoid excessive disk I/O
            if time.time() - last_update_time > 1:
                directory_size_mb = get_directory_size(save_dir)
                print(f"\r{Fore.GREEN}Files saved: {files_saved} | MB used: {directory_size_mb:.2f} MB{Style.RESET_ALL}", end='')
                last_update_time = time.time()

        time.sleep(0.1)

    # Final directory size update
    directory_size_mb = get_directory_size(save_dir)
    print(f"\r{Fore.GREEN}Files saved: {files_saved} | MB used: {directory_size_mb:.2f} MB{Style.RESET_ALL}")

    process.communicate()
    print()  # Move to the next line after completion

def main():
    while True:
        url = input(f"{Fore.CYAN}Enter the full URL (starting with http or https): {Style.RESET_ALL}").strip()

        if url.startswith('http://') or url.startswith('https://'):
            download_website(url)
            print(f"{Fore.GREEN}Website clone successful!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid URL! Please enter a valid URL starting with http or https.{Style.RESET_ALL}")
            continue

        choice = input(f"{Fore.CYAN}Do you want to clone another website? (yes/y or no/n or exit/e): {Style.RESET_ALL}").strip().lower()
        if choice in ['exit', 'e']:
            print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
            break
        elif choice not in ['yes', 'y']:
            print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
