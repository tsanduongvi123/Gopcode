import requests
import json
import random
import time
from colorama import init, Fore, Style
import sys
import threading
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Khởi tạo colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_effect(text, delay=0.05):
    """Hiệu ứng gõ chữ"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(stop_event, message=""):
    """Hiệu ứng loading khi tạo tài khoản"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}{animation[i % len(animation)]} {message}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{' ' * (len(message) + 5)}\r")
    sys.stdout.flush()

def load_proxies(filename):
    """Đọc proxy từ file"""
    proxies = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                proxy = line.strip()
                if proxy and ':' in proxy:
                    proxies.append(proxy)
        print(f"{Fore.GREEN}✔ Đã tải {len(proxies)} proxy từ file{Style.RESET_ALL}")
        return proxies
    except FileNotFoundError:
        print(f"{Fore.RED}✖ Không tìm thấy file proxy: {filename}{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}✖ Lỗi khi đọc file proxy: {e}{Style.RESET_ALL}")
        return []

def setup_session(proxy=None):
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    if proxy:
        session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    return session

def get_available_domains(session):
    url = "https://api.mail.tm/domains"
    headers = {"Accept": "application/json"}
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        domains = response.json()
        return domains[0]["domain"]
    except requests.exceptions.RequestException:
        return "mail.tm"

def create_mailtm_account(session, account_num, max_retries=3):
    url = "https://api.mail.tm/accounts"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ])
    }
    domain = get_available_domains(session)
    payload = {
        "address": f"DGVIKAKA{random.randint(1000, 9999)}@{domain}",
        "password": f"DGVIKAKA{random.randint(1000, 9999)}"
    }
    
    for attempt in range(max_retries):
        stop_event = threading.Event()
        loading_message = f"Đang tạo tài khoản thứ {account_num}... (Lần thử {attempt + 1}/{max_retries})"
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event, loading_message))
        loading_thread.start()
        
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            account_data = response.json()
            stop_event.set()
            loading_thread.join()
            
            remaining = response.headers.get('X-RateLimit-Remaining')
            if remaining and int(remaining) < 5:
                time.sleep(random.uniform(5, 10))
                
            if "address" in account_data:
                return account_data["address"], payload["password"]
            else:
                stop_event.set()
                loading_thread.join()
                return None, None
                
        except requests.exceptions.HTTPError as e:
            stop_event.set()
            loading_thread.join()
            if e.response.status_code == 429:
                retry_after = e.response.headers.get('Retry-After', 5 ** attempt)
                wait_time = max(int(retry_after), 5 ** attempt) + random.uniform(0, 2)
                time.sleep(wait_time)
                continue
            else:
                return None, None
        except requests.exceptions.RequestException as e:
            stop_event.set()
            loading_thread.join()
            return None, None
    
    return None, None

def save_to_file(username, password, filename):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{username}|{password}\n")
        return True
    except IOError as e:
        print(f"{Fore.RED}✖ Lỗi khi lưu file: {e}{Style.RESET_ALL}")
        return False

def create_multiple_accounts(num_accounts, filename, proxy_file=None):
    clear_screen()
    print(f"{Fore.CYAN}╔════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║      BẮT ĐẦU TẠO {num_accounts} TÀI KHOẢN      ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════╝{Style.RESET_ALL}")
    time.sleep(1)
    
    proxies = load_proxies(proxy_file) if proxy_file else []
    success_count = 0
    attempt_count = 0
    
    while success_count < num_accounts:
        attempt_count += 1
        proxy = random.choice(proxies) if proxies else None
        session = setup_session(proxy)
        if proxy and attempt_count == 1:
            print(f"{Fore.YELLOW}Đang sử dụng proxy: {proxy}{Style.RESET_ALL}")
        
        username, password = create_mailtm_account(session, success_count + 1)
        if username and password:
            if save_to_file(username, password, filename):
                success_count += 1
                print(f"{Fore.GREEN}✔ [{success_count}/{num_accounts}] Tài khoản: {username} | {password}{Style.RESET_ALL}")
        time.sleep(random.uniform(3, 7))
        
    print(f"{Fore.CYAN}╔════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ HOÀN TẤT! TẠO ĐƯỢC {success_count}/{num_accounts} TÀI KHOẢN  ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════╝{Style.RESET_ALL}")

def main():
    clear_screen()
    # Giao diện mới với Admin
    print(f"\033[1;31m{Fore.MAGENTA}╔════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"\033[1;31m{Fore.MAGENTA}\033[1;31m║      \033[1;34mMAILTM ACCOUNT CREATOR VIP👑          ║{Style.RESET_ALL}")
    print(f"\033[1;34m{Fore.MAGENTA}\033[1;34m║      \033[1;31mAdmin: DGVI KAKA💤                    ║{Style.RESET_ALL}")
    print(f"\033[1;34m{Fore.MAGENTA}╚════════════════════════════════════════════╝{Style.RESET_ALL}")
    typing_effect(f"{Fore.YELLOW}Công cụ tạo tài khoản MailTM với proxy support{Style.RESET_ALL}")
    print(f"{Fore.CYAN}--------------------------------------------{Style.RESET_ALL}")
    time.sleep(1)
    
    while True:
        try:
            num_accounts = int(input(f"{Fore.GREEN}Nhập số lượng tài khoản cần tạo: {Style.RESET_ALL}"))
            if num_accounts <= 0:
                print(f"{Fore.RED}✖ Số lượng phải lớn hơn 0!{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}✖ Vui lòng nhập một số hợp lệ!{Style.RESET_ALL}")
    
    filename = input(f"{Fore.GREEN}Nhập đường dẫn file lưu (Enter để dùng 'mailtm_accounts.txt'): {Style.RESET_ALL}") or "mailtm_accounts.txt"
    
    use_proxy = input(f"{Fore.GREEN}Sử dụng proxy từ file? (y/n): {Style.RESET_ALL}").lower() == 'y'
    proxy_file = None
    if use_proxy:
        proxy_file = input(f"{Fore.GREEN}Nhập đường dẫn file proxy (IP:PORT, mỗi dòng 1 proxy): {Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}Đường dẫn file lưu: {filename}{Style.RESET_ALL}")
    if proxy_file:
        print(f"{Fore.YELLOW}File proxy: {proxy_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}--------------------------------------------{Style.RESET_ALL}")
    input(f"{Fore.GREEN}Nhấn Enter để bắt đầu...{Style.RESET_ALL}")
    create_multiple_accounts(num_accounts, filename, proxy_file)

if __name__ == "__main__":
    main()
