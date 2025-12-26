import time
import subprocess
from pypresence import Presence

# ================= CẤU HÌNH =================
CLIENT_ID = 'YOUR-CLIENT-ID'  # <--- GIỮ NGUYÊN ID CŨ CỦA BẠN
PHONE_IP = 'YOUR-PHONE-IP'         # <--- GIỮ NGUYÊN IP CỦA BẠN

# Đường dẫn file ADB
ADB_PATH = r"C:\Users\son99\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

CHECK_INTERVAL = 3

GAME_MAP = {
    'com.vng.pubgmobile': {'name': 'PUBG Mobile VN', 'image': 'pubg_icon'},
    'com.levelinfinite.sgameGlobal': {'name': 'Honor of Kings', 'image': 'hok_icon'},
    'com.bandainamcoent.saovsww': {'name': 'SAO Variant Showdown', 'image': 'sao_icon'},
    'com.tencent.igceb': {'name': 'PUBG Mobile BETA', 'image': 'pubg_beta_icon'},
    'com.vng.cfm': {'name': 'Crossfire: Legends', 'image': 'cf_icon'},
    'com.tencent.tmgp.cf': {'name': 'Crossfire Mobile', 'image': 'cf_icon'}, 
    'com.vng.codmvn': {'name': 'Call of Duty: Mobile', 'image': 'cod_icon'},
    'com.HoYoverse.Nap': {'name': 'Zenless Zone Zero', 'image': 'zzz_icon'},
}
# ============================================

def adb_connect():
    try:
        cmd_check = [ADB_PATH, 'devices']
        output = subprocess.check_output(cmd_check, shell=False).decode('utf-8')
        if f"{PHONE_IP}:5555" in output and "\tdevice" in output:
            return True

        subprocess.run([ADB_PATH, 'disconnect', PHONE_IP], stdout=subprocess.DEVNULL)
        cmd_connect = [ADB_PATH, 'connect', PHONE_IP]
        subprocess.check_output(cmd_connect, shell=False)
        return True
    except:
        return False

def get_current_app_package():
    try:
        cmd = [ADB_PATH, '-s', f'{PHONE_IP}:5555', 'shell', 'dumpsys window | grep mCurrentFocus']
        output = subprocess.check_output(cmd, shell=False).decode('utf-8', errors='ignore')
        if '/' in output:
            return output.split('/')[0].split(' ')[-1].strip().replace('}', '')
    except:
        return None
    return None

def main():
    if not adb_connect():
        print("[-] Không thể kết nối ADB.")
        return

    print("[*] Đang khởi động Discord RPC...")
    try:
        RPC = Presence(CLIENT_ID)
        RPC.connect()
        print("[+] Đã kết nối Discord! Sẵn sàng.")
    except:
        print("[!] Lỗi kết nối Discord.")
        return

    last_package = ""
    start_time = None

    while True:
        if not adb_connect():
            time.sleep(5)
            continue

        current_package = get_current_app_package()

        # [DEBUG] Hiện tên gói để dễ kiểm tra
        if current_package and current_package != last_package:
             print(f"[System] App hiện tại: {current_package}")

        if current_package in GAME_MAP:
            game_info = GAME_MAP[current_package]
            
            if current_package != last_package:
                print(f"---> Đang chơi: {game_info['name']} <---")
                start_time = time.time()
                last_package = current_package
                
                try:
                    # --- SỬA ĐỔI HIỂN THỊ Ở ĐÂY ---
                    RPC.update(
                        # Details: Dòng chữ chính -> Hiện tên Game
                        details=game_info['name'],
                        
                        # State: Dòng chữ phụ -> Hiện trạng thái
                        state="Playing on Mobile", 
                        
                        # Ảnh lớn
                        large_image=game_info.get('image', 'default'),
                        large_text=game_info['name'],
                        
                        # Thời gian
                        start=start_time
                    )
                except:
                    print("Lỗi update RPC")

        elif current_package and current_package != last_package:
            RPC.clear()
            last_package = current_package

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()