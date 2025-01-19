import json
import pyglet
from game.controls import Controls
import pymunk
from typing import Any
from .entities.player import Player
from .tilemap_factory import tilemap_factory
from .camera import Camera
from tileset_manager import AutotileTile

with open("game/config.json", "r") as file:
    config_data = json.load(file)

global_scale = config_data["global_scale"]
window_width = config_data["window_width"]
window_height = config_data["window_height"]

zoom_level = 1


class Game:
    entities: list[Any] = []

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(window_width, window_height)

        self.camera = Camera(self.window)
        self.camera.zoom = zoom_level

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        # Initialize player
        player = Player(self.space)
        self.entities.append(player)
        self.player = player

        # player.set_position(
        #     window_width / 2, window_height / 2
        # )
        # player.set_scale(config_data["global_scale"], config_data["global_scale"])
        player.set_angle(180)

        self.tilemap_renderer = tilemap_factory()

        self.keys = pyglet.window.key.KeyStateHandler()
        self.controls = Controls(self.keys, self.player)

        def create_tile_callback(grid_x, grid_y):
            return AutotileTile((grid_x, grid_y), "wall")

        self.window.push_handlers(
            self.keys,
            self.tilemap_renderer.create_tile_on_click(
                self.tilemap_renderer.tilemap.layers["walls"], create_tile_callback
            ),
        )

    def update(self, dt):
        self.controls.update(dt)

        self.window.clear()

        self.camera.begin()

        self.tilemap_renderer.draw()

        self.player.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
