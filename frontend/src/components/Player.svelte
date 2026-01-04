<script>
  import { currentSong, isPlaying, currentTime, duration, pause, resume, seek } from '../lib/player.js';


  let imageError = false;
  
  function togglePlay() {
    if ($isPlaying) {
      pause();
    } else {
      resume();
    }
  }
  
  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
  
  function handleSeek(event) {
    const percent = event.offsetX / event.target.offsetWidth;
    seek(percent * $duration);
  }
</script>

{#if $currentSong}
  <div class="player">
    <div class="song-info">
      <div class="album-art">
        {#if !imageError}
          <img 
            src={$currentSong.coverUrl} 
            alt={$currentSong.album}
            on:error={() => imageError = true}
          />
        {:else}
          <div class="no-cover">
            {$currentSong.title.charAt(0)}
          </div>
        {/if}
      </div>
      
      <div class="text-info">
        <div class="title">{$currentSong.title}</div>
        <div class="artist">{$currentSong.artist}</div>
      </div>
    </div>
    
    <div class="controls">
      <button class="play-button" on:click={togglePlay}>
        {#if $isPlaying}
          <span class="pause-icon"></span>
        {:else}
          <span class="play-icon">▶</span>
        {/if}
      </button>
      
      <div class="progress-container">
        <span class="time">{formatTime($currentTime)}</span>
        <div class="progress-bar" on:click={handleSeek}>
          <div 
            class="progress-fill" 
            style="width: {($currentTime / $duration) * 100}%"
          ></div>
        </div>
        <span class="time">{formatTime($duration - $currentTime)}</span>
      </div>
    </div>
  </div>
{/if}

<style>
  .player {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--bg-player);
    border-top: 1px solid var(--border-primary);
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .play-icon {
    font-size: 1rem;
    margin-left: 3px;
    margin-bottom: 3px;
  }
  
  .pause-icon {
    width: 10px;
    height: 12px;
    position: relative;
  }

  .pause-icon::before,
  .pause-icon::after {
    content: '';
    position: absolute;
    width: 3px;
    height: 12px;
    background: var(--base);
    border-radius: 1px;
  }
  
  .pause-icon::before {
    left: 0;
  }
  
  .pause-icon::after {
    right: 0;
  }


  .song-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    min-width: 250px;
    flex: 0 0 30%;
  }

  .album-art {
    width: 56px;
    height: 56px;
    flex-shrink: 0;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .album-art img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .no-cover {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: bold;
    color: white;
    text-transform: uppercase;
  }
  
  .title {
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
  
  .artist {
    color: #aaa;
    font-size: 0.9rem;
  }
  
  .controls {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .play-button {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--accent-primary);
    color: var(--base);
    border: none;
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.1s, background 0.2s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  button:hover {
    transform: scale(1.1);
    background: var(--accent-secondary);
  }
  
  .progress-container {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .time {
    font-size: 0.85rem;
    color: var(--text-secondary);
    min-width: 30px;
  }
  
  .progress-bar {
    flex: 1;
    height: 6px;
    background: var(--overlay);
    border-radius: 3px;
    cursor: pointer;
    position: relative;
  }
  
  .progress-fill {
    height: 100%;
    background: var(--accent-primary); 
    border-radius: 3px;
    transition: width 0.1s;
  }
</style>
