import subprocess
import time
import pygetwindow as gw
import pyautogui
from PIL import Image

def main():
    print("Starting Flet Music Player...")
    # Start the flet music player in the background using the virtual env python interpreter
    proc = subprocess.Popen(
        ["C:\\Users\\santh\\Music\\flet-mobile-app\\flet_env\\Scripts\\python.exe", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait 8 seconds to fully load the Flet window with the music player UI
    print("Waiting 8 seconds for UI to fully load...")
    time.sleep(8)
    
    print("Searching for Flet window...")
    # Get active window titles
    titles = [w.title for w in gw.getAllWindows() if w.title]
    print("All active window titles:", titles)
    
    # Check for titles containing "Flet"
    flet_windows = [w for w in gw.getWindowsWithTitle("Flet Music Player") if w.title == "Flet Music Player"]
    if not flet_windows:
        flet_windows = [w for w in gw.getWindowsWithTitle("Flet") if "Flet" in w.title]
    if not flet_windows:
        flet_windows = [w for w in gw.getAllWindows() if "flet" in w.title.lower()]
        
    if flet_windows:
        win = flet_windows[0]
        print(f"Found window: {win.title} at left={win.left}, top={win.top}, width={win.width}, height={win.height}")
        try:
            win.activate()
            time.sleep(1)
        except Exception as e:
            print(f"Could not activate window: {e}")
            
        rect = (win.left, win.top, win.width, win.height)
        if win.width > 0 and win.height > 0:
            print("Taking screenshot of the window...")
            screenshot = pyautogui.screenshot(region=rect)
            screenshot.save("music_player_screenshot.png")
            print("Screenshot saved to music_player_screenshot.png")
        else:
            print("Window dimensions are invalid. Taking full screenshot instead.")
            screenshot = pyautogui.screenshot()
            screenshot.save("music_player_screenshot.png")
    else:
        print("Flet window not found! Taking full screenshot.")
        screenshot = pyautogui.screenshot()
        screenshot.save("music_player_screenshot.png")
        
    print("Stopping the app...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
    print("Done!")

if __name__ == "__main__":
    main()
