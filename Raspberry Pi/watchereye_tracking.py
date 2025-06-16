import subprocess
import time
import collections
import RPi.GPIO as GPIO

# ─── GPIO ─────────────────────────────────────────────────────────────────────
LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)  

def gaze_region_generator():
    p = subprocess.Popen(
        ['python3', '-u', '/home/wearableaac/calibration.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )

    print("[INFO] start monitoring outputlines:")

    for output_line in p.stdout:
        output_line = output_line.strip()
        print(f"output:{output_line}")

        if output_line in {"1", "2", "3", "4", "5", "6", "7", "8",
                           "9", "10", "12", "13", "14", "15", "16",
                           "17", "18", "19", "20", "21", "22", "23",
                           "24", "25", "center", "top_mid", "left_mid"
                            , "bottom_mid", "right_mid"}:
            yield output_line
#            time.sleep(0.5)  # control frequency
if __name__ == "__main__":
    # (timestamp, value)
    WINDOW = collections.deque()
    WINDOW_SPAN = 4.0  # sec

    try:
        for line in proc.stdout:
            now = time.time()
            val = line.strip()
            if not val:
                continue

            WINDOW.append((now, val))
            while WINDOW and WINDOW[0][0] < now - WINDOW_SPAN:
                WINDOW.popleft()

            counts = {}
            for _t, v in WINDOW:
                counts[v] = counts.get(v, 0) + 1

            if counts.get("24", 0) >= 4:
                GPIO.output(LED_PIN, GPIO.LOW)
                print("[LED] OFF — code 24 x4 within 4 s")
                continue

            for k in counts:
                if k.isdigit() and 1 <= int(k) <= 21 and counts[k] >= 4:
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    print(f"[LED] ON  — code {k} x4 within 4 s")
                    break

    finally:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()
        if proc.poll() is None:
            proc.terminate()

    for region in gaze_region_generator():
        continue

