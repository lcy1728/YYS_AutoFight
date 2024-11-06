import os
import pyautogui
import cv2
import numpy as np
import time
import win32gui
import win32con
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import random
import threading
from functools import partial
import sys

script_running = False
fight_number = 0
xuanshang_number = 0
start_fail_number_1 = 0
start_fail_number_2 = 0
end_fail_number_2 = 0
end_fail_number_1 = 0
quit_fail_number_1 = 0
quit_fail_number_2 = 0

def center_window(root, width, height):
    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 计算窗口左上角的坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    # 设置窗口位置
    root.geometry(f'{width}x{height}+{x}+{y}')

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def activate_client_window(window_title, width=None, height=None):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        
        # 如果指定了宽度和高度，则调整窗口大小
        if width is not None and height is not None:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, width, height, win32con.SWP_NOZORDER)
        
        return True
    else:
        return False

def is_color_similar(image1, image2, threshold=30):
    # 计算两个图像的平均颜色
    mean_color1 = np.mean(image1, axis=(0, 1))
    mean_color2 = np.mean(image2, axis=(0, 1))
    
    # 计算颜色差异
    color_diff = np.linalg.norm(mean_color1 - mean_color2)
    
    # 判断颜色差异是否在阈值范围内
    return color_diff < threshold

def find_and_click_image(window_title, target_image_path, confidence=0.9):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        messagebox.showerror("错误", f"未找到窗口: {window_title}")
        return False
    
    rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    if target_image is None:
        messagebox.showerror("错误", f"无法加载目标图像: {target_image_path}")
        return False

    if screenshot.dtype != target_image.dtype:
        messagebox.showerror("错误", "截图和目标图像的数据类型不匹配")
        return False

    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        target_height, target_width = target_image.shape[:2]
        center_x = max_loc[0] + target_width // 2 + rect[0]
        center_y = max_loc[1] + target_height // 2 + rect[1]

        # 提取匹配区域
        matched_region = screenshot[max_loc[1]:max_loc[1]+target_height, max_loc[0]:max_loc[0]+target_width]

        # 检查颜色相似度
        if is_color_similar(matched_region, target_image):
            random_offset_x = random.randint(-target_width // 4, target_width // 4)
            random_offset_y = random.randint(-target_height // 4, target_height // 4)

            if os.path.basename(target_image_path) == 'guibing_jieshu_2.png':
                print("find guibing_jieshu_2.png,waiting 3s")
                rd_time = 3
            else:
                rd_time = random.uniform(1, 3)

            time.sleep(rd_time)

            screenshot = ImageGrab.grab(bbox=rect)
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= confidence:
                pyautogui.moveTo(center_x + random_offset_x, center_y + random_offset_y)
                pyautogui.click()
                return True
    return False


def find_and_move(window_title, target_image_path, confidence=0.9):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        messagebox.showerror("错误", f"未找到窗口: {window_title}")
        return False
    
    rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    if target_image is None:
        messagebox.showerror("错误", f"无法加载目标图像: {target_image_path}")
        return False

    if screenshot.dtype != target_image.dtype:
        messagebox.showerror("错误", "截图和目标图像的数据类型不匹配")
        return False

    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        target_height, target_width = target_image.shape[:2]
        bottom_right_x = max_loc[0] + target_width + rect[0]
        bottom_right_y = max_loc[1] + target_height + rect[1]

        # 提取匹配区域
        matched_region = screenshot[max_loc[1]:max_loc[1]+target_height, max_loc[0]:max_loc[0]+target_width]

        # 检查颜色相似度
        if is_color_similar(matched_region, target_image):
            rd_time = random.uniform(1, 2)
            rd_move = random.randint(5, 10)

            time.sleep(rd_time)
            pyautogui.moveTo(bottom_right_x + rd_move, bottom_right_y + rd_move)

            pyautogui.click()
            return True

    return False


def find_and_quick_click(window_title, target_image_path, confidence=0.9):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        messagebox.showerror("错误", f"未找到窗口: {window_title}")
        return False
    
    rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    if target_image is None:
        messagebox.showerror("错误", f"无法加载目标图像: {target_image_path}")
        return False

    if screenshot.dtype != target_image.dtype:
        messagebox.showerror("错误", "截图和目标图像的数据类型不匹配")
        return False

    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        target_height, target_width = target_image.shape[:2]
        center_x = max_loc[0] + target_width // 2 + rect[0]
        center_y = max_loc[1] + target_height // 2 + rect[1]
        

        # 提取匹配区域
        matched_region = screenshot[max_loc[1]:max_loc[1]+target_height, max_loc[0]:max_loc[0]+target_width]

        # 检查颜色相似度
        if is_color_similar(matched_region, target_image):
            random_offset_x = random.randint(-target_width // 4, target_width // 4)
            random_offset_y = random.randint(-target_height // 4, target_height // 4)
            pyautogui.moveTo(center_x + random_offset_x, center_y + random_offset_y)
            pyautogui.click()
            return True

    return False

def find_and_not_click(window_title, target_image_path, confidence=0.9):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        messagebox.showerror("错误", f"未找到窗口: {window_title}")
        return False
    
    rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    if target_image is None:
        messagebox.showerror("错误", f"无法加载目标图像: {target_image_path}")
        return False

    if screenshot.dtype != target_image.dtype:
        messagebox.showerror("错误", "截图和目标图像的数据类型不匹配")
        return False

    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        target_height, target_width = target_image.shape[:2]
        center_x = max_loc[0] + target_width // 2 + rect[0]
        center_y = max_loc[1] + target_height // 2 + rect[1]
        

        # 提取匹配区域
        matched_region = screenshot[max_loc[1]:max_loc[1]+target_height, max_loc[0]:max_loc[0]+target_width]

        # 检查颜色相似度
        if is_color_similar(matched_region, target_image):
            return True

    return False

def find_game_window():
    client_window_title = entry_window_title.get()

    if not client_window_title:
        messagebox.showerror("错误", "请填写所有字段")
        return

    if activate_client_window(client_window_title, width=807, height=490):
        messagebox.showinfo("信息", "窗口已找到并调整大小，开始执行脚本")
    else:
        messagebox.showerror("错误", f"未找到窗口: {client_window_title}")

def start_script(target_function, *args, **kwargs):
    global script_running
    if script_running:
        return
    script_running = True
    script_thread = threading.Thread(target=target_function, args=args, kwargs=kwargs)
    script_thread.start()

def run_script(start_image, end_image1, end_image2 , other_image):
    global fight_number
    global xuanshang_number
    global start_fail_number_1
    global end_fail_number_2
    global end_fail_number_1
    global script_running  # 确保在此函数中使用全局变量

    # 使用 get_resource_path 函数获取资源文件的完整路径
    start = get_resource_path(os.path.join('resources', start_image))
    end1 = get_resource_path(os.path.join('resources', end_image1))
    end2 = get_resource_path(os.path.join('resources', end_image2))
    other = get_resource_path(os.path.join('resources', other_image))
    
    while script_running:  # 检查 script_running 的状态
        fight_end_num()

        if not script_running:  # 如果 script_running 被设置为 False，立即退出循环
            break

        if find_and_click_image(entry_window_title.get(), other):
            xuanshang_number += 1
            print("拒绝悬赏")
            time.sleep(1)

        if not script_running:
            break

        if find_and_click_image(entry_window_title.get(), start):
            print("\n点击挑战")
            end_fail_number_1 = 0
            end_fail_number_2 = 0
            start_fail_number_1 += 1
            fight_number += 1
            print(f"挑战次数:{fight_number}")
            time.sleep(3)

        if not script_running:
            break

        if find_and_click_image(entry_window_title.get(), end1):
            start_fail_number_1 = 0
            end_fail_number_2 = 0
            end_fail_number_1 += 1
            print(f"结束页面1   点击次数：{end_fail_number_1}")
            time.sleep(1)

        if find_and_click_image(entry_window_title.get(), end2):
            end_fail_number_1 = 0
            end_fail_number_2 += 1
            print(f"结束页面2   点击次数：{end_fail_number_2}")
            time.sleep(1)

def run_28_script(start_image1,start_image2,move_image,end_image1,quit1_image1,quit2_image1,other_image):
    global fight_number
    global xuanshang_number
    global start_fail_number_1
    global start_fail_number_2
    global end_fail_number_1
    global quit_fail_number_1
    global quit_fail_number_2
    global script_running  # 确保在此函数中使用全局变量 

    # 使用 get_resource_path 函数获取资源文件的完整路径
    start1 = get_resource_path(os.path.join('resources', start_image1))
    start2 = get_resource_path(os.path.join('resources', start_image2))
    move = get_resource_path(os.path.join('resources', move_image))
    end1 = get_resource_path(os.path.join('resources', end_image1))
    quit1 = get_resource_path(os.path.join('resources', quit1_image1))
    quit2 = get_resource_path(os.path.join('resources', quit2_image1))
    other = get_resource_path(os.path.join('resources', other_image))

    while script_running:  # 检查 script_running 的状态
        fight_end_num()
        
        if not script_running:  # 如果 script_running 被设置为 False，立即退出循环
            break

        if find_and_click_image(entry_window_title.get(), other):
            xuanshang_number += 1
            print("拒绝悬赏")

        if find_and_click_image(entry_window_title.get(),start1):
            print("\n开始探索")
            start_fail_number_1 += 1
            time.sleep(3)
            if find_and_move(entry_window_title.get(), move):
                start_fail_number_1 = 0
                print("点击移动")
                time.sleep(5)

        if find_and_quick_click(entry_window_title.get(), start2):
            start_fail_number_1 = 0
            end_fail_number_1 = 0
            start_fail_number_2 += 1
            fight_number += 1
            print(f"\n挑战,挑战次数:{fight_number}")
            time.sleep(1)

        if find_and_click_image(entry_window_title.get(), end1):
            print("结束")
            start_fail_number_2 = 0
            end_fail_number_1 += 1
            time.sleep(3)

            if not find_and_not_click(entry_window_title.get(), start2):
                if find_and_click_image(entry_window_title.get(), quit1):
                    end_fail_number_1 = 0
                    quit_fail_number_1 += 1
                    print("无怪物,点击退出")
                    time.sleep(1)
                    if find_and_click_image(entry_window_title.get(), quit2):
                        quit_fail_number_2 += 1
                        print("退出")
                        time.sleep(3)


def fight_end_num():
    global fight_number
    global start_fail_number_1
    global start_fail_number_2
    global end_fail_number_1
    global end_fail_number_2
    global quit_fail_number_1
    global quit_fail_number_2

    end_num =int(yuling_num.get())
    if not end_num:
        messagebox.showerror("错误", "请在挑战次数文本框中输入数字")
        return

    if fight_number == end_num:
        stop_script()

    if start_fail_number_1 == 3 or start_fail_number_2 == 3 or end_fail_number_1 == 3 or end_fail_number_2 == 3 or quit_fail_number_1 == 3 or quit_fail_number_2 == 3:
        stop_script()
        messagebox.showerror("错误","连续点击三次,脚本停止")


def stop_script():
    global script_running
    global fight_number
    script_running = False
    messagebox.showinfo("挑战结束", f"挑战次数: {fight_number}\n拒绝悬赏次数: {xuanshang_number}")
    fight_number = 0

# 创建主窗口
root = tk.Tk()
root.title("痒痒鼠护肝小助手")
# 设置窗口大小
window_width = 400
window_height = 200
# 使用 after 方法在窗口显示后设置窗口位置
root.after(0, center_window, root, window_width, window_height)

# 创建并放置窗口标题输入框和标签
tk.Label(root, text="客户端窗口标题:").grid(row=0, column=0, padx=10, pady=10)
entry_window_title = tk.Entry(root, width=20)
entry_window_title.grid(row=0, column=1, padx=20, pady=10)

# 创建并放置开始按钮
start_button = tk.Button(root, text="查找窗口", command=find_game_window)
start_button.grid(row=0, column=2, columnspan=2, pady=10)

# 挑战次数
tk.Label(root, text="挑战次数:").grid(row=2, column=0, padx=10, pady=10)
yuling_num = tk.Entry(root, width=20)
yuling_num.grid(row=2, column=1, padx=20, pady=10)

# 创建停止按钮
stop_yulin = tk.Button(root, text="停止战斗", command=stop_script)
stop_yulin.grid(row=2, column=2, pady=10)

# 创建御灵按钮
start_yulin = tk.Button(root, text="御灵挑战", command=partial(start_script, run_script, 'yulin_tiaozhan.png','yulin_jieshu.png','huntu_jieshu_2000.png','xuanshang_jvjue.png'))
start_yulin.grid(row=3, column=0, pady=10)

# 创建爬塔按钮
start_pata = tk.Button(root, text="活动挑战", command=partial(start_script, run_script, 'huodong_tiaozhan.png','huodong_jieshu_1.png','huodong_jieshu_2.png','xuanshang_jvjue.png'))
start_pata.grid(row=3, column=1, pady=10)

# 创建活动按钮
start_guibing = tk.Button(root, text="鬼兵演武", command=partial(start_script, run_script, 'guibing_tiaozhan.png','guibing_jieshu.png','guibing_jieshu_2.png','xuanshang_jvjue.png'))
start_guibing.grid(row=3, column=2, pady=10)

# 创建魂土组队按钮
start_huntu = tk.Button(root, text="魂土组队", command=partial(start_script, run_script, 'siji_tiaozhan.png','siji_jieshu_1.png','siji_jieshu_2.png','xuanshang_jvjue.png'))
start_huntu.grid(row=4, column=0, pady=10)

# 创建魂王组队按钮
start_hunwang = tk.Button(root, text="魂王组队", command=partial(start_script, run_script, 'siji_tiaozhan.png','hunwang_jieshu_1.png','hunwang_jieshu_2.png','xuanshang_jvjue.png'))
start_hunwang.grid(row=4, column=1, pady=10)

# 困难28按钮
start_28 = tk.Button(root, text="困难28",command=partial(start_script, run_28_script,'tansuo_tansuo.png','tansuo_start.png','tansuo_yidong.png','tansuo_jieshu.png','tansuo_tuichu_1.png','tansuo_tuichu_2.png','xuanshang_jvjue.png'))
start_28.grid(row=4, column=2, pady=10)

# 运行主循环
root.mainloop()