# data.py
import json
import os
import datetime
import shutil

def save_tasks(tasks, filename="tasks.json"):
    """保存任务到文件"""
    try:
        # 确保目录存在
        directory = os.path.dirname(filename)
        if (directory and not os.path.exists(directory)):
            os.makedirs(directory)
            
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存任务失败: {e}")
        return False

def load_tasks(filename="tasks.json"):
    """从文件加载任务"""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"加载任务失败: {e}")
        return []

def export_tasks_as_text(tasks, filename="tasks.txt"):
    """导出任务为文本文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("========== ToDo任务列表 ==========\n")
            f.write(f"导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总任务数: {len(tasks)}\n")
            f.write("================================\n\n")
            
            # 按优先级分组
            for priority in ["高", "中", "低"]:
                priority_tasks = [t for t in tasks if t.get("priority") == priority]
                if priority_tasks:
                    f.write(f"[{priority}优先级] ({len(priority_tasks)}项)\n")
                    f.write("--------------------------\n")
                    for i, task in enumerate(priority_tasks, 1):
                        status = "✓" if task.get("completed", False) else "□"
                        text = task.get("text", "")
                        due_date = f" (截止: {task['due_date']})" if task.get("due_date") else ""
                        f.write(f"{i}. {status} {text}{due_date}\n")
                    f.write("\n")
            
            # 统计信息
            completed = sum(1 for t in tasks if t.get("completed", False))
            f.write("========== 统计信息 ==========\n")
            f.write(f"已完成任务: {completed} ({(completed/len(tasks)*100) if tasks else 0:.1f}%)\n")
            f.write(f"未完成任务: {len(tasks) - completed}\n")
            
            # 检查过期任务
            today = datetime.date.today()
            overdue = 0
            for task in tasks:
                if not task.get("completed") and task.get("due_date"):
                    try:
                        due = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                        if due < today:
                            overdue += 1
                    except:
                        pass
            if overdue:
                f.write(f"已过期任务: {overdue}\n")
        return True
    except Exception as e:
        print(f"导出任务失败: {e}")
        return False

def backup_tasks(tasks, backup_dir="backups"):
    """备份任务数据"""
    try:
        # 确保备份目录存在
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 使用时间戳创建备份文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"tasks_backup_{timestamp}.json")
        
        # 创建备份
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        
        # 清理过旧的备份（保留最新的5个）
        backup_files = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir)
                             if f.startswith("tasks_backup_") and f.endswith(".json")])
        
        if len(backup_files) > 5:
            for old_file in backup_files[:-5]:
                os.remove(old_file)
                
        return True
    except Exception as e:
        print(f"备份任务失败: {e}")
        return False

def get_task_stats(tasks):
    """获取任务统计信息"""
    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "active": 0,
            "overdue": 0,
            "upcoming": 0,
            "completion_rate": 0
        }
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed", False))
    active = total - completed
    
    today = datetime.date.today()
    overdue = 0
    upcoming = 0
    
    for task in tasks:
        if not task.get("completed") and task.get("due_date"):
            try:
                due = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                if due < today:
                    overdue += 1
                elif (due - today).days <= 3:
                    upcoming += 1
            except:
                pass
    
    return {
        "total": total,
        "completed": completed,
        "active": active,
        "overdue": overdue,
        "upcoming": upcoming,
        "completion_rate": (completed / total * 100) if total > 0 else 0
    }

def import_from_text(filename):
    """从文本文件导入任务（简单格式）"""
    try:
        tasks = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # 解析格式: [优先级] 任务内容 (截止日期)
                    priority = "中"
                    if line.startswith("[高]"):
                        priority = "高"
                        line = line[3:].strip()
                    elif line.startswith("[中]"):
                        line = line[3:].strip()
                    elif line.startswith("[低]"):
                        priority = "低"
                        line = line[3:].strip()
                    
                    # 检查是否有截止日期
                    due_date = ""
                    if "(" in line and line.endswith(")"):
                        text, date_part = line.rsplit("(", 1)
                        text = text.strip()
                        date_part = date_part.rstrip(")")
                        if date_part:
                            due_date = date_part
                    else:
                        text = line
                    
                    task = {
                        "text": text,
                        "priority": priority,
                        "completed": False,
                        "due_date": due_date
                    }
                    tasks.append(task)
        return tasks
    except Exception as e:
        print(f"导入任务失败: {e}")
        return None

def search_tasks(tasks, keyword, case_sensitive=False, completed_filter=None, priority_filter=None, date_range=None):
    """
    搜索符合条件的任务
    
    参数:
    - tasks: 任务列表
    - keyword: 搜索关键词
    - case_sensitive: 是否区分大小写
    - completed_filter: None=全部, True=已完成, False=未完成
    - priority_filter: 优先级过滤("高", "中", "低" 或 None表示全部)
    - date_range: 日期范围元组 (start_date, end_date) 或 None
    
    返回:
    - 匹配的任务列表
    """
    results = []
    
    for task in tasks:
        # 检查完成状态过滤
        if completed_filter is not None and task.get("completed", False) != completed_filter:
            continue
            
        # 检查优先级过滤
        if priority_filter and task.get("priority") != priority_filter:
            continue
            
        # 检查日期范围
        if date_range and task.get("due_date"):
            try:
                task_date = datetime.datetime.strptime(task.get("due_date"), "%Y-%m-%d").date()
                start_date, end_date = date_range
                if start_date and task_date < start_date:
                    continue
                if end_date and task_date > end_date:
                    continue
            except:
                pass
                
        # 关键词搜索
        if keyword:
            task_text = task.get("text", "")
            if not case_sensitive:
                if keyword.lower() in task_text.lower():
                    results.append(task)
            else:
                if keyword in task_text:
                    results.append(task)
        else:
            # 如果没有提供关键词，但满足其他过滤条件，也加入结果
            results.append(task)
                
    return results

def sort_tasks_by_priority(tasks, reverse=False):
    """按优先级排序任务"""
    priority_map = {"高": 0, "中": 1, "低": 2}
    
    # 创建任务副本以避免修改原始数据
    sorted_tasks = tasks.copy()
    
    # 先按完成状态分组，然后在每组内按优先级排序
    sorted_tasks.sort(
        key=lambda t: (
            t.get("completed", False),  # 完成状态（False排在前面）
            priority_map.get(t.get("priority", "中"), 1)  # 优先级
        ),
        reverse=reverse
    )
    
    return sorted_tasks

def sort_tasks_by_date(tasks, reverse=False):
    """按截止日期排序任务"""
    today = datetime.date.today()
    
    # 创建任务副本以避免修改原始数据
    sorted_tasks = tasks.copy()
    
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
    
    sorted_tasks.sort(key=get_date_value, reverse=reverse)
    return sorted_tasks