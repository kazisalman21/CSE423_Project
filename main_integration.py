try:
    from member1_core_movement import *
    from member2_game_world import *  
    from member3_ui_customization import *
    print("All member modules loaded successfully!")
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all three member files are in the same directory")
    exit(1)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def integrated_reset_game():
    """Reset game using all three member systems"""
    print("Resetting game with all systems...")
    
    # Get difficulty settings from Member 3
    settings = apply_difficulty_settings()
    
    # Reset Member 1's core systems
    reset_game()
    global game_timer, max_speed, acceleration
    game_timer = settings["timer"]
    max_speed = settings["max_speed"] 
    acceleration = settings["acceleration"]
    
    # Reset Member 2's game world with difficulty settings
    set_difficulty_object_counts(
        settings["collectibles_count"],
        settings["bonus_count"], 
        settings["static_obstacles_count"]
    )
    
    # Member 3's UI systems maintain their state (colors, difficulty, etc.)
    print(f"Game reset complete - Difficulty: {get_difficulty_mode()}")

def integrated_handle_collisions(prev_pos, delta_time):
    """Handle all collision scenarios using integrated systems"""
    car_size = [35, 35, 35]
    cheat_active = get_cheat_mode()
    
    # Use Member 2's collision handler with Member 1's collision detection
    collision_results = handle_all_collisions(car_pos, car_size, car_vz, check_collision)
    
    # Handle collision consequences
    if collision_results['wall_hit'] or collision_results['obstacle_hit']:
        if not cheat_active:
            # Reset car position (Member 1 physics)
            car_pos[0], car_pos[1] = prev_pos[0], prev_pos[1]
            global car_speed
            car_speed = 0
            
            # Life already lost in Member 2's handler
            print(f"Collision! Lives remaining: {get_lives()}")
    
    # Handle jump from ramps (Member 1 physics + Member 2 ramps)
    if collision_results['jump_force'] > 0:
        global car_vz
        car_vz = collision_results['jump_force']
        print("Jump activated!")
    
    # Collectible pickups handled automatically in Member 2
    if collision_results['collectible_hit']:
        print(f"Collectible picked up! Score: {get_score()}")
    
    if collision_results['bonus_hit']:
        print(f"Bonus collected! Score: {get_score()}")

def integrated_check_win_lose():
    """Check win/lose conditions using all systems"""
    global is_game_over, win_message
    
    # Get data from all systems
    remaining_collectibles = get_collectibles_count()
    remaining_bonus = get_bonus_count()
    current_lives = get_lives()
    current_score = get_score()
    
    # Win condition: all items collected
    if remaining_collectibles == 0 and remaining_bonus == 0:
        is_game_over = True
        win_message = f"YOU WIN! Final Score: {current_score}"
        print(f"Victory! Final score: {current_score}")
    
    # Lose condition: no lives left  
    elif current_lives <= 0:
        is_game_over = True
        win_message = "GAME OVER - No Lives Left!"
        print("Game Over - No lives remaining")
    
    # Timer loss handled by Member 1's timer system

def integrated_keyboard_listener(key, x, y):
    """Handle keyboard input for all systems"""
    # Handle UI-specific input (Member 3)
    ui_result = handle_ui_keyboard_input(key, get_game_state())
    if ui_result is not None:
        print(f"Cheat mode: {'ON' if ui_result else 'OFF'}")
        glutPostRedisplay()
        return
    
    # Handle movement input (Member 1) with cheat mode integration
    if get_game_state() == "PLAY":
        if hasattr(key, "decode"):
            k = key.decode('utf-8').lower()
        else:
            k = chr(key).lower() if isinstance(key, int) else str(key).lower()
        
        # ESC returns to menu
        if ord(k) == 27:
            set_game_state("MENU")
            glutPostRedisplay()
            return
        
        # Restart game
        if k == 'r':
            integrated_reset_game()
            return
        
        # Movement with difficulty and cheat mode integration
        cheat_active = get_cheat_mode()
        settings = get_difficulty_settings()
        current_max_speed = get_cheat_max_speed() if cheat_active else settings["max_speed"]
        
        global car_speed, car_angle
        if k == 'w':
            car_speed = min(car_speed + settings["acceleration"] * 0.3, current_max_speed)
        elif k == 's':
            car_speed = max(car_speed - settings["acceleration"] * 0.3, -current_max_speed * 0.6)
        elif k == 'a' and abs(car_speed) > 5:
            car_angle += 10 if car_speed > 0 else -10
        elif k == 'd' and abs(car_speed) > 5:
            car_angle -= 10 if car_speed > 0 else 10

def integrated_mouse_listener(button, state, x, y):
    """Handle mouse input for menu navigation"""
    action = mouseListener(button, state, x, y, get_game_state)
    
    if action:
        if action == "PLAY":
            integrated_reset_game()
            set_game_state("PLAY")
            print("Starting new game...")
        elif action == "COLOR":
            set_game_state("COLOR")
        elif action == "DIFFICULTY":
            set_game_state("DIFFICULTY")
        elif action == "HOWTO":
            set_game_state("HOWTO")
        elif action == "MENU":
            set_game_state("MENU")
        elif action == "EXIT":
            print("Exiting game...")
            handle_exit()
        
        glutPostRedisplay()

def integrated_draw_car():
    """Draw car with Member 3's color customization"""
    glPushMatrix()
    glTranslatef(car_pos[0], car_pos[1], car_pos[2])
    glRotatef(car_angle, 0, 0, 1)
    
    # Get color from Member 3's customization system
    color = get_car_color_for_rendering()
    glColor3f(color[0], color[1], color[2])
    glutSolidCube(35)
    
    # Car details
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(-20, 0, 8)
    glScalef(0.2, 1.5, 0.3)
    glutSolidCube(20)
    glPopMatrix()
    
    # Car antenna
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.8)
    glTranslatef(0, 0, 20)
    glRotatef(90, 1, 0, 0)
    quad = gluNewQuadric()
    if quad is not None:
        gluCylinder(quad, 1, 1, 15, 4, 1)
    glPopMatrix()
    
    # Wheels
    glColor3f(0.1, 0.1, 0.1)
    for (x, y) in [(12, 18), (12, -18), (-12, 18), (-12, -18)]:
        glPushMatrix()
        glTranslatef(x, y, -8)
        glutSolidCube(8)
        glPopMatrix()
    
    glPopMatrix()

def integrated_idle():
    """Main game loop integrating all systems"""
    if get_game_state() != "PLAY":
        glutPostRedisplay()
        return
    
    if is_game_over:
        glutPostRedisplay()
        return
    
    # Get frame time (Member 1)
    delta_time = get_delta_time()
    
    # Update Member 2's animations
    member2_idle(delta_time)
    
    # Update Member 1's car physics
    prev_pos = update_car_physics(delta_time)
    
    # Handle all collisions
    integrated_handle_collisions(prev_pos, delta_time)
    
    # Update Member 1's timer
    update_timer(delta_time)
    
    # Check integrated win/lose conditions
    integrated_check_win_lose()
    
    glutPostRedisplay()

def integrated_display():
    """Main display function integrating all rendering"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, window_w, window_h)
    
    current_state = get_game_state()
    
    if current_state == "PLAY":
        # Set up 3D view (Member 1)
        setupCamera()
        
        # Draw arena floor (Member 2)
        draw_arena()
        
        # Draw all game objects with depth sorting (Member 2)
        draw_all_objects(car_pos, car_angle, camera_distance, camera_height)
        
        # Draw car with customization (Member 1 + Member 3)
        integrated_draw_car()
        
        # Prepare HUD data and draw (Member 3)
        game_data = {
            'score': get_score(),
            'game_timer': game_timer,
            'car_speed': car_speed,
            'collectibles_count': get_collectibles_count(),
            'bonus_count': get_bonus_count(),
            'obstacles_count': get_obstacles_count(),
            'current_lives': get_lives(),
            'max_lives': max_lives,
            'is_game_over': is_game_over,
            'win_message': win_message
        }
        
        draw_appropriate_screen(current_state, game_data)
        
    else:
        # Draw appropriate menu screen (Member 3)
        draw_appropriate_screen(current_state)
    
    glutSwapBuffers()

# ==================== MAIN FUNCTION ====================
def main():
    """Initialize and run the integrated game"""
    print("=== 3D Car Driving Game - Team Project ===")
    print("Member 1: Core Movement & Physics")
    print("Member 2: Game World & Collectibles") 
    print("Member 3: UI & Customization")
    print("==========================================")
    
    # Initialize OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_w, window_h)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Car in Maze Box - Team Project")
    
    # Set up OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.2, 1.0)  # Dark blue background
    
    # Initialize all member systems
    print("Initializing Member 1 systems...")
    init_member1()
    
    print("Initializing Member 2 systems...")
    init_member2()
    
    print("Initializing Member 3 systems...")
    init_member3()
    
    # Set initial game state
    set_game_state("MENU")
    
    print("Setting up game callbacks...")
    # Set up GLUT callbacks
    glutDisplayFunc(integrated_display)
    glutKeyboardFunc(integrated_keyboard_listener)
    glutSpecialFunc(specialKeyListener)  # Member 1's camera controls
    glutMouseFunc(integrated_mouse_listener)
    glutIdleFunc(integrated_idle)
    
    print("Game initialization complete!")
    print("\nControls:")
    print("- WASD: Move car")
    print("- Arrow Keys: Adjust camera") 
    print("- SPACE: Toggle cheat mode")
    print("- R: Restart game")
    print("- ESC: Return to menu")
    print("\nStarting main game loop...")
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main():
            
