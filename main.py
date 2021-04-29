from kivy.app import App
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.image import Image
import random

# Default Size of Window
width, height = Window.size

# Config of Window
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))
Config.set('graphics', 'resizable', False)
Config.write()

# Markup
Builder.load_file('common.kv')


# Widget "Ball"
class Ball(Widget):
    ball_status = ObjectProperty()
    im = Image()
    ball_color = ObjectProperty()
    ball_num = ObjectProperty()
    ball_side = ObjectProperty()
    size_window = Window.size

    def __init__(self, color="black", num="1", side="left", **kwargs):
        self.ball_status = str("rings/balls/" + color + "/" + side + "/" + num + ".png")
        super(Ball, self).__init__(**kwargs)

        self.ball_color = color
        self.ball_num = num
        self.ball_side = side

    def update(self, color="black", num="1", side="left"):
        self.ball_color = color
        self.ball_num = num
        self.ball_side = side
        self.ball_status = str("rings/balls/" + color + "/" + side + "/" + num + ".png")


# Widget "BackGround"
class BackGround(Widget):
    size_window = Window.size
    pass


# class Task. Generate color and count of balls
class Task(Widget):
    size_window = Window.size
    text_task = StringProperty()
    color = ObjectProperty('None')
    count = ObjectProperty(0)

    # Randomize color
    def rand_color(self):
        color = random.choice(['green', 'red', 'yellow', 'black', 'white'])
        return color

    # Give new Task
    def update(self, balls_color, combo):
        self.color = self.rand_color()
        self.count = random.choice([i for i in range(1, balls_color[self.color])])

        self.text_task = self.color + ' ' + str(self.count)

        pair = [self.count, self.color]

        while pair in combo:
            self.color = self.rand_color()
            self.count = random.choice([i for i in range(1, balls_color[self.color])])

            self.text_task = self.color + ' ' + str(self.count)

            pair = [self.count, self.color]

        return self.text_task


# Widget "Timer"
class MyClock(Label):
    a = NumericProperty(0)
    pos_hint_x = 0
    pos_hint_y = 0
    font_size = 70

    def start(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a)

        def finish_callback(animation, clock):
            clock.text = "Time's up("

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def reset(self):
        self.a = 20

    def on_a(self, instance, value):
        self.text = str(round(value, 1))


# Widget "Task"
class TaskLabel(Label):
    pass


# Widget "Score"
class ScoreLabel(Label):
    pass


# Game Engine
class RingsGame(Widget):
    # Window settings
    size_window = Window.size
    background = BackGround()

    # Objects in GamePlay
    score_text = StringProperty()
    text_task = ObjectProperty()
    score = NumericProperty(0)
    label = FloatLayout()
    timer = MyClock()
    task = Task()

    # Balls
    balls = dict()
    balls_color = {'green': 0, 'red': 0, 'yellow': 0, 'black': 0, 'white': 0}
    combo_color = []

    # Balls graph
    common_ball_1 = ObjectProperty()
    common_ball_20 = ObjectProperty()
    graph = [[0] * 53 for i in range(0, 53)]

    # Balls update after pressing
    def balls_update(self, side):
        if side == 'left':
            # Re-linking of Left Circle ( Switching only colors)
            local = self.balls[('left', 27)].ball_color
            for i in range(0, 26):
                self.balls[('left', 27 - i)].ball_color = self.balls[('left', 27 - i - 1)].ball_color
            self.balls[('left', 1)].ball_color = local
            for i in range(1, 28):
                self.balls[('left', i)].update(self.balls[('left', i)].ball_color, self.balls[('left', i)].ball_num,
                                               self.balls[('left', i)].ball_side)
                # self.add_widget(self.balls[('left', i)])
        if side == 'right':
            # Re-linking of Right Circle
            # First an twentieth Balls are common
            self.common_ball_1 = self.balls[('left', 1)].ball_color
            self.common_ball_20 = self.balls[('left', 20)].ball_color

            # Give new colors to common balls, before that backup 1 and 20 balls
            self.balls[('left', 1)].ball_color = self.balls[('right', 27)].ball_color
            self.balls[('left', 20)].ball_color = self.balls[('right', 19)].ball_color

            # Updating balls on the layer
            self.balls[('left', 1)].update(self.balls[('left', 1)].ball_color,
                                           self.balls[('left', 1)].ball_num,
                                           self.balls[('left', 1)].ball_side)
            self.balls[('left', 20)].update(self.balls[('left', 20)].ball_color,
                                            self.balls[('left', 20)].ball_num,
                                            self.balls[('left', 20)].ball_side)

            # Switching Colors in circle
            for i in range(0, 6):
                self.balls[('right', 27 - i)].ball_color = self.balls[('right', 27 - i - 1)].ball_color
            for i in range(8, 25):
                self.balls[('right', 27 - i)].ball_color = self.balls[('right', 27 - i - 1)].ball_color

            # Give colors of common balls to neighbours
            self.balls[('right', 2)].ball_color = self.common_ball_1
            self.balls[('right', 21)].ball_color = self.common_ball_20

            # Updating balls on the layer
            self.balls[('right', 2)].update(self.balls[('right', 2)].ball_color,
                                            self.balls[('right', 2)].ball_num,
                                            self.balls[('right', 2)].ball_side)
            self.balls[('right', 21)].update(self.balls[('right', 21)].ball_color,
                                             self.balls[('right', 21)].ball_num,
                                             self.balls[('right', 21)].ball_side)

            # Updating balls on the layer
            for i in range(1, 28):
                if i != 1 and i != 20:
                    self.balls[('right', i)].update(self.balls[('right', i)].ball_color,
                                                    self.balls[('right', i)].ball_num,
                                                    self.balls[('right', i)].ball_side)

    # Randomizer of color
    def rand_color(self):
        color = random.choice(['green', 'red', 'yellow', 'black', 'white'])
        self.balls_color[color] += 1
        return color

    # Initialize main Objects
    def __init__(self, **kwargs):
        super(RingsGame, self).__init__(**kwargs)

        # left
        for i in range(2, 27):
            self.graph[i][i + 1] = 1
            self.graph[i + 1][i] = 1
            self.graph[i][i - 1] = 1
            self.graph[i - 1][i] = 1

        self.graph[1][27] = 1
        self.graph[27][1] = 1
        self.graph[1][2] = 1
        self.graph[27][26] = 1

        # right
        for i in range(29, 52):
            self.graph[i][i + 1] = 1
            self.graph[i + 1][i] = 1
            self.graph[i][i - 1] = 1
            self.graph[i - 1][i] = 1

        self.graph[28][52] = 1
        self.graph[28][29] = 1
        self.graph[52][28] = 1
        self.graph[52][51] = 1

        # common
        self.graph[1][28] = 1
        self.graph[28][1] = 1
        self.graph[1][52] = 1
        self.graph[52][1] = 1

        self.graph[20][45] = 1
        self.graph[45][20] = 1
        self.graph[20][46] = 1
        self.graph[46][20] = 1

        for i in range(1, 28):
            self.balls[('left', i)] = Ball(self.rand_color(), str(i), 'left')
            self.add_widget(self.balls[('left', i)])
        for i in range(1, 28):
            if i != 1 and i != 20:
                self.balls[('right', i)] = Ball(self.rand_color(), str(i), 'right')
                self.add_widget(self.balls[('right', i)])
        self.score = 0
        self.score_text = str(self.score)
        self.label.add_widget(self.timer)
        self.add_widget(self.label)
        self.analysis()

    # Control
    def press(self, num_btn):
        if num_btn == 1:
            self.preparing_analysis()
            self.balls_update('left')
            self.simplified_analysis()
        if num_btn == 2:
            self.preparing_analysis()
            self.balls_update('right')
            self.simplified_analysis()

    # Convert to key for dict of colors in circles
    def convert_to_key(self, num):
        key = ('side', num)
        if num < 28:
            key = ('left', num)
        else:
            if num < 27 + 19:
                key = ('right', num - 27 + 1)
            else:
                key = ('right', num - 27 + 2)
        return key

    # Search all combo's
    def analysis(self):
        used = set()
        for v in range(1, 53):
            q = [v]
            color = self.balls[self.convert_to_key(v)].ball_color
            used.add(v)
            count = 1
            while len(q) > 0:
                now = q.pop(0)
                for i in range(1, 53):
                    if self.graph[now][i] == 1:
                        if i not in used and color == self.balls[self.convert_to_key(i)].ball_color:
                            q.append(i)
                            used.add(i)
                            count += 1
            while count > 0:
                self.combo_color.append([count, color])
                count -= 1

    # Simplified preparing to Analysis of combo's
    def preparing_analysis(self):
        used = set()
        q_g = [1, 20,2,27,19,21,28,45,46,52]
        for v in q_g:
            q = [v]
            color = self.balls[self.convert_to_key(v)].ball_color
            used.add(v)
            count = 1
            while len(q) > 0:
                now = q.pop(0)
                for i in range(1, 53):
                    if self.graph[now][i] == 1:
                        if i not in used and color == self.balls[self.convert_to_key(i)].ball_color:
                            q.append(i)
                            used.add(i)
                            count += 1
            while count > 0:
                self.combo_color.pop(self.combo_color.index([count, color]))
                count -= 1

    # Simplified Analyze of combo's
    def simplified_analysis(self):
        used = set()
        q_g = [1, 20,2,27,19,21,28,45,46,52]
        for v in q_g:
            q = [v]
            color = self.balls[self.convert_to_key(v)].ball_color
            used.add(v)
            count = 1
            while len(q) > 0:
                now = q.pop(0)
                for i in range(1, 53):
                    if self.graph[now][i] == 1:
                        if i not in used and color == self.balls[self.convert_to_key(i)].ball_color:
                            q.append(i)
                            used.add(i)
                            count += 1
            while count > 0:
                self.combo_color.append([count, color])
                count -= 1

    # Give a new task
    def set_new_task(self):
        return self.task.update(self.balls_color, self.combo_color)

    # Update main Game engine
    def update(self, dt):
        if self.timer.a == 0:
            self.text_task = self.set_new_task()
            self.timer.reset()
            self.timer.start()
        pair = [self.task.count, self.task.color]
        if pair in self.combo_color:
            self.text_task = self.set_new_task()
            self.timer.reset()
            self.timer.start()
            self.score += 1
            self.score_text = str(self.score)


# App
class TouchTheRingsApp(App):
    def build(self):
        game = RingsGame()
        Clock.schedule_interval(game.update, 1 / 90)
        return game


if __name__ == '__main__':
    TouchTheRingsApp().run()
