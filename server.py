import asyncio
import logging
import websockets
import names
import aiofile
from datetime import datetime
from aiopath import Path
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from main import get_exchange_data

logging.basicConfig(level=logging.INFO)

path_to_log = Path("exchange.log")


async def log_exchange_command():
    if not await path_to_log.exists():
        await path_to_log.touch()

    async with aiofile.async_open("exchange.log", "a") as file:
        await file.write(f"Exchange command executed at {datetime.now()}.\n")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.split()[0] == "exchange":
                await log_exchange_command()
                if len(message.split()) > 1:
                    days = message.split()[1]
                    result = await get_exchange_data(days)
                else:
                    result = await get_exchange_data()

                await self.send_to_clients(f"Exchange Rate: {'-----*****-----'.join(result)}")
            else:
                await self.send_to_clients(f"{ws.name}: {str(message)}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())