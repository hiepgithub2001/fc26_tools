import time
import datetime
import random
import multiprocessing
from pynput.keyboard import Controller, Key

# --- Global Setup (Used by all processes) ---
# Note: keyboard controller is initialized implicitly in each process.
MOVE_DIRECTIONS = [
    'h',
    'b', 
    'm',
    'n'
    # Key.down  # avoid choose another tab bar
]

keyboard = Controller()
# --- Key Press Utility Functions ---

def press_key(key):
    """Presses and immediately releases a key."""
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
    """1. (press S, sleep 1s, press 'Move right', sleep 1s, press Enter) every 3s"""
    interval = 30.0
    print(f"[P1: 3s] Process started. Running every ~{interval}s.")
    while True:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[P1: {timestamp}] Running 30s Cycle.")
        
        # 1a. Press S
        press_key('s')
        time.sleep(0.1)
        
        # 1b. Press Move right
        hold_key(Key.right, 1)
        
        # 1c. Press Enter
        press_key(Key.enter)
        
        # Approximate interval: Action takes ~2 seconds, so sleep is 1s
        time.sleep(interval) 

def task_1s_random_move_hold_x():
    """2. (press 'Move dir' random, sleep 1s, hold x random time [0.12- 1]) every 1s"""
    # NOTE: The action itself takes 1.12s to 2.0s, so this task WILL cause drift.
    interval = 1.0
    print(f"[P2: 1sR] Process started. Running every ~{interval}s (Will drift).")
    while True:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # 2a. Press random move direction
        direction_key = random.choice(MOVE_DIRECTIONS)
        print(f"[P2: {timestamp}] Press {str(direction_key).replace('Key.', '').upper()} + Hold V.")
        press_key(direction_key)
        time.sleep(0.3)
        
        # 2b. Hold v for random time
        hold_duration = random.uniform(0.1, 0.6)
        hold_key('v', hold_duration)
        
        time.sleep(interval)

def task_1s_hold_enter():
    """3. Press Enter every 1s"""
    interval = 10.0
    print(f"[P3: 1sE] Process started. Running every ~{interval}s.")
    while True:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[P3: {timestamp}] Press Enter.")
        hold_key(Key.enter, 1.0)
        
        # Simple sleep: Action is instantaneous, so sleep is full interval
        time.sleep(interval)

def task_1s_press_qi_simultaneous():
    """4. (press Q + I at the same time) every 1s"""
    interval = 1.0
    print(f"[P4: 1sQI] Process started. Running every ~{interval}s.")
    while True:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[P4: {timestamp}] Press Q+I simultaneously.")
        press_simultaneous('u', 'i')
        
        # Simple sleep: Action is instantaneous, so sleep is full interval
        time.sleep(interval) 

# ----------------------------------------------------------------------
# --- MAIN EXECUTION ---
# ----------------------------------------------------------------------

if __name__ == '__main__':
    multiprocessing.freeze_support() 
    
    print("-" * 70)
    print("Starting 4 concurrent processes (Approximate Timing). Press Ctrl+C to stop.")
    print("‼️ P2 (Random Move) will experience significant time drift.")
    print("-" * 70)

    # 1. Create Processes (Daemon=True ensures they stop when the main script is interrupted)
    # p1 = multiprocessing.Process(target=task_30s_cycle, daemon=True)
    p2 = multiprocessing.Process(target=task_1s_random_move_hold_x, daemon=True)
    p3 = multiprocessing.Process(target=task_1s_hold_enter, daemon=True)
    p4 = multiprocessing.Process(target=task_1s_press_qi_simultaneous, daemon=True)

    # 2. Start Processes
    # p1.start()
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