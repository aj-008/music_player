from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import urllib.parse
import base64
from typing import List
import json
import asyncio
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MUSIC_DIR = Path.home() / "music"

active_connections: List[WebSocket] = []

latest_state = {}
latest_state_lock = asyncio.Lock()

@app.get("/api/songs")
def get_songs():
    songs = []
    for file_path in MUSIC_DIR.rglob("*.mp3"):
        try:
            audio = MP3(file_path)
            
            cover_data = None
            try:
                id3 = ID3(file_path)
                for key in id3.keys():
                    if key.startswith('APIC'):
                        apic = id3[key]
                        img_base64 = base64.b64encode(apic.data).decode('utf-8')
                        mime = apic.mime if apic.mime else "image/jpeg"
                        cover_data = f"data:{mime};base64,{img_base64}"
                        break
            except:
                pass

            track_num = 0
            if "TRCK" in audio:
                track_str = str(audio["TRCK"][0])
                track_num = int(track_str.split('/')[0]) if track_str else 0
            
            songs.append({
                "id": str(file_path),
                "title": audio.get("TIT2", [file_path.stem])[0] if "TIT2" in audio else file_path.stem,
                "artist": audio.get("TPE1", ["Unknown Artist"])[0] if "TPE1" in audio else "Unknown Artist",
                "album": audio.get("TALB", ["Unknown Album"])[0] if "TALB" in audio else "Unknown Album",
                "duration": int(audio.info.length),
                "path": str(file_path),
                "coverUrl": cover_data,
                "trackNumber": track_num
            })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return songs


@app.get("/api/stream/{song_id:path}")
def stream_song(song_id: str):
    """Stream an audio file"""
    file_path = Path(urllib.parse.unquote(song_id))
    
    if not file_path.exists():
        return {"error": "File not found"}
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        headers={"Accept-Ranges": "bytes"}
    )




@app.get("/api/albums")
def get_albums():
    """Return list of albums with songs grouped"""
    songs = get_songs()
    
    albums = {}
    for song in songs:
        album_name = song["album"]
        if album_name not in albums:
            albums[album_name] = {
                "title": album_name,
                "artist": song["artist"],
                "cover": song["coverUrl"],
                "songs": []
            }
        albums[album_name]["songs"].append(song)

    for album in albums.values():
        album["songs"].sort(key=lambda s: s["trackNumber"])

    return list(albums.values())




# These are just for broadcasting to the pico w
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"WebSocket client connected. Total: {len(active_connections)}")
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            print(f"Received: {json.dumps(data)}")
            
            # Handle different command types
            command = data.get("command")
            
            if command in ["next", "prev", "play_pause"]:
                print(f"Broadcasting action: {command}")
                await broadcast({"action": command})
            else:
                print(f"Unknown command: {command}")
                
    except WebSocketDisconnect:
        print("Client disconnected")
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

async def broadcast(message: dict):
    """Send message to all connected clients"""
    print(f"Broadcasting to {len(active_connections)} clients: {json.dumps(message)}")
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
            print(f"Sent to client")
        except Exception as e:
            print(f"Failed to send to client: {e}")
            disconnected.append(connection)
    
    # Clean up disconnected clients
    for conn in disconnected:
        active_connections.remove(conn)



@app.post("/api/player/update")
async def update_player_state(state: dict):
    state_norm = dict(state)
    state_norm["duration"] = int(state.get("duration", 0) or 0)
    state_norm["current_time"] = int(state.get("current_time", 0) or 0)
    dur = state_norm["duration"] or 1
    ct = state_norm["current_time"]
    state_norm["progress"] = int((ct * 100) / dur)

    async with latest_state_lock:
        latest_state.clear()
        latest_state.update(state_norm)

    await broadcast({"type": "player_state", "data": state_norm})
    return {"status": "ok"}




