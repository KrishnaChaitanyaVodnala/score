// API base URL - empty in dev (uses Vite proxy), set via VITE_API_URL in production
const API_BASE = import.meta.env.VITE_API_URL || '';

export function apiUrl(path) {
  return `${API_BASE}${path}`;
}
