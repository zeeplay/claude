const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper function for API requests
async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

// Books API
export const booksApi = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return request(`/api/books${queryString ? `?${queryString}` : ''}`);
  },

  get: (id) => request(`/api/books/${id}`),

  create: (book) => request('/api/books', {
    method: 'POST',
    body: JSON.stringify(book),
  }),

  update: (id, book) => request(`/api/books/${id}`, {
    method: 'PUT',
    body: JSON.stringify(book),
  }),

  delete: (id) => request(`/api/books/${id}`, {
    method: 'DELETE',
  }),
};

// Movies API
export const moviesApi = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return request(`/api/movies${queryString ? `?${queryString}` : ''}`);
  },

  get: (id) => request(`/api/movies/${id}`),

  create: (movie) => request('/api/movies', {
    method: 'POST',
    body: JSON.stringify(movie),
  }),

  update: (id, movie) => request(`/api/movies/${id}`, {
    method: 'PUT',
    body: JSON.stringify(movie),
  }),

  delete: (id) => request(`/api/movies/${id}`, {
    method: 'DELETE',
  }),
};

// Stats API
export const statsApi = {
  getAll: () => request('/api/stats'),
  getBooks: () => request('/api/stats/books'),
  getMovies: () => request('/api/stats/movies'),
};

// Query API
export const queryApi = {
  ask: (question) => request('/api/query', {
    method: 'POST',
    body: JSON.stringify({ question }),
  }),
};
