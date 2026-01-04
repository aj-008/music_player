from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import urllib.parse
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MUSIC_DIR = Path.home() / "music"

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

