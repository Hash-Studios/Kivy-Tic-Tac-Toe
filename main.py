from PIL import Image, ImageDraw
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import game
from kivy.core.audio import SoundLoader


def interpolate(f_co, t_co, interval):
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


class BG(BoxLayout):
    def __init__(self, **kwargs):
        super(BG, self).__init__(**kwargs)
        Clock.schedule_once(self.bg_apply)

    def bg_apply(self, dt):
        window_sizes = Window.size
        self.w = window_sizes[0]
        self.h = window_sizes[1]
        gradient = Image.new('RGBA', (self.w, self.h), color=0)
        draw = ImageDraw.Draw(gradient)
        f_co = (23, 147, 156)
        t_co = (192, 232, 146)
        for i, color in enumerate(interpolate(f_co, t_co, self.h)):
            draw.line([(0, i), (self.w, i)], tuple(color), width=1)
        with open('assets/images/bg.png', 'wb') as f:
            gradient.save(f)
        self.ids.bg.source = 'assets/images/bg.png'
        self.ids.bg.reload()


class Main_Card(FloatLayout):
    def __init__(self, **kwargs):
        super(Main_Card, self).__init__(**kwargs)


class Button_Card(FloatLayout):
    def __init__(self, **kwargs):
        super(Button_Card, self).__init__(**kwargs)


class Main_Screen(Screen):
    def __init__(self, **kwargs):
        super(Main_Screen, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # if touch.spos[1]<0.118:
        # print(touch.spos)
        # if self.collide_point(*touch.pos):
        #     print("Touch down")
        #     return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.spos[1] < 0.118:  # Bottom Button
            main_app.select.play()
            if self.collide_point(*touch.pos):
                print("RESET")
                self.manager.current = "win"
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)


class Win_Screen(Screen):
    def __init__(self, **kwargs):
        super(Win_Screen, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # if touch.spos[1]<0.118:
        # print(touch.spos)
        # if self.collide_point(*touch.pos):
        #     print("Touch down")
        #     return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.spos[1] < 0.118:  # Bottom Button
            main_app.select.play()
            if self.collide_point(*touch.pos):
                print("BACK")
                self.manager.current = "lose"
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)


class Lose_Screen(Screen):
    def __init__(self, **kwargs):
        super(Lose_Screen, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # if touch.spos[1]<0.118:
        # print(touch.spos)
        # if self.collide_point(*touch.pos):
        #     print("Touch down")
        #     return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.spos[1] < 0.118:  # Bottom Button
            main_app.select.play()
            if self.collide_point(*touch.pos):
                print("BACK")
                self.manager.current = "main"
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)


class Intro_Screen(Screen):
    def __init__(self, **kwargs):
        super(Intro_Screen, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # if touch.spos[1]<0.118:
        # print(touch.spos)
        # if self.collide_point(*touch.pos):
        #     print("Touch down")
        #     return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.spos[1] < 0.118:  # Bottom Button
            main_app.start.play()
            if self.collide_point(*touch.pos):
                print("BACK")
                self.manager.current = "main"
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)


class MainApp(App):
    def build(self):
        Window.size = (360, 640)
        self.app_start = SoundLoader.load('assets/sounds/app_start.wav')
        self.app_start.volume = 0.8
        self.app_start.play()
        self.select = SoundLoader.load('assets/sounds/select.wav')
        self.start = SoundLoader.load('assets/sounds/start.wav')
        self.select.volume = 0.5


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
