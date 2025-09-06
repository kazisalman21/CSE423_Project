# 3D Car Driving Game (CSE423 Project)

A 3D Car Driving Game built for the CSE423 course, split into three modules for collaborative development and GitHub submission.  
Each team member contributed a distinct set of features, making it easy for faculty to review individual work via commit history.

---

## 🚗 Game Overview

Drive your car in a 3D arena:
- Collect items to score points.
- Avoid obstacles and walls.
- Jump ramps, choose your car color, and select your difficulty.
- Race against the clock and survive with limited lives!

---

## 📁 Project Structure

The game is divided into three main Python files, each representing a module developed by a different team member:

| File Name                   | Member Responsibilities (Features)                     |
|-----------------------------|-------------------------------------------------------|
| `car_game_part1_core.py`    | Core mechanics: car movement, collision, lives, timer, score |
| `car_game_part2_environment.py` | Environment & interactables: collectibles, bonus items, ramps, obstacles, arena & walls |
| `car_game_part3_ui.py`      | UI & advanced: menu, color selection, difficulty, HUD, game states, cheat mode |

---

## 🛠️ How to Run

1. **Requirements:**
   - Python 3.x
   - [PyOpenGL](https://pypi.org/project/PyOpenGL/)
   - [PyOpenGL_accelerate](https://pypi.org/project/PyOpenGL-accelerate/) (optional but recommended)
   - (Optionally) `freeglut` or similar OpenGL GLUT implementation for your system.

2. **Install dependencies:**
   ```
   pip install PyOpenGL PyOpenGL_accelerate
   ```

3. **Run any part individually for feature demo:**
   ```bash
   python car_game_part1_core.py           # Core car mechanics
   python car_game_part2_environment.py    # Environment/obstacle logic (to be integrated)
   python car_game_part3_ui.py             # UI and game state demo
   ```

4. **Final integration:**
   - Merge the three parts (and resolve imports/links) into a single main game file for complete play.

---

## 👥 Team Members & Contributions

| Name            | GitHub                | Module                  | Features                              |
|-----------------|----------------------|-------------------------|---------------------------------------|
|        | @your-github1        | car_game_part1_core.py  | Car movement, collision, lives, timer, score |
| Member 2        | @your-github2        | car_game_part2_environment.py | Collectibles, bonus, ramps, obstacles, arena/walls |
| Member 3        | @your-github3        | car_game_part3_ui.py    | Menu, color select, difficulty, HUD, states |

> **Tip:**  
> Commit history for each file will show who contributed what—reviewable by faculty.

---

## 🎮 Game Features

- 3D car movement (WASD)
- Collision detection with arena walls and obstacles
- Collectibles (cubes), bonus collectibles (cylinders)
- Life system
- timer
- Jump ramps
- Dynamic arena with random placements
- Menu system
- UI overlays (HUD)
- Car color selection
- Difficulty modes (Easy/Medium/Hard)
- Game states: win, lose, restart
- Cheat/debug mode

---

## 📋 How to Play

- **WASD:** Drive the car
- **Arrow Keys:** Adjust camera (if implemented)
- **Collect yellow cubes:** +10 points each
- **Collect gold cylinders:** +50 points each
- **Jump ramps:** Jump!
- **Collide with obstacles/walls:** Lose a life
- **ESC:** Return to main menu

---

## 📝 Notes

- For full game play, all three modules must be integrated.
- Each file is individually runnable for demonstration and grading.
- This split ensures clear contribution tracking for each member.

---

## 📦 Repository

> [github.com/kazisalman21/CSE423_Project](https://github.com/kazisalman21/CSE423_Project)

---

## 🏁 Good Luck & Have Fun!
