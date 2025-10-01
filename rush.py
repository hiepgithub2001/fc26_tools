import time
import datetime
import random
import multiprocessing
from pynput.keyboard import Controller, Key

# --- Global Setup (Used by all processes) ---
# Define the pool of keys for the first random task (P2: Movement).
RANDOM_MOVE_KEYS = ['b', 'n', 'm', 'h']
# Define the pool of keys for the second random task (P3: Weighted Attack/Action).
# Keys are weighted: 'v' (4/8), 'e' (3/8), 'a' (1/8).
RANDOM_ATTACK_KEYS = ['v', 'v', 'v', 'v', 'a', 'e', 'e', 'e']

# Initialize the keyboard controller (needs to be initialized in the main process, 
# and implicitly available in child processes via shared state or re-initialization).
keyboard = Controller()

# --- Key Press Utility Function ---

def hold_key(key, duration):
    """Holds a specified key for a given duration (BLOCKING)."""
    # Note: For pynput, using a string for alphabetical keys ('a', 'b') works well.
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)
    
# ----------------------------------------------------------------------
# --- CONCURRENT PROCESS FUNCTIONS ---
# ----------------------------------------------------------------------

def task_enter_hold():
    """1. Hold Enter 1s every 10s."""
    interval = 15.0
    hold_duration = 1.0
    print(f"[P1: 10sE] Process started. Running every {interval}s.")
    
    while True:
        start_time = time.time()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"[P1: {timestamp}] Holding ENTER for {hold_duration}s.")
        
        # Hold Enter for the required duration (1.0s)
        hold_key(Key.enter, hold_duration)
        
        # Calculate time spent and sleep for the remainder of the 10s interval
        time_spent = time.time() - start_time
        sleep_time = interval - time_spent
        
        if sleep_time > 0:
            time.sleep(sleep_time)

def task_random_move_hold():
    """2. Every 0.1s, hold random of ('b', 'n', 'm', 'h') exactly 1s."""
    interval = 0.1
    hold_duration = 1.0
    
    print(f"[P2: 0.1sR] Process started. Running every {interval}s.")
    # WARNING: Action time (1.0s) > Interval (0.1s). The effective cycle time will be ~1.0s + minimal sleep.
    print(f"[P2: 0.1sR] ‼️ WARNING: Hold duration ({hold_duration}s) > interval ({interval}s). Significant time drift.")
    
    while True:
        start_time = time.time()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Select random key from the updated list
        random_key = random.choice(RANDOM_MOVE_KEYS)
        
        print(f"[P2: {timestamp}] Holding '{random_key}' for {hold_duration}s.")
        
        # Hold the key for the required duration (1.0s)
        hold_key(random_key, hold_duration)
        
        # Calculate time spent and sleep for the remainder of the 0.1s interval
        time_spent = time.time() - start_time
        sleep_time = interval - time_spent 
        
        # Since the action is longer than the interval, we add a minimal sleep 
        # to ensure the CPU scheduler has a moment before the next 1s hold starts.
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            time.sleep(0.01) # Minimal sleep to prevent busy-waiting

def task_random_attack_hold():
    """3. Every 0.1s hold random of ('v', 'v', 'v' , 'v', 'a', 'e', 'e', 'e') exactly 0.3s."""
    interval = 0.1
    hold_duration = 0.3
    
    print(f"[P3: 0.1sA] Process started. Running every {interval}s.")
    # WARNING: Action time (0.3s) > Interval (0.1s). The effective cycle time will be ~0.3s + minimal sleep.
    print(f"[P3: 0.1sA] ‼️ WARNING: Hold duration ({hold_duration}s) > interval ({interval}s). Significant time drift.")
    
    while True:
        start_time = time.time()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Select random key from the weighted list
        random_key = random.choice(RANDOM_ATTACK_KEYS)
        
        print(f"[P3: {timestamp}] Holding '{random_key}' for {hold_duration}s.")
        
        # Hold the key for the required duration (0.3s)
        hold_key(random_key, hold_duration)
        
        # Calculate time spent and sleep for the remainder of the 0.1s interval
        time_spent = time.time() - start_time
        sleep_time = interval - time_spent 
        
        # Since the action is longer than the interval, we add a minimal sleep 
        # to ensure the CPU scheduler has a moment.
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            time.sleep(0.01) # Minimal sleep to prevent busy-waiting

# ----------------------------------------------------------------------
# --- MAIN EXECUTION ---
# ----------------------------------------------------------------------

if __name__ == '__main__':
    multiprocessing.freeze_support() 
    
    print("-" * 70)
    print("Starting 3 concurrent processes. Press Ctrl+C to stop.")
    print("‼️ P2 (Random Move) and P3 (Random Attack) will experience significant time drift.")
    print("-" * 70)

    # 1. Create Processes (Daemon=True ensures they stop when the main script is interrupted)
    p1 = multiprocessing.Process(target=task_enter_hold, daemon=True)
    p2 = multiprocessing.Process(target=task_random_move_hold, daemon=True)
    p3 = multiprocessing.Process(target=task_random_attack_hold, daemon=True)

    # 2. Start Processes
    p1.start()
    p2.start()
    p3.start()

    # 3. Keep the main process alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("-" * 70)
        print("Script stopped.")
