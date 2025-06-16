import socket
import time
from watchereye_tracking import gaze_region_generator
# from watcherIMU import status

def send_regions_to_glass():
    print('[DEBUG] Entered send_regions_to_glass')
    HOST = '172.20.10.3'  # Google Glass 的 IP
    PORT = 5051
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print(f"[INFO] Connected to Glass at {HOST}:{PORT}")

                for region in gaze_region_generator():
                    print(f"[SEND] Sending region: {region}")
                    try:
                        s.sendall((region + '\n').encode())  # 添加换行符以便分割
                    except Exception as e:
                        print(f"[ERROR] Failed to send: {e}")
                        break  # 重连
                    time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Could not connect to Google Glass: {e}")
            time.sleep(2)  # 等待后重试

if __name__ == '__main__':
    # 可按需接入 IMU 状态判断
       # while True:
       # if status == True:
    send_regions_to_glass()
