<script>
    import { currentSong, isPlaying, currentTime, duration, pause, resume, seek } from '../lib/player.js';
  import { playNext, playPrevious } from '../queue.js';


  let imageError = false;
  
  function togglePlay() {
    if ($isPlaying) {
      pause();
    } else {
      resume();
    }
  }

  function handleNext() {
    playNext();
  }
  
  function handlePrevious() {
    playPrevious();
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

  $: if ($currentSong) imageError = false;
</script>

{#if $currentSong}
  <div class="player">
    <div class="song-info">
      <div class="album-art">
        {#if $currentSong.coverUrl && !imageError}
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
      <div class="playback-buttons">
        <button class="control-button" on:click={handlePrevious} title="Previous">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M3 2v12h2V2H3zm3 6l8 6V2l-8 6z"/>
          </svg>
        </button>
        
        <button class="play-button" on:click={togglePlay}>
          {#if $isPlaying}
            <span class="pause-icon"></span>
          {:else}
            <span class="play-icon">▶</span>
          {/if}
        </button>
        
        <button class="control-button" on:click={handleNext} title="Next">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M11 2v12h2V2h-2zM2 2v12l8-6-8-6z"/>
          </svg>
        </button>
      </div>
      
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
    z-index: 100;
  }

  .play-icon {
    font-size: 1rem;
    margin-left: 3px;
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
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    max-width: 600px;
  }


  .playback-buttons {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .control-button {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: transparent;
    color: var(--text-secondary);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }

  .control-button:hover {
    color: var(--text-primary);
    transform: scale(1.1);
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
  
  .play-button:hover {
    transform: scale(1.1);
    background: var(--accent-secondary);
  }
  
  .progress-container {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .time {
    font-size: 0.85rem;
    color: var(--text-secondary);
    min-width: 40px;
    text-align: center;
    font-variant-numeric: tabular-nums;
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
