import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty, ReferenceListProperty

kivy.require('1.8.0')

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'width', '1920')

class Playground(Widget):
    # Кольца
    rings = ObjectProperty(None)
    # Игровые задания
    tasks = ObjectProperty(None)

    # Игровые переменные
    score = NumericProperty(0)
    timer = NumericProperty(0)
    record = NumericProperty(0)

    # Обработка входных данных
    touch_start_pos = ListProperty()
    action_triggered = BooleanProperty(False)


class Rings(Widget):
    # Кольца
    first_ring = ObjectProperty(None)
    second_ring = ObjectProperty(None)
    # Цветовые наборы в кольцах
    sets = ListProperty(ObjectProperty(None))
    # Общие шары
    first_common_ball = ObjectProperty(None)
    second_common_ball = ObjectProperty(None)

    # Представление на холсте
    # Позиция по х
    pos_x = NumericProperty(0)
    # Позиция по y
    pos_y = NumericProperty(0)
    # Позиция
    position = ReferenceListProperty(pos_x, pos_y)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class Ring(Widget):
    # кол-во шаров
    balls_count = NumericProperty(0)
    # Шары
    balls = ListProperty()
    # Цветовые наборы в кольце
    sets = ListProperty(ObjectProperty(None))

    # Представление на холсте
    # Позиция по х
    pos_x = NumericProperty(0)
    # Позиция по y
    pos_y = NumericProperty(0)
    # Позиция
    position = ReferenceListProperty(pos_x, pos_y)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class Tasks(Widget):
    # Шар
    ball = ObjectProperty(None)
    # Кол-во шаров
    count = NumericProperty(0)

    # Представление на холсте
    # Позиция по х
    pos_x = NumericProperty(0)
    # Позиция по y
    pos_y = NumericProperty(0)
    # Позиция
    position = ReferenceListProperty(pos_x, pos_y)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class Ball(Widget):
    # Цвет шара
    color = ObjectProperty()

    # Представление на холсте
    # Позиция по х
    pos_x = NumericProperty(0)
    # Позиция по y
    pos_y = NumericProperty(0)
    # Позиция
    position = ReferenceListProperty(pos_x, pos_y)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class Set(Widget):
    # Шар
    ball = ObjectProperty(None)
    # Кол-во шаров
    count = NumericProperty(0)

    # Представление на поле
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class TTRApp(App):
    game_engine = ObjectProperty(None)

    def build(self):
        game_engine = Playground()
        return game_engine


if __name__ == '__main__':
    TTRApp().run()
