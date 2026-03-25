"""
Simple Alarm Clock - Command Line Version
Run: python alarm_cli.py
No extra libraries needed — uses only Python standard library.
"""

import time
import datetime
import threading
import sys

try:
    import winsound
    PLATFORM = "windows"
except ImportError:
    PLATFORM = "unix"

stop_flag = threading.Event()

def beep():
    """Cross-platform beep sound."""
    if PLATFORM == "windows":
        for _ in range(15):
            if stop_flag.is_set(): break
            winsound.Beep(880, 400)
            time.sleep(0.2)
            winsound.Beep(660, 300)
            time.sleep(0.2)
    else:
        for _ in range(15):
            if stop_flag.is_set(): break
            print('\a', end='', flush=True)  # terminal bell
            time.sleep(0.5)

def get_time_input():
    while True:
        try:
            t = input("Enter alarm time (HH:MM, 24-hour format): ").strip()
            h, m = map(int, t.split(":"))
            assert 0 <= h <= 23 and 0 <= m <= 59
            return f"{h:02d}:{m:02d}"
        except (ValueError, AssertionError):
            print("  ❌ Invalid time. Try again (e.g. 07:30)\n")

def countdown(alarm_time):
    print(f"\n  ✅ Alarm set for {alarm_time}")
    print("  Press Ctrl+C to cancel.\n")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        current = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\r  🕐 Current time: {current}  |  Alarm: {alarm_time}", end="", flush=True)
        if now == alarm_time:
            print(f"\n\n  🔔 ALARM RINGING! Time is {alarm_time}\n")
            t = threading.Thread(target=beep, daemon=True)
            t.start()
            input("  Press ENTER to stop the alarm...\n")
            stop_flag.set()
            print("  ✅ Alarm stopped. Goodbye!\n")
            break
        time.sleep(1)

def main():
    print("\n" + "="*45)
    print("       ⏰  SIMPLE ALARM CLOCK (CLI)")
    print("="*45)
    print(f"  Current time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print()

    while True:
        alarm_time = get_time_input()
        label = input("  Enter a label (optional, press Enter to skip): ").strip() or "Alarm"
        print(f"\n  Label: {label}")
        try:
            countdown(alarm_time)
        except KeyboardInterrupt:
            print("\n\n  ❌ Alarm cancelled.\n")

        again = input("  Set another alarm? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Bye! 👋\n")
            break
        stop_flag.clear()

if __name__ == "__main__":
    main()
