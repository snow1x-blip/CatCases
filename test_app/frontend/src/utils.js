import { BACKEND_URL } from './api';

export const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }
  const base = BACKEND_URL.endsWith('/') ? BACKEND_URL.slice(0, -1) : BACKEND_URL;
  const path = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
  return `${base}${path}`;
};
