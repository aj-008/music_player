import { playNext, playPrevious } from '../queue.js';
import { pause, resume, isPlaying } from './player.js';
import { get } from 'svelte/store';

let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 3;

export function connectWebSocket() {
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
    console.log('Max WebSocket reconnect attempts reached. Pico features disabled.');
    return;
  }
  
  try {
    ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('WebSocket connected - Pico controller enabled');
      reconnectAttempts = 0;
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket received:', data);
      
      if (data.action === 'next') {
        playNext();
      } else if (data.action === 'prev') {
        playPrevious();
      } else if (data.action === 'play_pause') {
        const playing = get(isPlaying);
        if (playing) pause();
        else resume();
      }
    };
    
    ws.onerror = (error) => {
      console.log('WebSocket error (Pico features disabled):', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      reconnectAttempts++;
      
      if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
        console.log(`Reconnecting... (attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
        setTimeout(connectWebSocket, 3000);
      }
    };
  } catch (error) {
    console.log('WebSocket unavailable (Pico features disabled)');
  }
}

export function sendPlayerState(state) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    fetch('http://localhost:8000/api/player/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state)
    }).catch(err => {
    });
  }
}
