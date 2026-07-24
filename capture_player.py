import subprocess
import time
import pygetwindow as gw
import pyautogui
from PIL import Image

def main():
    print("Starting Flet Music Player...")
    # Start the flet music player in the background
    proc = subprocess.Popen(
        ["C:\\Users\\santh\\Music\\flet-mobile-app\\flet_env\\Scripts\\python.exe", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait 6 seconds for the UI to fully load
    print("Waiting 6 seconds for UI to fully load...")
    time.sleep(6)
    
    # Let's find the Flet window
    # Flet window title is "Flet Music Player" or starts with "Flet"
    print("Searching for Flet Music Player window...")
    titles = gw.getAllTitles()
    print("All active window titles:", titles)
    
    flet_windows = [w for w in gw.getWindowsWithTitle("Flet Music Player") if w.title == "Flet Music Player"]
    if not flet_windows:
        # fallback
        flet_windows = [w for w in gw.getWindowsWithTitle("Flet") if "Flet" in w.title]
        
    if flet_windows:
        win = flet_windows[0]
        print(f"Found window: {win.title} at left={win.left}, top={win.top}, width={win.width}, height={win.height}")
        # Activate/focus the window
        try:
            win.activate()
            time.sleep(1)
        except Exception as e:
            print(f"Could not activate window: {e}")
            
        # Take screen shot of the specific window
        rect = (win.left, win.top, win.width, win.height)
        # Ensure coordinates are within screen bounds and valid
        if win.width > 0 and win.height > 0:
            print("Taking screenshot...")
            screenshot = pyautogui.screenshot(region=rect)
            screenshot.save("player_ui.png")
            print("Screenshot saved to player_ui.png")
        else:
            print("Window dimensions are invalid. Taking full screenshot instead.")
            screenshot = pyautogui.screenshot()
            screenshot.save("player_ui.png")
    else:
        print("Flet window not found! Taking full screenshot.")
        screenshot = pyautogui.screenshot()
        screenshot.save("player_ui.png")
        
    # Terminate process
    print("Stopping the process...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
    print("Done!")

if __name__ == "__main__":
    main()
