from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', 0)

GRAVITY = -0.5


class RunivyObstacle(Widget):

    def move(self):
        self.x -= 4

    def is_out(self):
        return self.x + self.width <= 0


class RunivyPlayer(Widget):
    jumping = BooleanProperty(False)
    velocity = NumericProperty(0)
    source = StringProperty("atlas://data/runivy/dino-run-1")

    # Used to animate our widget
    frame_per_picture = 9
    current_animation_frame = 0
    animation = [
        "atlas://data/runivy/dino-run-1",
        "atlas://data/runivy/dino-run-2",
        "atlas://data/runivy/dino-run-3",
        "atlas://data/runivy/dino-run-2",
    ]

    def stop(self):
        self.jumping = False
        self.y = 104
        self.velocity = 0

    def _update_source(self):
        if self.jumping:
            self.source = "atlas://data/runivy/dino-jump"
        else:
            current_picture = int(self.current_animation_frame / self.frame_per_picture)
            self.source = self.animation[current_picture]
            self.current_animation_frame = (self.current_animation_frame + 1) % (self.frame_per_picture * len(self.animation))

    def move(self):
        self._update_source()
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
    score = ObjectProperty(None)
    obstacles = ListProperty([])

    running = True

    def spawn_obstacle(self):
        obstacle = RunivyObstacle(x=self.width, y=104)
        self.obstacles.append(obstacle)
        self.add_widget(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.is_out():
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
                self.score.text = str(int(self.score.text) + 1)

    def check_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.collide_widget(self.player):
                self.running = False

    def update(self, dt):
        if not self.running:
            return

        self.player.move()

        self.move_obstacles()
        if not self.obstacles:
            self.spawn_obstacle()
        self.check_obstacles()


class RunivyApp(App):
    def build(self):
        game = RunivyGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    RunivyApp().run()
