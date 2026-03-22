export const BACKEND_URL = 'https://49a4b443e41a40.lhr.life';

const getInitDataFromUrl = () => {
  const searchParams = new URLSearchParams(window.location.search);
  const hashParams = new URLSearchParams(window.location.hash.replace(/^#/, ''));

  // Telegram can provide signed data as tgWebAppData in URL for some launch modes.
  return (
    searchParams.get('tgWebAppData') ||
    hashParams.get('tgWebAppData') ||
    ''
  );
};

const getTelegramInitData = () => {
  const webApp = window.Telegram?.WebApp;
  if (webApp?.ready) {
    webApp.ready();
  }

  const initData = webApp?.initData || getInitDataFromUrl();
  if (!initData) {
    throw new Error('Telegram authentication data is missing. Please reopen the app from the bot menu button.');
  }
  return initData;
};

const authFetch = async (path) => {
  const initData = getTelegramInitData();
  return fetch(`${BACKEND_URL}${path}`, {
    method: 'GET',
    headers: {
      'X-Telegram-Init-Data': initData,
    },
  });
};

export const spinCase = async (caseId) => {
  const response = await authFetch(`/api/spin?case_id=${encodeURIComponent(caseId)}`);
  
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Server ${response.status}: ${errText}`);
  }
  return response.json();
};

export const getInventory = async () => {
  const response = await authFetch('/api/inventory');
  if (!response.ok) throw new Error('Inventory fetch failed');
  return response.json();
};

export const getItems = async () => {
  const response = await authFetch('/api/items');
  if (!response.ok) throw new Error('Items fetch failed');
  return response.json();
};

export const getCases = async () => {
  const response = await authFetch('/api/cases');
  if (!response.ok) throw new Error('Cases fetch failed');
  return response.json();
};

export const getCaseItems = async (caseId) => {
  const response = await authFetch(`/api/cases/${encodeURIComponent(caseId)}/items`);
  if (!response.ok) throw new Error('Case items fetch failed');
  return response.json();
};
