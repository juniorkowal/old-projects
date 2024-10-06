# Heroes 3 Bot Project

## Overview
This project aims to develop a bot capable of playing **Heroes of Might and Magic 3** using image processing, Optical Character Recognition (OCR), and machine learning algorithms such as Convolutional Neural Networks (CNN) and Deep-Q Learning. The bot can perform tasks like exploration, combat, and adventure map navigation through a combination of hierarchical algorithms and reinforcement learning techniques.

This is a **group project** carried out by **10 members** with varying levels of Python experience. The project is in an **experimental state**.

For neural network implementations, the project utilizes **TensorFlow**.

## Key Components

### 1. Image Processing
The bot processes in-game images to identify objects within the game window. It detects non-red objects, such as obstacles, and dynamically tracks changes on the map after every game reset. 

### 2. Optical Character Recognition (OCR)
OCR is used to manage game windows and pop-ups, extracting critical game state information after each move. The project uses the `pytesseract` library for OCR, with OpenCV's template matching employed for recognizing additional game elements. The `hero_filling.py` script fills hero data into the environment.

### 3. Convolutional Neural Network (CNN)
The CNN is used to detect obstacles on the adventure map. The architecture is simple:
- `Conv2D -> MaxPooling -> Conv2D -> Flatten -> Dense -> Dropout -> Dense -> Dropout -> Dense -> Dense`

### 4. Q-Learning Neural Network (QNN)
QNN is implemented to recognize and classify unit portraits during battle, helping in decision-making processes. The architecture includes:
- `Conv2D -> Conv2D -> Conv2D -> Flatten -> Dense`

## Agent Flow

### 1. General Workflow
The agent begins by scanning the environment to identify objects and manage city operations and hero movement. After each move, the system scans for new objects, and if new terrain is found, it reevaluates its strategy.

### 2. Adventure Map Navigation
The agent assigns values to objects on the map using hierarchical algorithms and chooses the highest-priority target. It uses the A* pathfinding algorithm, minimizing the cost function `f(x) = g(x) + h(x)`.

### 3. Battle System
The battle system is powered by Deep-Q Learning. A custom-built environment simulates Heroes 3 battles, and the agent has been trained over 182 hours. The loop-based battle system continuously checks the game state, move availability, and battle outcomes.

#### Key Battle Features:
- **Deep-Q Learning**: The agent selects optimal actions based on the battle state. It uses two neural networks—one for its actions and one for predicting the opponent’s moves.
- **Reward System**: The reward system was initially designed around partial rewards but was later changed to focus on offensive actions due to the agent avoiding combat.

### 4. Hierarchical Algorithms
Hierarchical algorithms prioritize map objects based on their relevance. Scripts like `artifact_value.py` and `mines_and_resources_value.py` assign values to different map objects, helping the agent decide its next move.

### 5. Pathfinding
The A* algorithm is used for pathfinding, optimizing the movement cost across the map.

## Results

### 1. Battle AI
The final version of the battle AI achieved a 48% win rate against easy-level opponents. Average times for various tasks are as follows:
- Spell selection (24 spells): ~9.07 s
- Spell selection (18 spells): ~7.12 s
- Unit movement: ~5.77 s
- Full turn: ~9.44 s

### 2. Adventure AI
The adventure AI faced some challenges due to the complexity of the game and did not manage to complete a full game.

## Future Development

### 1. Improved Reinforcement Learning for Battle AI
To improve battle performance, we plan to revise the reward system so that rewards are only given for winning a battle, rather than for individual actions. With extended training, we expect better results.

### 2. Reinforcement Learning for Adventure Map Navigation
The current navigation system uses hierarchical algorithms. Future plans include integrating reinforcement learning to make more efficient movement decisions on the adventure map.

## Usage Instructions

### Prerequisites
- Python 3.x
- Heroes of Might and Magic 3 installed

### Installation
Clone the repository and install the required dependencies:

```bash
git clone https://git.pg.edu.pl/p1253175/homm3-bot
cd homm3-bot
pip install -r requirements.txt
```

### Running the Bot
```bash
python main.py
```

## Additional Information

- The **documentation** is available in **Polish** in the `docs` folder.
- The project is hosted at [this repository](https://git.pg.edu.pl/p1253175/homm3-bot).


