import { writable } from 'svelte/store';

export const currentSong = writable(null);
export const isPlaying = writable(false);
export const currentTime = writable(0);
export const duration = writable(0);

let audio = null;
let onSongEndCallback = null;

if (typeof window !== 'undefined') {
  audio = new Audio();
  
  audio.addEventListener('timeupdate', () => {
    currentTime.set(audio.currentTime);
  });
  
  audio.addEventListener('loadedmetadata', () => {
    duration.set(audio.duration);
  });
  
  audio.addEventListener('ended', () => {
    isPlaying.set(false);
    if (onSongEndCallback) {
      onSongEndCallback();
    }
  });
  
  audio.addEventListener('play', () => {
    isPlaying.set(true);
  });
  
  audio.addEventListener('pause', () => {
    isPlaying.set(false);
  });
}

export function playSong(song) {
  if (!audio) return;
  
  currentSong.set(song);
  audio.src = `http://localhost:8000/api/stream/${encodeURIComponent(song.path)}`;
  audio.play();
}

export function pause() {
  if (audio) audio.pause();
}

export function resume() {
  if (audio) audio.play();
}

export function seek(time) {
  if (audio) audio.currentTime = time;
}

export function setVolume(volume) {
  if (audio) audio.volume = volume;
}

export function setOnSongEnd(callback) {
  onSongEndCallback = callback;
}
