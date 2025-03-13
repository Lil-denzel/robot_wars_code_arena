import random

# Arena dimensions (adjust as needed)
ARENA_WIDTH = 10
ARENA_HEIGHT = 10

# Actions a bot can take
ACTIONS = ['move_up', 'move_down', 'move_left', 'move_right', 'shoot']

# Game state
class GameState:
    def __init__(self):
        self.robots = []
        self.projectiles = []
        self.turns = 0
    
    def add_robot(self, robot):
        self.robots.append(robot)
    
    def remove_robot(self, robot):
        self.robots.remove(robot)

    def next_turn(self):
        self.turns += 1

# Position handling
def is_within_bounds(x, y):
    return 0 <= x < ARENA_WIDTH and 0 <= y < ARENA_HEIGHT

class Robot:
    def __init__(self, name, x=None, y=None):
        self.name = name
        self.hp = 100
        self.x = x if x is not None else random.randint(0, ARENA_WIDTH - 1)
        self.y = y if y is not None else random.randint(0, ARENA_HEIGHT - 1)

    def take_action(self, action, game_state):
        if action == 'move_up' and is_within_bounds(self.x, self.y - 1):
            self.y -= 1
        elif action == 'move_down' and is_within_bounds(self.x, self.y + 1):
            self.y += 1
        elif action == 'move_left' and is_within_bounds(self.x - 1, self.y):
            self.x -= 1
        elif action == 'move_right' and is_within_bounds(self.x + 1, self.y):
            self.x += 1
        elif action == 'shoot':
            for robot in game_state.robots:
                if robot != self and (robot.x == self.x or robot.y == self.y):
                    robot.hp -= 20
                    print(f"{self.name} shot {robot.name}!")
        else:
            print(f"{self.name} did nothing...")

    def is_alive(self):
        return self.hp > 0

def simulate_game():
    game_state = GameState()

    # Create robots
    bot1 = Robot("Bot-A")
    bot2 = Robot("Bot-B")
    game_state.add_robot(bot1)
    game_state.add_robot(bot2)

    print("Starting Robot Wars!")

    # Game loop
    while len([r for r in game_state.robots if r.is_alive()]) > 1:
        game_state.next_turn()
        print(f"\n--- Turn {game_state.turns} ---")
        
        for robot in game_state.robots:
            if robot.is_alive():
                action = random.choice(ACTIONS)
                robot.take_action(action, game_state)
                print(f"{robot.name} ({robot.hp} HP) is at ({robot.x}, {robot.y})")

    # Determine Winner
    winner = [r for r in game_state.robots if r.is_alive()][0]
    print(f"\n🏆 {winner.name} wins with {winner.hp} HP remaining!")

if __name__ == "__main__":
    simulate_game()
import random
import time

# Arena settings
ARENA_SIZE = 10
MAX_HEALTH = 100

# Directions: (dx, dy)
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Obstacles
OBSTACLE_COUNT = 10

# Timer per turn (in seconds)
TURN_TIMER = 10

class Robot:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(0, ARENA_SIZE - 1)
        self.y = random.randint(0, ARENA_SIZE - 1)
        self.health = MAX_HEALTH
        self.attack_power = 20

    def move(self, direction):
        if direction in DIRECTIONS:
            new_x = self.x + DIRECTIONS[direction][0]
            new_y = self.y + DIRECTIONS[direction][1]

            # Check arena boundaries
            if 0 <= new_x < ARENA_SIZE and 0 <= new_y < ARENA_SIZE:
                self.x = new_x
                self.y = new_y
                print(f"{self.name} moved {direction} to ({self.x}, {self.y})")
            else:
                print(f"Invalid move! {self.name} hit the wall at ({self.x}, {self.y})")

    def attack(self, target):
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power
            print(f"{self.name} attacked {target.name} for {self.attack_power} damage! 💥")
        else:
            print(f"{self.name} missed! Target is too far away. 🎯")

    def is_alive(self):
        return self.health > 0

def create_obstacles():
    obstacles = set()
    while len(obstacles) < OBSTACLE_COUNT:
        obstacle = (random.randint(0, ARENA_SIZE - 1), random.randint(0, ARENA_SIZE - 1))
        obstacles.add(obstacle)
    return obstacles

def display_arena(robot1, robot2, obstacles):
    for y in range(ARENA_SIZE):
        row = ""
        for x in range(ARENA_SIZE):
            if (x, y) == (robot1.x, robot1.y):
                row += "R1 "
            elif (x, y) == (robot2.x, robot2.y):
                row += "R2 "
            elif (x, y) in obstacles:
                row += "## "
            else:
                row += "-- "
        print(row)
    print("\n")

def game_loop():
    robot1 = Robot("Robot 1")
    robot2 = Robot("Robot 2")
    obstacles = create_obstacles()

    print("🚀 Welcome to Robot Wars: Code Arena! Let the battle begin! 🎉")
    display_arena(robot1, robot2, obstacles)

    turn = 0

    while robot1.is_alive() and robot2.is_alive():
        current_robot = robot1 if turn % 2 == 0 else robot2

        print(f"\n{current_robot.name}'s turn! Health: {current_robot.health}")

        start_time = time.time()
        action = input("Choose action (move [UP/DOWN/LEFT/RIGHT], attack): ").upper()

        if time.time() - start_time > TURN_TIMER:
            print("⏰ Time's up! Skipping turn...")
        elif action.startswith("MOVE "):
            direction = action.split(" ")[1]
            if (current_robot.x + DIRECTIONS.get(direction, (0, 0))[0],
                current_robot.y + DIRECTIONS.get(direction, (0, 0))[1]) not in obstacles:
                current_robot.move(direction)
            else:
                print("🚧 Obstacle ahead! Move blocked.")
        elif action == "ATTACK":
            current_robot.attack(robot2 if current_robot == robot1 else robot1)
        else:
            print("Invalid action. Turn skipped.")

        display_arena(robot1, robot2, obstacles)
        turn += 1

    winner = robot1 if robot1.is_alive() else robot2
    print(f"🏆 {winner.name} wins the battle!")

# Run the game
if __name__ == "__main__":
    game_loop()
