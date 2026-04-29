import tkinter as tk
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener
import threading
import time

mouse = Controller()

clicking = False
cps = 20  # höherer Startwert

def click_loop():
    global clicking, cps
    while True:
        if clicking:
            interval = 1.0 / cps
            next_click = time.perf_counter()

            while clicking:
                mouse.click(Button.left, 1)
                next_click += interval
                sleep_time = next_click - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)
        else:
            time.sleep(0.01)

def on_press(key):
    global clicking
    try:
        if key.char == '#':
            clicking = not clicking
            update_status()
            time.sleep(0.2)
    except:
        pass

def update_status():
    if clicking:
        status_label.config(text="STATUS: AN", fg="#00ff88")
    else:
        status_label.config(text="STATUS: AUS", fg="#ff4444")

def update_cps(val):
    global cps
    cps = int(float(val))
    cps_label.config(text=f"CPS: {cps}")

# Threads
threading.Thread(target=click_loop, daemon=True).start()
threading.Thread(target=lambda: Listener(on_press=on_press).run(), daemon=True).start()

# GUI
root = tk.Tk()
root.title("pro autoclicker by rajonaise")
root.geometry("320x220")
root.configure(bg="#0f0f0f")

frame = tk.Frame(root, bg="#0f0f0f")
frame.pack(expand=True)

title = tk.Label(frame, text="pro autoclicker by rajonaise",
                 fg="white", bg="#0f0f0f", font=("Segoe UI", 14))
title.pack(pady=10)

status_label = tk.Label(frame, text="STATUS: AUS",
                        fg="#ff4444", bg="#0f0f0f")
status_label.pack(pady=5)

cps_label = tk.Label(frame, text="CPS: 20",
                     fg="white", bg="#0f0f0f")
cps_label.pack()

slider = tk.Scale(frame, from_=1, to=200, orient="horizontal",
                  command=update_cps, bg="#0f0f0f", fg="white",
                  highlightthickness=0, troughcolor="#222",
                  activebackground="#00ff88")
slider.set(20)
slider.pack(pady=10)

info = tk.Label(frame, text="Toggle mit #",
                fg="#888", bg="#0f0f0f")
info.pack(pady=5)

root.mainloop()