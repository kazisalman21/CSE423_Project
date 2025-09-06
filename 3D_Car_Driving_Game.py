# Member 3: UI/UX & Customization
# Features: Menu System, HUD Display, Car Color Customization, Difficulty Levels, Cheat Mode

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

#  display size 
window_w, window_h = 1000, 800

# Car er body colour change
car_color = [0, 0, 1]  # Default blue

# Cheat-mode er jonno flag
cheat_mode = False

# Difficulty level
difficulty_mode = "MEDIUM"
difficulty_settings = {
    "EASY": {
        "timer": 120.0,
        "max_speed": 100,
        "acceleration": 80,
        "collectibles_count": 12,
        "bonus_count": 3,
        "static_obstacles_count": 8,
        "color": [0, 1, 0]  # Green
    },
    "MEDIUM": {
        "timer": 90.0,
        "max_speed": 150,
        "acceleration": 120,
        "collectibles_count": 16,
        "bonus_count": 4,
        "static_obstacles_count": 12,
        "color": [1, 1, 0]  # Yellow
    },
    "HARD": {
        "timer": 60.0,
        "max_speed": 200,
        "acceleration": 160,
        "collectibles_count": 20,
        "bonus_count": 5,
        "static_obstacles_count": 16,
        "color": [1, 0, 0]  # Red
    }
}

# Menu button er kaj
menu_buttons = [
    {"label": "Play", "rect": [window_w // 2 - 150, window_h // 2 + 140, 300, 60], "action": "PLAY"},
    {"label": "Change Car Colour", "rect": [window_w // 2 - 150, window_h // 2 + 60, 300, 60], "action": "COLOR"},
    {"label": "Difficulty Mode", "rect": [window_w // 2 - 150, window_h // 2 - 20, 300, 60], "action": "DIFFICULTY"},
    {"label": "How to Play", "rect": [window_w // 2 - 150, window_h // 2 - 100, 300, 60], "action": "HOWTO"},
    {"label": "Exit", "rect": [window_w // 2 - 150, window_h // 2 - 180, 300, 60], "action": "EXIT"},
]

# color changing button
color_options = [
    {"label": "Red", "color": [1, 0, 0], "rect": [window_w // 2 - 200, window_h // 2 - 40, 80, 80]},
    {"label": "Blue", "color": [0, 0, 1], "rect": [window_w // 2 - 80, window_h // 2 - 40, 80, 80]},
    {"label": "White", "color": [1, 1, 1], "rect": [window_w // 2 + 40, window_h // 2 - 40, 80, 80]},
    {"label": "Yellow", "color": [1, 1, 0], "rect": [window_w // 2 + 160, window_h // 2 - 40, 80, 80]},
]

# difficulty button
difficulty_buttons = [
    {"label": "Easy", "mode": "EASY", "rect": [window_w // 2 - 200, window_h // 2 + 40, 120, 60]},
    {"label": "Medium", "mode": "MEDIUM", "rect": [window_w // 2 - 60, window_h // 2 + 40, 120, 60]},
    {"label": "Hard", "mode": "HARD", "rect": [window_w // 2 + 80, window_h // 2 + 40, 120, 60]},
    {"label": "Back", "mode": None, "rect": [window_w // 2 - 60, window_h // 2 - 80, 120, 60]}
]

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """ text show korar func"""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_w, 0, window_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_menu():
    """feature1: menu system - main menu """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_w, 0, window_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # game er nam
    glColor3f(1, 1, 1)
    title_text = "Car In Maze Box"
    title_width = len(title_text) * 12
    title_x = (window_w - title_width) // 2
    draw_text(title_x + 15, window_h // 2 + 250, title_text, GLUT_BITMAP_TIMES_ROMAN_24)
    
    #  menur 5ta button
    for btn in menu_buttons:
        x, y, w, h = btn["rect"]
        
        # button background
        glColor3f(0.4, 0.4, 0.9)
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0)
        glVertex3f(x + w, y, 0)
        glVertex3f(x + w, y + h, 0)
        glVertex3f(x, y + h, 0)
        glEnd()
        
        # button text
        glColor3f(1, 1, 1)
        text_width = len(btn["label"]) * 10
        text_x = x + (w - text_width) // 2
        text_y = y + h // 2 - 5
        draw_text(text_x, text_y, btn["label"], GLUT_BITMAP_HELVETICA_18)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

##colour functionn st
def draw_enhanced_color_menu():
    """feature 3: car Color change - 4 ta color """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_w, 0, window_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # title
    title_text = "Select Car Colour"
    title_width = len(title_text) * 10
    title_x = (window_w - title_width) // 2
    draw_text(title_x + 15, window_h // 2 + 130, title_text, GLUT_BITMAP_TIMES_ROMAN_24)
    
    # Current car preview (3D cube)
    glPushMatrix()
    glTranslatef(window_w // 2, window_h // 2 + 60, 0)
    glScalef(20, 20, 20)
    glColor3f(car_color[0], car_color[1], car_color[2])
    glutSolidCube(1)
    glPopMatrix()
    
    # current color konta
    glColor3f(car_color[0], car_color[1], car_color[2])
    ind_x, ind_y, ind_w, ind_h = window_w // 2 + 45, window_h // 2 + 80, 100, 20
    glBegin(GL_QUADS)
    glVertex3f(ind_x, ind_y, 0)
    glVertex3f(ind_x + ind_w, ind_y, 0)
    glVertex3f(ind_x + ind_w, ind_y + ind_h, 0)
    glVertex3f(ind_x, ind_y + ind_h, 0)
    glEnd()
    
    # Label for indicator
    glColor3f(1, 1, 1)
    draw_text(window_w // 2 - 70, window_h // 2 + 85, "Current Colour -->", GLUT_BITMAP_HELVETICA_12)
    
    # Color option buttons
    for opt in color_options:
        x, y, w, h = opt["rect"]
        
        # Draw color button
        glColor3f(opt["color"][0], opt["color"][1], opt["color"][2])
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0)
        glVertex3f(x + w, y, 0)
        glVertex3f(x + w, y + h, 0)
        glVertex3f(x, y + h, 0)
        glEnd()
        
        # Button text with proper contrast
        text_width = len(opt["label"]) * 7
        text_x = x + (w - text_width) // 2
        text_y = y + h // 2 - 3
        
        if opt["label"] in ["White", "Yellow"]:
            glColor3f(0.0, 0.0, 0.0)  # Black text for light colors
        else:
            glColor3f(1.0, 1.0, 1.0)  # White text for dark colors
            
        glRasterPos2f(text_x, text_y)
        for char in opt["label"]:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Back button
    bx, by, bw, bh = window_w // 2 - 45, window_h // 2 - 130, 120, 50
    glColor3f(0.7, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(bx, by, 0)
    glVertex3f(bx + bw, by, 0)
    glVertex3f(bx + bw, by + bh, 0)
    glVertex3f(bx, by + bh, 0)
    glEnd()
    
    glColor3f(1, 1, 1)
    back_text_width = len("Back") * 10
    back_text_x = bx + (bw - back_text_width) // 2
    back_text_y = by + bh // 2 - 5
    draw_text(back_text_x, back_text_y, "Back", GLUT_BITMAP_HELVETICA_18)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
##colour function end

def draw_enhanced_difficulty_menu():
    """Feature 4: Difficulty Levels - Easy/Medium/Hard with different settings"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_w, 0, window_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Title
    title_text = "Select Difficulty"
    title_width = len(title_text) * 10
    title_x = (window_w - title_width) // 2
    draw_text(title_x + 10, window_h // 2 + 140, title_text, GLUT_BITMAP_TIMES_ROMAN_24)
    
    # Difficulty buttons
    for btn in difficulty_buttons:
        x, y, w, h = btn["rect"]
        
        # Highlight selected difficulty
        if btn["mode"] == difficulty_mode:
            glColor3f(0.2, 0.8, 0.2)  # Green for selected
        else:
            glColor3f(0.4, 0.4, 0.9)  # Blue for unselected
            
        # Draw button background
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0)
        glVertex3f(x + w, y, 0)
        glVertex3f(x + w, y + h, 0)
        glVertex3f(x, y + h, 0)
        glEnd()
        
        # Button text
        glColor3f(1, 1, 1)
        text_width = len(btn["label"]) * 10
        text_x = x + (w - text_width) // 2
        text_y = y + h // 2 - 5
        draw_text(text_x, text_y, btn["label"], GLUT_BITMAP_HELVETICA_18)
    
    # Display current difficulty settings
    if difficulty_mode in difficulty_settings:
        settings = difficulty_settings[difficulty_mode]
        glColor3f(1, 1, 1)
        info_y = window_h // 2 - 40
        draw_text(window_w // 2 - 100, info_y, f"Timer: {int(settings['timer'])}s", GLUT_BITMAP_HELVETICA_12)
        draw_text(window_w // 2 - 100, info_y - 20, f"Max Speed: {settings['max_speed']}", GLUT_BITMAP_HELVETICA_12)
        draw_text(window_w // 2 - 100, info_y - 40, f"Collectibles: {settings['collectibles_count']}", GLUT_BITMAP_HELVETICA_12)
        draw_text(window_w // 2 - 100, info_y - 60, f"Obstacles: {settings['static_obstacles_count']}", GLUT_BITMAP_HELVETICA_12)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_howto_screen():
    """How to Play instructions screen"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_w, 0, window_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Title
    title = "How to Play"
    title_x = (window_w - len(title) * 12) // 2
    draw_text(title_x, window_h - 100, title, GLUT_BITMAP_TIMES_ROMAN_24)
    
    # Instructions
    instructions = [
        "W - Move Forward",
        "S - Move Backward", 
        "A - Turn Left",
        "D - Turn Right",
        "SPACE - Toggle Cheat Mode (Super Speed)",
        "R - Restart Game",
        "Arrow Keys - Adjust Camera View",
        "You have 3 lives per game",
        "Hitting walls or obstacles costs 1 life",
        "Collect yellow cubes (+10 points)",
        "Collect gold cylinders (+50 points)",
        "Hit cyan ramps to jump!",
        "ESC - Return to Menu"
    ]
    
    y = window_h - 200
    for line in instructions:
        draw_text(250, y, line, GLUT_BITMAP_HELVETICA_18)
        y -= 30
    
    # Back button
    bx, by, bw, bh = window_w // 2 - 60, 50, 120, 50
    glColor3f(0.4, 0.4, 0.9)
    glBegin(GL_QUADS)
    glVertex3f(bx, by, 0)
    glVertex3f(bx + bw, by, 0)
    glVertex3f(bx + bw, by + bh, 0)
    glVertex3f(bx, by + bh, 0)
    glEnd()
    draw_text(bx + 30, by + 20, "Back", GLUT_BITMAP_HELVETICA_18)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_hud(score, game_timer, car_speed, collectibles_count, bonus_count, obstacles_count, current_lives, max_lives):
    """Feature 2: HUD Display - Real-time game information overlay"""
    # Game statistics
    draw_text(10, window_h - 30, f"Score: {score}")
    draw_text(10, window_h - 50, f"Time: {int(game_timer)}")
    draw_text(10, window_h - 70, f"Speed: {int(abs(car_speed))}")
    draw_text(10, window_h - 90, f"Items: {collectibles_count}")
    draw_text(10, window_h - 110, f"Bonus: {bonus_count}")
    draw_text(10, window_h - 130, f"Obstacles: {obstacles_count}")
    
    # Difficulty indicator with color
    difficulty_color = difficulty_settings[difficulty_mode]["color"]
    glColor3f(difficulty_color[0], difficulty_color[1], difficulty_color[2])
    draw_text(10, window_h - 150, f"Mode: {difficulty_mode}")
    glColor3f(1, 1, 1)  # Reset to white
    
    # Life system display
    lives_display = f"{current_lives}/{max_lives}"
    draw_text(10, window_h - 170, f"Lives: {lives_display}")
    
    # Visual life indicator
    lives_visual = ""
    for i in range(max_lives):
        if i < current_lives:
            lives_visual += "* "  # Asterisk for remaining life
        else:
            lives_visual += "- "  # Dash for lost life
    draw_text(100, window_h - 170, f"[{lives_visual.strip()}]")
    
    # Feature 5: Cheat mode indicator
    if cheat_mode:
        glColor3f(1, 0, 1)  # Magenta for cheat mode
        draw_text(10, window_h - 200, "CHEAT MODE: SUPER SPEED!", GLUT_BITMAP_HELVETICA_12)
        draw_text(10, window_h - 220, "Press SPACE to toggle", GLUT_BITMAP_HELVETICA_10)
        glColor3f(1, 1, 1)  # Reset to white

def draw_game_over_screen(is_game_over, win_message):
    """Draw game over messages and restart instructions"""
    if is_game_over:
        glColor3f(1, 1, 1)
        draw_text(window_w // 2 - 120, window_h // 2 + 10, win_message, GLUT_BITMAP_HELVETICA_18)
        draw_text(window_w // 2 - 60, window_h // 2 - 20, "Press 'R' to restart", GLUT_BITMAP_HELVETICA_12)

def get_car_color_for_rendering():
    """Get current car color, accounting for cheat mode"""
    if cheat_mode:
        return [0.8, 0.5, 1.0]  # Purple for cheat mode
    else:
        return car_color[:]  # Normal selected color

def toggle_cheat_mode():
    """Feature 5: Cheat Mode - Toggle super speed and visual indicator"""
    global cheat_mode
    cheat_mode = not cheat_mode
    return cheat_mode

def get_cheat_mode():
    """Get current cheat mode status"""
    return cheat_mode

def apply_difficulty_settings():
    """Apply selected difficulty settings to game variables"""
    if difficulty_mode in difficulty_settings:
        return difficulty_settings[difficulty_mode]
    return difficulty_settings["MEDIUM"]

def set_difficulty_mode(new_mode):
    """Set new difficulty mode"""
    global difficulty_mode
    if new_mode in difficulty_settings:
        difficulty_mode = new_mode

def get_difficulty_mode():
    """Get current difficulty mode"""
    return difficulty_mode

def set_car_color(new_color):
    """Set new car color"""
    global car_color
    car_color[:] = new_color[:]

def get_car_color():
    """Get current car color"""
    return car_color[:]

def mouseListener(button, state, x, y, game_state_callback):
    """Handle mouse clicks for menu navigation"""
    if state != GLUT_DOWN:
        return None
        
    mx, my = x, window_h - y  # Convert mouse coordinates
    current_game_state = game_state_callback()  # Get current game state
    
    if current_game_state == "MENU":
        for btn in menu_buttons:
            bx, by, bw, bh = btn["rect"]
            if bx <= mx <= bx + bw and by <= my <= by + bh:
                return btn["action"]
                
    elif current_game_state == "COLOR":
        # Handle color selection
        for opt in color_options:
            bx, by, bw, bh = opt["rect"]
            if bx <= mx <= bx + bw and by <= my <= by + bh:
                set_car_color(opt["color"])
                return None
        
        # Handle back button
        bx, by, bw, bh = window_w // 2 - 45, window_h // 2 - 130, 120, 50
        if bx <= mx <= bx + bw and by <= my <= by + bh:
            return "MENU"
            
    elif current_game_state == "DIFFICULTY":
        for btn in difficulty_buttons:
            bx, by, bw, bh = btn["rect"]
            if bx <= mx <= bx + bw and by <= my <= by + bh:
                if btn["mode"] is not None:
                    set_difficulty_mode(btn["mode"])
                    return None
                else:
                    return "MENU"
                    
    elif current_game_state == "HOWTO":
        bx, by, bw, bh = window_w // 2 - 60, 50, 120, 50
        if bx <= mx <= bx + bw and by <= my <= by + bh:
            return "MENU"
    
    return None

def handle_cheat_key():
    """Handle spacebar press for cheat mode toggle"""
    return toggle_cheat_mode()

def handle_exit():
    """Handle game exit"""
    if hasattr(sys.modules.get('OpenGL.GLUT'), 'glutLeaveMainLoop'):
        glutLeaveMainLoop()
    else:
        sys.exit(0)

# Export functions for integration
__all__ = [
    'draw_menu', 'draw_enhanced_color_menu', 'draw_enhanced_difficulty_menu', 
    'draw_howto_screen', 'draw_hud', 'draw_game_over_screen',
    'get_car_color_for_rendering', 'toggle_cheat_mode', 'get_cheat_mode',
    'apply_difficulty_settings', 'set_difficulty_mode', 'get_difficulty_mode',
    'set_car_color', 'get_car_color', 'mouseListener', 'handle_cheat_key', 'handle_exit',
    'car_color', 'cheat_mode', 'difficulty_mode', 'difficulty_settings'
]