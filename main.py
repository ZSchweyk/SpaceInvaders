import os
import time
import random

os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import sys
from threading import Thread


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity  # x and y components of the ball's velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)  # ball's offset relative to center of paddle
            bounced = Vector(-1 * vx, vy)  # a Vector representing the initial speed of the ball after bounced
            vel = bounced * 1.05  # increases the x and y components of the ball's velocity by a factor of 10%
            ball.velocity = min(vel.x, 20) if vel.x > 0 else max(vel.x,
                                                                 -20), vel.y + offset  # sets the ball's new velocity, accounting for the offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(PongGame, self).__init__(*args, **kwargs)
        self._keyboard1 = Window.request_keyboard(self._keyboard_closed, self)

        self._keyboard1.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard1.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard1 = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        increment = self.height / 50
        if keycode[1] == "escape":
            sys.exit(0)

        if keycode[1] == "up":
            self.player2.center_y += increment
        elif keycode[1] == "down":
            self.player2.center_y -= increment
        elif keycode[1] == "a":
            self.player1.center_y += increment
        elif keycode[1] == "z":
            self.player1.center_y -= increment

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
            self.player1.center_y = self.player2.center_y = self.height / 2
            time.sleep(.75)
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            self.player1.center_y = self.player2.center_y = self.height / 2
            time.sleep(.75)

    def on_touch_move(self, touch):
        if touch.x < self.width / 2:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 2:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1 / 600)
        return game


if __name__ == '__main__':
    PongApp().run()
