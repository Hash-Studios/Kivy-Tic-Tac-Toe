from PIL import Image, ImageDraw
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


def interpolate(f_co, t_co, interval):
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


KV = '''
#:import Window kivy.core.window.Window
<BG>:
	orientation: "vertical"
	Image:
		id: bg
		source: 'bg.png'
Screen:
	id: main_screen
	BG:
    FloatLayout:
        canvas:
            Color:
                rgba: (0.576, 0.721, 0.411, 0.25)
            RoundedRectangle:
                pos: Window.size[0]*0.0694, Window.size[1]*0.2578
                size: Window.size[0]*0.861, Window.size[1]*0.4843
                radius: [22]
            Color:
                rgba: (0.5764, 0.7215, 0.4117, 0.5)
            RoundedRectangle:
                pos: 0, 0
                size: Window.size[0], Window.size[1]*0.1171
                radius: [22,22,0,0]
        Label:
            text: "Tic - Tac - Toe"
            markup: True
            pos_hint: {'center_x': 0.5, 'center_y':0.882}
            size_hint_x: None
            font_name: "Marvel-Bold"
            color: (0.917, 0.929, 0.901, 0.75)
            font_size: Window.size[0]*0.133
        Label:
            text: "RESET"
            markup: True
            pos_hint: {'center_x': 0.5, 'center_y':0.0585}
            size_hint_x: None
            font_name: "Marvel-Bold"
            color: (0.337, 0.564, 0.58, 0.5)
            font_size: Window.size[0]*0.133
'''


class BG(BoxLayout):
    def __init__(self, **kwargs):
        super(BG, self).__init__(**kwargs)
        Clock.schedule_once(self.bg_apply)
    def bg_apply(self,dt):
        window_sizes = Window.size
        self.w = window_sizes[0]
        self.h = window_sizes[1]
        gradient = Image.new('RGBA', (self.w, self.h), color=0)
        draw = ImageDraw.Draw(gradient)
        f_co = (23, 147, 156)
        t_co = (192, 232, 146)
        for i, color in enumerate(interpolate(f_co, t_co, self.h)):
            draw.line([(0, i), (self.w, i)], tuple(color), width=1)
        with open('bg.png', 'wb') as f:
            gradient.save(f)
        self.ids.bg.source = 'bg.png'
        self.ids.bg.reload()


class MainApp(App):
    def build(self):
        Window.size = (360, 640)
        return Builder.load_string(KV)


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
