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
<BG@BoxLayout>:
	orientation: "vertical"
	Image:
		id: bg
		source: 'bg.png'
Screen:
	id: main_screen
	BG:
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
        return Builder.load_string(KV)


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
