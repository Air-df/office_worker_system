import tkinter


def main(win):
    root = tkinter.Toplevel()
    # 创建一个Label
    label1 = tkinter.Label(root, text='调整透明度')
    label1.pack()

    def scale2(value):
        nonlocal win
        scale1.set(value)
        n = int(value) / 100
        win.attributes("-alpha", n)
        print("scale1的当前值是:", value)

    # 创建一个Scale控件
    scale1 = tkinter.Scale(root, from_=100, to=10, command=scale2)
    scale1.pack()
