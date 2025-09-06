# Features: Collectible Items, Bonus Collectibles, Jump Ramps, Life System, Score Tracking

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Arena and grid constants
ARENA_SIZE = 350
GRID_SIZE = 500

# Game objects lists
walls = []
collectibles = []
bonus_collectibles = []
static_obstacles = []
ramps = []

# Score and life system
score = 0
max_lives = 3
current_lives = 3

# Animation variables
spin_angle = 0.0
_quad = None

# Difficulty-based object counts (will be set by Member 3's difficulty system)
current_difficulty_settings = {
    "collectibles_count": 16,
    "bonus_count": 4,
    "static_obstacles_count": 12
}

def init_game_objects():
    """Initialize game objects system"""
    global _quad
    _quad = gluNewQuadric()

def generate_random_position(min_distance_from_center=50, max_distance_from_center=300, height=15):
    """Generate a random position that's not too close to the center (car spawn)"""
    while True:
        x = random.uniform(-max_distance_from_center, max_distance_from_center)
        y = random.uniform(-max_distance_from_center, max_distance_from_center)
        
        # Make sure it's not too close to center and within arena bounds
        distance_from_center = math.sqrt(x * x + y * y)
        if (distance_from_center >= min_distance_from_center and 
            abs(x) < ARENA_SIZE - 30 and abs(y) < ARENA_SIZE - 30):
            return [x, y, height]

def check_position_conflicts(new_pos, existing_objects, min_distance=60):
    """Check if a new position conflicts with existing objects"""
    for obj in existing_objects:
        distance = math.sqrt((new_pos[0] - obj['pos'][0])**2 + (new_pos[1] - obj['pos'][1])**2)
        if distance < min_distance:
            return True
    return False

def generate_random_collectibles(count):
    """Feature 1: Collectible Items - Yellow cubes worth 10 points"""
    global collectibles
    collectibles_list = []
    all_objects = walls[:]  # Start with walls to avoid conflicts
    
    for _ in range(count):
        attempts = 0
        while attempts < 50:  # Prevent infinite loop
            pos = generate_random_position(min_distance_from_center=60, max_distance_from_center=280, height=15)
            if not check_position_conflicts(pos, all_objects, min_distance=50):
                collectible = {
                    'pos': pos[:], 
                    'size': [15, 15, 15],
                    'collected': False,
                    'points': 10
                }
                collectibles_list.append(collectible)
                all_objects.append(collectible)
                break
            attempts += 1
    
    return collectibles_list

def generate_random_bonus_collectibles(count, existing_objects):
    """Feature 2: Bonus Collectibles - Gold cylinders worth 50 points"""
    global bonus_collectibles
    bonus_list = []
    all_objects = existing_objects[:]
    
    for _ in range(count):
        attempts = 0
        while attempts < 50:
            pos = generate_random_position(min_distance_from_center=80, max_distance_from_center=320, height=20)
            if not check_position_conflicts(pos, all_objects, min_distance=70):
                bonus = {
                    'pos': pos[:], 
                    'size': [20, 20, 30],
                    'collected': False,
                    'points': 50
                }
                bonus_list.append(bonus)
                all_objects.append(bonus)
                break
            attempts += 1
    
    return bonus_list

def generate_jump_ramps():
    """Feature 3: Jump Ramps - Cyan ramps with jump physics"""
    global ramps
    ramps = []
    ramp_positions = [
        [160, 160, 15], 
        [-160, -160, 15],
        [160, -160, 15],
        [-160, 160, 15]
    ]
    
    for pos in ramp_positions:
        ramp = {
            'pos': pos[:], 
            'size': [30, 30, 30],
            'jump_force': 120.0
        }
        ramps.append(ramp)
    
    return ramps

def generate_static_obstacles(count, existing_objects):
    """Generate static obstacles that cause life loss"""
    obstacles_list = []
    all_objects = existing_objects[:]
    
    obstacle_types = [
        {'size': [25, 25, 40], 'color': [0.9, 0.1, 0.1]},  # Red
        {'size': [40, 20, 25], 'color': [0.1, 0.9, 0.1]},  # Green
        {'size': [20, 40, 25], 'color': [0.1, 0.1, 0.9]},  # Blue
        {'size': [30, 30, 50], 'color': [0.9, 0.9, 0.1]},  # Yellow
        {'size': [35, 15, 20], 'color': [0.9, 0.1, 0.9]},  # Magenta
        {'size': [25, 30, 35], 'color': [0.1, 0.9, 0.9]},  # Cyan
        {'size': [45, 25, 20], 'color': [1.0, 0.5, 0.0]},  # Orange
        {'size': [20, 20, 60], 'color': [0.5, 0.0, 0.5]},  # Purple
    ]
    
    for i in range(count):
        attempts = 0
        while attempts < 50:
            pos = generate_random_position(min_distance_from_center=70, max_distance_from_center=300, height=25)
            obstacle_type = random.choice(obstacle_types)
            
            if not check_position_conflicts(pos, all_objects, min_distance=65):
                obstacle = {
                    'pos': pos[:],
                    'size': obstacle_type['size'][:],
                    'color': obstacle_type['color'][:],
                    'damages_life': True
                }
                obstacles_list.append(obstacle)
                all_objects.append(obstacle)
                break
            attempts += 1
    
    return obstacles_list

def generate_arena_walls():
    """Generate arena boundary walls"""
    walls = []
    wall_height = 50
    wall_thickness = 20
    
    # Top and bottom walls
    for i in range(-9, 10):
        walls.append({'pos': [i * 40, ARENA_SIZE, wall_height/2], 
                     'size': [wall_thickness, wall_thickness, wall_height]})
        walls.append({'pos': [i * 40, -ARENA_SIZE, wall_height/2], 
                     'size': [wall_thickness, wall_thickness, wall_height]})
    
    # Left and right walls  
    for i in range(-8, 9):
        walls.append({'pos': [-ARENA_SIZE, i * 40, wall_height/2], 
                     'size': [wall_thickness, wall_thickness, wall_height]})
        walls.append({'pos': [ARENA_SIZE, i * 40, wall_height/2], 
                     'size': [wall_thickness, wall_thickness, wall_height]})
    
    # Internal structural walls
    internal_walls = [
        {'pos': [150, 150, 25], 'size': [30, 30, 50]},
        {'pos': [-150, -150, 25], 'size': [30, 30, 50]},
        {'pos': [150, -150, 25], 'size': [30, 30, 50]},
        {'pos': [-150, 150, 25], 'size': [30, 30, 50]},
    ]
    walls.extend(internal_walls)
    
    return walls

def reset_all_objects():
    """Reset all game objects for new game"""
    global walls, collectibles, bonus_collectibles, static_obstacles, ramps
    global score, current_lives
    
    # Reset score and life system
    score = 0
    current_lives = max_lives
    
    # Generate arena walls
    walls = generate_arena_walls()
    
    # Get counts from difficulty settings
    collectible_count = current_difficulty_settings["collectibles_count"]
    bonus_count = current_difficulty_settings["bonus_count"] 
    obstacle_count = current_difficulty_settings["static_obstacles_count"]
    
    # Generate collectibles
    collectibles = generate_random_collectibles(collectible_count)
    
    # Generate bonus collectibles
    all_existing = walls + collectibles
    bonus_collectibles = generate_random_bonus_collectibles(bonus_count, all_existing)
    
    # Generate static obstacles
    all_existing = walls + collectibles + bonus_collectibles
    static_obstacles = generate_static_obstacles(obstacle_count, all_existing)
    
    # Generate jump ramps
    ramps = generate_jump_ramps()

def update_score(points):
    """Feature 5: Score Tracking - Point accumulation system"""
    global score
    score += points

def lose_life():
    """Feature 4: Life System - Lose life on collision"""
    global current_lives
    if current_lives > 0:
        current_lives -= 1
    return current_lives

def get_lives():
    """Get current lives count"""
    return current_lives

def get_score():
    """Get current score"""
    return score

def handle_collectible_collision(car_pos, car_size):
    """Handle collisions with regular collectibles"""
    global collectibles
    
    for collectible in collectibles[:]:
        if not collectible['collected']:
            # Import collision function from Member 1
            # For now, using placeholder collision detection
            if check_distance_collision(car_pos, collectible['pos'], car_size, collectible['size']):
                collectibles.remove(collectible)
                update_score(collectible['points'])
                return True
    return False

def handle_bonus_collision(car_pos, car_size):
    """Handle collisions with bonus collectibles"""
    global bonus_collectibles
    
    for bonus in bonus_collectibles[:]:
        if not bonus['collected']:
            if check_distance_collision(car_pos, bonus['pos'], car_size, bonus['size']):
                bonus_collectibles.remove(bonus)
                update_score(bonus['points'])
                return True
    return False

def handle_ramp_collision(car_pos, car_size, car_vz):
    """Feature 3: Jump Ramps - Handle ramp collisions and jumping"""
    for ramp in ramps:
        if check_distance_collision(car_pos, ramp['pos'], car_size, ramp['size']):
            # Only jump if car is on ground
            if car_pos[2] <= 21 and car_vz == 0:
                return ramp['jump_force']  # Return jump velocity
    return 0

def handle_obstacle_collision(car_pos, car_size):
    """Handle collisions with static obstacles (causes life loss)"""
    for obstacle in static_obstacles:
        if check_distance_collision(car_pos, obstacle['pos'], car_size, obstacle['size']):
            if obstacle.get('damages_life', False):
                return True
    return False

def check_distance_collision(pos1, pos2, size1, size2):
    """Simple distance-based collision detection (placeholder)"""
    # This will be replaced with Member 1's collision detection
    distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    avg_size = (max(size1) + max(size2)) / 2
    return distance < avg_size

def update_animations(delta_time):
    """Update object animations"""
    global spin_angle
    spin_angle = (spin_angle + 120.0 * delta_time) % 360.0

def calculate_camera_distance(pos, car_pos, car_angle, camera_distance, camera_height):
    """Calculate distance from camera for depth sorting"""
    camera_x = car_pos[0] - camera_distance * math.cos(math.radians(car_angle))
    camera_y = car_pos[1] - camera_distance * math.sin(math.radians(car_angle))
    camera_z = car_pos[2] + camera_height
    
    dx = pos[0] - camera_x
    dy = pos[1] - camera_y  
    dz = pos[2] - camera_z
    
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def get_all_objects_sorted(car_pos, car_angle, camera_distance, camera_height):
    """Get all objects sorted by distance from camera for proper rendering"""
    all_objects = []
    
    # Add walls
    for wall in walls:
        all_objects.append({
            'type': 'wall',
            'obj': wall,
            'distance': calculate_camera_distance(wall['pos'], car_pos, car_angle, camera_distance, camera_height)
        })
    
    # Add collectibles  
    for collectible in collectibles:
        all_objects.append({
            'type': 'collectible',
            'obj': collectible,
            'distance': calculate_camera_distance(collectible['pos'], car_pos, car_angle, camera_distance, camera_height)
        })
    
    # Add bonus collectibles
    for bonus in bonus_collectibles:
        all_objects.append({
            'type': 'bonus',
            'obj': bonus,
            'distance': calculate_camera_distance(bonus['pos'], car_pos, car_angle, camera_distance, camera_height)
        })
    
    # Add static obstacles
    for obstacle in static_obstacles:
        all_objects.append({
            'type': 'obstacle', 
            'obj': obstacle,
            'distance': calculate_camera_distance(obstacle['pos'], car_pos, car_angle, camera_distance, camera_height)
        })
    
    # Add ramps
    for ramp in ramps:
        all_objects.append({
            'type': 'ramp',
            'obj': ramp,
            'distance': calculate_camera_distance(ramp['pos'], car_pos, car_angle, camera_distance, camera_height)
        })
    
    # Sort by distance (furthest first for proper depth rendering)
    all_objects.sort(key=lambda x: x['distance'], reverse=True)
    return all_objects

def draw_objects(car_pos, car_angle, camera_distance, camera_height):
    """Render all game objects with proper depth sorting"""
    global _quad
    
    # Get sorted objects
    sorted_objects = get_all_objects_sorted(car_pos, car_angle, camera_distance, camera_height)
    
    # Draw objects from back to front
    for item in sorted_objects:
        obj_type = item['type']
        obj = item['obj']
        
        glPushMatrix()
        
        if obj_type == 'wall':
            # Draw walls
            glColor3f(0.6, 0.3, 0.1)
            glTranslatef(obj['pos'][0], obj['pos'][1], obj['pos'][2])
            glScalef(obj['size'][0]/50, obj['size'][1]/50, obj['size'][2]/50)
            glutSolidCube(50)
            
        elif obj_type == 'collectible':
            # Feature 1: Draw collectible items (yellow spinning cubes)
            glColor3f(1, 1, 0)  # Yellow
            glTranslatef(obj['pos'][0], obj['pos'][1], obj['pos'][2])
            glRotatef(spin_angle, 0, 0, 1)
            glutSolidCube(obj['size'][0])
            
        elif obj_type == 'bonus':
            # Feature 2: Draw bonus collectibles (gold spinning cylinders)
            glColor3f(1, 0.8, 0)  # Gold
            glTranslatef(obj['pos'][0], obj['pos'][1], obj['pos'][2])
            glRotatef(spin_angle * 2, 0, 0, 1)
            glRotatef(90, 1, 0, 0)
            if _quad is not None:
                gluCylinder(_quad, 10, 10, obj['size'][2], 8, 1)
                
        elif obj_type == 'obstacle':
            # Draw static obstacles
            glColor3f(obj['color'][0], obj['color'][1], obj['color'][2])
            glTranslatef(obj['pos'][0], obj['pos'][1], obj['pos'][2])
            glScalef(obj['size'][0]/50, obj['size'][1]/50, obj['size'][2]/50)
            glutSolidCube(50)
            
        elif obj_type == 'ramp':
            # Feature 3: Draw jump ramps (cyan spinning blocks)
            glColor3f(0, 0.8, 0.8)  # Cyan
            glTranslatef(obj['pos'][0], obj['pos'][1], obj['pos'][2])
            glRotatef(spin_angle * 0.5, 1, 1, 0)
            glScalef(obj['size'][0]/50, obj['size'][1]/50, obj['size'][2]/50)
            glutSolidCube(50)
            
        glPopMatrix()

def draw_arena():
    """Draw the arena floor"""
    glBegin(GL_QUADS)
    glColor3f(0.1, 0.6, 0.1)  # Green floor
    glVertex3f(-GRID_SIZE, -GRID_SIZE, 0)
    glVertex3f(GRID_SIZE, -GRID_SIZE, 0)
    glVertex3f(GRID_SIZE, GRID_SIZE, 0)
    glVertex3f(-GRID_SIZE, GRID_SIZE, 0)
    glEnd()

def get_collectibles_count():
    """Get remaining collectibles count"""
    return len(collectibles)

def get_bonus_count():
    """Get remaining bonus collectibles count"""
    return len(bonus_collectibles)

def get_obstacles_count():
    """Get static obstacles count"""
    return len(static_obstacles)

def set_difficulty_settings(settings):
    """Set object counts based on difficulty (called by Member 3)"""
    global current_difficulty_settings
    current_difficulty_settings = settings

# Export functions for integration
__all__ = [
    'init_game_objects', 'reset_all_objects', 'update_score', 'lose_life', 'get_lives', 'get_score',
    'handle_collectible_collision', 'handle_bonus_collision', 'handle_ramp_collision', 
    'handle_obstacle_collision', 'update_animations', 'draw_objects', 'draw_arena',
    'get_collectibles_count', 'get_bonus_count', 'get_obstacles_count', 'set_difficulty_settings',
    'walls', 'collectibles', 'bonus_collectibles', 'static_obstacles', 'ramps',
    'score', 'current_lives', 'max_lives'
]
