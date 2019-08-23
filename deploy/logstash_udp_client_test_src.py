# -*- coding: utf-8 -*-
import asyncio
import json


class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

        # 不需要等待服务器数据返回，直接发送完毕数据后关闭
        self.transport.close()

    # def datagram_received(self, data, addr):
    #     print("Received:", data.decode())
    #
    #     print("Close the socket")
    #     self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()


loop = asyncio.get_event_loop()
message = json.dumps({
    "msg": "Hello World! 123444",
    "name": "zhexxx"
})

connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 21561)
)
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()
