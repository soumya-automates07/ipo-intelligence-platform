const API_BASE = "http://98.70.25.163:8000";

export async function getStats() {
  const res = await fetch(
    `${API_BASE}/ipo/stats`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export async function getLatestEvent() {
  const res = await fetch(
    `${API_BASE}/ipo/check-new-alert`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export async function getCompanies() {
  const res = await fetch(
    `${API_BASE}/ipo/watchlist`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export async function getWatchlistStatus() {
  const res = await fetch(
    `${API_BASE}/ipo/watchlist-status`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}