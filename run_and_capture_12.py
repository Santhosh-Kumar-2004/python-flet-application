import subprocess
import time
import sys

def main():
    print("Starting main.py with virtualenv python...", flush=True)
    
    proc = subprocess.Popen(
        [r"c:\Users\santh\Music\flet-mobile-app\flet_env\Scripts\python.exe", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    
    print("Waiting 12 seconds...", flush=True)
    time.sleep(12)
    
    print("Terminating main.py...", flush=True)
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        
    stdout_data, stderr_data = proc.communicate()
    
    print("\n--- STDOUT ---")
    print(stdout_data)
    print("\n--- STDERR ---")
    print(stderr_data)
    
    with open("stdout_capture_new.log", "w", encoding="utf-8") as f:
        f.write(stdout_data)
        
    with open("stderr_capture_new.log", "w", encoding="utf-8") as f:
        f.write(stderr_data)

if __name__ == "__main__":
    main()
