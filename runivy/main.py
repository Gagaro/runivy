import random

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Image
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', 0)

GRAVITY = -0.5


class RunivyObject(Widget):
    speed = NumericProperty(0)
    obstacle = False

    def __init__(self, **kwargs):
        super(RunivyObject, self).__init__(**kwargs)
        self.speed = kwargs.get('speed', 4)

    def move(self):
        self.x -= self.speed

    def is_out(self):
        return self.x + self.width <= 0


class RunivyCloud(RunivyObject):
    pass


class RunivySkyscraper(RunivyObject):
    obstacle = True


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
    objects = ListProperty([])
    ground = ObjectProperty(None)
    scroll = NumericProperty(0.0)

    running = True
    next_cloud = 0

    def __init__(self, **kwargs):
        super(RunivyGame, self).__init__(**kwargs)
        self.ground = Image('data/ground.png').texture
        self.ground.wrap = "repeat"

    def should_spawn_obstacle(self):
        return not [obj for obj in self.objects if obj.obstacle]

    def spawn_obstacle(self):
        obstacle = RunivySkyscraper(x=self.width, y=104)
        self.objects.append(obstacle)
        self.add_widget(obstacle)

    def spawn_cloud(self):
        top = self.height - random.randint(100, 400)
        speed = random.randint(1, 8)
        cloud = RunivyCloud(x=self.width, y=top, speed=speed)
        self.objects.append(cloud)
        self.add_widget(cloud, canvas='before')
        self.next_cloud = random.randint(60, 180)

    def move_objects(self):
        for obj in self.objects[:]:
            obj.move()
            if obj.is_out():
                self.remove_widget(obj)
                self.objects.remove(obj)
                if obj.obstacle:
                    self.score.text = str(int(self.score.text) + 1)
        self.scroll = (self.scroll * self.width + 4) % self.width / self.width
        #print(self.scroll)

    def check_obstacles(self):
        for obj in self.objects:
            if obj.obstacle and obj.collide_widget(self.player):
                self.running = False

    def update(self, dt):
        if not self.running:
            return

        self.player.move()

        self.move_objects()
        if self.should_spawn_obstacle():
            self.spawn_obstacle()
        self.check_obstacles()
        if self.next_cloud <= 0:
            self.spawn_cloud()
        else:
            self.next_cloud -= 1


class RunivyApp(App):
    def build(self):
        game = RunivyGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    RunivyApp().run()
