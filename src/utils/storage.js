const STORAGE_KEY = 'your-own-game-state-v1';

export const loadGameState = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

export const saveGameState = (state) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // Игнорируем ошибки переполнения/quota, чтобы игра продолжала работать.
  }
};

export const clearGameState = () => {
  localStorage.removeItem(STORAGE_KEY);
};
