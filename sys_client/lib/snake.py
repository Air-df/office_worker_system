#! /usr/bin/python3

# 线程
import threading,time,random,tkinter,traceback


class snake_game(tkinter.Toplevel):
    def __init__(self, rows=20, columns=20,speed=0.2):
        super().__init__()
        # 行数
        self.rows = rows
        # 列数
        self.columns = columns
        # 游戏速度
        self.speed = speed
        self.stop = 10000
        # 定义　地板　蛇　　蛇头　　食物的颜色
        self.colors = {'floor': 'yellow', 'body': 'green',
                       'head': 'red', 'food': 'blue'}
        # top 上面的界面
        self.top_ui()
        # bottom 下面的界面
        self.bottom_ui()
        # 生成　蛇　还有　食物
        self.make_all()
        # 把　蛇　和　食物都放入ui
        self.show_snake_and_food()
        # 链接控制
        self.direction = [-1, 0]
        self.playing = True  # 游戏可以进行
        self.start = True  # 开始按钮　在游戏开始前有效
        self.control()
    # 放置　蛇　还有　食物

    def make_all(self):
        # 蛇中心位置
        position = [self.rows // 2, self.columns // 2]
        # 蛇头
        self.head = [position[0], position[1] + 1]
        # 蛇尾
        self.tail = [position[0], position[1] - 1]
        # 整条蛇
        self.snake = [self.tail, position, self.head]
        # 生成食物
        self.food = self.make_food()
    # 把蛇和食物放入ui

    def show_snake_and_food(self):
        # 放蛇
        for i in self.snake:
            self.labels[i[0]][i[1]]['bg'] = self.colors['body']
        # 放蛇头
        self.labels[self.head[0]][self.head[1]]['bg'] = self.colors['head']
        # 放食物
        self.labels[self.food[0]][self.food[1]]['bg'] = self.colors['food']

    # 生成食物
    def make_food(self):
        x = random.randint(0, self.rows - 1)
        y = random.randint(0, self.columns - 1)
        food = [x, y]
        if food not in self.snake:
            return food
        self.make_food()




    # top 上面的界面

    def top_ui(self):
        # 放入一个框架frame
        self.top = tkinter.Frame(self)
        self.top.pack(fill=tkinter.X)
        # 框架里面 左边 放入两个按钮　重置　和　开始
        self.re_btn = tkinter.Button(
            self.top, text='重置', command=self.re_btn_func)
        self.re_btn.pack(side=tkinter.LEFT)
        self.start_btn = tkinter.Button(
            self.top, text='开始', command=self.start_btn_func)
        self.start_btn.pack(side=tkinter.LEFT)
        # 框架里面 中间 放入　　计分 Label
        self.score = 0
        self.score_label = tkinter.Label(
            self.top, text=self.get_score(), font=('宋体', 20))
        self.score_label.pack()
    # re_btn函数func　　重置按钮

    def re_btn_func(self):
        for i in self.labels:
            for j in i:
                j['bg'] = self.colors['floor']
        self.make_all()
        self.playing = False
        self.start = True
        self.direction = [1, 0]
        self.show_snake_and_food()
        self.score = 0
        self.score_label['text'] = self.get_score()
        self.score_label['fg'] = 'black'
    # 得分

    def get_score(self):
        return 'score:' + str(self.score)

    # bottom 下面的界面
    def bottom_ui(self):
        # 生成一个属组放置lables
        self.labels = [[0] * self.columns for i in range(self.rows)]
        self.bottom = tkinter.Frame(self)
        self.bottom.pack(fill=tkinter.BOTH)
        # 生成地图　　二维
        for i in range(self.rows):
            for j in range(self.columns):
                label = tkinter.Label(
                    self.bottom, height=1, width=3, bg=self.colors['floor'])
                label.grid(row=i, column=j)
                self.labels[i][j] = label
    # 开始的button的函数

    def start_btn_func(self):
        if self.start:
            self.playing = True
            self.t = threading.Thread(target=self.move)
            self.t.start()
            self.start = False
            # 每走一步只能调一次头
            self.turn_around = True

    # 移动

    def move(self):
        # n=0
        # print(n)
        while self.playing:
            # print(n)
            # 越界
            if (self.head[0] + self.direction[0] < 0 or self.head[0] + self.direction[0] >= self.rows or
                    self.head[1] + self.direction[1] < 0 or self.head[1] + self.direction[1] >= self.columns):
                print('游戏结束')
                self.score_label['text'] = self.get_score() + '  游戏结束'
                self.score_label['fg'] = 'red'
                self.playing = False
                return
            # 碰到自己身体
            elif self.labels[self.head[0] + self.direction[0]][self.head[1] + self.direction[1]]['bg'] == self.colors['body']:
                print('游戏结束')
                self.playing = False
                return
            # 吃到食物
            elif self.labels[self.head[0] + self.direction[0]][self.head[1] + self.direction[1]]['bg'] == self.colors['food']:
                self.one_step(0)
                self.score += 1
                self.score_label['text'] = self.get_score()
                self.food = self.make_food()
            # 正常的一步
            elif self.labels[self.head[0] + self.direction[0]][self.head[1] + self.direction[1]]['bg'] == self.colors['floor']:
                self.one_step(1)
            # 每走一步相隔0.2s
            time.sleep(self.speed)
            # n+=1

    # 移动一步
    def one_step(self, eat):
        # 头前进
        self.head = [self.head[0] + self.direction[0],
                     self.head[1] + self.direction[1]]
        self.snake.append(self.head)
        # 尾巴删除
        if eat:
            self.tail = self.snake.pop(0)
            self.labels[self.tail[0]][self.tail[1]
                                      ]['bg'] = self.colors['floor']
        # 屏幕刷新
        self.show_snake_and_food()
        # 每走一步　　只能调一次头
        self.turn_around = True

    # 控制移动
    def control(self):
        # 依次上左下右
        self.bind('<KeyPress-w>', lambda e: self.where_go(0))
        self.bind('<KeyPress-a>', lambda e: self.where_go(1))
        self.bind('<KeyPress-s>', lambda e: self.where_go(2))
        self.bind('<KeyPress-d>', lambda e: self.where_go(3))
    # 控制方向

    def where_go(self, n):
        directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        if self.direction != directions[(n + 2) % len(directions)] and self.turn_around:
            self.direction = directions[n]
            self.turn_around = False



def main(难度):
    try:
        snake_game(*难度)
    except Exception:
        traceback.print_exc()


def choice():
    难度s = [(10,10,0.5),(20,20,0.2),(30,30,0.06)]
    root = tkinter.Toplevel()
    tkinter.Label(root,text='请选择游戏难度').pack()
    def 简单():
        main(难度s[0])
        root.destroy()
    bt1 = tkinter.Button(root,text='简单',command=简单)
    bt1.pack()
    def 普通():
        main(难度s[1])
        root.destroy()
    bt1 = tkinter.Button(root,text='普通',command=普通)
    bt1.pack()
    def 困难():
        main(难度s[2])
        root.destroy()
    bt1 = tkinter.Button(root,text='困难',command=困难)
    bt1.pack()

if __name__ == '__main__':
    game = snake_game()
    game.mainloop()
