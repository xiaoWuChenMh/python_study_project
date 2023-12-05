import customtkinter as ctk
import tkinter as tk

# 这是被绑定的函数，它会打印出触发事件的按钮的文本
def button_callback(button_text):
    print(button_text)

# 初始化Tkinter窗口
root = ctk.CTk()

# 创建三个按钮并将它们绑定到同一个函数
button_texts = ["A11", "A12", "A13"]
buttons = []
for text in button_texts:
    # 在lambda函数中传递按钮的文本
    button = ctk.CTkButton(root, text=text, command=lambda t=text: button_callback(t))
    button.pack(pady=10)  # 使用pack布局管理器并添加一些垂直间距
    buttons.append(button)

# 运行主循环
root.mainloop()