import SipRegistry
import asyncio
import logging
import sys

log = None

def main():
    global sipRegs
    logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stdout,)

    # Parse the registry
    logging.info("Parsing registry")
    sipRegs = SipRegistry.SipRegistry("../regs")
    logging.info("Parsing complete")

    # Set up the event server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handleConnection, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve connection requests until Ctrl+C is pressed
    logging.info('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server when done
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

async def handleConnection(reader, writer):
    """
    Callback executed every time there is a connection from a client
    """
    try:
        addr = writer.get_extra_info('peername')
        logging.info("record request from %s", addr)
        await asyncio.wait_for(handleRecordRequest(reader, writer), timeout=10)
    except asyncio.TimeoutError:
        logging.error("Connection Timeout ")
    finally:
        writer.close()

async def handleRecordRequest(reader, writer):
    """
    Callback that handles the data exchange protocol between the client and the server
    """
    global sipRegs
    aorBytes = await reader.read(100)
    aorString = aorBytes.decode('utf-8')
    sipRecordStr = sipRegs.getSipDataString(aorString)
    logging.info("Sending %s", sipRecordStr)
    writer.write(sipRecordStr.encode('utf-8'))

if __name__ == "__main__":
    main()
