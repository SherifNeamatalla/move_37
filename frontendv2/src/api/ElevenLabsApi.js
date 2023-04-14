// voiceApi.ts

import axios from 'axios'

const API_KEY = process.env.REACT_APP_ELEVENLABS_API_KEY


export async function synthesizeSpeech(text, voice) {
    const requestBody = {
        text,
        voice,
    }

    try {
        const response = await axios.post(
            `https://api.elevenlabs.io/v1/text-to-speech/${voice}/stream`,
            requestBody,
            {
                headers: {
                    'xi-api-key': `${API_KEY}`,
                    'Content-Type': 'application/json',
                },
                responseType: 'blob',
            },
        )
        console.debug({ kek: response.data })

        // @ts-ignore
        return URL.createObjectURL(response.data)

        return response.data.audioUrl
    } catch (error) {
        console.error('Error synthesizing speech:', error)
        throw error
    }
}
