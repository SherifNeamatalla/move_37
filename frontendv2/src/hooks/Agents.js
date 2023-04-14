import React, { useEffect, useState } from 'react'
import { listAgents } from '../api/AgentsApiService'

export function useAgents() {
    const [agents, setAgents] = useState([])

    useEffect(() => {
        async function fetchAgents() {
            const response = await listAgents()
            setAgents(response.data)
        }

        fetchAgents()
    }, [])

    return agents
}