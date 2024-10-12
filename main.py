import tkinter as tk
from tkinter import messagebox, filedialog
import win32gui  # type: ignore
import win32con  # type: ignore
import win32api  # type: ignore
import subprocess
import json
import os

# 文件路径保存文件
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "护肝小助手配置.json")

script_running = False
fight_number = 0
xuanshang_number = 0

def find_windows_by_title(title):
    hwnds = []
    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
    win32gui.EnumWindows(enum_windows_callback, None)
    return hwnds

def set_game_window_width(width, gap):
    hwnds = find_windows_by_title("阴阳师-网易游戏")
    if hwnds:
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        total_width = width * len(hwnds) + gap * (len(hwnds) - 1)
        x = (screen_width - total_width) // 2
        for hwnd in hwnds:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, 0, width, win32gui.GetWindowRect(hwnd)[3] - win32gui.GetWindowRect(hwnd)[1], win32con.SWP_NOZORDER)
            x += width + gap
    else:
        messagebox.showerror("错误", "未找到游戏窗口")

def on_submit():
    try:
        width = int(entry_width.get())
        gap = int(entry_gap.get())
        set_game_window_width(width, gap)
        update_preset_widths(width)
        save_config({"width": width, "gap": gap, "last_path": entry_file_path.get(), "width1": preset_width1, "width2": preset_width2})
    except ValueError:
        messagebox.showerror("错误", "请输入有效的宽度和间隙")

def select_file_path():
    initial_dir = os.path.dirname(entry_file_path.get()) if entry_file_path.get() else os.getcwd()
    file_path = filedialog.askopenfilename(title="选择文件", initialdir=initial_dir)
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)
        save_config({"last_path": file_path, "width": entry_width.get(), "gap": entry_gap.get(), "width1": preset_width1, "width2": preset_width2})

def open_multiple_instances():
    file_path = entry_file_path.get()
    if file_path:
        subprocess.Popen([file_path])
    else:
        messagebox.showerror("错误", "请先选择文件路径")

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

def update_preset_widths(new_width):
    global preset_width1, preset_width2
    if new_width != preset_width1 and new_width != preset_width2:
        preset_width2 = preset_width1
        preset_width1 = new_width

def set_preset_width(width):
    entry_width.delete(0, tk.END)
    entry_width.insert(0, width)

# 创建主窗口
root = tk.Tk()
root.title("痒痒鼠护肝小助手Demo版")
window_width = 450
window_height = 280
root.after(0, center_window, root, window_width, window_height)

# 加载配置
config = load_config()
last_path = config.get("last_path", "")
last_width = config.get("width", "")
last_gap = config.get("gap", "")
preset_width1 = config.get("width1", "")
preset_width2 = config.get("width2", "")
last_window_title = config.get("last_window_title", "")

# 创建并放置文件路径选择框和按钮
tk.Label(root, text="V5路径:").grid(row=0, column=0, padx=10, pady=10)
entry_file_path = tk.Entry(root, width=20)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)
entry_file_path.insert(0, last_path)
select_file_button = tk.Button(root, text="...", command=select_file_path)
select_file_button.grid(row=0, column=2, padx=5, pady=10)

# 创建并放置多开按钮
multi_open_button = tk.Button(root, text="打开V5", command=open_multiple_instances)
multi_open_button.grid(row=0, column=3, padx=5, pady=10)

# 创建并放置标签和输入框
tk.Label(root, text="宽度:").grid(row=1, column=0, padx=10, pady=10)
entry_width = tk.Entry(root)
entry_width.grid(row=1, column=1, padx=10, pady=10)
entry_width.insert(0, last_width)

# 创建并放置预设宽度按钮
preset_button1 = tk.Button(root, text=str(preset_width1), command=lambda: set_preset_width(preset_width1))
preset_button1.grid(row=1, column=2, padx=5, pady=10)
preset_button2 = tk.Button(root, text=str(preset_width2), command=lambda: set_preset_width(preset_width2))
preset_button2.grid(row=1, column=3, padx=5, pady=10)

tk.Label(root, text="间隙:").grid(row=2, column=0, padx=10, pady=10)
entry_gap = tk.Entry(root)
entry_gap.grid(row=2, column=1, padx=10, pady=10)
entry_gap.insert(0, last_gap)

# 创建并排序窗口
submit_button = tk.Button(root, text="排列窗口", command=on_submit)
submit_button.grid(row=2, column=2,columnspan=5, pady=10)

# 运行主循环
root.mainloop()