import time
import mc6470
import math
import subprocess
import requests
import psutil

accl = mc6470.Accelerometer()
script_path = '/home/wearableaac/send_regions_to_glass.py'

def is_script_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if script_name in ' '.join(proc.info['cmdline']):
                return True
        except Exception:
            continue
    return False

while True:
    time.sleep(1)
    ax, ay, az = accl.get_data()
    roll_rad = math.atan2(ay, az)
    roll_deg = math.degrees(roll_rad)
    degtest = roll_deg + 180

    if 45 < degtest < 90:
        if not is_script_running('send_regions_to_glass.py'):
            subprocess.Popen(['python3', script_path])
            print("Started script due to left tilt")
        else:
            print("Script already running.")
    elif 270 < degtest < 315:
        print("⚠️ right head tilt", flush=True)
    elif degtest < 30 or degtest > 330:
        # optional: stop the process when head is straight
        #if process and process.poll() is None:
            #process.terminate()
            #print("✅ head upright: process terminated", flush=True)
        continue
    else:
        #print("✅ normal position", flush=True)
        continue



    #print("", flush=True)
    #print(f"aX: {ax:.2f} m/s², Y: {ay:.2f} m/s², Z: {az:.2f} m/s²", flush=True)
    #print(f"head roll angle: {degtest:.2f}°", flush=True)
    #print("acceleration in x-axis: %.2f m/s2"%ax, flush=True)
    #print("acceleration in y-axis: %.2f m/s2"%ay, flush=True)
    #print("acceleration in z-axis: %.2f m/s2"%az, flush=True)
    #print("angular position: %.2f degrees"%accl.get_angle_in_degrees(ax,ay), flush=True)
    #print("", flush=True)

