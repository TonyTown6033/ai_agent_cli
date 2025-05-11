import tkinter as tk
from PIL import ImageGrab

def take_screenshot():
    """启动截图功能，用户可以自由选择截图区域"""
    print("请拖动鼠标选择截图区域...")

    # 隐藏主窗口
    root = tk.Tk()
    root.withdraw()

    # 获取屏幕分辨率
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 创建全屏透明窗口
    canvas = tk.Toplevel(root)
    canvas.attributes("-fullscreen", True)
    canvas.attributes("-alpha", 0.3)
    canvas.configure(bg="black")

    # 创建一个画布用于绘制矩形
    overlay = tk.Canvas(canvas, bg="black", highlightthickness=0)
    overlay.pack(fill=tk.BOTH, expand=True)

    # 用于存储选择的区域
    start_x = start_y = [0]
    end_x = end_y = [0]
    rect_id = None  # 用于存储矩形的 ID

    def on_mouse_down(event):
        """鼠标按下时记录起始点"""
        nonlocal rect_id
        start_x[0], start_y[0] = event.x, event.y
        # 创建一个矩形
        rect_id = overlay.create_rectangle(start_x[0], start_y[0], start_x[0], start_y[0], outline="red", width=2)

    def on_mouse_move(event):
        """鼠标移动时更新矩形"""
        if rect_id:
            overlay.coords(rect_id, start_x[0], start_y[0], event.x, event.y)

    def on_mouse_up(event):
        """鼠标释放时记录结束点并完成截图"""
        end_x[0], end_y[0] = event.x, event.y
        canvas.destroy()  # 关闭透明窗口
        root.quit()  # 退出主循环

    # 绑定鼠标事件
    overlay.bind("<ButtonPress-1>", on_mouse_down)
    overlay.bind("<B1-Motion>", on_mouse_move)
    overlay.bind("<ButtonRelease-1>", on_mouse_up)

    # 启动主循环
    root.mainloop()

    # 确保截图区域在屏幕范围内
    left = max(0, min(start_x[0], end_x[0]))
    top = max(0, min(start_y[0], end_y[0]))
    right = min(screen_width, max(start_x[0], end_x[0]))
    bottom = min(screen_height, max(start_y[0], end_y[0]))

    # 检查是否选择了有效区域
    if left >= right or top >= bottom:
        print(f"选择的区域无效: ({left}, {top}, {right}, {bottom})")
        print("未选择有效的截图区域！")
        return

    # 截图并保存
    try:
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)
        screenshot.save("screenshot.png")
        print("截图已保存为 screenshot.png")
    except Exception as e:
        print(f"截图失败: {e}")

if __name__ == "__main__":
    take_screenshot()