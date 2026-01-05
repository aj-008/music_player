<script>
  import Router from 'svelte-spa-router';
  import NavBar from './components/NavBar.svelte';
  import Player from './components/Player.svelte';


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
