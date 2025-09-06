# 3D Car Driving Game (CSE423 Project)

A 3D Car Driving Game built for the CSE423 course, designed for collaborative development with **clear team division**.  
Each member is responsible for a set of features, tracked via GitHub branches and commit history for easy faculty review.

---

## 🚦 Team Division

### 🚗 Salman — Core Game Engine & Movement
- **3D Car Movement:** WASD controls, positioning, rotation
- **Collision Detection:** Walls/obstacles
- **Camera Controls:** Arrow key adjustment, follow system
- **Timer System:** Countdown, time-based ending
- **Game States:** Win/lose, restart logic

### 🎮 Nisa — Game Objects & Collectibles
- **Collectible Items:** Yellow cubes (+10 points)
- **Bonus Collectibles:** Gold cylinders (+50 points)
- **Jump Ramps:** Cyan ramps, jump physics
- **Life System:** 3 lives, lose on collision
- **Score Tracking:** Point display, accumulation

### 🖥️ Anika — UI/UX & Customization
- **Menu System:** Main menu, navigation
- **HUD Display:** Real-time overlay
- **Car Color Customization:** 4 options
- **Difficulty Levels:** Easy/Medium/Hard
- **Cheat Mode:** Super speed, visual cues

---

## 📁 Project Structure

| File Name                      | Features Assigned                                         |
|--------------------------------|----------------------------------------------------------|
| `car_game_part1_core.py`       | Car movement, collision, camera, timer, game states      |
| `car_game_part2_environment.py`| Collectibles, bonus, ramps, lives, score                 |
| `car_game_part3_ui.py`         | Menu, HUD, color, difficulty, cheat mode                 |

---

## 🛠️ How to Run

1. **Requirements:**
   - Python 3.x
   - [PyOpenGL](https://pypi.org/project/PyOpenGL/)
   - [PyOpenGL_accelerate](https://pypi.org/project/PyOpenGL-accelerate/) (optional)
   - (Optionally) `freeglut` or similar

2. **Install dependencies:**
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```

3. **Run a module for feature demo:**
   ```bash
   python car_game_part1_core.py
   python car_game_part2_environment.py
   python car_game_part3_ui.py
   ```

4. **Final integration:**  
   Merge all three for the complete game.

---

## 👥 Team Members

| Name    | GitHub           | Part/Branch              |
|---------|------------------|--------------------------|
| Salman  | @your-github1    | Salman-core-engine       |
| Anika   | @your-github3    | Anika-ui-system          |
| Nisa    | @your-github2    | Nisa-game-objects        |


---

## 🎮 Game Features (All 15)

1. **3D Car Movement** (WASD controls, car positioning, rotation)
2. **Collision Detection** (Wall and obstacle collision system)
3. **Camera Controls** (Arrow key camera adjustment, follow system)
4. **Timer System** (Countdown timer, time-based game ending)
5. **Game States** (Win/lose, restart functionality)
6. **Collectible Items** (Yellow cubes worth 10 points)
7. **Bonus Collectibles** (Gold cylinders worth 50 points)
8. **Jump Ramps** (Cyan ramps with jump physics)
9. **Life System** (3 lives, lose life on collision)
10. **Score Tracking** (Point accumulation and display)
11. **Menu System** (Main menu, navigation between screens)
12. **HUD Display** (Real-time game information overlay)
13. **Car Color Customization** (4 color options with preview)
14. **Difficulty Levels** (Easy/Medium/Hard with different settings)
15. **Cheat Mode** (Super speed toggle, visual indicators)

---

## 📋 How to Play

- **WASD:** Drive the car
- **Arrow Keys:** Adjust camera
- **Collect yellow cubes:** +10 points each
- **Collect gold cylinders:** +50 points each
- **Jump ramps:** Jump!
- **Collide with obstacles/walls:** Lose a life
- **ESC:** Return to main menu
- **Space:** Toggle cheat mode (super speed)
- **R:** Restart game

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
