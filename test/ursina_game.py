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

# Create some platforms (low to high, accending order)
platforms = [
    Entity(model='cube', scale=(2, 1, 1), position=(0, -2, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(3, 1, 1), position=(4, 2, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(2, 1, 1), position=(-3, 4, 0), color=color.gray, collider='box')
]

# Function to spawn a random platform
def spawn_random_platform():
    highest_platform = max(platforms, key=lambda p: p.y)
    xneg = random.randint(-5, -3)
    xpos = random.randint(3, 5)
    new_x = highest_platform.x + random.choice([xneg, xpos])
    new_y = highest_platform.y + random.uniform(3, 4)
        
    new_platform = Entity(model='cube', scale=(random.uniform(2, 3), 1, 1), position=(new_x, new_y, 0), color=color.gray, collider='box')
    platforms.append(new_platform)


def update():
    global score
    highest_platform = max(platforms, key=lambda p: p.y)
    # Check if the player is within a certain distance from the highest platform
    if player.y > highest_platform.y + 4:
        spawn_random_platform()
        score += 1
        score_text.text = f'Score: {score}'

# Initialize score
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2, color=color.white)


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')
input_handler.bind('w', 'space')

app.run()