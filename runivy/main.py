from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', 0)

GRAVITY = -0.5


class RunivyPlayer(Widget):
    jumping = BooleanProperty(False)
    velocity = NumericProperty(0)

    def stop(self):
        self.jumping = False
        self.y = 104
        self.velocity = 0

    def move(self):
        self.y += self.velocity
        self.velocity += GRAVITY
        if self.y < 104:
            self.stop()

    def on_touch_down(self, touch):
        if not self.jumping:
            self.velocity = 14.0
            self.jumping = True

    def on_touch_up(self, touch):
        if self.velocity > 6.0:
            self.velocity = 6.0


class RunivyGame(Widget):
    player = ObjectProperty(None)

    running = True

    def update(self, dt):
        if not self.running:
            return

        self.player.move()


class RunivyApp(App):
    def build(self):
        game = RunivyGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    RunivyApp().run()
