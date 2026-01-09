<script>
  import { onMount, onDestroy } from 'svelte';
  import Router from 'svelte-spa-router';
  import NavBar from './components/NavBar.svelte';
  import Player from './components/Player.svelte';
  import { connectWebSocket, sendPlayerState } from './lib/websocket.js';
  import { currentSong, currentTime, duration, isPlaying } from './lib/player.js';
  


  import Library from './pages/Library.svelte';
  import Albums from './pages/Albums.svelte';
  import AlbumDetail from './pages/AlbumDetail.svelte';
  import Queue from './pages/Queue.svelte';
  import Search from './pages/Search.svelte';
  
  const routes = {
    '/': Library,  
    '/albums': Albums,
    '/albums/:title': AlbumDetail,
    '/queue': Queue,
    '/search': Search,
  };

  let updateInterval;

  onMount(() => {
    connectWebSocket();
  });

  $: if ($isPlaying && $currentSong) {
    if (!updateInterval) {
      updateInterval = setInterval(() => {
        sendPlayerState({
          title: $currentSong.title,
          artist: $currentSong.artist,
          progress: ($currentTime / $duration) * 100 || 0,
          current_time: Math.floor($currentTime),
          duration: Math.floor($duration)
        });
      }, 1000);
    }
  } else {
    if (updateInterval) {
      clearInterval(updateInterval);
      updateInterval = null;
    }
    
    if ($currentSong) {
      sendPlayerState({
        title: $currentSong.title,
        artist: $currentSong.artist,
        progress: ($currentTime / $duration) * 100 || 0,
        current_time: Math.floor($currentTime),
        duration: Math.floor($duration)
      });
    }
  }
  
  onDestroy(() => {
    if (updateInterval) {
      clearInterval(updateInterval);
    }
  });
</script>

<div class="app">
  <NavBar />
  
  <main>
    <Router {routes} />
  </main>

  <Player />
  
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  main {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
  }
</style>
