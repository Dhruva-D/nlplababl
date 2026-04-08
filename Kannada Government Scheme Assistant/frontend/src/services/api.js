import axios from 'axios';

// Create a central Axios instance hooked to our FastAPI server
const api = axios.create({
    baseURL: 'http://localhost:8000/api', // FastAPI runs on port 8000
});

export const searchScheme = async (text) => {
    try {
        // We POST the Kannada text to the /search route we just built
        const response = await api.post('/search', { text });
        return response.data;
    } catch (error) {
        console.error("Error communicating with backend:", error);
        throw error;
    }
};
