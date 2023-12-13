import customtkinter as ctk
import tkinter as tk

def on_resize(event):
    # 获取CTkFrame的当前宽度和高度
    width = frame.winfo_width()
    height = frame.winfo_height()
    print(f"CTkFrame size: {width}x{height}")

# 初始化Tkinter窗口
root = ctk.CTk()

# 创建一个CTkFrame
frame = ctk.CTkFrame(root)
frame.pack(fill='both', expand=True)

# 绑定窗口大小改变事件
frame.bind("<Configure>", on_resize)

# 运行主循环
root.mainloop()