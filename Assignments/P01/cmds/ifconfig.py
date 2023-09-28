# ifconfig_command.py

import subprocess

def ifconfig(**kwargs):
    print('/n')
    try:
        # Use the "ip" command to fetch network interface information
        result = subprocess.check_output(["ip", "a"], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
