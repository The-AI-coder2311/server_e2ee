import asyncio
import websockets
import json

clients = {}
pubkeys = {}

async def broadcast_users():
    msg = json.dumps({
        "type": "users",
        "data": pubkeys
    })
    for c in clients.values():
        await c.send(msg)

async def handler(ws):
    username = await ws.recv()
    pub = await ws.recv()

    clients[username] = ws
    pubkeys[username] = pub

    await broadcast_users()

    try:
        async for message in ws:
            msg = json.loads(message)

            for r in msg["to"]:
                if r in clients:
                    await clients[r].send(message)

    finally:
        clients.pop(username, None)
        pubkeys.pop(username, None)
        await broadcast_users()

async def main():
    async with websockets.serve(handler, "0.0.0.0", 5555):
        await asyncio.Future()

asyncio.run(main())
