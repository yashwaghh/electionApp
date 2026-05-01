import axios from 'axios';

// When deployed, this hits the same domain. Locally, it can still hit localhost if running dev servers.
const API_BASE_URL = import.meta.env.PROD ? '/api/v1' : 'http://localhost:8000/api/v1';

export const sendMessage = async (message, sessionId, language = 'en', imageBase64 = null) => {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        session_id: sessionId,
        language: language,
        image_base64: imageBase64
    });
    return response.data;
};
