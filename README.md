﻿# **YatToDo**

## 简介

（中山大学软件工程实践作业）YatToDo是一个简洁高效的待办事项管理应用程序，帮助用户组织和跟踪日常任务。该应用程序提供了一个用户友好的界面，让您能够轻松创建、编辑、删除和管理待办事项，提高工作和生活效率。

## 功能

- 创建、编辑和删除待办事项
- 为待办事项设置优先级和截止日期
- 标记待办事项为已完成状态
- 根据不同条件筛选和排序待办事项
- 自动备份功能，防止数据丢失
- 自定义主题和界面设置
- 支持导入/导出待办事项列表
- 可调整窗口大小和字体大小

## 开发环境

- 编程语言：Python 3.8+
- 图形界面：Tkinter
- 数据存储：JSON
- 系统兼容性：Windows、macOS、Linux

## 项目结构

```
YatToDo/
├── code/
│   ├── main.py           # 程序入口点
│   ├── config.py         # 配置管理模块
│   ├── todo.py           # 待办事项核心功能
│   ├── ui.py             # 用户界面模块
│   └── utils.py          # 工具函数
├── data/
│   ├── todos.json        # 待办事项数据文件
│   └── backup/           # 自动备份目录
├── config.json           # 用户配置文件
└── README.md             # 项目说明文档
```

## 使用说明

### 安装与运行

1. 确保您的系统已安装Python 3.8或更高版本
2. 克隆或下载项目到本地
3. 导航到项目目录
4. 运行以下命令启动应用程序：
   ```
   python code/main.py
   ```

### 配置选项

YatToDo提供了多种配置选项，可以通过程序界面的"设置"菜单进行修改，或直接编辑 `config.json`文件：

- `theme`: 应用程序主题 ("light" 或 "dark")
- `auto_backup`: 是否启用自动备份 (true 或 false)
- `backup_count`: 保留的备份数量
- `window_size`: 窗口大小 (格式为 "宽x高")
- `font_size`: 字体大小
- `date_format`: 日期显示格式

### 基本操作

- 添加待办事项：点击"添加"按钮或按下Enter键
- 编辑待办事项：双击待办事项或选中后点击"编辑"按钮
- 删除待办事项：选中待办事项后点击"删除"按钮
- 标记完成：点击待办事项前的复选框
- 筛选待办事项：使用筛选下拉菜单选择筛选条件
- 备份数据：点击"文件"菜单中的"备份"选项

## 使用示例

见说明文档

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件

## 作者

马福泉

## 联系方式

[邮箱：mafq5@mail2.sysu.edu.cn]
