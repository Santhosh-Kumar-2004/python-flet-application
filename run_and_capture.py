import subprocess
import time
import sys

def main():
    print("Starting Flet Music Player process...", flush=True)
    
    # We want to run main.py and capture BOTH stdout and stderr, without redirection blocks.
    # Start the process with direct pipelines.
    proc = subprocess.Popen(
        ["C:\\Users\\santh\\Music\\flet-mobile-app\\flet_env\\Scripts\\python.exe", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for 8 seconds
    print("Waiting 8 seconds to capture logs...", flush=True)
    time.sleep(8)
    
    print("Stopping Flet Music Player...", flush=True)
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        
    print("Reading capturing outputs...", flush=True)
    stdout_data, stderr_data = proc.communicate()
    
    print("\n--- STDOUT ---")
    print(stdout_data)
    print("\n--- STDERR ---")
    print(stderr_data)
    
if __name__ == "__main__":
    main()
