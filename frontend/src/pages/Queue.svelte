<script>
  import { queue, currentIndex, playFromQueue, removeFromQueue, clearQueue } from '../queue.js';
  
  let draggedIndex = null;
  
  function handleDragStart(event, index) {
    draggedIndex = index;
    event.dataTransfer.effectAllowed = 'move';
    event.target.style.opacity = '0.5';
  }
  
  function handleDragEnd(event) {
    event.target.style.opacity = '1';
    draggedIndex = null;
  }
  
  function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }
  
  function handleDrop(event, dropIndex) {
    event.preventDefault();
    
    if (draggedIndex !== null && draggedIndex !== dropIndex) {
      queue.update(q => {
        const newQueue = [...q];
        const [removed] = newQueue.splice(draggedIndex, 1);
        newQueue.splice(dropIndex, 0, removed);
        
        currentIndex.update(idx => {
          if (idx === draggedIndex) return dropIndex;
          if (draggedIndex < idx && dropIndex >= idx) return idx - 1;
          if (draggedIndex > idx && dropIndex <= idx) return idx + 1;
          return idx;
        });
        
        return newQueue;
      });
    }
  }
  
  function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
  
  function handlePlayClick(index) {
    playFromQueue(index);
  }
  
  function handleRemoveClick(index) {
    removeFromQueue(index);
  }
  
  function handleClearQueue() {
    if (confirm('Clear entire queue?')) {
      clearQueue();
    }
  }
</script>

<div class="queue-page">
  <div class="queue-header">
    <h2>Queue</h2>
    {#if $queue.length > 0}
      <button class="clear-button" on:click={handleClearQueue}>
        Clear Queue
      </button>
    {/if}
  </div>
  
  {#if $queue.length === 0}
    <div class="empty-state">
      <p>Queue is empty</p>
      <p class="hint">Add songs from your library or albums</p>
    </div>
  {:else}
    <div class="queue-info">
      <p>{$queue.length} songs</p>
    </div>
    
    <div class="queue-list">
      {#each $queue as song, index (song.id + index)}
        <div
          class="queue-item"
          class:current={index === $currentIndex}
          draggable="true"
          on:dragstart={(e) => handleDragStart(e, index)}
          on:dragend={handleDragEnd}
          on:dragover={handleDragOver}
          on:drop={(e) => handleDrop(e, index)}
        >
          <div class="drag-handle">☰</div>
          
          <div class="queue-number">
            {#if index === $currentIndex}
              <span class="playing-indicator">▶</span>
            {:else}
              {index + 1}
            {/if}
          </div>
          
          <div class="album-art">
            {#if song.coverUrl}
              <img src={song.coverUrl} alt={song.album} />
            {:else}
              <div class="no-cover">
                {song.title.charAt(0)}
              </div>
            {/if}
          </div>
          
          <div class="song-info" on:click={() => handlePlayClick(index)}>
            <div class="title">{song.title}</div>
            <div class="artist">{song.artist}</div>
          </div>
          
          <div class="album">{song.album}</div>
          <div class="duration">{formatDuration(song.duration)}</div>
          
          <button class="remove-button" on:click={() => handleRemoveClick(index)}>
            ×
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .queue-page {
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }
  
  .queue-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }
  
  h2 {
    margin: 0;
    color: var(--text-primary);
  }
  
  .clear-button {
    padding: 0.5rem 1rem;
    background: transparent;
    border: 1px solid var(--border-secondary);
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .clear-button:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }
  
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-secondary);
  }
  
  .empty-state p {
    margin: 0.5rem 0;
  }
  
  .hint {
    font-size: 0.9rem;
    color: var(--text-muted);
  }
  
  .queue-info {
    margin-bottom: var(--spacing-md);
    color: var(--text-secondary);
    font-size: 0.9rem;
  }
  
  .queue-list {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .queue-item {
    display: grid;
    grid-template-columns: 30px 40px 48px 2fr 1.5fr 80px 40px;
    gap: 1rem;
    align-items: center;
    padding: 0.5rem 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    cursor: grab;
    transition: background 0.2s;
  }
  
  .queue-item:hover {
    background: var(--bg-tertiary);
  }
  
  .queue-item.current {
    background: var(--overlay);
    border-left: 3px solid var(--accent-primary);
  }
  
  .queue-item:active {
    cursor: grabbing;
  }
  
  .drag-handle {
    color: var(--text-muted);
    font-size: 1.2rem;
    cursor: grab;
  }
  
  .queue-number {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-variant-numeric: tabular-nums;
  }
  
  .playing-indicator {
    color: var(--accent-primary);
  }
  
  .album-art {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-sm);
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
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--text-primary);
  }
  
  .song-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    cursor: pointer;
    min-width: 0;
  }
  
  .title {
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .artist {
    font-size: 0.9rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .album {
    font-size: 0.9rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .duration {
    font-size: 0.9rem;
    color: var(--text-secondary);
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  
  .remove-button {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 1.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
  
  .remove-button:hover {
    background: var(--bg-tertiary);
    color: var(--error);
  }
</style>
