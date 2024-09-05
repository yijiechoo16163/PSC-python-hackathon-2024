from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import random

app = Ursina()

# Create the player
player = PlatformerController2d()
player.x = 5
player.y = raycast(player.world_position, player.down).world_point[1] + .01
camera.add_script(SmoothFollow(target=player, offset=[0, 5, -30], speed=4))

# Function to create ground segments
def create_ground_segment(position):
    return Entity(model='cube', scale=(10, 1, 1), position=position, color=color.green, collider='box')

# Create multiple ground segments to simulate an infinite ground
ground_segments = [create_ground_segment((i * 10, -4, 0)) for i in range(-10, 11)]

# Create some platforms (low to high, ascending order)
platforms = [
    Entity(model='cube', scale=(2, 1, 1), position=(0, -2, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(3, 1, 1), position=(4, 2, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(2, 1, 1), position=(-2, 4, 0), color=color.gray, collider='box')
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

# Points display
points_display = Text(text='Points: 0', position=(-.5, .45), scale=2, color=color.white)

# Track the highest platform the player has landed on
highest_platform_landed_on = platforms[2]

def update():
    global highest_platform_landed_on
    highest_platform_landed_on = platforms[-1]
    
    # Update the player's height and points
    height = player.y
    points = int(height * 10) + 35  # Calculate points based on height
    points_display.text = f'Points: {points}'

    # Check if the player has landed on a new highest platform
    if player.intersects(highest_platform_landed_on).hit:
        highest_platform_landed_on = max(platforms, key=lambda p: p.y)
        spawn_random_platform()

# Restart game function
def restart_game():
    # Reset player position
    player.position = (5, 0, 0)
    
    # Reset the points
    points_display.text = 'Points: 0'
    
    # Reset the platforms (clear old platforms and add initial ones)
    for platform in platforms:
        destroy(platform)
    platforms.clear()
    
    platforms.append(Entity(model='cube', scale=(2, 1, 1), position=(0, -2, 0), color=color.gray, collider='box'))
    platforms.append(Entity(model='cube', scale=(3, 1, 1), position=(4, 2, 0), color=color.gray, collider='box'))
    platforms.append(Entity(model='cube', scale=(2, 1, 1), position=(-2, 4, 0), color=color.gray, collider='box'))

    # Reset the highest platform landed on
    global highest_platform_landed_on
    highest_platform_landed_on = platforms[2]

def quit_game():
    print("Quit Game")
    sys.exit()

# Add buttons using Ursina's Button class
restart_button = Button(text='Restart', color=color.azure, scale=(0.2, 0.1), position=(-0.7, 0.4), on_click=restart_game)
quit_button = Button(text='Quit', color=color.red, scale=(0.2, 0.1), position=(0.7, 0.4), on_click=quit_game)

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')
input_handler.bind('w', 'space')

app.run()
