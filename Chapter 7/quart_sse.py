import json
import struct
import asyncio
import datetime
import pytz
from quart import Quart, Response, request

app = Quart(__name__)

class NTPProtocol:
    def __init__(self, loop, timezone):
        self.loop = loop
        self.future = loop.create_future()
        self.transport = None
        self.timezone = timezone

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.future.set_result(data)
        self.transport.close()

    def connection_lost(self, exc):
        if not self.future.done():
            if exc is None:
                self.future.set_exception(Exception("Connection closed"))
            else:
                self.future.set_exception(exc)

async def get_ntp_time(host="pool.ntp.org", timezone="UTC"):
    port = 123
    address = (host, port)
    msg = b'\x1b' + b'\0' * 47

    TIME1970 = 2208988800

    try:
        loop = asyncio.get_running_loop()
        protocol = NTPProtocol(loop, timezone)
        transport, _ = await loop.create_datagram_endpoint(
            lambda: protocol, remote_addr=address
        )

        transport.sendto(msg)
        data = await protocol.future

        t = struct.unpack("!12I", data)[10]
        t -= TIME1970

        utc_time = datetime.datetime.utcfromtimestamp(t)
        local_tz = pytz.timezone(timezone)
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

        return local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    except Exception as e:
        print(f"Error getting NTP time: {e}")
        return None

async def time_generator(host="pool.ntp.org", timezone="UTC", interval=5):
    while True:
        local_time = await get_ntp_time(host, timezone)
        if local_time:
            yield json.dumps({'time': local_time})
        await asyncio.sleep(interval)

@app.route("/ntp_sse")
async def ntp_sse():
    timezone = request.args.get("timezone", "UTC")
    interval = int(request.args.get("interval", 5))

    async def generate():
        try:
            async for time_data in time_generator(timezone=timezone, interval=interval):
                yield time_data
        except pytz.exceptions.UnknownTimeZoneError:
            yield json.dumps({"error": "Invalid timezone"})
        except Exception as e:
            yield json.dumps({"error": e})

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
