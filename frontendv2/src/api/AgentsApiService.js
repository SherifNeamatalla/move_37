import { axiosInstance } from './Axios'

export function listAgents() {
    return axiosInstance.get('/agent/list')
}

export function createAgent(name, role, goals, config) {
    return axiosInstance.post('/agent/create', { name, role, goals, config })
}

export function loadAgent(agentId) {
    return axiosInstance.get(`/agent/load/${agentId}`)
}

export function chatAgent(agentId, message) {
    return axiosInstance.post(`/agent/chat/${agentId}`, message)
}


export function actAgent(agentId, commandResponse, command) {
    return axiosInstance.post(`/agent/act/${agentId}`, {
        command_response: commandResponse,
        command: command,
    })
}

export function resetAgentShortMemory(agentId) {
    return axiosInstance.post(`/agent/reset/${agentId}`)
}
