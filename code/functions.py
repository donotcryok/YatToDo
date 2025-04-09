# functions.py
import tkinter as tk

def add_task(listbox, task):
    """添加任务到列表"""
    listbox.insert(tk.END, task)

def delete_task(listbox, index):
    """删除指定任务"""
    listbox.delete(index)

def modify_task(listbox, index, new_task):
    """修改指定任务"""
    listbox.delete(index)
    listbox.insert(index, new_task)

def set_task_completed(listbox, index, is_completed=True):
    """标记任务为已完成/未完成"""
    current_text = listbox.get(index)
    
    # 如果已经标记为完成并且要设为未完成
    if current_text.startswith("✓ ") and not is_completed:
        new_text = current_text[2:]  # 去掉完成标记
        listbox.delete(index)
        listbox.insert(index, new_text)
        listbox.itemconfig(index, fg="black")
        return True
    
    # 如果未标记为完成并且要设为已完成
    elif not current_text.startswith("✓ ") and is_completed:
        new_text = f"✓ {current_text}"
        listbox.delete(index)
        listbox.insert(index, new_text)
        listbox.itemconfig(index, fg="gray")
        return True
        
    return False

def get_priority(task_text):
    """从任务文本中提取优先级"""
    if task_text.startswith("[高]"):
        return "高"
    elif task_text.startswith("[低]"):
        return "低"
    else:
        return "中"