<script>
  import { onMount } from 'svelte';
  import SongItem from '../components/SongItem.svelte';
  import { playSongWithQueue, addToQueue, addMultipleToQueue } from '../queue.js';
  
  export let params = {};  
  
  let album = null;
  let loading = true;
  
  onMount(async () => {
    const response = await fetch('http://localhost:8000/api/albums');
    const albums = await response.json();
    
    const albumTitle = decodeURIComponent(params.title);
    album = albums.find(a => a.title === albumTitle);
    
    loading = false;
  });
  
  function handlePlay(event) {
    const song = event.detail;
    playSongWithQueue(song, album.songs); 
  }

  function handleAddToQueue(event) {
    const song = event.detail;
    addToQueue(song);
  }
  
  function playAll() {
    if (album && album.songs.length > 0) {
      playSongWithQueue(album.songs[0], album.songs);
    }
  }

  function queueAll() {
    if (album && album.songs.length > 0) {
      addMultipleToQueue(album.songs);
    }
  }
</script>

{#if loading}
  <div class="loading">Loading...</div>
{:else if album}
  <div class="album-detail">
    <div class="album-header">
      <div class="album-art-large">
        {#if album.cover}
          <img src={album.cover} alt={album.title} />
        {:else}
          <div class="no-cover">
            {album.title.charAt(0)}
          </div>
        {/if}
      </div>
      
      <div class="album-info">
        <h1>{album.title}</h1>
        <p class="artist">{album.artist}</p>
        <p class="meta">{album.songs.length} songs</p>
        
        <button class="play-all" on:click={playAll}>
          ▶ Play Album
        </button>
        <button class="queue-all" on:click={queueAll}>
            Queue Album
        </button>
      </div>
    </div>
    
    <div class="song-list">
      <div class="song-header">
        <div class="header-number">#</div>
        <div class="header-title">Title</div>
        <div class="header-artist">Artist</div>
        <div class="header-duration">Duration</div>
      </div>
      
      {#each album.songs as song, index (song.id)}
        <div class="song-wrapper">
          <div class="track-number">{song.trackNumber}</div>
          <SongItem 
            {song} 
            hideAlbumArt={true} 
            hideAlbum={true} 
            on:play={handlePlay} 
            on:addToQueue={handleAddToQueue}
          />
        </div>
      {/each}
    </div>
  </div>
{:else}
  <div class="error">Album not found</div>
{/if}

<style>
  .album-detail {
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary);
  }
  
  .error {
    text-align: center;
    padding: 2rem;
    color: var(--error);
  }
  
  .album-header {
    display: flex;
    gap: 2rem;
    padding: 2rem 0;
    margin-bottom: 2rem;
  }
  
  .album-art-large {
    width: 232px;
    height: 232px;
    flex-shrink: 0;
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  }
  
  .album-art-large img {
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
    font-size: 6rem;
    color: var(--text-primary);
    font-weight: bold;
    text-transform: uppercase;
  }
  
  .album-info {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .album-label {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-secondary);
    letter-spacing: 1px;
  }
  
  h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary);
    line-height: 1.2;
  }
  
  .artist {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 0;
  }
  
  .meta {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin: 0;
  }
  
  .play-all {
    margin-top: 1rem;
    padding: 0.75rem 2rem;
    background: var(--accent-primary);
    color: var(--base);
    border: none;
    border-radius: 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, background 0.2s;
    align-self: flex-start;
  }
  
  .play-all:hover {
    transform: scale(1.05);
    background: var(--accent-secondary);
  }

.queue-all {
  padding: 0.75rem 2rem;
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-secondary);
  border-radius: 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, background 0.2s;
  align-self: flex-start;
}

.queue-all:hover {
  transform: scale(1.05);
  background: var(--bg-tertiary);
}
  
  .song-list {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .song-header {
    display: grid;
    grid-template-columns: 40px 2fr 1.5fr 80px;
    gap: 1rem;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid var(--border-primary);
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .header-duration {
    text-align: right;
  }
  
  .song-wrapper {
    display: grid;
    grid-template-columns: 40px 1fr;
    gap: 1rem;
    align-items: center;
  }
  
  .track-number {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-variant-numeric: tabular-nums;
  }
</style>
