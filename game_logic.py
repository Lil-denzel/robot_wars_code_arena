import random
import time
import threading

# Game settings
POWER_UPS = ["speed_boost", "damage_boost", "shield", "health_pack", "invisibility", "nuke"]
POWER_UP_SPAWN_INTERVAL = 10
POWER_UP_DURATION = 5  # Seconds
arena_power_ups = []

# Leaderboard to track bot performance
leaderboard = {}

# Store connected bots
bots = []

class Bot:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.speed = 1
        self.damage = 10
        self.shield = False
        self.invisible = False
        self.x = random.randint(0, 100)
        self.y = random.randint(0, 100)
        leaderboard[name] = 0

    def make_move(self):
        """Random bot movement."""
        self.x += random.choice([-1, 0, 1]) * self.speed
        self.y += random.choice([-1, 0, 1]) * self.speed

    def attack(self, target):
        """Attack another bot."""
        if target.shield:
            print(f"{target.name} blocked the attack with a shield! 🛡️")
            target.shield = False
        else:
            target.health -= self.damage
            print(f"{self.name} attacked {target.name}! 💥 Health: {target.health}")
            if target.health <= 0:
                print(f"{target.name} has been destroyed! ☠️")
                leaderboard[self.name] += 1

def spawn_power_up():
    """Randomly spawns power-ups."""
    new_power_up = {
        "type": random.choice(POWER_UPS),
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }
    arena_power_ups.append(new_power_up)
    print(f"Power-up spawned: {new_power_up['type']} at ({new_power_up['x']}, {new_power_up['y']})")

def apply_power_up(bot, power_up):
    """Applies power-ups to bots."""
    if power_up["type"] == "speed_boost":
        bot.speed += 2
        print(f"{bot.name} got a Speed Boost! ⚡")

    elif power_up["type"] == "damage_boost":
        bot.damage *= 2
        print(f"{bot.name} got a Damage Boost! 💥")

    elif power_up["type"] == "shield":
        bot.shield = True
        print(f"{bot.name} got a Shield! 🛡️")

    elif power_up["type"] == "health_pack":
        bot.health = min(bot.max_health, bot.health + 20)
        print(f"{bot.name} picked up a Health Pack! ❤️ (+20 health)")

    elif power_up["type"] == "invisibility":
        bot.invisible = True
        print(f"{bot.name} turned Invisible! 🫥")

    elif power_up["type"] == "nuke":
        print(f"{bot.name} activated a Nuke! 💣 All other bots take 50 damage!")
        for other_bot in bots:
            if other_bot != bot:
                other_bot.health -= 50
                print(f"{other_bot.name} now has {other_bot.health} health.")

def check_power_up_pickup(bot):
    """Check if the bot is close enough to pick up a power-up."""
    for power_up in arena_power_ups:
        if abs(bot.x - power_up["x"]) <= 5 and abs(bot.y - power_up["y"]) <= 5:
            apply_power_up(bot, power_up)
            arena_power_ups.remove(power_up)
            break

def display_leaderboard():
    """Display the current leaderboard."""
    print("\n🏆 Leaderboard:")
    for bot, score in leaderboard.items():
        print(f"{bot}: {score} kills")
    print("-" * 20)

def game_loop():
    """Main game loop."""
    last_power_up_time = time.time()
    
    while True:
        # Spawn power-ups at intervals
        if time.time() - last_power_up_time > POWER_UP_SPAWN_INTERVAL:
            spawn_power_up()
            last_power_up_time = time.time()

        # Bots take turns making moves
        for bot in bots:
            bot.make_move()
            check_power_up_pickup(bot)

        # Check if game is over
        alive_bots = [b for b in bots if b.health > 0]
        if len(alive_bots) == 1:
            print(f"🏅 {alive_bots[0].name} wins the game!")
            display_leaderboard()
            break

        time.sleep(0.5)  # Simulate game tick

# Multiplayer support — add bots to the game
def add_bot(bot_name):
    new_bot = Bot(bot_name)
    bots.append(new_bot)
    print(f"🤖 New bot added: {bot_name}")

# Run the game
if __name__ == "__main__":
    print("🚀 Welcome to Robot Wars: Code Arena!")
    add_bot("Alpha")
    add_bot("Bravo")
    add_bot("Charlie")

    # Start the game in a separate thread so we can add features while it runs
    game_thread = threading.Thread(target=game_loop)
    game_thread.start()
