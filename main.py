import os
import time
import random

from kivy.uix.label import Label

os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import sys
from threading import Thread
import numpy as np
from kivy.lang import Builder


def bounce(widget, ball):
    if widget.collide_widget(ball):
        vx, vy = ball.velocity  # x and y components of the ball's velocity
        offset = (ball.center_x - widget.center_x) / (widget.width / 2)  # ball's offset relative to center of paddle
        bounced = Vector(vx, -1 * vy)  # a Vector representing the initial speed of the ball after bounced
        vel = bounced * 1.025  # increases the x and y components of the ball's velocity by a factor of 10%
        ball.velocity = min(vel.x + offset, 17) if vel.x + offset > 0 else max(vel.x + offset, -17), \
                        min(vel.y, 17) if vel.y > 0 else max(vel.y,
                                                             -17)  # sets the ball's new velocity, accounting for the offset


class Alien(Widget):
    image_path = "SpaceInvader.png"
    alien_size = .3, .3


class Paddle(Widget):
    score = NumericProperty(0)


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Game(Widget):
    ball = ObjectProperty(None)
    paddle = ObjectProperty(None)
    aliens = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard1 = Window.request_keyboard(self._keyboard_closed, self)

        self._keyboard1.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard1.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard1 = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        increment = self.width / 50
        if keycode[1] == "escape":
            sys.exit(0)

        if keycode[1] == "left":
            self.paddle.center_x -= increment
        elif keycode[1] == "right":
            self.paddle.center_x += increment

    def serve_ball(self, vel=(0, -4)):
        self.ball.center = self.center
        self.ball.velocity = vel

        # a = Alien(center_x=.75, center_y=.8)
        #
        # self.add_widget(a)

        # for i in np.arange(.1, 1, .1):
        #     alien = Alien(center_x=50+i, center_y=.7)
        #     self.add_widget(alien)

        # alien = Alien(pos=(10, 100))
        # self.add_widget(alien)
        # print(len(self.children))
        # print(alien.get_root_window())
        # print(self.pos)

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        bounce(self.paddle, self.ball)
        # self.paddle.bounce_ball(self.ball)

        # bounce ball off the top or sides
        if self.ball.top > self.top:
            self.ball.velocity_y *= -1
        elif self.ball.x + self.ball.width > self.width or self.ball.x < self.x:
            self.ball.velocity_x *= -1

        # went off to the bottom side to lose a life?
        if self.ball.y < self.y:
            print("Lost")
            time.sleep(2)
            self.paddle.center_x = self.width / 2
            self.serve_ball()
        if self.ball.x > self.width:
            pass

    def on_touch_move(self, touch):
        self.paddle.center_x = touch.x



class SpaceInvaders(App):
    def build(self):
        game = Game()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1 / 600)
        return game


# Need the line below in order for the program to run on Ubuntu. I don't know why; the .kv file is named appropriately
# Builder.load_file("SpaceInvaders.kv")

if __name__ == '__main__':
    SpaceInvaders().run()
