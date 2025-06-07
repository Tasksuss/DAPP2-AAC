import time
import mc6470
import math

accl = mc6470.Accelerometer()

while True:
    time.sleep(1)
    ax, ay, az = accl.get_data()

    roll_rad = math.atan2(ay, az)
    roll_deg = math.degrees(roll_rad)

    print(f"aX: {ax:.2f} m/s², Y: {ay:.2f} m/s², Z: {az:.2f} m/s²", flush=True)
    print(f"head roll angle: {roll_deg:.2f}°", flush=True)

    if roll_deg > 45:
        print("⚠️ right head tilt", flush=True)
    elif roll_deg < -45:
        print("⚠️ left head tilt", flush=True)
    else:
        print("✅ normal position", flush=True)

        print("", flush=True)

        print("acceleration in x-axis: %.2f m/s2"%ax, flush=True)
        print("acceleration in y-axis: %.2f m/s2"%ay, flush=True)
        print("acceleration in z-axis: %.2f m/s2"%az, flush=True)
        print("angular position: %.2f degrees"%accl.get_angle_in_degrees(ax,ay), fl>
        print("", flush=True)

