export interface Message {
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export interface ApiResponse {
  response: string;
  timestamp: string;
  provider: string;
}