<script>
    import { link } from 'svelte-spa-router';
    import { queue } from '../queue.js';
</script>

<nav>
  <ul>
    <li><a href="/" use:link>Library</a></li>
    <li><a href="/albums" use:link>Albums</a></li>
    <li><a href="/search" use:link>Search</a></li>
    <li>
      <a href="/queue" use:link>
        Queue
        {#if $queue.length > 0}
          <span class="queue-count">({$queue.length})</span>
        {/if}
      </a>
    </li>
  </ul>
</nav>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    padding: 1rem 2rem;
    background: var(--bg-tertiary);
    border-bottom: 1px solid #333;
  }
  
  
  ul {
    display: flex;
    gap: 2rem;
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  a {
    color: #aaa;
    text-decoration: none;
    font-weight: 500; 
    color: var(--text-secondary);
  }
  
  a:hover {
    color: #fff;
  }

  .queue-count {
    font-size: 0.85rem;
    opacity: 0.7;
  }
</style>
