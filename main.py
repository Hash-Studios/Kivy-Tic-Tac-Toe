import os
from functools import partial

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from PIL import Image, ImageDraw

import game

fonts_path = os.path.dirname(__file__)
font_path = os.path.join(fonts_path, 'Marvel-Bold.ttf')
sound1_path = os.path.join(fonts_path, 'select.wav')
sound2_path = os.path.join(fonts_path, 'app_start.wav')
sound3_path = os.path.join(fonts_path, 'start.wav')

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
        self.game_start()

    def game_start(self):
        self.turn = game.whoGoesFirst()
        #self.turn = "player"
        print(self.turn)
        self.gameIsPlaying = True
        if self.turn == "computer":
            move = game.getComputerMove(main_app.board, "O")
            game.makeMove(main_app.board, "O", move)
            self.turn = "player"
        elif self.turn == "player":
            pass

    def computer_move(self):
        if self.turn == "computer":
            move = game.getComputerMove(main_app.board, "O")
            game.makeMove(main_app.board, "O", move)
            a = {1: self.o_1, 2: self.o_2, 3: self.o_3, 4: self.o_4,
                5: self.o_5, 6: self.o_6, 7: self.o_7, 8: self.o_8, 9: self.o_9}
            Clock.schedule_once(partial(self.set_opacity, a[move], 1, 0.25), 1)
            if game.isWinner(main_app.board, "O"):
                print('The computer has beaten you! You lose.')
                self.gameIsPlaying = False
                self.manager.current = "lose"
                self.clear_screen()
                main_app.board = [" "]*10
            else:
                if game.isBoardFull(main_app.board):
                    print('The game is a tie!')
                    self.gameIsPlaying = False
                    self.clear_screen()
                    self.manager.current = "tie"
                    main_app.board = [" "]*10
                else:
                    self.turn = "player"
        self.turn = "player"

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # if touch.spos[1]<0.118:
        # print(touch.spos)
        # if self.collide_point(*touch.pos):
        #     print("Touch down")
        #     return False

    def clear_screen(self):
        Clock.schedule_once(partial(self.clear_opacity, self.x_1), 0)
        Clock.schedule_once(partial(self.clear_opacity, self.o_1), 0)
        Clock.schedule_once(
            partial(self.clear_opacity, self.x_2), 0.15)
        Clock.schedule_once(
            partial(self.clear_opacity, self.o_2), 0.15)
        Clock.schedule_once(partial(self.clear_opacity, self.x_3), 0.3)
        Clock.schedule_once(partial(self.clear_opacity, self.o_3), 0.3)
        Clock.schedule_once(
            partial(self.clear_opacity, self.x_4), 0.45)
        Clock.schedule_once(
            partial(self.clear_opacity, self.o_4), 0.45)
        Clock.schedule_once(partial(self.clear_opacity, self.x_5), 0.6)
        Clock.schedule_once(partial(self.clear_opacity, self.o_5), 0.6)
        Clock.schedule_once(
            partial(self.clear_opacity, self.x_6), 0.75)
        Clock.schedule_once(
            partial(self.clear_opacity, self.o_6), 0.75)
        Clock.schedule_once(
            partial(self.clear_opacity, self.x_7), 0.90)
        Clock.schedule_once(
            partial(self.clear_opacity, self.o_7), 0.90)
        Clock.schedule_once(
            partial(self.clear_opacity, self.x_8), 1.05)
        Clock.schedule_once(
            partial(self.clear_opacity, self.o_8), 1.05)
        Clock.schedule_once(partial(self.clear_opacity, self.x_9), 1.2)
        Clock.schedule_once(partial(self.clear_opacity, self.o_9), 1.2)
        main_app.board = [" "]*10
    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        a_delay = 0.1
        if touch.spos[1] < 0.118:           # Bottom Button
            main_app.select.play()
            if self.collide_point(*touch.pos):
                self.clear_screen()
                return False

        # 1st button
        if 0.15 < touch.spos[0] < 0.355 and 0.576 < touch.spos[1] < 0.696:
            # if main_app.board[1] == "X":
            #     main_app.board[1] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_1, 1, a_delay), 0)
            #     self.o_1.opacity = 1
            if main_app.board[1] != "O" and main_app.board[1] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[1] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_1, 1, a_delay), 0)
            #     self.o_1.opacity = 0
            # else:
                main_app.board[1] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_1, 1, a_delay), 0)
                self.o_1.opacity = 0
                game.makeMove(main_app.board, "X", 1)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 2nd button
        if 0.380 < touch.spos[0] < 0.611 and 0.576 < touch.spos[1] < 0.696:
            # if main_app.board[2] == "X":
            #     main_app.board[2] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_2, 1, a_delay), 0)
            #     self.o_2.opacity = 1
            if main_app.board[2] != "O" and main_app.board[2] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[2] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_2, 1, a_delay), 0)
            #     self.o_2.opacity = 0
            # else:
                main_app.board[2] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_2, 1, a_delay), 0)
                self.o_2.opacity = 0
                game.makeMove(main_app.board, "X", 2)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 3rd button
        if 0.633 < touch.spos[0] < 0.847 and 0.576 < touch.spos[1] < 0.696:
            # if main_app.board[3] == "X":
            #     main_app.board[3] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_3, 1, a_delay), 0)
            #     self.o_3.opacity = 1
            if main_app.board[3] != "O" and main_app.board[3] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[3] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_3, 1, a_delay), 0)
            #     self.o_3.opacity = 0
            # else:
                main_app.board[3] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_3, 1, a_delay), 0)
                self.o_3.opacity = 0
                game.makeMove(main_app.board, "X", 3)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 4th button
        if 0.15 < touch.spos[0] < 0.355 and 0.437 < touch.spos[1] < 0.567:
            # if main_app.board[4] == "X":
            #     main_app.board[4] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_4, 1, a_delay), 0)
            #     self.o_4.opacity = 1
            if main_app.board[4] != "O" and main_app.board[4] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[4] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_4, 1, a_delay), 0)
            #     self.o_4.opacity = 0
            # else:
                main_app.board[4] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_4, 1, a_delay), 0)
                self.o_4.opacity = 0
                game.makeMove(main_app.board, "X", 4)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 5th button
        if 0.380 < touch.spos[0] < 0.611 and 0.437 < touch.spos[1] < 0.567:
            # if main_app.board[5] == "X":
            #     main_app.board[5] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_5, 1, a_delay), 0)
            #     self.o_5.opacity = 1
            if main_app.board[5] != "O" and main_app.board[5] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[5] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_5, 1, a_delay), 0)
            #     self.o_5.opacity = 0
            # else:
                main_app.board[5] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_5, 1, a_delay), 0)
                self.o_5.opacity = 0
                game.makeMove(main_app.board, "X", 5)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 6th button
        if 0.633 < touch.spos[0] < 0.847 and 0.437 < touch.spos[1] < 0.567:
            # if main_app.board[6] == "X":
            #     main_app.board[6] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_6, 1, a_delay), 0)
            #     self.o_6.opacity = 1
            if main_app.board[6] != "O" and main_app.board[6] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[6] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_6, 1, a_delay), 0)
            #     self.o_6.opacity = 0
            # else:
                main_app.board[6] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_6, 1, a_delay), 0)
                self.o_6.opacity = 0
                game.makeMove(main_app.board, "X", 6)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 7th button
        if 0.15 < touch.spos[0] < 0.355 and 0.304 < touch.spos[1] < 0.423:
            # if main_app.board[7] == "X":
            #     main_app.board[7] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_7, 1, a_delay), 0)
            #     self.o_7.opacity = 1
            if main_app.board[7] != "O" and main_app.board[7] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[7] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_7, 1, a_delay), 0)
            #     self.o_7.opacity = 0
            # else:
                main_app.board[7] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_7, 1, a_delay), 0)
                self.o_7.opacity = 0
                game.makeMove(main_app.board, "X", 7)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 8th button
        if 0.380 < touch.spos[0] < 0.611 and 0.304 < touch.spos[1] < 0.423:
            # if main_app.board[8] == "X":
            #     main_app.board[8] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_8, 1, a_delay), 0)
            #     self.o_8.opacity = 1
            if main_app.board[8] != "O" and main_app.board[8] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[8] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_8, 1, a_delay), 0)
            #     self.o_8.opacity = 0
            # else:
                main_app.board[8] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_8, 1, a_delay), 0)
                self.o_8.opacity = 0
                game.makeMove(main_app.board, "X", 8)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

        # 9th button
        if 0.633 < touch.spos[0] < 0.847 and 0.304 < touch.spos[1] < 0.423:
            # if main_app.board[9] == "X":
            #     main_app.board[9] = "O"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_9, 1, a_delay), 0)
            #     self.o_9.opacity = 1
            if main_app.board[9] != "O" and main_app.board[9] != "X" and self.turn == "player":
                main_app.select.play()
            #     main_app.board[9] = "X"
            #     Clock.schedule_once(partial(self.set_opacity, self.x_9, 1, a_delay), 0)
            #     self.o_9.opacity = 0
            # else:
                main_app.board[9] = "X"
                Clock.schedule_once(partial(self.set_opacity, self.x_9, 1, a_delay), 0)
                self.o_9.opacity = 0
                game.makeMove(main_app.board, "X", 9)
                if game.isWinner(main_app.board, "X"):
                    print('Hooray! You have won the game!')
                    self.gameIsPlaying = False
                    self.manager.current = "win"
                    self.clear_screen()
                    main_app.board = [" "]*10
                else:
                    if game.isBoardFull(main_app.board):
                        print('The game is a tie!')
                        self.gameIsPlaying = False
                        self.manager.current = "tie"
                        self.clear_screen()
                        main_app.board = [" "]*10
                    else:
                        self.turn = 'computer'
                        self.computer_move()
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

    def clear_opacity(self, image, dt):
        anim = Animation(opacity=0, duration=0.35)
        anim.start(image)

    def set_opacity(self, image, opacity, duration, dt):
        anim = Animation(opacity=opacity, duration=duration)
        anim.start(image)


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
                self.manager.current = "intro"
                main_app.board = [' '] * 10
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
                self.manager.current = "intro"
                main_app.board = [' '] * 10
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

class Tie_Screen(Screen):
    def __init__(self, **kwargs):
        super(Tie_Screen, self).__init__(**kwargs)

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
                self.manager.current = "intro"
                main_app.board = [' '] * 10
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
                self.manager.current = "main"
                return False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)


class Main_Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Main_Manager, self).__init__(**kwargs)


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.board = [' '] * 10

    def build(self):
        #Window.size = (540, 960)
        self.app_start = SoundLoader.load('assets/sounds/app_start.wav')
        self.app_start.volume = 0.8
        self.app_start.play()
        self.select = SoundLoader.load('assets/sounds/select.wav')
        self.start = SoundLoader.load('assets/sounds/start.wav')
        self.select.volume = 0.5


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
