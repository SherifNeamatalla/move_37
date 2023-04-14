import React from 'react'
import SmartToyIcon from '@mui/icons-material/SmartToy'

import { useAgents } from '../hooks/Agents'
import { ListItemButton, ListItemIcon, ListItemText, useTheme } from '@mui/material'

function AgentsList({ currentAgentId, setCurrentAgentId }) {

    const theme = useTheme()

    const agents = useAgents()


    const AnimatedSmartToyIcon = (props) => (
        <SmartToyIcon
            {...props}
            sx={{
                transition: 'transform 1s linear',
                animation: 'rotate 10s linear infinite',
                '@keyframes rotate': {
                    '0%': {
                        transform: 'rotate(0deg)',
                    },
                    '100%': {
                        transform: 'rotate(360deg)',
                    },
                },
            }}
        />
    )

    const AgentsListContainer = (props) => (
        <div
            {...props}
            style={{
                height: '100%',
                backgroundColor: theme.palette.agentsList.background,
                borderRadius: '10px',
            }}
        />
    )

    const ListContainer = (props) => (
        <div
            {...props}
            style={{
                height: '100%',
                backgroundColor: theme.palette.agentsList.background,
                color: theme.palette.primary.contrastText,
                padding: theme.spacing(2),
                borderRadius: '10px',
            }}
        />
    )

    const ListItemContainer = (props) => (
        <div
            {...props}
            style={{
                borderRadius: '10px',
                margin: theme.spacing(1, 0),
                '&:hover': {
                    backgroundColor: theme.palette.agentsList.main,
                    cursor: 'pointer',
                },
            }}
        />
    )

    const ListItemButtonContainer = ({ selected, ...props }) => (
        <ListItemButton
            {...props}
            selected={selected}
            sx={{
                borderRadius: '10px',
                '&.Mui-selected': {
                    backgroundColor: theme.palette.agentsList.main,
                },
            }}
        />
    )

    const ListItemIconContainer = (props) => (
        <ListItemIcon
            {...props}
            sx={{
                color: theme.palette.customColors.brightGreen2,
            }}
        />
    )

    const ListItemTextContainer = (props) => (
        <ListItemText
            {...props}
            sx={{
                fontWeight: 'bold',
                color: theme.palette.customColors.brightGreen2,
            }}
        />
    )

    function agentComponent(agent) {
        return (
            <ListItemContainer key={agent.id}>
                <ListItemButtonContainer selected={currentAgentId === agent.id}
                                         onClick={() => setCurrentAgentId(agent.id)}>
                    <ListItemIconContainer>
                        {currentAgentId === agent.id ? <AnimatedSmartToyIcon /> : <SmartToyIcon />}
                    </ListItemIconContainer>
                    <ListItemTextContainer primary={agent.name} />
                </ListItemButtonContainer>
            </ListItemContainer>
        )
    }

    function body() {
        return (
            <ListContainer>
                {(agents || []).map((agent) => agentComponent(agent))}
            </ListContainer>
        )
    }

    return <AgentsListContainer>{body()}</AgentsListContainer>
}

export default AgentsList

