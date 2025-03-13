import asyncio
import websockets
import json
import random

# Store connected clients and game state
connected_clients = set()
game_state = {
    "bots": {},
    "power_ups": [],
    "leaderboard": {}
}

# Game settings
ARENA_WIDTH = 600
ARENA_HEIGHT = 400
BOT_SIZE = 40
POWER_UP_SIZE = 20
MAX_HEALTH = 100

# Power-up types
POWER_UP_TYPES = ["health", "speed", "damage"]

def spawn_power_up():
    return {
        "x": random.randint(0, ARENA_WIDTH - POWER_UP_SIZE),
        "y": random.randint(0, ARENA_HEIGHT - POWER_UP_SIZE),
        "type": random.choice(POWER_UP_TYPES)
    }

# Game loop to handle power-ups and updates
async def game_loop():
    while True:
        if len(game_state["power_ups"]) < 3:
            game_state["power_ups"].append(spawn_power_up())

        # Broadcast the updated game state to all clients
        message = json.dumps(game_state)
        for client in connected_clients:
            await client.send(message)

        await asyncio.sleep(1)  # Update every second

# WebSocket handler
async def handler(websocket, path):
    connected_clients.add(websocket)
    bot_id = f"bot_{len(connected_clients)}"

    # Initialize the bot
    game_state["bots"][bot_id] = {
        "x": random.randint(0, ARENA_WIDTH - BOT_SIZE),
        "y": random.randint(0, ARENA_HEIGHT - BOT_SIZE),
        "health": MAX_HEALTH,
        "damage": 10,
        "speed": 10
    }
    print(f"{bot_id} joined the game!")

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            bot = game_state["bots"].get(bot_id)

            # Handle movement
            if action in ["up", "down", "left", "right"]:
                speed = bot["speed"]
                if action == "up":
                    bot["y"] = max(0, bot["y"] - speed)
                elif action == "down":
                    bot["y"] = min(ARENA_HEIGHT - BOT_SIZE, bot["y"] + speed)
                elif action == "left":
                    bot["x"] = max(0, bot["x"] - speed)
                elif action == "right":
                    bot["x"] = min(ARENA_WIDTH - BOT_SIZE, bot["x"] + speed)

            # Handle attacks
            elif action == "attack":
                target_id = data.get("target_id")
                if target_id and target_id in game_state["bots"]:
                    target = game_state["bots"][target_id]
                    target["health"] -= bot["damage"]
                    if target["health"] <= 0:
                        del game_state["bots"][target_id]
                        print(f"{target_id} has been destroyed!")

            # Handle power-up collection
            for power_up in game_state["power_ups"]:
                if abs(bot["x"] - power_up["x"]) < POWER_UP_SIZE and abs(bot["y"] - power_up["y"]) < POWER_UP_SIZE:
                    if power_up["type"] == "health":
                        bot["health"] = min(MAX_HEALTH, bot["health"] + 20)
                    elif power_up["type"] == "speed":
                        bot["speed"] += 2
                    elif power_up["type"] == "damage":
                        bot["damage"] += 5
                    game_state["power_ups"].remove(power_up)

    except websockets.exceptions.ConnectionClosed:
        print(f"{bot_id} disconnected.")
        connected_clients.remove(websocket)
        del game_state["bots"][bot_id]

# Run the game loop and WebSocket server
async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server running at ws://localhost:8765")
    await asyncio.gather(game_loop(), server.wait_closed())

asyncio.run(main())

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/frontend/index.html"
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(("localhost", 8000), CustomHandler)
    print("Serving on http://localhost:8000")
    server.serve_forever()
