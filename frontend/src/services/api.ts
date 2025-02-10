import { ApiResponse } from '../types/chat';

const API_URL = 'http://localhost:8000/api';

export const sendMessage = async (message: string): Promise<ApiResponse> => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
};