import json
import os

# 默认配置
DEFAULT_CONFIG = {
    "theme": "light",
    "auto_backup": False,
    "backup_count": 5,
    "window_size": "600x500",
    "font_size": 10,
    "date_format": "%Y-%m-%d",
}

def load_config(config_file="config.json"):
    """加载配置文件，如果不存在则创建默认配置"""
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                # 确保所有默认配置项都存在
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"加载配置失败: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        # 创建默认配置文件
        save_config(DEFAULT_CONFIG.copy(), config_file)
        return DEFAULT_CONFIG.copy()

def save_config(config, config_file="config.json"):
    """保存配置到文件"""
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False

def update_config(key, value, config_file="config.json"):
    """更新单个配置项并保存"""
    config = load_config(config_file)
    config[key] = value
    return save_config(config, config_file)
