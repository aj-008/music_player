<script>
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  
  let albums = [];
  let loading = true;
  
  onMount(async () => {
    const response = await fetch('http://localhost:8000/api/albums');
    albums = await response.json();
    loading = false;
  });

  function handleAlbumClick(album) {
    push(`/albums/${encodeURIComponent(album.title)}`);
  }

  function handleRightClick() {
    // do nothing on right click
  }
</script>

<div class="albums">
  <h2>Albums</h2>
  
  {#if loading}
    <p>Loading...</p>
  {:else}
    <div class="album-grid">
      {#each albums as album (album.title)}
          <div class="album-card" on:click={() => handleAlbumClick(album)} 
          on:contextmenu|preventDefault={handleRightClick}
          >

          <div class="album-art">
            {#if album.cover}
              <img src={album.cover} alt={album.title} />
            {:else}
              <div class="no-cover">
                {album.title.charAt(0)}
              </div>
            {/if}
          </div>
          <h3>{album.title}</h3>
          <p>{album.artist}</p>
          <p class="song-count">{album.songs.length} songs</p>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .albums {
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }

  .album-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: var(--spacing-lg);
  }

  h2 {
    margin-bottom: var(--spacing-lg);
    color: var(--text-primary);
  }
  
  .album-card {
    cursor: pointer;
    padding: var(--spacing-md);
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    transition: background 0.2s, transform 0.2s;
  }

  .album-card:hover {
    background: var(--bg-tertiary);
    transform: translateY(-4px);
  }
  
  .album-art {
    width: 100%;
    aspect-ratio: 1;
    border-radius: var(--radius-md);
    overflow: hidden;
    margin-bottom: var(--spacing-md);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
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
    font-size: 4rem;
    color: var(--text-primary);
    font-weight: bold;
    text-transform: uppercase;
  }
  
  h3 {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  p {
    margin: var(--spacing-xs) 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .song-count {
    font-size: 0.85rem;
    color: var(--text-muted);
  }
</style>
