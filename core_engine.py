# Member 1: Core Game Engine & Movement
# Features: 3D Car Movement, Collision Detection, Camera Controls, Timer System, Game States

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# Window size globals
window_w, window_h = 1000, 800

# Core movement and physics variables
car_pos = [0, 0, 20]
car_angle = 0
car_speed = 0
max_speed = 150
cheat_max_speed = 300
acceleration = 120
deceleration = 80
car_vz = 0.0
gravity = 120.0

# Camera system variables
camera_distance = 180
camera_height = 80
fovY = 60

# Timer and game state variables
game_timer = 90.0
is_game_over = False
win_message = ""
last_time = 0

# Game state management
game_state = "MENU"  # MENU, PLAY, COLOR, DIFFICULTY, HOWTO

def get_delta_time():
    """Calculate delta time for smooth movement"""
    global last_time
    current_time = time.time()
    if last_time == 0:
        last_time = current_time
        return 0.016
    delta = current_time - last_time
    last_time = current_time
    return min(delta, 0.05)

def check_collision(obj1_pos, obj1_size, obj2_pos, obj2_size):
    """Advanced collision detection system"""
    obj1_min_x = obj1_pos[0] - obj1_size[0] / 2
    obj1_max_x = obj1_pos[0] + obj1_size[0] / 2
    obj1_min_y = obj1_pos[1] - obj1_size[1] / 2
    obj1_max_y = obj1_pos[1] + obj1_size[1] / 2
    obj1_min_z = obj1_pos[2] - obj1_size[2] / 2
    obj1_max_z = obj1_pos[2] + obj1_size[2] / 2
    
    obj2_min_x = obj2_pos[0] - obj2_size[0] / 2
    obj2_max_x = obj2_pos[0] + obj2_size[0] / 2
    obj2_min_y = obj2_pos[1] - obj2_size[1] / 2
    obj2_max_y = obj2_pos[1] + obj2_size[1] / 2
    obj2_min_z = obj2_pos[2] - obj2_size[2] / 2
    obj2_max_z = obj2_pos[2] + obj2_size[2] / 2
    
    x_overlap = obj1_max_x >= obj2_min_x and obj1_min_x <= obj2_max_x
    y_overlap = obj1_max_y >= obj2_min_y and obj1_min_y <= obj2_max_y
    z_overlap = obj1_max_z >= obj2_min_z and obj1_min_z <= obj2_max_z
    
    return x_overlap and y_overlap and z_overlap

def setupCamera():
    """3D Camera system with following mechanics"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = window_w / float(window_h)
    gluPerspective(fovY, aspect, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Calculate camera position based on car position and angle
    camera_x = car_pos[0] - camera_distance * math.cos(math.radians(car_angle))
    camera_y = car_pos[1] - camera_distance * math.sin(math.radians(car_angle))
    camera_z = car_pos[2] + camera_height
    
    gluLookAt(camera_x, camera_y, camera_z, car_pos[0], car_pos[1], car_pos[2], 0, 0, 1)

def keyboardListener(key, x, y):
    """3D Car Movement System - WASD Controls"""
    global car_speed, car_angle, game_state
    
    # Handle key decoding
    if hasattr(key, "decode"):
        k = key.decode('utf-8').lower()
    else:
        k = chr(key).lower() if isinstance(key, int) else str(key).lower()
    
    # ESC returns to menu at any time
    if ord(k) == 27:  # ESC key
        game_state = "MENU"
        glutPostRedisplay()
        return
    
    if game_state != "PLAY":
        return
        
    # Import cheat_mode from other modules (will be integrated)
    cheat_mode = False  # Placeholder - will be integrated with Member 3's code
    current_max_speed = cheat_max_speed if cheat_mode else max_speed
    
    # Car movement controls
    if k == 'w':  # Forward
        car_speed = min(car_speed + acceleration * 0.3, current_max_speed)
    elif k == 's':  # Backward
        car_speed = max(car_speed - acceleration * 0.3, -current_max_speed * 0.6)
    elif k == 'a' and abs(car_speed) > 5:  # Left turn
        if car_speed > 0:  # Forward
            car_angle += 10
        else:  # Reverse
            car_angle -= 10
    elif k == 'd' and abs(car_speed) > 5:  # Right turn
        if car_speed > 0:  # Forward
            car_angle -= 10
        else:  # Reverse
            car_angle += 10

def specialKeyListener(key, x, y):
    """Camera Controls - Arrow Key System"""
    global camera_distance, camera_height
    
    if game_state != "PLAY":
        return
        
    if key == GLUT_KEY_LEFT:
        camera_distance += 10
    elif key == GLUT_KEY_RIGHT:
        camera_distance = max(10, camera_distance - 10)
    elif key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height = max(10, camera_height - 10)

def update_car_physics(delta_time):
    """Core car physics and movement update"""
    global car_pos, car_speed, car_vz
    
    # Apply deceleration when no input
    if car_speed > 0:
        car_speed = max(0, car_speed - deceleration * delta_time)
    elif car_speed < 0:
        car_speed = min(0, car_speed + deceleration * delta_time)
    
    # Store previous position for collision handling
    prev_pos = car_pos[:]
    
    # Update position based on speed and angle
    car_pos[0] += car_speed * math.cos(math.radians(car_angle)) * delta_time
    car_pos[1] += car_speed * math.sin(math.radians(car_angle)) * delta_time
    
    # Handle vertical movement (jumping)
    car_pos[2] += car_vz * delta_time
    car_vz -= gravity * delta_time
    
    # Ground collision
    if car_pos[2] <= 20:
        car_pos[2] = 20
        car_vz = 0
    
    return prev_pos

def update_timer(delta_time):
    """Timer System - Countdown and Game End Logic"""
    global game_timer, is_game_over, win_message
    
    if game_state != "PLAY" or is_game_over:
        return
        
    game_timer -= delta_time
    
    # Check timer-based game end condition
    if game_timer <= 0:
        is_game_over = True
        win_message = "TIME'S UP - Game Over!"

def check_win_lose_conditions():
    """Game States - Win/Lose/Restart Logic"""
    global is_game_over, win_message
    
    # These will be integrated with Member 2's collectible system
    # Placeholder conditions - will be connected to actual game objects
    collectibles_count = 0  # Will be imported from Member 2's code
    bonus_collectibles_count = 0  # Will be imported from Member 2's code
    current_lives = 3  # Will be imported from Member 2's code
    
    # Win condition: all collectibles collected
    if collectibles_count == 0 and bonus_collectibles_count == 0:
        is_game_over = True
        # Score will be imported from Member 2's code
        win_message = f"YOU WIN! Final Score: 0"  # Placeholder
    
    # Lose condition: no lives left
    if current_lives <= 0:
        is_game_over = True
        win_message = "GAME OVER - No Lives Left!"

def handle_restart():
    """Restart Game Functionality"""
    global car_pos, car_angle, car_speed, car_vz, is_game_over, win_message, game_timer
    
    # Reset car state
    car_pos = [0, 0, 20]
    car_angle = 0
    car_speed = 0
    car_vz = 0.0
    
    # Reset game state
    is_game_over = False
    win_message = ""
    game_timer = 90.0  # Will be adjusted based on difficulty from Member 3
    
    # Reset other game elements (will be integrated with other members' code)
    # Member 2 will handle: lives, score, collectibles reset
    # Member 3 will handle: difficulty settings application

def idle():
    """Main game loop - coordinates all core systems"""
    global spin_angle  # Will be used by Member 2 for object animations
    
    if game_state != "PLAY":
        glutPostRedisplay()
        return
        
    if is_game_over:
        glutPostRedisplay()
        return
    
    # Get frame time
    delta_time = get_delta_time()
    
    # Update core systems
    prev_pos = update_car_physics(delta_time)
    update_timer(delta_time)
    
    # Handle collisions (will be integrated with Member 2's objects)
    handle_collisions(prev_pos)  # This will be implemented when integrating
    
    # Check win/lose conditions
    check_win_lose_conditions()
    
    glutPostRedisplay()

# Integration functions (to be completed when combining with other members)
def handle_collisions(prev_pos):
    """Handle all collision scenarios - will be integrated with Member 2's objects"""
    # This will be implemented when integrating all three parts
    pass

def draw_car():
    """Basic car rendering - will be enhanced with Member 3's color system"""
    glPushMatrix()
    glTranslatef(car_pos[0], car_pos[1], car_pos[2])
    glRotatef(car_angle, 0, 0, 1)
    
    # Basic car color (will be integrated with Member 3's customization)
    glColor3f(0, 0, 1)  # Default blue
    glutSolidCube(35)
    
    # Car details
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(-20, 0, 8)
    glScalef(0.2, 1.5, 0.3)
    glutSolidCube(20)
    glPopMatrix()
    
    # Wheels
    glColor3f(0.1, 0.1, 0.1)
    for (x, y) in [(12, 18), (12, -18), (-12, 18), (-12, -18)]:
        glPushMatrix()
        glTranslatef(x, y, -8)
        glutSolidCube(8)
        glPopMatrix()
    
    glPopMatrix()

# Main initialization for core engine
def init_core_engine():
    """Initialize core engine components"""
    global last_time
    last_time = 0
    
    # Set up OpenGL depth testing
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.2, 1.0)

# Export functions for integration
__all__ = [
    'check_collision', 'setupCamera', 'keyboardListener', 'specialKeyListener',
    'update_car_physics', 'update_timer', 'check_win_lose_conditions',
    'handle_restart', 'idle', 'draw_car', 'init_core_engine',
    'car_pos', 'car_angle', 'car_speed', 'game_timer', 'is_game_over', 'win_message'
]