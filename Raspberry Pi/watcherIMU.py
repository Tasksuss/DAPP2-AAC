import subprocess
import requests

def main():
    p = subprocess.Popen(
        ['python3', 'IMUflask.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for output_line in p.stdout:
        output_line = output_line.strip()
        print(output_line)

        if "⚠️ right head tilt" in output_line:
            print("calibration starts")
            try:
                # open file
                subprocess.Popen(['python3', '/home/wearableaac/send_regions_to_glass.py'])
                print("file open")
            except Exception as e:
                print("fail to open")

if __name__ == '__main__':
    main()
