# 🎮 Greedy Bag Race

Greedy Bag Race is a **turn-based strategy game** based on **Greedy Algorithms**, where players race to pick items into a limited-capacity bag.  
The goal is simple: **collect more items than your opponent before the bag is full or items run out**.

The game supports **Single Player (vs AI)** and **Local Multiplayer**, with multiple AI difficulty levels demonstrating different greedy strategies.

---

## 🚀 Features

- 🧠 **Greedy Algorithm Based AI**
  - Easy: Random item selection
  - Medium: Maximum value selection
  - Hard: Maximum value-to-weight ratio
- 👥 **Game Modes**
  - Single Player vs AI
  - Local Multiplayer (2 Players)
- 🔄 **Turn-Based Gameplay**
- 🎨 **Graphical User Interface (GUI)**
- 🔊 **Sound Effects & Background Music**
- 📊 **Live Bag Weight Tracking**
- 🏆 **Automatic Winner Declaration**

---

## 🕹️ Game Rules

- Each player has a bag with a **fixed weight capacity**
- Players take turns picking **one item at a time**
- An item can be picked by **only one player**
- A player **cannot pick an item** if it exceeds remaining bag capacity
- The game ends when:
  - All items are picked, OR
  - Both players can no longer pick any item
- The player with **more items** wins

---

## 🧩 AI Strategy Logic

| Difficulty | Strategy Used |
|----------|---------------|
| Easy | Random valid item |
| Medium | Item with maximum value |
| Hard | Item with maximum value/weight ratio |

This makes the game a practical demonstration of **greedy decision-making**.

---

## 🗂️ Project Structure

```

greedy_bag_race/
├── main.py
├── backend/
│   ├── items.py
│   ├── player.py
│   ├── ai.py
│   ├── game_engine.py
│   └── scoring.py
├── gui/
│   ├── window.py
│   ├── animations.py
│   └── sounds.py
├── assets/
│   ├── images/
│   └── sounds/
└── README.md

````

---

## ⚙️ Technologies Used

- **Python**
- **Tkinter / PyGame** (for GUI & sounds)
- **Object-Oriented Programming**
- **Greedy Algorithms**

---

## ▶️ How to Run the Game

1. Clone the repository:
   ```bash
   git clone https://github.com/FANGxPC/Greedy_algo_game
````

2. Navigate to the project directory:

   ```bash
   cd greedy-bag-race
   ```

3. Run the game:

   ```bash
   python main.py
   ```

---

## 📸 Screenshots (Optional)

*Add screenshots or GIFs of gameplay here*

---

## 🎯 Learning Outcomes

* Practical implementation of **Greedy Algorithms**
* Understanding **AI decision-making strategies**
* Game design with **turn-based logic**
* GUI development in Python
* Team-based project structure

---

## 👥 Team Members

* **Person 1** – GUI, animations, sounds
* **Person 2** – Backend logic, AI, game engine

---

## 📌 Future Improvements

* Online multiplayer
* Leaderboard system
* More AI strategies
* Mobile version

---

## 📜 License

This project is for **educational purposes**.
Feel free to fork and modify.

---

⭐ If you like this project, don’t forget to star the repository!

```

---

If you want, I can also:
- 🔥 Customize it for **college submission**
- 📄 Add **algorithm explanation section**
- 🎥 Write a **demo video description**
- 🧠 Add **greedy algorithm theory**

Just tell me 👍
```
