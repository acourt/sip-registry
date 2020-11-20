import SipRegistry
import asyncio
import logging
import sys

log = None

def main():
    global sipRegs
    print("Hello, world!")
    logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,)

    sipRegs = SipRegistry.SipRegistry("regs")
    print(sipRegs.getSipDataString('01574393bae33557c3000100620007'))
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handleRecordRequest, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    logging.info('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


async def handleRecordRequest(reader, writer):
    global sipRegs
    aorBytes = await reader.read(100)
    aorString = aorBytes.decode('utf-8')
    addr = writer.get_extra_info('peername')
    logging.info("record request from %s", addr)
    sipRecordStr = sipRegs.getSipDataString(aorString)
    logging.info("Sending %s", sipRecordStr)
    writer.write(sipRecordStr.encode('utf-8'))
    writer.close()

if __name__ == "__main__":
    main()
