import { writable, derived, get } from 'svelte/store';
import { playSong as playAudio, setOnSongEnd } from './lib/player.js';

export const queue = writable([]);
export const currentIndex = writable(-1);

setOnSongEnd(() => {
  playNext();
});

export const currentQueueSong = derived(
  [queue, currentIndex],
  ([$queue, $currentIndex]) =>
    $currentIndex >= 0 && $currentIndex < $queue.length ? $queue[$currentIndex] : null
);

function clampIndex(idx, len) {
  if (len <= 0) return -1;
  return Math.max(0, Math.min(idx, len - 1));
}

export function addToQueue(song) {
  queue.update(q => [...q, song]);
}

export function addMultipleToQueue(songs) {
  queue.update(q => [...q, ...songs]);
}

export function removeFromQueue(index) {
  const q = get(queue);
  if (index < 0 || index >= q.length) return;

  queue.set(q.filter((_, i) => i !== index));

  const idx = get(currentIndex);
  const newLen = q.length - 1;

  if (newLen <= 0) {
    currentIndex.set(-1);
    return;
  }

  if (idx > index) {
    currentIndex.set(idx - 1);
  } else if (idx === index) {
    currentIndex.set(clampIndex(idx, newLen));
  }
}

export function clearQueue() {
  queue.set([]);
  currentIndex.set(-1);
}

export function playFromQueue(index) {
  const q = get(queue);
  if (index < 0 || index >= q.length) return;

  currentIndex.set(index);
  playAudio(q[index]);
}

export function playNext() {
  const q = get(queue);
  const idx = get(currentIndex);
  const next = idx + 1;

  if (next >= 0 && next < q.length) {
    currentIndex.set(next);
    playAudio(q[next]);
  }
}

export function playPrevious() {
  const q = get(queue);
  const idx = get(currentIndex);
  const prev = Math.max(0, idx - 1);

  if (prev >= 0 && prev < q.length) {
    currentIndex.set(prev);
    playAudio(q[prev]);
  }
}


export function playSongWithQueue(song, contextSongs = []) {
  const q = get(queue);
  const idx = get(currentIndex);

  const key = (s) => s?.id ?? s?.path;
  const songKey = key(song);

  if (q.length === 0 && contextSongs.length > 0) {
    const startIndex = contextSongs.findIndex(s => key(s) === songKey);
    queue.set(contextSongs);
    currentIndex.set(startIndex >= 0 ? startIndex : 0);
    playAudio(startIndex >= 0 ? contextSongs[startIndex] : contextSongs[0]);
    return;
  }

  const existing = q.findIndex(s => key(s) === songKey);
  if (existing !== -1) {
    currentIndex.set(existing);
    playAudio(q[existing]);
    return;
  }

  const insertAt = idx >= 0 ? idx + 1 : 0;

  let block = [];
  if (contextSongs.length > 0) {
    const start = contextSongs.findIndex(s => key(s) === songKey);
    if (start !== -1) {
      block = contextSongs.slice(start);
    } else {
      block = [song];
    }
  } else {
    block = [song];
  }

  currentIndex.set(insertAt);
  playAudio(song);
}


