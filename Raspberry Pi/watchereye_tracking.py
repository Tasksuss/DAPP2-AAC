import subprocess
import time

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
                           "24", "25"}:
            yield output_line
#            time.sleep(0.5)  # control frequency
if __name__ == "__main__":
    for region in gaze_region_generator():
        continue
