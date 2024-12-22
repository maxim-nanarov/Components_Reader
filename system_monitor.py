import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import signal
import sys

def update_usage():
    cpu_usage_per_core = psutil.cpu_percent(interval=0, percpu=True)
    cpu_usage = sum(cpu_usage_per_core)
    ram_usage = psutil.virtual_memory().percent

    cpu_label.config(text=f"CPU: {cpu_usage}%")
    ram_label.config(text=f"RAM: {ram_usage}%")

    ax1.clear()
    ax2.clear()

    draw_gauge(ax1, cpu_usage, 'CPU Usage')
    draw_gauge(ax2, ram_usage, 'RAM Usage')

    canvas.draw()

    root.after(1000, update_usage)

def draw_gauge(ax, value, title):
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')

    # Draw the semi-circle background
    theta = np.linspace(np.pi, 0 * np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.fill_between(x, y, color='#333333', edgecolor='lightblue', linewidth=2)

    # Draw the glow effect
    for i in range(10, 0, -1):
        ax.fill_between(x * (1 + i * 0.01), y * (1 + i * 0.01), color='lightblue', alpha=0.1)

    # Draw the percentage text
    ax.text(0, -0.3, f'{value}%', horizontalalignment='center', verticalalignment='center', fontsize=20, fontweight='bold', color='lightblue')

    # Draw the title
    ax.text(0, -0.7, title, horizontalalignment='center', verticalalignment='center', fontsize=12, color='lightblue')

    # Draw the needle
    angle = np.deg2rad(180 * (value / 100))
    ax.plot([0, np.cos(angle)], [0, np.sin(angle)], color='lightblue', lw=3)

    # Draw markers every 25%
    for i in range(5):
        angle = np.deg2rad(180 * (i * 25 / 100))
        ax.plot([0.9 * np.cos(angle), 1.1 * np.cos(angle)], [0.9 * np.sin(angle), 1.1 * np.sin(angle)], color='lightblue', lw=2)
        ax.text(1.2 * np.cos(angle), 1.2 * np.sin(angle), f'{i * 25}%', horizontalalignment='center', verticalalignment='center', fontsize=10, color='lightblue')

def signal_handler(sig, frame):
    print("Exiting gracefully...")
    root.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

root = tk.Tk()
root.title("System Monitor")
root.geometry("600x400")
root.configure(bg='#333333')

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 16), background='#333333', foreground='lightblue')
style.configure("TFrame", background="#333333")

frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

cpu_label = ttk.Label(frame, text="CPU: 0%", style="TLabel")
cpu_label.pack(pady=10)

ram_label = ttk.Label(frame, text="RAM: 0%", style="TLabel")
ram_label.pack(pady=10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
fig.patch.set_facecolor('#333333')
fig.tight_layout(pad=3.0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

update_usage()

root.mainloop()