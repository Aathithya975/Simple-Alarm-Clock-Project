"""
Simple Alarm Clock - Python Tkinter Mini Project
Run: python alarm_clock.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime
import winsound  # Windows built-in beep (no extra install needed)
import sys
import os

# ── Try importing pygame for better audio (optional) ──────────────────────────
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# ── Color Palette ──────────────────────────────────────────────────────────────
BG        = "#0b0f1a"
CARD      = "#111827"
BORDER    = "#1f2937"
ACCENT    = "#00d4aa"
ACCENT2   = "#6366f1"
TEXT      = "#e2e8f0"
MUTED     = "#4b5563"
RED       = "#ef4444"
GREEN     = "#10b981"
FONT_MONO = ("Courier New", 10)
FONT_CLOCK= ("Courier New", 52, "bold")
FONT_TITLE= ("Courier New", 13, "bold")
FONT_LABEL= ("Courier New", 9)
FONT_BTN  = ("Courier New", 10, "bold")

# ── Global state ───────────────────────────────────────────────────────────────
alarms        = []          # list of {"time": "HH:MM", "label": str, "enabled": bool}
alarm_ringing = False
stop_alarm_flag = threading.Event()


# ══════════════════════════════════════════════════════════════════════════════
#  Audio helpers
# ══════════════════════════════════════════════════════════════════════════════
def play_beep():
    """Play alarm sound — uses pygame if available, else Windows beep."""
    global alarm_ringing
    alarm_ringing = True
    stop_alarm_flag.clear()

    def _play():
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
            # Generate a simple beep using pygame
            sample_rate = 44100
            duration    = 0.4
            freq        = 880
            import numpy as np
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
            stereo = np.column_stack([wave, wave])
            sound  = pygame.sndarray.make_sound(stereo)
            for _ in range(20):
                if stop_alarm_flag.is_set():
                    break
                sound.play()
                time.sleep(0.6)
        else:
            # Windows built-in beep (no install)
            for _ in range(20):
                if stop_alarm_flag.is_set():
                    break
                try:
                    winsound.Beep(880, 400)
                    time.sleep(0.3)
                    winsound.Beep(660, 300)
                    time.sleep(0.3)
                except Exception:
                    time.sleep(0.7)

    t = threading.Thread(target=_play, daemon=True)
    t.start()

def stop_beep():
    global alarm_ringing
    alarm_ringing = False
    stop_alarm_flag.set()


# ══════════════════════════════════════════════════════════════════════════════
#  Main Application
# ══════════════════════════════════════════════════════════════════════════════
class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Alarm Clock")
        self.root.geometry("520x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self._build_ui()
        self._tick()
        self._check_alarms()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title
        tk.Label(self.root, text="⏰  ALARM CLOCK", bg=BG, fg=ACCENT,
                 font=FONT_TITLE).pack(pady=(20, 0))
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=8)

        # Live Clock Display
        clock_frame = tk.Frame(self.root, bg=CARD, bd=0, relief="flat")
        clock_frame.pack(padx=30, pady=0, fill="x")

        self.clock_label = tk.Label(
            clock_frame, text="00:00:00",
            bg=CARD, fg=ACCENT, font=FONT_CLOCK,
            pady=18, padx=10
        )
        self.clock_label.pack()

        self.date_label = tk.Label(
            clock_frame, text="",
            bg=CARD, fg=MUTED, font=FONT_LABEL
        )
        self.date_label.pack(pady=(0, 14))

        # Separator
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=10)

        # ── Set Alarm Section ─────────────────────────────────────────────────
        tk.Label(self.root, text="SET ALARM", bg=BG, fg=MUTED,
                 font=FONT_LABEL).pack(anchor="w", padx=32)

        set_frame = tk.Frame(self.root, bg=CARD)
        set_frame.pack(padx=30, pady=6, fill="x")

        # Hour / Minute / AM-PM selectors
        time_row = tk.Frame(set_frame, bg=CARD)
        time_row.pack(pady=14, padx=14)

        tk.Label(time_row, text="HH", bg=CARD, fg=MUTED, font=FONT_LABEL).grid(row=0, column=0, padx=6)
        tk.Label(time_row, text="MM", bg=CARD, fg=MUTED, font=FONT_LABEL).grid(row=0, column=2, padx=6)
        tk.Label(time_row, text="AM/PM", bg=CARD, fg=MUTED, font=FONT_LABEL).grid(row=0, column=4, padx=6)

        self.hour_var   = tk.StringVar(value="07")
        self.minute_var = tk.StringVar(value="00")
        self.ampm_var   = tk.StringVar(value="AM")

        sp_style = dict(bg=BORDER, fg=TEXT, font=FONT_MONO, bd=0,
                        relief="flat", width=4, justify="center",
                        insertbackground=ACCENT)

        self.hour_spin = tk.Spinbox(
            time_row, from_=1, to=12, textvariable=self.hour_var,
            format="%02.0f", wrap=True, **sp_style)
        self.hour_spin.grid(row=1, column=0, padx=6, ipady=6)

        tk.Label(time_row, text=":", bg=CARD, fg=ACCENT,
                 font=("Courier New", 22, "bold")).grid(row=1, column=1)

        self.min_spin = tk.Spinbox(
            time_row, from_=0, to=59, textvariable=self.minute_var,
            format="%02.0f", wrap=True, **sp_style)
        self.min_spin.grid(row=1, column=2, padx=6, ipady=6)

        ampm_menu = tk.OptionMenu(time_row, self.ampm_var, "AM", "PM")
        ampm_menu.config(bg=BORDER, fg=TEXT, font=FONT_MONO,
                         activebackground=ACCENT2, activeforeground=TEXT,
                         bd=0, relief="flat", highlightthickness=0, width=4)
        ampm_menu.grid(row=1, column=4, padx=6, ipady=4)

        # Label entry
        label_row = tk.Frame(set_frame, bg=CARD)
        label_row.pack(pady=(0, 10), padx=14, fill="x")

        tk.Label(label_row, text="Label (optional):", bg=CARD,
                 fg=MUTED, font=FONT_LABEL).pack(side="left")
        self.label_var = tk.StringVar(value="")
        tk.Entry(label_row, textvariable=self.label_var,
                 bg=BORDER, fg=TEXT, font=FONT_MONO, bd=0,
                 insertbackground=ACCENT, width=20).pack(side="left", padx=8, ipady=4)

        # Add Alarm button
        tk.Button(
            set_frame, text="＋  ADD ALARM",
            bg=ACCENT, fg="#000", font=FONT_BTN,
            bd=0, relief="flat", padx=14, pady=8,
            activebackground=ACCENT2, activeforeground=TEXT,
            cursor="hand2", command=self._add_alarm
        ).pack(pady=(4, 14))

        # Separator
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=6)

        # ── Alarm List ────────────────────────────────────────────────────────
        tk.Label(self.root, text="ACTIVE ALARMS", bg=BG, fg=MUTED,
                 font=FONT_LABEL).pack(anchor="w", padx=32)

        list_frame = tk.Frame(self.root, bg=CARD)
        list_frame.pack(padx=30, pady=6, fill="both", expand=True)

        self.alarm_listbox = tk.Listbox(
            list_frame, bg=CARD, fg=TEXT, font=FONT_MONO,
            selectbackground=ACCENT2, selectforeground=TEXT,
            bd=0, relief="flat", highlightthickness=0,
            activestyle="none", height=5
        )
        self.alarm_listbox.pack(fill="both", expand=True, padx=8, pady=8)

        btn_row = tk.Frame(list_frame, bg=CARD)
        btn_row.pack(fill="x", padx=8, pady=(0, 8))

        tk.Button(btn_row, text="🗑  DELETE", bg=BORDER, fg=RED,
                  font=FONT_LABEL, bd=0, relief="flat", padx=10, pady=5,
                  activebackground=RED, activeforeground=TEXT,
                  cursor="hand2", command=self._delete_alarm).pack(side="left", padx=4)

        tk.Button(btn_row, text="⏹  STOP ALARM", bg=BORDER, fg=TEXT,
                  font=FONT_LABEL, bd=0, relief="flat", padx=10, pady=5,
                  activebackground=BORDER, activeforeground=ACCENT,
                  cursor="hand2", command=self._stop_alarm).pack(side="right", padx=4)

        # Status bar
        self.status_var = tk.StringVar(value="Ready · No active alarm")
        tk.Label(self.root, textvariable=self.status_var,
                 bg=BG, fg=MUTED, font=FONT_LABEL).pack(pady=8)

    # ── Alarm Management ───────────────────────────────────────────────────────
    def _add_alarm(self):
        try:
            h = int(self.hour_var.get())
            m = int(self.minute_var.get())
            ampm = self.ampm_var.get()
            label = self.label_var.get().strip() or "Alarm"

            # Convert to 24h
            if ampm == "AM":
                if h == 12: h = 0
            else:
                if h != 12: h += 12

            alarm_time = f"{h:02d}:{m:02d}"
            alarms.append({"time": alarm_time, "label": label, "enabled": True})
            self._refresh_list()
            display = f"{self.hour_var.get()}:{self.minute_var.get()} {ampm}"
            self.status_var.set(f"✓ Alarm set for {display} — {label}")
        except ValueError:
            messagebox.showerror("Error", "Invalid time. Please enter a valid hour and minute.")

    def _delete_alarm(self):
        sel = self.alarm_listbox.curselection()
        if not sel:
            messagebox.showinfo("Select Alarm", "Please select an alarm to delete.")
            return
        idx = sel[0]
        del alarms[idx]
        self._refresh_list()
        self.status_var.set("Alarm deleted.")

    def _stop_alarm(self):
        stop_beep()
        self.status_var.set("Alarm stopped.")
        self.clock_label.config(fg=ACCENT)

    def _refresh_list(self):
        self.alarm_listbox.delete(0, tk.END)
        for a in alarms:
            h = int(a["time"].split(":")[0])
            m = int(a["time"].split(":")[1])
            ampm = "AM" if h < 12 else "PM"
            h12 = h % 12 or 12
            display = f"  {h12:02d}:{m:02d} {ampm}  —  {a['label']}"
            self.alarm_listbox.insert(tk.END, display)

    # ── Clock Tick ─────────────────────────────────────────────────────────────
    def _tick(self):
        now = datetime.datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%A, %d %B %Y"))
        self.root.after(1000, self._tick)

    # ── Alarm Checker ──────────────────────────────────────────────────────────
    def _check_alarms(self):
        now = datetime.datetime.now().strftime("%H:%M")
        for alarm in alarms:
            if alarm["enabled"] and alarm["time"] == now and not alarm_ringing:
                self.status_var.set(f"🔔 ALARM RINGING — {alarm['label']}!")
                self.clock_label.config(fg=RED)
                threading.Thread(target=play_beep, daemon=True).start()
                alarm["enabled"] = False  # ring once per set
                self._refresh_list()
                messagebox.showinfo("⏰ Alarm!", f"Time's up!\n\n{alarm['label']}")
                stop_beep()
                self.clock_label.config(fg=ACCENT)
                self.status_var.set("Ready · No active alarm")
        self.root.after(1000, self._check_alarms)


# ══════════════════════════════════════════════════════════════════════════════
#  Entry Point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = AlarmClockApp(root)
    root.mainloop()
