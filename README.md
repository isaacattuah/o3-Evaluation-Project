# o3 Programming Tasks Evaluation Project

This project is designed to evaluate o3's performance across a variety of programming tasks at different difficulty levels. It includes several Python programs that demonstrate low, medium, and high complexity tasks, allowing for a broad assessment of programming capabilities.

## Project Overview
Each task demonstrates different programming complexity levels:

- **Low-Level Task:** An interactive Snake game (snake.py) using basic game logic and Pygame graphics.
- **Medium-Level Task:** A tesseract simulation (tesseract.py) with 4-D transformations and Matplotlib animations.
- **High-Level Task:** A basic FPS raycaster (basic_fps.py) implementing 2D-to-3D rendering techniques.

## Project Structure

```
.
├── basic_fps.py    # High-level task: Basic FPS raycasting engine
├── snake.py        # Low-level task: Interactive Snake game
├── tesseract.py    # Medium-level task: 4D tesseract simulation
├── prompts.txt     # Original programming task prompts
└── requirements.txt # Project dependencies
```

## Requirements

The project relies on the following Python libraries:
- **numpy**
- **matplotlib**
- **pygame**

A requirements.txt file is provided to simplify installation of these dependencies.

## Installation

1. **Clone the Repository:**
   Clone or download this repository to your local machine.

2. **Set Up a Virtual Environment (Recommended):**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Set Up a Virtual Environment (Recommended):**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

**Run the Snake Game (Low-Level Task):**
    ```sh
    python snake.py
    ```

**Run the Tesseract Bouncing Ball Simulation (Medium-Level Task):**
    ```sh
    python tesseract.py
    ```

**Run the Basic FPS Raycaster (High-Level Task):**
    ```sh
    python basic_fps.py
    ```

## Evaluation
This project is used to evaluate o3's performance on:

- Low-Level Tasks: Basic game logic and event handling (e.g., the Snake game).

- Medium-Level Tasks: Simulation and visualization of complex mathematical concepts (e.g., the 4-D tesseract simulation).

- High-Level Tasks: More complex graphics programming and pseudo-3D rendering techniques (e.g., the FPS raycaster).

Each script demonstrates different levels of programming complexity and design challenges, providing a comprehensive test suite for evaluating various programming capabilities.

## Contributing
Contributions, improvements, and suggestions are welcome! If you have ideas to extend the functionality or add more evaluation tasks, please feel free to open an issue or submit a pull request.

## License
This project is provided for educational and evaluation purposes. Feel free to use and modify the code as needed.

Happy coding and evaluating!