import tkinter as tk
import math
import datetime

# 予定： [開始時, 開始分, 終了時, 終了分, 内容]
schedule = []
schedule_colors = ["lightblue", "yellow", "lightgreen", "pink", "purple", "orange", "cyan"]

def input_int_in_range(prompt, min_val, max_val):
    while True:
        val = input(prompt)
        if val.isdigit():
            num = int(val)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"{min_val}から{max_val}の範囲で入力してください。")
        else:
            print("整数で入力してください。")

# 予定入力
while True:
    com = input("予定を入力しますか？(Yes/No): ")
    if com.lower() in ["no", "n"]:
        print("----- 時計を表示します -----")
        break

    while True:
        sh = input_int_in_range("開始時刻(0-23):", 0, 23)
        sm = input_int_in_range("開始分(0-59):", 0, 59)
        eh = input_int_in_range("終了時刻(0-23):", 0, 23)
        em = input_int_in_range("終了分(0-59):", 0, 59)

        start_total = sh * 60 + sm
        end_total = eh * 60 + em

        if end_total <= start_total:
            resp = input("終了が開始より早いです。日付をまたぎますか？(Yes/No): ")
            if resp.lower() in ["yes", "y"]:
                end_total += 24 * 60  # 翌日に延長
                break
            else:
                print("もう一度入力してください。")
        else:
            break

    title = input("予定の内容（例：打ち合わせ）を入力してください：")
    schedule.append([sh, sm, eh, em, title, start_total, end_total])

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("予定付きアナログ時計")
        self.canvas_size = 300
        self.center = self.canvas_size // 2
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()
        self.update_clock()

    def update_clock(self):
        self.canvas.delete("all")
        now = datetime.datetime.now()
        total_min = now.hour * 60 + now.minute

        self.draw_dial(total_min)
        self.draw_hands(now)
        self.draw_schedule_text(total_min)

        self.root.after(1000, self.update_clock)

    def draw_dial(self, now_min):
        c = self.center
        r_out = c - 10
        r_in = c - 60  # 0,10,20分の内側に来るよう調整

        # スケジュールの背景色を設定
        outer_color = "white"
        inner_color = "white"
        for i, sc in enumerate(schedule):
            start = sc[5]
            end = sc[6]
            cmp_now = now_min
            if end >= 24*60 and now_min < start % (24*60):
                cmp_now += 24*60  # 翌日扱い
            if start <= cmp_now < end:
                outer_color = schedule_colors[i % len(schedule_colors)]
                inner_color = schedule_colors[(i + 1) % len(schedule_colors)]
                break

        self.canvas.create_oval(c - r_out, c - r_out, c + r_out, c + r_out,
                                outline="black", width=2, fill=outer_color)
        self.canvas.create_oval(c - r_in, c - r_in, c + r_in, c + r_in,
                                outline="black", width=2, fill=inner_color)

        # 黒い点（1分ごと）
        for i in range(60):
            angle = math.radians(i * 6)
            x = c + math.cos(angle) * (r_out - 5)
            y = c + math.sin(angle) * (r_out - 5)
            self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black")

        # 赤点（5分ごと）
        for i in range(0, 60, 5):
            angle = math.radians(i * 6)
            x = c + math.cos(angle) * (r_out - 5)
            y = c + math.sin(angle) * (r_out - 5)
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")

        # 時の数字（1-12 または 13-24）
        hour_base = 1 if datetime.datetime.now().hour < 13 else 13
        for i in range(1, 13):
            label = str(i if hour_base == 1 else i + 12)
            angle = math.radians(i * 30 - 90)
            x = c + math.cos(angle) * (r_in - 10)
            y = c + math.sin(angle) * (r_in - 10)
            self.canvas.create_text(x, y, text=label, font=("Helvetica", 17))

        # 10分ごとの数字（0,10,...50）
        for i in range(0, 60, 10):
            angle = math.radians(i * 6 - 90)
            x = c + math.cos(angle) * (r_out - 25)
            y = c + math.sin(angle) * (r_out - 25)
            self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 13))

    def draw_hands(self, now):
        c = self.center

        # 時針
        h_angle = math.radians(((now.hour % 12) + now.minute / 60) * 30 - 90)
        h_len = self.center - 70
        hx = c + math.cos(h_angle) * h_len
        hy = c + math.sin(h_angle) * h_len
        self.canvas.create_line(c, c, hx, hy, width=4, fill="black")

        # 分針
        m_angle = math.radians(now.minute * 6 - 90)
        m_len = self.center - 45
        mx = c + math.cos(m_angle) * m_len
        my = c + math.sin(m_angle) * m_len
        self.canvas.create_line(c, c, mx, my, width=3, fill="black")

        # 秒針
        s_angle = math.radians(now.second * 6 - 90)
        s_len = self.center - 30
        sx = c + math.cos(s_angle) * s_len
        sy = c + math.sin(s_angle) * s_len
        self.canvas.create_line(c, c, sx, sy, width=1, fill="red")

    def draw_schedule_text(self, now_min):
        c = self.center
        displayed = False
        for sc in schedule:
            start = sc[5]
            end = sc[6]
            cmp_now = now_min
            if end >= 24*60 and now_min < start % (24*60):
                cmp_now += 24*60
            if start <= cmp_now < end:
                self.canvas.create_text(c, c + 60, text=f"予定: {sc[4]}", font=("Helvetica", 12), fill="black")
                displayed = True
                break
        if not displayed:
            self.canvas.create_text(c, c + 60, text="予定なし", font=("Helvetica", 12), fill="gray")


# 起動
root = tk.Tk()
app = ClockApp(root)
root.mainloop()




