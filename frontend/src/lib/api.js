const API_BASE = 'http://localhost:8000';

export async function getSongs() {
  const response = await fetch(`${API_BASE}/api/songs`);
  return response.json();
}

export async function getAlbums() {
  const response = await fetch(`${API_BASE}/api/albums`);
  return response.json();
}

