import time
import datetime
import random
import multiprocessing
from pynput.keyboard import Controller, Key

# --- Global Setup (Used by all processes) ---
# Define directional keys for movement tasks.
MOVE_DIRECTIONS = [
    'h', 
    'b',  
    'm', 
    'n' 
] 

keyboard = Controller()

# --- Key Press Utility Functions ---

def press_key(key): 
    """Presses and immediately releases a key, with a 0.5s duration.""" 
    keyboard.press(key) 
    time.sleep(0.5) 
    keyboard.release(key) 

def hold_key(key, duration): 
    """Holds a specified key for a given duration (BLOCKING).""" 
    keyboard.press(key) 
    time.sleep(duration) 
    keyboard.release(key) 

def press_simultaneous(key1, key2): 
    """Presses and releases two keys at the same time.""" 
    keyboard.press(key1) 
    keyboard.press(key2) 
    time.sleep(0.5) # Minimal sleep for simultaneous press registration 
    keyboard.release(key1) 
    keyboard.release(key2) 


# ---------------------------------------------------------------------- 
# --- CONCURRENT PROCESS FUNCTIONS --- 
# ---------------------------------------------------------------------- 

def task_30s_cycle(): 
    """P1: (Press 's', hold Key.right 1s, press Enter) every 30s.""" 
    interval = 30.0 
    print(f"[P1: 30s] Process started. Running every ~{interval}s.") 
    while True: 
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] 
        print(f"[P1: {timestamp}] Running 30s Cycle.") 
         
        # 1a. Press S 
        press_key('s') 
        time.sleep(0.1) 
         
        # 1b. Hold Move right for 1s
        hold_key(Key.right, 1) 
         
        # 1c. Press Enter 
        press_key(Key.enter) 
         
        # Sleep for the remainder of the interval
        time.sleep(interval)  

def task_1s_random_move_hold_x(): 
    """P2: (Press random direction, sleep 0.3s, hold 'v' for random time [0.1-0.6]) every 1s.""" 
    interval = 1.0 
    print(f"[P2: 1sR] Process started. Running every ~{interval}s (Will drift).") 
    while True: 
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] 
         
        # 2a. Press random move direction 
        direction_key = random.choice(MOVE_DIRECTIONS) 
        print(f"[P2: {timestamp}] Press {str(direction_key).replace('Key.', '').upper()} + Hold V.") 
        press_key(direction_key) 
        time.sleep(0.3) 
         
        # 2b. Hold 'v' for random time 
        hold_duration = random.uniform(0.1, 0.6) 
        hold_key('v', hold_duration) 
         
        time.sleep(interval) 

def task_1s_hold_enter(): 
    """P3: Hold Enter 1s every 1s.""" 
    interval = 1.0 
    print(f"[P3: 1sE] Process started. Running every ~{interval}s.") 
    while True: 
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] 
        print(f"[P3: {timestamp}] Press Enter.") 
        hold_key(Key.enter, 1.0) 
         
        # Simple sleep: Action takes 1.0s, so sleep is the remainder of the 1.0s interval
        time.sleep(interval - 1.0) # This should theoretically be 0 or very close to 0

def task_1s_press_ui_simultaneous(): 
    """P4: (Hold 'o' + press Enter, then press 'u' + 'i' simultaneously) every 1s.""" 
    interval = 1.0 
    print(f"[P4: 1sQI] Process started. Running every ~{interval}s.") 
    while True: 
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] 
        
        # Action 1: thay nguoi (Switch player/substitute) 
        print("P4: Thay nguoi: hold o + press Enter") 
        keyboard.press('o') 
        time.sleep(0.5) 
        press_key(Key.enter) # press_key holds for 0.5s internally
        time.sleep(0.5) 
        keyboard.release('o') 

        # Action 2: bo qua (Skip/pass) 
        print(f"[P4: {timestamp}] Press U+I simultaneously.") 
        press_simultaneous('u', 'i') # press_simultaneous holds for 0.5s internally

        # Simple sleep: This task takes ~2.0s due to internal sleeps (0.5 + 0.5 + 0.5 + 0.5)
        # It will immediately run the next cycle with almost no sleep.
        time.sleep(interval) 

# ---------------------------------------------------------------------- 
# --- MAIN EXECUTION --- 
# ---------------------------------------------------------------------- 


if __name__ == '__main__': 
    multiprocessing.freeze_support()  
     
    print("-" * 70) 
    print("Starting 4 concurrent processes (Approximate Timing). Press Ctrl+C to stop.") 
    print("‼️ P2 (Random Move) and P4 (Sub/Skip) will experience significant time drift.") 
    print("-" * 70) 

    # 1. Create Processes (Daemon=True ensures they stop when the main script is interrupted) 
    # P1 (task_30s_cycle) is commented out in your original logic.
    p1 = multiprocessing.Process(target=task_30s_cycle, daemon=True) 
    p2 = multiprocessing.Process(target=task_1s_random_move_hold_x, daemon=True) 
    p3 = multiprocessing.Process(target=task_1s_hold_enter, daemon=True) 
    p4 = multiprocessing.Process(target=task_1s_press_ui_simultaneous, daemon=True) 

    # 2. Start Processes 
    p1.start()
    p2.start() 
    p3.start() 
    p4.start()

    # 3. Keep the main process alive 
    try: 
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt: 
        print("-" * 70) 
        print("Script stopped.")
