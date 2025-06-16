import time
import mc6470
import math
import subprocess
import requests
import psutil
import RPi.GPIO as GPIO

GPIO.cleanup()
# ─── GPIO / LED SETUP ──────────────────────────────────────────────────────────
LED_PIN = 24  # BCM pin where LED anode (via resistor) is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)  # LED off at first

# Track LED state for blinking
led_state = False  # True = ON (GPIO.HIGH)

# ─── SENSOR & SCRIPT PATH SETUP ───────────────────────────────────────────────
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
    time.sleep(0.5)
    ax, ay, az = accl.get_data()
    roll = math.degrees(math.atan2(ax, az))
    rel = roll - 90
    blink_on = False

    if -90 < rel < -45:      # left head tilt
        blink_on = True
        if not is_script_running('Emergency.py'):
            subprocess.Popen(['python3', '/home/wearableaac/Emergency.py'])
            print("Started script due to left tilt")
#        else:
#            print("Script already running.")
    elif 45 < rel < 90:      # right head tilt
        if not is_script_running('send_regions_to_glass.py'):
            subprocess.Popen(['python3', script_path])
#            print("Started script due to right tilt")
#        else:
            print("Script already running.")
    elif -45 < rel < 45:      # normal
#        print("normal")
        continue
    else:
        print("Emergency")
    # ── LED handling ───────────────────────────────────────────────────────
    if blink_on:
        # Toggle LED state to create blink effect (1 Hz)
        led_state = not led_state
        GPIO.output(LED_PIN, GPIO.HIGH if led_state else GPIO.LOW)
    else:
        # Ensure LED is solid ON
        if not led_state:
            led_state = True
            GPIO.output(LED_PIN, GPIO.LOW)




    #print("", flush=True)
    #print(f"aX: {ax:.2f} m/s², Y: {ay:.2f} m/s², Z: {az:.2f} m/s²", flush=True)
    #print(f"head roll angle: {rel:.2f}°", flush=True)
    #print("acceleration in x-axis: %.2f m/s2"%ax, flush=True)
    #print("acceleration in y-axis: %.2f m/s2"%ay, flush=True)
    #print("acceleration in z-axis: %.2f m/s2"%az, flush=True)
    #print("angular position: %.2f degrees"%accl.get_angle_in_degrees(ax,ay), flush=True)
    #print("", flush=True)

