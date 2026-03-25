# ⏰ Simple Alarm Clock

A Python mini project featuring both a **GUI Alarm Clock** (Tkinter) and a **CLI Alarm Clock** — set multiple alarms, get audio alerts, and manage them easily.

---

## 🖥️ Two Versions Included

| File | Type | Description |
|---|---|---|
| `alarm_clock.py` | GUI (Tkinter) | Full graphical alarm clock with dark theme |
| `alarm_cli.py` | Terminal (CLI) | Lightweight command-line version |

---

## ✨ Features

### GUI Version (`alarm_clock.py`)
- 🕐 **Live digital clock** — updates every second
- ➕ **Set multiple alarms** with custom labels
- 🔢 **Hour/Minute spinners** with AM/PM toggle
- 🔔 **Audio alert** when alarm triggers (beep sound)
- 🗑️ **Delete alarms** from the list
- ⏹️ **Stop alarm** button
- 🌑 Clean dark-themed interface

### CLI Version (`alarm_cli.py`)
- ⚡ No GUI — runs directly in terminal
- 🕐 Live clock display in terminal
- 🔔 Alarm beep using `winsound` (Windows) or terminal bell
- 🔁 Set multiple alarms one after another
- ✅ Zero dependencies — pure Python standard library

---

## 🚀 How to Run

### ▶️ GUI Version
```bash
python alarm_clock.py
```

### ▶️ CLI Version (No install needed!)
```bash
python alarm_cli.py
```

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Aathithya975/Simple-Alarm-Clock-Project.git
cd Simple-Alarm-Clock-Project

# (Optional) Install pygame for better audio in GUI version
pip install pygame

# Run GUI version
python alarm_clock.py

# OR run CLI version (no install needed)
python alarm_cli.py
```

---

## 🗂️ Project Structure

```
Simple-Alarm-Clock-Project/
├── alarm_clock.py     # GUI version — Tkinter dark theme
├── alarm_cli.py       # CLI version — terminal only
├── requirements.txt   # Optional dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| Tkinter | GUI interface (built-in) |
| threading | Non-blocking alarm checker |
| datetime | Time tracking |
| winsound | Windows alarm beep (built-in) |
| pygame *(optional)* | Better audio support |

---

## 📌 How It Works

1. User enters alarm time (HH:MM) and an optional label
2. A background thread checks the current time every second
3. When current time matches alarm time → audio alert triggers
4. User clicks "Stop Alarm" or presses Enter (CLI) to dismiss

---

## 👨‍💻 Author

Built as a Python mini project to learn **Tkinter GUI**, **threading**, and **datetime** handling.

---

## 📄 License

MIT License
