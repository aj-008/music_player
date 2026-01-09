import serial
import asyncio
import websockets
import json
import sys

SERIAL_PORT = "/dev/ttyACM0"  # This is the port on which the pico is connected
BAUD_RATE = 115200
WS_URL = "ws://localhost:8000/ws"

async def handle_pico_to_server(ws, ser):
    """Read from Pico and send to FastAPI"""
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f" Pico → Bridge: {line}")
                    data = json.loads(line)
                    button = data.get("button")
                    
                    if button in ["next", "prev", "play_pause"]:
                        command = {"command": button}
                        await ws.send(json.dumps(command))
                        print(f" Bridge → Server: {json.dumps(command)}")
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f" Parse error: {e} | Raw: {line}")
        
        await asyncio.sleep(0.01)

async def handle_server_to_pico(ws, ser):
    """Receive from FastAPI and send to Pico"""
    try:
        async for message in ws:
            data = json.loads(message)
            print(f" Server → Bridge: {json.dumps(data)[:100]}...")
            
            if data.get("type") == "player_state":
                state = data["data"]
                pico_data = {
                    "title": state.get("title", "")[:32],
                    "artist": state.get("artist", "")[:32],
                    "progress": int(state.get("progress", 0)),
                    "duration": int(state.get("duration", 0)),
                    "current_time": int(state.get("current_time", 0))
                }
                
                json_str = json.dumps(pico_data, separators=(',', ':')) + "\n"

                ser.write(json_str.encode('utf-8'))
                print(f" Bridge → Pico: {json_str.strip()}")
            elif data.get("action"):
                # Forward button actions back to Pico (for confirmation LEDs etc)
                action_data = {"action": data["action"]} 
                ser.write((json.dumps(action_data) + "\n").encode('utf-8'))
                print(f" Bridge → Pico (action): {data['action']}")
    except Exception as e:
        print(f" Server handler error: {e}")

async def main():
    print(f" Connecting to Pico on {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        print(f" Pico connected")
    except serial.SerialException as e:
        print(f" Pico connection failed: {e}")
        print(f"\n Try: ls /dev/tty* | grep -E 'ACM|USB'")
        sys.exit(1)
    
    print(f"🔌 Connecting to WebSocket at {WS_URL}...")
    
    try:
        async with websockets.connect(WS_URL) as ws:
            print(" WebSocket connected\n")
            print("=" * 50)
            print("Bridge active! Legend:")
            print(" Pico → Server")
            print(" Server → Pico")
            print("=" * 50 + "\n")
            
            await asyncio.gather(
                handle_pico_to_server(ws, ser),
                handle_server_to_pico(ws, ser)
            )
    except Exception as e:
        print(f"WebSocket failed: {e}")
        ser.close()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nBridge stopped")
