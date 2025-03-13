import asyncio
import websockets

# Store connected clients
connected_clients = set()

async def conn_handler(connection, path):
    # Your existing code

    # Add client to the set when they connect
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    try:
        async for message in websocket:
            print(f"Message received: {message}")
            # Broadcast message to all connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected gracefully.")
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected unexpectedly.")
    finally:
        # Remove client from the set when they disconnect
        connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")

async def main():
    async with websockets.serve(conn_handler, "localhost", 8765, ping_interval=None):
       print("WebSocket server started on ws://localhost:8765")
    try:
        await asyncio.Future()  # Keep running forever
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.close()
        await server.wait_closed()

asyncio.run(main())
