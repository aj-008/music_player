<script>
  import { createEventDispatcher } from 'svelte';
  export let song;  
  const dispatch = createEventDispatcher(); 
  let showMenu = false;
  let menuX = 0;
  let menuY = 0;

  let imageError = false;

  export let hideAlbumArt = false;  
  export let hideAlbum = false; 

  function handleRightClick(event) {
    event.preventDefault();
    showMenu = true;
    menuX = event.clientX;
    menuY = event.clientY;
  }
  
  function addToQueue() {
    dispatch('addToQueue', song);
    showMenu = false;
  }
  
  function addToPlaylist() {
    dispatch('addToPlaylist', song);
    showMenu = false;
  }

  function handleClickOutside() {
    showMenu = false;
  }

  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
</script>

<svelte:window on:click={handleClickOutside} />

<div  
  class="song-item"
  class:no-art={hideAlbumArt}
  class:no-album-column={hideAlbum}
  on:click={() => dispatch('play', song)}
  on:contextmenu={handleRightClick}
  >

  {#if !hideAlbumArt}
    <div class="album-art">
      {#if song.coverUrl && !imageError}
        <img 
          src={song.coverUrl} 
          alt={song.album}
          on:error={() => imageError = true}
        />
      {:else}
        <div class="no-cover">
          {song.title.charAt(0)}
        </div>
      {/if}
    </div>
  {/if}

  <span class="title">{song.title}</span>
  <span class="artist">{song.artist}</span>
  {#if !hideAlbum}
    <div class="album">{song.album}</div>
  {/if}
  <span class="duration">{formatTime(song.duration)}</span>
</div>


{#if showMenu}
  <div 
    class="context-menu" 
    style="left: {menuX}px; top: {menuY}px"
    on:click|stopPropagation
  >
    <button on:click={addToQueue}>Add to Queue</button>
    <button on:click={addToPlaylist}>Add to Playlist</button>
  </div>
{/if}

<style>
  .song-item {
    display: grid;
    grid-template-columns: 48px 1.5fr 1.5fr 1.5fr 80px;  
    gap: 1rem;
    align-items: center;
    padding: 0.5rem 1rem;
    min-height: 60px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: background 0.3s;
  }

  .song-item.no-art.no-album-column {
    grid-template-columns: 2fr 1.5fr 80px;
  }

  .info {
    display: flex;
    flex-direction: row;
    gap: 0.10rem;
  }
  
  .song-item:hover {
    background: var(--bg-tertiary);
  }
  
  .album-art {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    border-radius: 10px;
    overflow: hidden;
  }
  
  .album-art img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .no-cover {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, 
      var(--accent-gradient-start), 
      var(--accent-gradient-end)
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
  }
  
  .title {
    color: var(--text-primary);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
  }
  
  .artist {
    color: var(--text-secondary);
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
  }
  
  .album {
    color: var(--text-secondary);
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
  }
  
  .duration {
    color: var(--text-secondary);
    font-size: 0.9rem;
    text-align: right;
    font-variant-numeric: tabular-nums;
    text-align: right;
  }
  
  .context-menu {
    position: fixed;
    background: #1a1a1a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    z-index: 1000;
  }
  
  .context-menu button {
    display: block;
    width: 100%;
    padding: 0.5rem 1rem;
    background: none;
    border: none;
    color: white;
    text-align: left;
    cursor: pointer;
  }
  
  .context-menu button:hover {
    background: #333;
  }
</style>
