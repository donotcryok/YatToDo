# main.py
import tkinter as tk
import os
import sys
from ui import ToDoAppUI

def resource_path(relative_path):
    """获取资源的绝对路径，用于在开发和PyInstaller的打包环境中都能找到资源文件"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    root = tk.Tk()
    root.title("ToDo任务列表应用 - （Ctrl+F查找 | 支持排序）")
    root.geometry("600x500")  # 增加窗口大小
    root.minsize(500, 400)  # 设置最小窗口大小
    root.resizable(True, True)  # 允许调整窗口大小
    
    # 设置窗口图标
    try:
        # 尝试设置图标 - 如果有图标文件
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except tk.TclError:
        pass
    
    # 设置窗口在屏幕中央显示
    window_width = 600
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    # 创建应用实例
    app = ToDoAppUI(root)
    
    # 程序关闭前的确认
    def on_closing():
        if len(app.tasks) > 0:
            if tk.messagebox.askyesno("确认", "是否要退出应用？\n您的数据已自动保存。"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()