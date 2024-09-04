from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import random

app = Ursina()

# Create the player
player = PlatformerController2d()
player.x=5
player.y = raycast(player.world_position, player.down).world_point[1] + .01
camera.add_script(SmoothFollow(target=player, offset=[0,5,-30], speed=4))

# Function to create ground segments
def create_ground_segment(position):
    return Entity(model='cube', scale=(10, 1, 1), position=position, color=color.green, collider='box')

# Create multiple ground segments to simulate an infinite ground
ground_segments = [create_ground_segment((i * 10, -4, 0)) for i in range(-10, 11)]

# Create some platforms
platform1 = Entity(model='cube', scale=(3, 1, 1), position=(4, 2, 0), color=color.gray, collider='box')
platform2 = Entity(model='cube', scale=(2, 1, 1), position=(-3, 4, 0), color=color.gray, collider='box')
platform3 = Entity(model='cube', scale=(2, 1, 1), position=(0, -2, 0), color=color.gray, collider='box')

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')
input_handler.bind('w', 'space')

app.run()