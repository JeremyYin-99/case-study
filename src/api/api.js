const API_BASE_URL = 'http://localhost:8000';

export const sendMessageToAgent = async (message) => {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to send message to agent');
        }

        const data = await response.json();
        return data.response; // Assuming the backend sends back a 'response' field
    } catch (error) {
        console.error('Error sending message to agent:', error);
        // You might want to re-throw the error, or return a default value,
        // or handle it in a way that your UI can display an error message.
        throw error; // Re-throw to be caught by the component calling this function
    }
};