<script>
  import { onMount } from 'svelte';
  import SongItem from '../components/SongItem.svelte';
  import { playSong } from '../lib/player.js';
  import { playSongWithQueue, addToQueue } from '../queue.js';
  import { push } from 'svelte-spa-router';

  let query = '';
  let songs = [];
  let albums = [];
  let loading = true;
  let error = null;

  let songResults = [];
  let bestAlbum = null;

  onMount(async () => {
    try {
      const [songsRes, albumsRes] = await Promise.all([
        fetch('http://localhost:8000/api/songs'),
        fetch('http://localhost:8000/api/albums'),
      ]);

      if (!songsRes.ok) throw new Error('Failed to load songs');
      if (!albumsRes.ok) throw new Error('Failed to load albums');

      songs = await songsRes.json();
      albums = await albumsRes.json();
    } catch (e) {
      error = e.message ?? String(e);
    } finally {
      loading = false;
    }
  });




  function norm(s) {
    return (s ?? '').toString().toLowerCase().trim();
  }

  function tokens(q) {
    return norm(q).split(/\s+/).filter(Boolean);
  }

  function fuzzyScore(haystack, needle) {
    const h = norm(haystack);
    const n = norm(needle);
    
    if (n.length === 0) return 0;
    if (h.length === 0) return 0;
    
    // Check if needle is in haystack
    if (h.includes(n)) {
      // Score based on how early it appears
      const index = h.indexOf(n);
      return 100 - index;  // Earlier match = higher score
    }
    
    return 0;
  }

  function fuzzyScoreTokens(haystack, q) {
    const ts = tokens(q);
    if (ts.length === 0) return 0;

    let total = 0;
    let matched = 0;

    for (const t of ts) {
      const s = fuzzyScore(haystack, t);
      if (s !== -Infinity) {
        total += s;
        matched++;
      }
    }

    return matched === 0 ? -Infinity : total;
  }




    function scoreSong(song, q) {
      const title  = fuzzyScoreTokens(song.title, q);
      const artist = fuzzyScoreTokens(song.artist, q) * 0.75;
      const album  = fuzzyScoreTokens(song.album, q) * 0.6;

      return title * 1.2 + artist + album;
    }

    function scoreAlbum(album, q) {
      const title  = fuzzyScoreTokens(album.title, q) * 1.2;
      const artist = fuzzyScoreTokens(album.artist, q) * 0.8;
      return title + artist;
    }


  $: if (!loading) {
    const q = norm(query);

    if (q.length === 0) {
      songResults = [];
      bestAlbum = null;
    } else {
      songResults = songs
        .map(s => ({ s, score: scoreSong(s, q) }))
        .filter(x => x.score > -Infinity)
        .sort((a, b) => b.score - a.score)
        .slice(0, 5)
        .map(x => x.s);

      bestAlbum = albums
        .map(a => ({ a, score: scoreAlbum(a, q) }))
        .filter(x => x.score > -Infinity)
        .sort((a, b) => b.score - a.score)[0]?.a ?? null;
    }
  }

  function onSongPlay(event) {
    const song = event.detail;
    playSong(song);
  }

  function onAddToQueue(event) {
    addToQueue(event.detail);
  }

  function openAlbum(album) {
    push(`/albums/${encodeURIComponent(album.title)}`);
  }
</script>

<div class="search-page">
  <div class="search-header">
    <h2>Search</h2>
    <input
      class="search-input"
      type="text"
      placeholder="Search songs, artists, or albums…"
      bind:value={query}
      spellcheck="false"
      autocomplete="off"
    />
  </div>

  {#if loading}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">Error: {error}</p>
  {:else}
    {#if query.trim().length === 0}
      <div class="empty-state">
        <p class="muted">Start typing to search your library</p>
      </div>
    {:else}
      <div class="results">
        <section class="panel">
          <div class="panel-title">Top Songs</div>

          {#if songResults.length === 0}
            <div class="muted">No matching songs.</div>
          {:else}
            <div class="song-list">
              <div class="song-header-row">
                <div class="header-art">#</div>
                <div>Title</div>
                <div>Artist</div>
                <div>Album</div>
                <div class="right">Duration</div>
              </div>

              {#each songResults as song (song.id)}
                <SongItem
                  {song}
                  on:play={onSongPlay}
                  on:addToQueue={onAddToQueue}
                />
              {/each}
            </div>
          {/if}
        </section>

        <section class="panel">
          <div class="panel-title">Top Album</div>

          {#if !bestAlbum}
            <div class="muted">No matching album.</div>
          {:else}
            <div 
              class="album-result" 
              on:click={() => openAlbum(bestAlbum)} 
              on:keydown={(e) => e.key === 'Enter' && openAlbum(bestAlbum)}
              role="button" 
              tabindex="0"
            >
              <div class="album-art">
                {#if bestAlbum.cover}
                  <img src={bestAlbum.cover} alt={bestAlbum.title} />
                {:else}
                  <div class="no-cover">{bestAlbum.title.charAt(0)}</div>
                {/if}
              </div>
              <div class="album-meta">
                <div class="album-title">{bestAlbum.title}</div>
                <div class="album-artist">{bestAlbum.artist}</div>
                <div class="album-count muted">{bestAlbum.songs.length} songs</div>
              </div>
            </div>
          {/if}
        </section>
      </div>
    {/if}
  {/if}
</div>
<style>
  .search-page {
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }

  .search-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: var(--spacing-lg);
  }

  h2 {
    margin: 0;
    color: var(--text-primary);
  }

  .search-input {
    width: min(720px, 100%);
    padding: 0.85rem 1rem;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-secondary);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-input:focus {
    border-color: var(--accent-primary);
  }

  .results {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--spacing-xl);
    align-items: start;
  }

  .panel {
    background: transparent;
  }

  .panel-title {
    margin-bottom: var(--spacing-md);
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
  }

  .song-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .song-header-row {
    display: grid;
    grid-template-columns: 48px 2fr 1.5fr 1.5fr 80px;
    gap: 1rem;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid var(--border-primary);
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .right { text-align: right; }
  .header-art { opacity: 0.8; }

  .album-result {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
  }

  .album-result:hover {
    background: var(--bg-tertiary);
    transform: translateY(-2px);
  }

  .album-art {
    width: 80px;
    height: 80px;
    border-radius: var(--radius-md);
    overflow: hidden;
    flex-shrink: 0;
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
    background: linear-gradient(135deg, var(--accent-gradient-start), var(--accent-gradient-end));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--text-primary);
    text-transform: uppercase;
  }

  .album-meta {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    justify-content: center;
  }

  .album-title {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .album-artist {
    color: var(--text-secondary);
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .album-count {
    font-size: 0.85rem;
  }

  .muted { 
    color: var(--text-muted); 
    padding: 1rem;
  }
  
  .error { 
    color: var(--error);
    padding: 1rem;
  }

  .empty-state {
    padding: 3rem 1rem;
    text-align: center;
  }

  @media (max-width: 1000px) {
    .results {
      grid-template-columns: 1fr;
    }
    
    .search-header {
      flex-direction: column;
      align-items: stretch;
    }
    
    .search-input {
      width: 100%;
    }
  }
</style>

