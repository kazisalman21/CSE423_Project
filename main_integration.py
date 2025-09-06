# Main Integration File - 3D Car Driving Game
# Combines all three team member contributions

# Import all team member modules
from core_engine import *  # Member 1: Core Game Engine & Movement
from game_objects import *  # Member 2: Game Objects & Collectibles  
from ui_system import *  # Member 3: UI/UX & Customization

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Global game state
current_game_state = "MENU"

def get_current_game_state():
    """Helper function for UI system"""
    return current_game_state

def set_game_state(new_state):
    """Set the current game state"""
    global current_game_state
    current_game_state = new_state

def integrated_reset_game():
    """Reset game using all three systems"""
    # Apply difficulty settings from Member 3
    settings = apply_difficulty_settings()
    
    # Set difficulty settings for Member 2's object system
    set_difficulty_settings(settings)
    
    # Reset all objects (Member 2)
    reset_all_objects()
    
    # Reset core engine (Member 1)
    handle_restart()
    
    # Update global game timer with difficulty setting
    global game_timer
    game_timer = settings["timer"]

def integrated_idle():
    """Main game loop integrating all systems"""
    global current_game_state
    
    if current_game_state != "PLAY":
        glutPostRedisplay()
        return
    
    if is_game_over:
        glutPostRedisplay() 
        return
    
    # Get frame time
    delta_time = get_delta_time()
    
    # Update Member 2's animations
    update_animations(delta_time)
    
    # Update Member 1's car physics  
    prev_pos = update_car_physics(delta_time)
    
    # Handle collisions between Member 1's car and Member 2's objects
    handle_integrated_collisions(prev_pos, delta_time)
    
    # Update Member 1's timer system
    update_timer(delta_time)
    
    # Check win/lose with Member 2's object counts
    check_integrated_win_lose_conditions()
    
    glutPostRedisplay()

def handle_integrated_collisions(prev_pos, delta_time):
    """Handle collisions between car and all game objects"""
    car_size = [35, 35, 35]
    cheat_active = get_cheat_mode()
    
    # Handle collectible collisions (Member 2)
    handle_collectible_collision(car_pos, car_size)
    handle_bonus_collision(car_pos, car_size)
    
    # Handle ramp collisions and jumping (Member 2 + Member 1 physics)
    jump_force = handle_ramp_collision(car_pos, car_size, car_vz)
    if jump_force > 0:
        global car_vz
        car_vz = jump_force
    
    # Handle wall collisions (Member 1 collision + Member 2 life system)
    for wall in walls:
        if check_collision(car_pos, car_size, wall['pos'], wall['size']):
            