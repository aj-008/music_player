<script>
  import { onMount } from 'svelte';  
  import { getSongs } from '../lib/api.js';
  import SongItem from '../components/SongItem.svelte';
  import { playSong } from '../lib/player.js';
  import { addToQueue } from '../queue.js';

  let songs = [];
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
        songs = await getSongs();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function handlePlay(event) {
    const song = event.detail;
    playSong(song); 
  }
  
  function handleAddToQueue(event) {
    const song = event.detail;
    addToQueue(song);        
  }
  
  function handleAddToPlaylist(event) {
    const song = event.detail;
    console.log('Add to playlist:', song.title);
    // TODO: Show playlist selector
  }
</script>

<div class="library">
  <h2>Your Library ({songs.length} songs)</h2>
  
  {#if loading}
    <p>Loading songs...</p>
  {:else if error}
    <p class="error">Error: {error}</p>
  {:else if songs.length === 0}
    <p>No songs found. Add MP3 files to your Music folder!</p>
  {:else}
      <div class="song-list">

      <div class="song-header">
        <div class="header-art">#</div>
        <div class="header-title">Title</div>
        <div class="header-artist">Artist</div>
        <div class="header-album">Album</div>
        <div class="header-duration">Duration</div>
      </div>
      {#each songs as song (song.id)}
          <SongItem 
              {song}
              on:play={handlePlay}
              on:addToQueue={handleAddToQueue}
              on:addToPlaylist={handleAddToPlaylist}
          />
      {/each}
    </div>
  {/if}
</div>

<style>
  .library {
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }
  
  .error {
    color: #ff4444;
  }
  
  .song-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  
  .song-header {
    display: grid;
    grid-template-columns: 48px 1.5fr 1.5fr 1.5fr 80px;  
    gap: 1rem;  
    padding: 0.5rem 1rem; 
    border-bottom: 1px solid var(--border-primary);
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: left;
  }
  
  .header-duration {
    text-align: right;
  }
  
</style>
