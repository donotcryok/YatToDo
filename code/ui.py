# ui.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry  # 需要安装: pip install tkcalendar
import datetime
from functions import add_task, delete_task, modify_task
from data import save_tasks, load_tasks, export_tasks_as_text, backup_tasks

class ToDoAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo任务列表应用")
        
        # 主题设置
        self.theme_color = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#e0e0e0",
                "highlight_bg": "#4CAF50",
                "listbox_bg": "#ffffff",
                "completed_fg": "#a0a0a0"
            },
            "dark": {
                "bg": "#2c2c2c",
                "fg": "#ffffff",
                "button_bg": "#3c3c3c",
                "highlight_bg": "#388E3C",
                "listbox_bg": "#383838",
                "completed_fg": "#808080"
            }
        }
        self.current_theme = "light"
        
        # 创建菜单栏
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        # 文件菜单
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="导出为文本", command=self.export_as_text)
        self.file_menu.add_command(label="备份数据", command=self.backup_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=root.quit)
        
        # 编辑菜单
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)
        self.edit_menu.add_command(label="查找", command=self.open_search_dialog)
        
        # 视图菜单 - 添加排序选项
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="视图", menu=self.view_menu)
        
        # 排序子菜单
        self.sort_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="排序方式", menu=self.sort_menu)
        
        # 排序选项
        self.sort_menu.add_command(label="按优先级（高→低）", command=lambda: self.sort_tasks("priority", False))
        self.sort_menu.add_command(label="按优先级（低→高）", command=lambda: self.sort_tasks("priority", True))
        self.sort_menu.add_command(label="按截止日期（近→远）", command=lambda: self.sort_tasks("date", False))
        self.sort_menu.add_command(label="按截止日期（远→近）", command=lambda: self.sort_tasks("date", True))
        self.sort_menu.add_separator()
        self.sort_menu.add_command(label="不排序（按添加顺序）", command=lambda: self.sort_tasks("none", False))
        
        # 设置菜单
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="设置", menu=self.settings_menu)
        self.settings_menu.add_command(label="切换主题", command=self.toggle_theme)
        self.settings_menu.add_command(label="设置", command=self.open_settings)
        
        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题标签
        self.title_label = tk.Label(self.main_frame, text="ToDo任务管理器", font=("黑体", 14, "bold"))
        self.title_label.pack(pady=5)
        
        # 创建任务输入框架
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=5)
        
        # 输入框标签
        self.entry_label = tk.Label(self.input_frame, text="任务内容:")
        self.entry_label.pack(side=tk.LEFT, padx=5)
        
        # 输入框
        self.entry = tk.Entry(self.input_frame, width=30)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda event: self.on_add_task())
        
        # 任务优先级
        self.priority_label = tk.Label(self.input_frame, text="优先级:")
        self.priority_label.pack(side=tk.LEFT, padx=5)
        
        self.priority_var = tk.StringVar()
        self.priority_var.set("中")
        self.priority_options = ttk.Combobox(self.input_frame, textvariable=self.priority_var, 
                                           values=["高", "中", "低"], width=5, state="readonly")
        self.priority_options.pack(side=tk.LEFT, padx=5)
        
        # 截止日期
        self.date_label = tk.Label(self.input_frame, text="截止日期:")
        self.date_label.pack(side=tk.LEFT, padx=5)
        
        self.date_picker = DateEntry(self.input_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(side=tk.LEFT, padx=5)
        
        # 按钮框架
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 添加任务按钮
        self.add_button = tk.Button(self.button_frame, text="添加任务", command=self.on_add_task,
                                  bg="#4CAF50", fg="white", width=10)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        # 删除任务按钮
        self.delete_button = tk.Button(self.button_frame, text="删除任务", command=self.on_delete_task,
                                    bg="#F44336", fg="white", width=10)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # 修改任务按钮
        self.modify_button = tk.Button(self.button_frame, text="修改任务", command=self.on_modify_task,
                                    bg="#2196F3", fg="white", width=10)
        self.modify_button.pack(side=tk.LEFT, padx=5)
        
        # 完成任务按钮
        self.complete_button = tk.Button(self.button_frame, text="标记完成", command=self.on_complete_task,
                                      bg="#FF9800", fg="white", width=10)
        self.complete_button.pack(side=tk.LEFT, padx=5)
        
        # 过滤框架
        self.filter_frame = tk.Frame(self.main_frame)
        self.filter_frame.pack(fill=tk.X, pady=5)
        
        self.filter_label = tk.Label(self.filter_frame, text="过滤：")
        self.filter_label.pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="全部")
        self.filter_all = tk.Radiobutton(self.filter_frame, text="全部", variable=self.filter_var, 
                                       value="全部", command=self.apply_filter)
        self.filter_all.pack(side=tk.LEFT, padx=5)
        
        self.filter_active = tk.Radiobutton(self.filter_frame, text="未完成", variable=self.filter_var,
                                          value="未完成", command=self.apply_filter)
        self.filter_active.pack(side=tk.LEFT, padx=5)
        
        self.filter_completed = tk.Radiobutton(self.filter_frame, text="已完成", variable=self.filter_var,
                                             value="已完成", command=self.apply_filter)
        self.filter_completed.pack(side=tk.LEFT, padx=5)
        
        self.filter_priority = tk.Radiobutton(self.filter_frame, text="按优先级", variable=self.filter_var,
                                            value="优先级", command=self.apply_filter)
        self.filter_priority.pack(side=tk.LEFT, padx=5)
        
        self.priority_filter_var = tk.StringVar(value="高")
        self.priority_filter = ttk.Combobox(self.filter_frame, textvariable=self.priority_filter_var, 
                                          values=["高", "中", "低"], width=5, state="readonly")
        self.priority_filter.pack(side=tk.LEFT, padx=5)
        self.priority_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        # 排序框架 - 在过滤框架下方添加
        self.sort_frame = tk.Frame(self.main_frame)
        self.sort_frame.pack(fill=tk.X, pady=2)
        
        self.sort_label = tk.Label(self.sort_frame, text="排序：")
        self.sort_label.pack(side=tk.LEFT, padx=5)
        
        # 排序按钮
        self.sort_priority_asc_btn = tk.Button(self.sort_frame, text="优先级↑", 
                                             command=lambda: self.sort_tasks("priority", False),
                                             width=8)
        self.sort_priority_asc_btn.pack(side=tk.LEFT, padx=2)
        
        self.sort_priority_desc_btn = tk.Button(self.sort_frame, text="优先级↓", 
                                              command=lambda: self.sort_tasks("priority", True),
                                              width=8)
        self.sort_priority_desc_btn.pack(side=tk.LEFT, padx=2)
        
        self.sort_date_asc_btn = tk.Button(self.sort_frame, text="日期↑", 
                                         command=lambda: self.sort_tasks("date", False),
                                         width=8)
        self.sort_date_asc_btn.pack(side=tk.LEFT, padx=2)
        
        self.sort_date_desc_btn = tk.Button(self.sort_frame, text="日期↓", 
                                          command=lambda: self.sort_tasks("date", True),
                                          width=8)
        self.sort_date_desc_btn.pack(side=tk.LEFT, padx=2)
        
        # 当前排序方式
        self.current_sort = ("none", False)  # (sort_type, reverse)
        
        # 任务列表框架
        self.list_frame = tk.Frame(self.main_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 任务列表和滚动条
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.list_frame, width=50, height=10, 
                                yscrollcommand=self.scrollbar.set,
                                font=("微软雅黑", 10),
                                selectbackground="#a6a6a6",
                                activestyle="none")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        
        # 双击事件绑定
        self.listbox.bind("<Double-1>", self.on_task_double_click)
        
        # 状态栏
        self.status_frame = tk.Frame(self.main_frame, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(self.status_frame, text="就绪 | 总任务数: 0", anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # 加载保存的任务
        self.tasks = load_tasks()
        self.filtered_tasks = self.tasks.copy()  # 用于过滤显示
        self.reload_tasks()
        
        # 应用主题
        self.apply_theme()
        
        # 添加快捷键绑定
        self.root.bind("<Control-f>", lambda event: self.open_search_dialog())
    
    def reload_tasks(self):
        """重新加载任务列表到UI"""
        self.listbox.delete(0, tk.END)
        for task in self.filtered_tasks:
            self._display_task(task)
        self._update_status()
    
    def _display_task(self, task):
        """将任务显示在列表中，带有优先级和完成状态标记"""
        priority = task.get("priority", "中")
        completed = task.get("completed", False)
        text = task.get("text", "")
        due_date = task.get("due_date", "")
        
        display_text = f"[{priority}] {text}"
        if due_date:
            display_text += f" (截止: {due_date})"
        
        if completed:
            display_text = f"✓ {display_text}"
        
        self.listbox.insert(tk.END, display_text)
        
        # 如果完成则设置样式
        if completed:
            idx = self.listbox.size() - 1
            self.listbox.itemconfig(idx, fg=self.theme_color[self.current_theme]["completed_fg"])
        
        # 如果已过期且未完成，标红显示
        if due_date and not completed:
            try:
                due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
                today = datetime.date.today()
                if due_date_obj < today:
                    idx = self.listbox.size() - 1
                    self.listbox.itemconfig(idx, fg="red")
            except:
                pass
    
    def _update_status(self):
        """更新状态栏信息"""
        total = len(self.tasks)
        displayed = len(self.filtered_tasks)
        completed = sum(1 for task in self.tasks if task.get("completed", False))
        
        status_text = f"就绪 | 总任务数: {total} | 显示中: {displayed} | 已完成: {completed}"
        
        # 如果有即将到期的任务，提醒用户
        today = datetime.date.today()
        upcoming = sum(1 for task in self.tasks 
                      if not task.get("completed", False) 
                      and task.get("due_date") 
                      and (today <= datetime.datetime.strptime(task.get("due_date"), "%Y-%m-%d").date() <= today + datetime.timedelta(days=3)))
        
        if upcoming > 0:
            status_text += f" | 近期截止: {upcoming}"
            
        self.status_label.config(text=status_text)
    
    def on_add_task(self):
        task = self.entry.get().strip()
        if task:
            priority = self.priority_var.get()
            due_date = self.date_picker.get() if self.date_picker.get_date() != datetime.date.today() else ""
            
            task_data = {
                "text": task,
                "priority": priority,
                "completed": False,
                "due_date": due_date
            }
            
            # 添加到数据
            self.tasks.append(task_data)
            save_tasks(self.tasks)
            
            # 应用过滤并更新界面
            self.apply_filter()
            self.entry.delete(0, tk.END)
        else:
            tk.messagebox.showwarning("警告", "任务不能为空！")
    
    def on_delete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            # 获取在过滤列表中的索引，转换为在完整任务列表中的索引
            task_to_delete = self.filtered_tasks[selected_task_index]
            original_index = self.tasks.index(task_to_delete)
            
            # 从两个列表中都删除
            del self.tasks[original_index]
            self.filtered_tasks.remove(task_to_delete)
            
            self.listbox.delete(selected_task_index)
            save_tasks(self.tasks)
            self._update_status()
        except IndexError:
            tk.messagebox.showwarning("警告", "请选择一个任务进行删除！")
    
    def on_modify_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            new_task = self.entry.get().strip()
            if new_task:
                # 获取在完整任务列表中的索引
                task_to_modify = self.filtered_tasks[selected_task_index]
                original_index = self.tasks.index(task_to_modify)
                
                # 保持原有的完成状态
                completed = self.tasks[original_index].get("completed", False)
                priority = self.priority_var.get()
                due_date = self.date_picker.get() if self.date_picker.get_date() != datetime.date.today() else ""
                
                # 更新任务
                self.tasks[original_index] = {
                    "text": new_task,
                    "priority": priority,
                    "completed": completed,
                    "due_date": due_date
                }
                
                # 如果任务仍然符合过滤条件，则更新显示
                self.filtered_tasks[selected_task_index] = self.tasks[original_index]
                self.listbox.delete(selected_task_index)
                self._display_task(self.tasks[original_index])
                
                save_tasks(self.tasks)
                self.entry.delete(0, tk.END)
                # 重新应用过滤
                self.apply_filter()
            else:
                tk.messagebox.showwarning("警告", "新任务不能为空！")
        except IndexError:
            tk.messagebox.showwarning("警告", "请选择一个任务进行修改！")
    
    def on_complete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            
            # 获取在完整任务列表中的索引
            task_to_complete = self.filtered_tasks[selected_task_index]
            original_index = self.tasks.index(task_to_complete)
            
            # 切换完成状态
            self.tasks[original_index]["completed"] = not self.tasks[original_index].get("completed", False)
            
            # 更新过滤任务列表
            self.filtered_tasks[selected_task_index] = self.tasks[original_index]
            
            # 更新显示
            self.listbox.delete(selected_task_index)
            self._display_task(self.tasks[original_index])
            
            save_tasks(self.tasks)
            
            # 重新应用过滤
            self.apply_filter()
        except IndexError:
            tk.messagebox.showwarning("警告", "请选择一个任务标记完成状态！")
    
    def on_task_double_click(self, event):
        """双击任务时的操作，显示任务详情或直接编辑"""
        try:
            selected_index = self.listbox.curselection()[0]
            task = self.filtered_tasks[selected_index]
            
            # 将任务信息填充到编辑区域
            self.entry.delete(0, tk.END)
            self.entry.insert(0, task["text"])
            self.priority_var.set(task["priority"])
            
            if task.get("due_date"):
                try:
                    due_date = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    self.date_picker.set_date(due_date)
                except:
                    pass
            else:
                self.date_picker.set_date(datetime.date.today())
                
        except IndexError:
            pass
    
    def apply_filter(self):
        """应用过滤条件"""
        filter_type = self.filter_var.get()
        
        if filter_type == "全部":
            self.filtered_tasks = self.tasks.copy()
        elif filter_type == "未完成":
            self.filtered_tasks = [task for task in self.tasks if not task.get("completed", False)]
        elif filter_type == "已完成":
            self.filtered_tasks = [task for task in self.tasks if task.get("completed", False)]
        elif filter_type == "优先级":
            priority = self.priority_filter_var.get()
            self.filtered_tasks = [task for task in self.tasks if task.get("priority") == priority]
        
        # 应用当前排序方式
        self.sort_tasks(self.current_sort[0], self.current_sort[1], refresh_ui=False)
        
        self.reload_tasks()
    
    def sort_tasks(self, sort_type, reverse=False, refresh_ui=True):
        """
        排序任务列表
        
        参数:
        - sort_type: 排序类型 ("priority", "date", "none")
        - reverse: 是否倒序
        - refresh_ui: 是否刷新界面
        """
        self.current_sort = (sort_type, reverse)
        
        if sort_type == "none":
            # 不做任何排序，保持原有顺序
            pass
        elif sort_type == "priority":
            # 优先级映射为数值，便于排序
            priority_map = {"高": 0, "中": 1, "低": 2}
            
            # 先按完成状态分组，未完成的在前，已完成的在后
            # 然后在每组内部按优先级排序
            self.filtered_tasks.sort(
                key=lambda t: (
                    t.get("completed", False),  # 完成状态（False排在前面）
                    priority_map.get(t.get("priority", "中"), 1)  # 优先级
                ),
                reverse=reverse
            )
        elif sort_type == "date":
            today = datetime.date.today()
            
            def get_date_value(task):
                # 完成的任务放在最后
                if task.get("completed", False):
                    return datetime.date.max
                
                # 没有截止日期的任务根据reverse决定位置
                if not task.get("due_date"):
                    return datetime.date.min if reverse else datetime.date.max
                
                # 有截止日期的按日期排序
                try:
                    return datetime.datetime.strptime(task.get("due_date"), "%Y-%m-%d").date()
                except:
                    return today
            
            self.filtered_tasks.sort(key=get_date_value, reverse=reverse)
        
        # 更新排序按钮样式
        self.update_sort_buttons()
        
        # 刷新界面
        if refresh_ui:
            self.reload_tasks()
    
    def update_sort_buttons(self):
        """更新排序按钮的样式，突出显示当前排序方式"""
        # 重置所有按钮样式
        buttons = [
            self.sort_priority_asc_btn, 
            self.sort_priority_desc_btn,
            self.sort_date_asc_btn,
            self.sort_date_desc_btn
        ]
        
        theme = self.theme_color[self.current_theme]
        for btn in buttons:
            btn.config(relief=tk.RAISED, bg=theme["button_bg"])
        
        # 设置当前排序按钮样式
        sort_type, reverse = self.current_sort
        if sort_type == "priority":
            btn = self.sort_priority_desc_btn if reverse else self.sort_priority_asc_btn
            btn.config(relief=tk.SUNKEN, bg=theme["highlight_bg"])
        elif sort_type == "date":
            btn = self.sort_date_desc_btn if reverse else self.sort_date_asc_btn
            btn.config(relief=tk.SUNKEN, bg=theme["highlight_bg"])
    
    def toggle_theme(self):
        """切换明暗主题"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
    
    def apply_theme(self):
        """应用当前主题"""
        theme = self.theme_color[self.current_theme]
        
        # 主背景色
        self.main_frame.config(bg=theme["bg"])
        self.input_frame.config(bg=theme["bg"])
        self.button_frame.config(bg=theme["bg"])
        self.filter_frame.config(bg=theme["bg"])
        self.sort_frame.config(bg=theme["bg"])  # 添加排序框架
        self.list_frame.config(bg=theme["bg"])
        
        # 标签颜色
        self.title_label.config(bg=theme["bg"], fg=theme["fg"])
        self.entry_label.config(bg=theme["bg"], fg=theme["fg"])
        self.priority_label.config(bg=theme["bg"], fg=theme["fg"])
        self.date_label.config(bg=theme["bg"], fg=theme["fg"])
        self.filter_label.config(bg=theme["bg"], fg=theme["fg"])
        self.sort_label.config(bg=theme["bg"], fg=theme["fg"])  # 添加排序标签
        self.status_label.config(bg=theme["bg"], fg=theme["fg"])
        
        # 单选按钮
        self.filter_all.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        self.filter_active.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        self.filter_completed.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        self.filter_priority.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        
        # 列表框
        self.listbox.config(bg=theme["listbox_bg"], fg=theme["fg"])
        
        # 排序按钮
        self.sort_priority_asc_btn.config(bg=theme["button_bg"], fg=theme["fg"])
        self.sort_priority_desc_btn.config(bg=theme["button_bg"], fg=theme["fg"])
        self.sort_date_asc_btn.config(bg=theme["button_bg"], fg=theme["fg"])
        self.sort_date_desc_btn.config(bg=theme["button_bg"], fg=theme["fg"])
        
        # 更新排序按钮样式
        self.update_sort_buttons()
        
        # 更新任务显示以应用完成任务的颜色
        self.reload_tasks()
    
    def export_as_text(self):
        """导出任务为文本文件"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="导出任务列表"
        )
        if filename:
            if export_tasks_as_text(self.tasks, filename):
                messagebox.showinfo("成功", "任务已成功导出为文本文件！")
            else:
                messagebox.showerror("错误", "导出任务失败！")
    
    def backup_data(self):
        """备份任务数据"""
        if backup_tasks(self.tasks):
            messagebox.showinfo("成功", "任务数据已成功备份！")
        else:
            messagebox.showerror("错误", "备份任务数据失败！")
    
    def open_settings(self):
        """打开设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)
        
        # 使设置窗口在父窗口上居中
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        settings_window.geometry(f"+{x}+{y}")
        
        # 防止与主窗口交互直到关闭设置窗口
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 设置面板内容
        settings_frame = tk.Frame(settings_window, padx=20, pady=20)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # 主题设置
        theme_label = tk.Label(settings_frame, text="主题:", anchor="w")
        theme_label.pack(fill=tk.X, pady=(0, 5))
        
        theme_var = tk.StringVar(value=self.current_theme)
        theme_light = tk.Radiobutton(settings_frame, text="浅色主题", variable=theme_var, value="light")
        theme_light.pack(anchor="w", padx=20)
        
        theme_dark = tk.Radiobutton(settings_frame, text="深色主题", variable=theme_var, value="dark")
        theme_dark.pack(anchor="w", padx=20, pady=(0, 10))
        
        # 自动备份设置
        backup_var = tk.BooleanVar(value=False)
        backup_check = tk.Checkbutton(settings_frame, text="退出时自动备份", variable=backup_var)
        backup_check.pack(anchor="w", pady=(10, 5))
        
        # 确定按钮
        def save_settings():
            self.current_theme = theme_var.get()
            self.apply_theme()
            settings_window.destroy()
        
        save_button = tk.Button(settings_frame, text="确定", command=save_settings, width=10)
        save_button.pack(pady=10)
        
        # 聚焦设置窗口
        settings_window.focus_set()
    
    def open_search_dialog(self):
        """打开查找对话框"""
        search_window = tk.Toplevel(self.root)
        search_window.title("查找任务")
        search_window.geometry("400x300")
        search_window.resizable(False, False)
        
        # 使搜索窗口在父窗口上居中
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        search_window.geometry(f"+{x}+{y}")
        
        # 防止与主窗口交互直到关闭搜索窗口
        search_window.transient(self.root)
        search_window.grab_set()
        
        # 搜索框架
        search_frame = tk.Frame(search_window, padx=10, pady=10)
        search_frame.pack(fill=tk.X)
        
        # 搜索标签和输入框
        search_label = tk.Label(search_frame, text="关键词:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.focus_set()  # 聚焦到搜索框
        
        # 搜索选项框架
        options_frame = tk.Frame(search_window, padx=10)
        options_frame.pack(fill=tk.X, pady=5)
        
        # 搜索范围选项
        search_scope_label = tk.Label(options_frame, text="搜索范围:")
        search_scope_label.pack(side=tk.LEFT, padx=5)
        
        scope_var = tk.StringVar(value="all")
        scope_all = tk.Radiobutton(options_frame, text="全部任务", variable=scope_var, value="all")
        scope_all.pack(side=tk.LEFT, padx=5)
        
        scope_active = tk.Radiobutton(options_frame, text="未完成", variable=scope_var, value="active")
        scope_active.pack(side=tk.LEFT, padx=5)
        
        scope_completed = tk.Radiobutton(options_frame, text="已完成", variable=scope_var, value="completed")
        scope_completed.pack(side=tk.LEFT, padx=5)
        
        # 区分大小写复选框
        case_sensitive_var = tk.BooleanVar(value=False)
        case_sensitive_check = tk.Checkbutton(search_window, text="区分大小写", variable=case_sensitive_var)
        case_sensitive_check.pack(anchor="w", padx=15, pady=5)
        
        # 结果框架
        results_frame = tk.Frame(search_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 结果列表和滚动条
        result_scrollbar = tk.Scrollbar(results_frame)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        result_listbox = tk.Listbox(results_frame, width=50, height=10, 
                                    yscrollcommand=result_scrollbar.set,
                                    font=("微软雅黑", 10),
                                    selectbackground="#a6a6a6")
        result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.config(command=result_listbox.yview)
        
        # 底部按钮框架
        button_frame = tk.Frame(search_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 搜索函数
        def perform_search():
            keyword = search_entry.get().strip()
            if not keyword:
                return
            
            # 清空之前的结果
            result_listbox.delete(0, tk.END)
            
            # 搜索逻辑
            scope = scope_var.get()
            case_sensitive = case_sensitive_var.get()
            
            # 确定要搜索的任务范围
            if scope == "all":
                search_tasks = self.tasks
            elif scope == "active":
                search_tasks = [t for t in self.tasks if not t.get("completed", False)]
            else:  # completed
                search_tasks = [t for t in self.tasks if t.get("completed", False)]
            
            # 执行搜索
            results = []
            for task in search_tasks:
                task_text = task.get("text", "")
                if not case_sensitive:
                    if keyword.lower() in task_text.lower():
                        results.append(task)
                else:
                    if keyword in task_text:
                        results.append(task)
            
            # 显示结果
            if results:
                for task in results:
                    priority = task.get("priority", "中")
                    completed = task.get("completed", False)
                    text = task.get("text", "")
                    due_date = task.get("due_date", "")
                    
                    display_text = f"[{priority}] {text}"
                    if due_date:
                        display_text += f" (截止: {due_date})"
                    if completed:
                        display_text = f"✓ {display_text}"
                    
                    result_listbox.insert(tk.END, display_text)
                    
                    # 设置完成任务的样式
                    if completed:
                        idx = result_listbox.size() - 1
                        result_listbox.itemconfig(idx, fg="gray")
                
                status_label.config(text=f"找到 {len(results)} 个匹配项")
            else:
                result_listbox.insert(tk.END, "没有找到匹配的任务")
                status_label.config(text="没有找到匹配的任务")
        
        # 跳转到任务
        def go_to_task():
            try:
                selected_idx = result_listbox.curselection()[0]
                # 获取显示文本，从中提取任务信息
                display_text = result_listbox.get(selected_idx)
                
                # 在主任务列表中查找匹配的任务
                for i, task in enumerate(self.tasks):
                    priority = task.get("priority", "中")
                    completed = task.get("completed", False)
                    text = task.get("text", "")
                    due_date = task.get("due_date", "")
                    
                    task_display = f"[{priority}] {text}"
                    if due_date:
                        task_display += f" (截止: {due_date})"
                    if completed:
                        task_display = f"✓ {task_display}"
                    
                    # 如果找到匹配任务
                    if task_display == display_text:
                        # 应用"全部"过滤以显示所有任务
                        self.filter_var.set("全部")
                        self.apply_filter()
                        
                        # 查找在过滤后列表中的位置
                        try:
                            filtered_idx = self.filtered_tasks.index(task)
                            # 选中该任务
                            self.listbox.selection_clear(0, tk.END)
                            self.listbox.selection_set(filtered_idx)
                            self.listbox.see(filtered_idx)  # 确保可见
                            
                            # 将任务信息填充到编辑区域
                            self.entry.delete(0, tk.END)
                            self.entry.insert(0, task["text"])
                            self.priority_var.set(task["priority"])
                            
                            if task.get("due_date"):
                                try:
                                    due_date = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                                    self.date_picker.set_date(due_date)
                                except:
                                    pass
                            else:
                                self.date_picker.set_date(datetime.date.today())
                                
                            search_window.destroy()
                            break
                        except ValueError:
                            # 任务不在过滤列表中
                            pass
            except IndexError:
                pass
        
        # 绑定双击事件
        result_listbox.bind("<Double-1>", lambda e: go_to_task())
        
        # 搜索按钮
        search_button = tk.Button(button_frame, text="查找", command=perform_search, width=10)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # 跳转按钮
        goto_button = tk.Button(button_frame, text="跳转到任务", command=go_to_task, width=10)
        goto_button.pack(side=tk.LEFT, padx=5)
        
        # 关闭按钮
        close_button = tk.Button(button_frame, text="关闭", command=search_window.destroy, width=10)
        close_button.pack(side=tk.RIGHT, padx=5)
        
        # 状态标签
        status_label = tk.Label(search_window, text="", anchor="w", bd=1, relief=tk.SUNKEN)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定回车键
        search_entry.bind("<Return>", lambda e: perform_search())
        
        # 应用当前主题
        theme = self.theme_color[self.current_theme]
        search_window.configure(bg=theme["bg"])
        search_frame.configure(bg=theme["bg"])
        options_frame.configure(bg=theme["bg"])
        results_frame.configure(bg=theme["bg"])
        button_frame.configure(bg=theme["bg"])
        
        search_label.configure(bg=theme["bg"], fg=theme["fg"])
        search_scope_label.configure(bg=theme["bg"], fg=theme["fg"])
        scope_all.configure(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        scope_active.configure(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        scope_completed.configure(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        case_sensitive_check.configure(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["button_bg"])
        status_label.configure(bg=theme["bg"], fg=theme["fg"])
        
        result_listbox.configure(bg=theme["listbox_bg"], fg=theme["fg"])