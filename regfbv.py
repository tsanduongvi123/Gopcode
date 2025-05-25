import hashlib
import random
import requests
import time
from datetime import datetime
import json
import sys
import urllib3

# Định nghĩa màu sắc và ký hiệu mới
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\x1b[38;2;0;255;127m"   # Xanh lá nhạt
RED = "\x1b[38;2;255;69;0m"       # Đỏ cam
CYAN = "\x1b[38;2;0;255;255m"     # Xanh dương nhạt
YELLOW = "\x1b[38;2;255;215;0m"   # Vàng nhạt
PINK = "\x1b[38;2;255;105;180m"   # Hồng phấn
WHITE = "\x1b[38;2;245;245;245m"  # Trắng sáng

# Ký hiệu đẹp hơn
CHECK = f"{GREEN}✔{RESET}"
CROSS = f"{RED}✘{RESET}"
STAR = f"{YELLOW}★{RESET}"
INFO = f"{CYAN}ℹ{RESET}"
LINE = f"{CYAN}═{'═' * 48}═{RESET}"
HALF_LINE = f"{PINK}─{'─' * 20}─{RESET}"

# Vô hiệu hóa cảnh báo InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cấu hình API và Key
app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32',
    'key': ['NVĐ_KeyRegFBVIP_9999', 'DCHVIPKEYREG']
}

email_prefix = [
    'gmail.com', 'hotmail.com', 'yahoo.com', 'live.com',
    'rocket.com', 'outlook.com',
]

# Hàm tạo tài khoản
def create_account():
    random_birth_day = datetime.strftime(datetime.fromtimestamp(random.randint(
        int(time.mktime(datetime.strptime('1980-01-01', '%Y-%m-%d').timetuple())),
        int(time.mktime(datetime.strptime('1995-12-30', '%Y-%m-%d').timetuple()))
    )), '%Y-%m-%d')

    names = {
        'first': ['JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID'],
        'last': ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER'],
        'mid': ['Alexander', 'Anthony', 'Charles', 'Dash', 'David', 'Edward']
    }

    random_first_name = random.choice(names['first'])
    random_name = f"{random.choice(names['mid'])} {random.choice(names['last'])}"
    password = f'NVĐ{random.randint(0, 9999999)}?#@'
    full_name = f"{random_first_name} {random_name}"
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()

    hash_ = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"
    email_rand = f"{full_name.replace(' ', '').lower()}{hashlib.md5((str(time.time()) + datetime.strftime(datetime.now(), '%Y%m%d')).encode()).hexdigest()[0:6]}@{random.choice(email_prefix)}"
    gender = 'M' if random.randint(0, 10) > 5 else 'F'

    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_,
        'return_multiple_errors': True
    }

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig

    api = 'https://b-api.facebook.com/method/user.register'

    def _call(url='', params=None, post=True):
        headers = {
            'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
        }
        if post:
            response = requests.post(url, data=params, headers=headers, verify=False)
        else:
            response = requests.get(url, params=params, headers=headers, verify=False)
        return response.text

    reg = _call(api, req)
    reg_json = json.loads(reg)
    uid = reg_json.get('session_info', {}).get('uid')
    access_token = reg_json.get('session_info', {}).get('access_token')
    error_code = reg_json.get('error_code')
    error_msg = reg_json.get('error_msg')

    if uid is not None and access_token is not None:
        data_to_save = f"{random_birth_day}:{full_name}:{email_rand}:{password}:{uid}:{access_token}"
        with open(file_name, "a") as file:
            file.write(data_to_save + "\n")
        
        print(f"{LINE}")
        print(f"{CHECK} {GREEN}Đăng ký thành công!{RESET}")
        print(f"{INFO} Birthday: {WHITE}{random_birth_day}{RESET}")
        print(f"{INFO} Fullname: {WHITE}{full_name}{RESET}")
        print(f"{INFO} Email: {WHITE}{email_rand}{RESET}")
        print(f"{INFO} Password: {WHITE}{password}{RESET}")
        print(f"{INFO} UID: {WHITE}{uid}{RESET}")
        print(f"{INFO} Token: {WHITE}{access_token}{RESET}")
        print(f"{LINE}")
    else:
        print(f"{LINE}")
        print(f"{CROSS} {RED}Đăng ký thất bại!{RESET}")
        if error_code and error_msg:
            print(f"{INFO} Error Code: {YELLOW}{error_code}{RESET}")
            print(f"{INFO} Error Msg: {YELLOW}{error_msg}{RESET}")
        else:
            print(f"{INFO} {YELLOW}Lỗi không xác định!{RESET}")
        print(f"{LINE}")

# Nhập thông tin từ người dùng
while True:
    try:
        account_count = int(input(f"{STAR} {CYAN}Nhập số lượng tài khoản muốn tạo: {RESET}"))
        if account_count > 0:
            break
        else:
            print(f"{CROSS} {RED}Số lượng phải lớn hơn 0!{RESET}")
    except ValueError:
        print(f"{CROSS} {RED}Vui lòng nhập số hợp lệ!{RESET}")

while True:
    file_name = input(f"{STAR} {CYAN}Nhập tên file để lưu thông tin: {RESET}")
    if file_name.strip():
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        break
    else:
        print(f"{CROSS} {RED}Tên file không được để trống!{RESET}")

while True:
    try:
        delay = int(input(f"{STAR} {CYAN}Nhập thời gian delay (tối thiểu 180s): {RESET}"))
        if delay >= 180:
            break
        else:
            print(f"{CROSS} {RED}Delay phải từ 180 giây trở lên!{RESET}")
    except ValueError:
        print(f"{CROSS} {RED}Vui lòng nhập số hợp lệ!{RESET}")

print(f"{LINE}")
print(f"{CHECK} {GREEN}Bắt đầu tạo {account_count} tài khoản...{RESET}")
print(f"{LINE}")

# Vòng lặp tạo tài khoản
for i in range(account_count):
    print(f"{HALF_LINE} Tài khoản {i+1}/{account_count} {HALF_LINE}")
    create_account()
    if i < account_count - 1:
        print(f"{INFO} {YELLOW}Đang chờ {delay} giây...{RESET}", end='')
        for remaining in range(delay, 0, -1):
            print(f"\r{INFO} {YELLOW}Đang chờ: {remaining} giây{RESET}", end='', flush=True)
            time.sleep(1)
        print()

print(f"{LINE}")
print(f"{CHECK} {GREEN}Hoàn tất! Đã lưu vào file: {WHITE}{file_name}{RESET}")
print(f"{LINE}")
sys.exit()