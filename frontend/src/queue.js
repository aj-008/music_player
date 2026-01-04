import { writable, derived } from 'svelte/store';
import { playSong as playAudio } from './lib/player.js';

export const queue = writable([]);
export const currentIndex = writable(-1);

export const currentQueueSong = derived(
  [queue, currentIndex],
  ([$queue, $currentIndex]) => {
    if ($currentIndex >= 0 && $currentIndex < $queue.length) {
      return $queue[$currentIndex];
    }
    return null;
  }
);

export function addToQueue(song) {
  queue.update(q => [...q, song]);
}

export function addMultipleToQueue(songs) {
  queue.update(q => [...q, ...songs]);
}

export function removeFromQueue(index) {
  queue.update(q => {
    const newQueue = [...q];
    newQueue.splice(index, 1);
    return newQueue;
  });
  
  currentIndex.update(idx => {
    if (idx > index) return idx - 1;
    if (idx === index) return idx;
    return idx;
  });
}

export function clearQueue() {
  queue.set([]);
  currentIndex.set(-1);
}

export function playFromQueue(index) {
  let songToPlay;
  queue.update(q => {
    if (index >= 0 && index < q.length) {
      songToPlay = q[index];
    }
    return q;
  });
  
  if (songToPlay) {
    currentIndex.set(index);
    playAudio(songToPlay);
  }
}

export function playNext() {
  let nextSong;
  let nextIndex;
  
  currentIndex.update(idx => {
    nextIndex = idx + 1;
    return nextIndex;
  });
  
  queue.update(q => {
    if (nextIndex < q.length) {
      nextSong = q[nextIndex];
    }
    return q;
  });
  
  if (nextSong) {
    playAudio(nextSong);
  }
}

export function playPrevious() {
  let prevSong;
  let prevIndex;
  
  currentIndex.update(idx => {
    prevIndex = Math.max(0, idx - 1);
    return prevIndex;
  });
  
  queue.update(q => {
    if (prevIndex >= 0 && prevIndex < q.length) {
      prevSong = q[prevIndex];
    }
    return q;
  });
  
  if (prevSong) {
    playAudio(prevSong);
  }
}

export function playSongWithQueue(song, songsToQueue = []) {
  const songIndex = songsToQueue.findIndex(s => s.id === song.id);
  
  if (songIndex !== -1) {
    queue.set(songsToQueue);
    currentIndex.set(songIndex);
  } else {
    queue.update(q => [song, ...q]);
    currentIndex.set(0);
  }
  
  playAudio(song);
}
