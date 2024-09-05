from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import random
import sys

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

# Define highest_platform_landed_on
highest_platform_landed_on = platforms[2]

# Flag to track if advancements have been shown
advancements_shown = []

# List of advancements with different thresholds, messages, and colors
advancements = [
    {'threshold': 500, 'message': 'Congratulations! You reached 500 points!', 'color': color.yellow},
    {'threshold': 1000, 'message': 'Amazing! 1000 points achieved!', 'color': color.orange},
    {'threshold': 1500, 'message': 'Incredible! 1500 points!', 'color': color.blue},
    {'threshold': 5000, 'message': 'You Beat The Game!!!', 'color': color.red}
]

# Function to show advancement text
def show_advancement(advancement):
    text = Text(text=advancement['message'], position=(-0.5, 0), scale=2, color=advancement['color'], enabled=True)
    invoke(lambda: text.disable(), delay=2)  # Hide the text after 2 seconds

# Update function
def update():
    global highest_platform_landed_on, advancements_shown
    highest_platform_landed_on = platforms[-1]
    # Update the player's height and points
    height = player.y
    points = int(height * 10) + 35  # Calculate points based on height (adjust multiplier as needed)
    points_display.text = f'Points: {points}'

    highest_platform = max(platforms, key=lambda p: p.y)
    # Check if the player is within a certain distance from the highest platform
    if player.y > highest_platform.y + 4:
        spawn_random_platform()

    # Check if the player has landed on a new highest platform
    if player.intersects(highest_platform_landed_on).hit:
        spawn_random_platform()

    # Check for advancements
    for advancement in advancements:
        if points >= advancement['threshold'] and advancement['threshold'] not in advancements_shown:
            show_advancement(advancement)
            advancements_shown.append(advancement['threshold'])

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

    # Reset the advancements
    global advancements_shown
    advancements_shown = []

def quit_game():
    print("Quit Game")
    sys.exit()

# Create buttons
restart_button = Button(text='Restart', color=color.azure, scale=(0.2, 0.1), position=(-0.7, 0.4), on_click=restart_game)
quit_button = Button(text='Quit', color=color.red, scale=(0.2, 0.1), position=(0.7, 0.4), on_click=quit_game)

app.run()
