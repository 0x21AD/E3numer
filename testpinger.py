import os
import subprocess

with open(os.devnull, 'w') as DEVNULL:
    try:
        subprocess.check_call(
            ['ping', '-c', '3', 'asdfajkshbfahbcnasfcua.com'],
            stdout=DEVNULL,  # suppress output
            stderr=DEVNULL
        )
        is_up = True   
    except subprocess.CalledProcessError:
        is_up = False
        print("down")