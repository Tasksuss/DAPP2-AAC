import socket
import time

def send_regions_to_glass():
    region = "Emergency"
    print('[DEBUG] Entered send_regions_to_glass')
    HOST = '172.20.10.3'  # Google Glass 的 IP
    PORT = 5051
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"[INFO] Connected to Glass at {HOST}:{PORT}")

            print(f"[SEND] Sending region: {region}")
            try:
                s.sendall((region + '\n').encode())  
            except Exception as e:
                print(f"[ERROR] Failed to send: {e}")
                time.sleep(0.5)
    except Exception as e:
        print(f"[ERROR] Could not connect to Google Glass: {e}")
        time.sleep(2)

if __name__ == '__main__':
    send_regions_to_glass()
