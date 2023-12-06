import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# 创建主窗口
app = ctk.CTk()
app.geometry("800x600")
app.title("基础画像表")

# 创建水平布局的容器
frame_left = ctk.CTkFrame(master=app, width=240)
frame_right = ctk.CTkFrame(master=app, width=560)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 创建树形菜单
tree_menu_data = {
    "menu": [
        {"item_name": "设备", "index": 0},
        {"item_name": "运行", "index": 1},
        {
            "item_name": "常规任务",
            "two_item": [
                {"item_name": "一条龙", "index": 2},
                {"item_name": "师门", "index": 3},
            ],
        },
        {
            "item_name": "帮会任务",
            "two_item": [
                {"item_name": "战龙", "index": 4},
                {"item_name": "帮花", "index": 5},
            ],
        },
        {
            "item_name": "家园任务",
            "two_item": [
                {"item_name": "收菜", "index": 6},
            ],
        },
    ]
}

tree_menu = ttk.Treeview(frame_left)
tree_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 插入菜单项
for item in tree_menu_data["menu"]:
    parent = tree_menu.insert("", tk.END, text=item["item_name"], open=True)
    if "two_item" in item:
        for sub_item in item["two_item"]:
            tree_menu.insert(parent, tk.END, text=sub_item["item_name"])

# 创建右侧内容区域
content_title = ctk.CTkLabel(frame_right, text="", font=("Arial", 18))
content_title.pack(pady=20)
content_frame = ctk.CTkFrame(frame_right)
content_frame.pack(fill=tk.BOTH, expand=True)
content_scrollbar = ttk.Scrollbar(content_frame)
content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
content_text = tk.Text(content_frame, yscrollcommand=content_scrollbar.set)
content_text.pack(fill=tk.BOTH, expand=True)
content_scrollbar.config(command=content_text.yview)
confirm_button = ctk.CTkButton(frame_right, text="确定")
confirm_button.pack(pady=20)

# 更新右侧内容区域的函数
def update_content(event):
    selected_item = tree_menu.focus()
    item_text = tree_menu.item(selected_item, 'text')
    content_title.configure(text=item_text)
    content_text.delete(1.0, tk.END)
    content_text.insert(tk.END, f"这里是关于{item_text}的详细介绍。")

# 绑定选择事件
tree_menu.bind("<<TreeviewSelect>>", update_content)

# 运行主循环
app.mainloop()