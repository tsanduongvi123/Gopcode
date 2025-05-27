import os
import sys
import time
import json
import random
import string
import requests

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/tsanduongvi123/Gopcode/main/"
ADMIN_JSON = GITHUB_RAW_BASE + "admin.json"
KEY_JSON = GITHUB_RAW_BASE + "key_data.json"
WEBHOOK_URL = "https://your-vercel-app.vercel.app/api/key-gen"  # Thay bằng URL Vercel sau khi deploy

colors = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m", "\033[90m"]
reset = "\033[0m"

banner_lines = [
    "╔" + "═" * 90 + "╗",
    "║{:^90}║".format("TOOL AUTO VIP KEY - DUONG VI"),
    "║{:^90}║".format("██████╗░██╗░░░██╗██╗  ████████╗░█████╗░░█████╗░██╗░░░░░"),
    "║{:^90}║".format("██╔══██╗██║░░░██║██║  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░"),
    "║{:^90}║".format("██║░░██║╚██╗░██╔╝██║  ░░░██║░░░██║░░██║██║░░██║██║░░░░░"),
    "║{:^90}║".format("██║░░██║░╚████╔╝░██║  ░░░██║░░░██║░░██║██║░░██║██║░░░░░"),
    "║{:^90}║".format("██████╔╝░░╚██╔╝░░██║  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗"),
    "║{:^90}║".format("╚═════╝░░░░╚═╝░░░╚═╝  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝"),
    "╠" + "═" * 90 + "╣",
]

ascii_art = [
    "⠀⠀⢠⡶⠛⠛⠢⣄⠀⠀⣀⣀⣀⣤⣀⣀⣀⢀⡤⠖⠛⠓⣆",
    "⠀⠀⣾⠁⢠⡆⠀⣌⠿⠿⠛⣻⣿⣯⠙⣛⠻⠏⠀⣠⣤⡀⢸",
    "⠀⠀⢹⣤⣻⠏⠚⢉⣠⣾⡵⠭⢻⠂⠠⣭⣓⠦⣀⠙⢻⣷⠟",
    "⠀⠀⠈⢯⠤⡤⢞⡧⠈⡵⠃⡞⢻⡈⠳⡙⢦⡘⢧⡓⢄⢾",
    "⠀⠀⢰⠃⡾⢡⡏⡧⢾⢄⠸⠡⠛⠋⠒⠛⡠⣽⢆⢳⡘⡎⢢",
    "⠀⢠⡇⢸⡇⣿⢰⢻⣶⣾⡷⡄⠀⠀⠀⣾⣟⣿⡹⠋⡇⣧⠀⢇",
    "⠀⢸⠀⢸⡇⢻⡸⢦⣙⡊⣿⠁⠀⠀⠀⢻⡉⠉⠀⠀⡇⣿⠀⢸⣷⣄",
    "⠀⡾⠀⢸⣧⠘⡟⠂⠲⣤⡿⠀⠀⠀⠀⠈⠓⣜⣶⢶⠁⣿⠁⢸⣿⡏",
    "⢀⣿⡀⠈⢻⣄⢸⡌⢷⡎⠀⠀⠀⠀⠀⠀⠆⠈⣯⣄⣤⡿⠀⢸⠁⢀",
    "⠈⠘⣷⡀⠀⢿⣷⣿⣟⣻⡤⡷⣶⡒⡶⠞⣠⣾⣿⡶⠿⠋⢐⠆⠀⣼",
    "⠀⠀⠹⣿⡇⠀⡎⡏⡿⣯⢽⡟⠈⣻⡁⠠⢿⣿⠟⠁⢀⢀⡾⠀⢰⡟",
    "⠀⠀⠀⣿⣧⣀⢀⣿⢠⠈⡻⠓⠉⠉⠉⠒⢾⠙⡄⢱⣤⡿⠄⣠⡿⠃",
    "⠀⠀⢀⡸⡛⠿⣧⣉⡋⠛⠧⢄⣀⣀⡀⣠⠾⢯⠴⠿⠏⣠⣾⣿⠃",
    "⠀⠀⠈⢳⡕⣄⠀⠙⠻⢶⣤⡀⠉⠙⠻⡁⠀⠀⠀⢀⡼⣻⣿⠃",
    "⠀⠀⠀⠀⠙⣮⠑⠦⣀⠀⠉⠻⢶⣄⠀⠈⠦⡀⠖⠉⢰⣿⠋",
    "⠀⠀⠀⠀⠀⠈⠳⣤⣀⠉⠓⠄⠀⠙⢿⣤⡀⠀⠀⣠⡿⠁",
    "⠀⠀⠀⠀⠀⠀⠀⠈⠛⠷⣶⣤⡀⠀⠈⠻⡛⠂⠀⣉",
]

for art in ascii_art:
    banner_lines.append("║{:^90}║".format(art))
banner_lines += [
    "╠" + "═" * 90 + "╣",
    "║ {:<88} ║".format("ZALO: 0785308626"),
    "║ {:<88} ║".format("FACEBOOK: https://www.facebook.com/share/19db7bX5Jr/"),
    "╚" + "═" * 90 + "╝"
]

def print_banner():
    os.system("clear")
    for i, line in enumerate(banner_lines):
        print(colors[i % len(colors)] + line + reset)
        time.sleep(0.003)

def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def shorten_link(url):
    token = "28eb61f0b99302a47b7da55f3170c73934e6613c9d5c1dc99a9c123a548e3776"
    api = "https://yeumoney.com/QL_api.php"
    try:
        res = requests.get(api, params={"token": token, "format": "json", "url": url}, timeout=10)
        if res.ok:
            return res.json().get("shortenedUrl")
        print(colors[0] + f"[X] Lỗi rút gọn link: {res.text}" + reset)
        return None
    except Exception as e:
        print(colors[0] + f"[X] Lỗi rút gọn link: {str(e)}" + reset)
        return None

def notify_webhook(link_id):
    try:
        user_ip = requests.get('https://api.ipify.org', timeout=5).text
        payload = {"id": link_id, "ip": user_ip}
        res = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if res.ok:
            data = res.json()
            print(colors[2] + "[✓] Đã gửi tín hiệu đến server." + reset)
            print(colors[3] + f"[+] IP người dùng: {data.get('ip', 'Unknown')}" + reset)
            print(colors[3] + f"[+] Key được tạo: {data.get('key', 'Unknown')}" + reset)
            return True
        else:
            print(colors[0] + f"[X] Lỗi gửi tín hiệu: {res.text}" + reset)
            return False
    except Exception as e:
        print(colors[0] + f"[X] Lỗi gửi tín hiệu: {str(e)}" + reset)
        return False

def double_shorten_link():
    rand_id = generate_random_id()
    base_url = f"https://tsanduongvi123.github.io/key-generator/?id={rand_id}"
    if not notify_webhook(rand_id):
        print(colors[0] + "[X] Không thể gửi tín hiệu, thử lại." + reset)
        return
    s1 = shorten_link(base_url)
    if not s1:
        print(colors[0] + "[X] Không rút gọn được lần 1." + reset)
        return
    time.sleep(1)
    s2 = shorten_link(s1)
    if not s2:
        print(colors[0] + "[X] Không rút gọn được lần 2." + reset)
        return
    print(colors[2] + "[✓] Link vượt 2 lớp: " + s2 + reset)

def check_key(key):
    try:
        res = requests.get(KEY_JSON, timeout=10)
        if not res.ok:
            print(colors[0] + f"[X] Lỗi tải key_data.json: {res.status_code}" + reset)
            return False
        keys = res.json().get("vip_keys", [])
        return key in keys
    except Exception as e:
        print(colors[0] + f"[X] Lỗi kiểm tra key: {str(e)}" + reset)
        return False

def show_tools():
    try:
        res = requests.get(ADMIN_JSON, timeout=10)
        if not res.ok:
            print(colors[0] + f"[X] Lỗi tải admin.json: {res.status_code}" + reset)
            return
        tools_data = res.json()
        tool_dict = tools_data.get("file_display_names", {})
        print("\n" + colors[3] + "[+] Danh sách tool:" + reset)
        for i, (filename, display_name) in enumerate(tool_dict.items(), 1):
            print(f"{colors[i%len(colors)]}[{i}] {display_name} ({filename}){reset}")
        print("\nChọn tool để chạy hoặc nhập 0 để thoát.")
        while True:
            choice = input("Chọn tool: ").strip()
            if choice == "0":
                print("Thoát menu tool.")
                break
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tool_dict):
                print(colors[0] + "Lựa chọn không hợp lệ, thử lại." + reset)
                continue
            idx = int(choice) - 1
            filename = list(tool_dict.keys())[idx]
            display_name = list(tool_dict.values())[idx]
            print(colors[2] + f"Bạn đã chọn tool: {display_name} ({filename})" + reset)
            try:
                os.system(f"python3 {filename}")
            except Exception as e:
                print(colors[0] + f"[X] Lỗi chạy tool: {str(e)}" + reset)
            break
    except Exception as e:
        print(colors[0] + f"[X] Lỗi tải tool: {str(e)}" + reset)

def main():
    print_banner()
    while True:
        print(colors[4] + "\n[1] Lấy key 48h (nếu chưa có hoặc hết hạn)")
        print("[2] Nhập key đã có")
        print("[3] Nhập key VIP")
        print("[0] Thoát" + reset)
        ch = input("\n[?] Chọn: ").strip()
        if ch == "1":
            print(colors[3] + "[!] Vào link để lấy key:" + reset)
            double_shorten_link()
        elif ch == "2" or ch == "3":
            key = input("Nhập key: ").strip()
            if check_key(key):
                print(colors[2] + "[✓] Key hợp lệ!" + reset)
                os.system("rm -rf __pycache__")
                print_banner()
                show_tools()
            else:
                print(colors[0] + "[X] Key sai hoặc hết hạn!" + reset)
        elif ch == "0":
            print(colors[3] + "Thoát chương trình." + reset)
            break
        else:
            print(colors[0] + "Lựa chọn không hợp lệ." + reset)

if __name__ == "__main__":
    main()
