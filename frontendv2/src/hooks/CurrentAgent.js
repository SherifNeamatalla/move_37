import React, { useEffect, useState } from 'react'
import { loadAgent } from '../api/AgentsApiService'

export function useCurrentAgent() {
    const [currentAgentId, setCurrentAgentId] = useState(null)

    const [currentAgent, setCurrentAgent] = useState(null)

    useEffect(() => {
        if (!currentAgentId) {
            setCurrentAgent(null)
            return
        }

        async function fetchAgent() {
            const response = await loadAgent(currentAgentId)
            const agent = response.data
            setCurrentAgent(agent)
        }

        fetchAgent()
    }, [currentAgentId])

    return {
        currentAgentId,
        setCurrentAgentId,
        currentAgent,
        setCurrentAgent,
    }
}