import React from 'react'
import { Stack } from '@mui/material'
import AgentsList from '../components/AgentsList'
import { useCurrentAgent } from '../hooks/CurrentAgent'
import AgentState from '../components/AgentState'
import Actions from '../components/Actions'
import ChatWindow from '../components/ChatWindow'
import { makeStyles } from '@mui/styles'

const useStyles = makeStyles((theme) => {
    // @ts-ignore
    // @ts-ignore
    return ({
        root: {
            height: '100%',
            backgroundColor: theme.palette.background.default,
        },
        sidebar: {
            padding: theme.spacing(2),

        },
        mainContent: {
            padding: theme.spacing(2),
            position: 'relative',
        },
        actions: {
            padding: theme.spacing(2),
        },
        agentState: {
            padding: theme.spacing(2),
        },
    });
});
export function MainPage() {
    const classes = useStyles();

    const { currentAgentId, setCurrentAgentId, currentAgent } = useCurrentAgent()

    function sendMessage(message) {
        console.debug('sendMessage', message)
    }

    return (
        <div style={{
            width: '100vw',
            height: '100vh',
            boxSizing: 'border-box',
            overflowX: 'hidden',
            overflowY: 'hidden',
        }} className={classes.root}>
            <Stack direction='row' spacing={2} justifyContent='center' alignItems='stretch' sx={{ height: '100%' }}>
                <Stack sx={{ width: '25%', height: '85%' }} className={classes.sidebar}>
                    <AgentsList currentAgentId={currentAgentId} setCurrentAgentId={setCurrentAgentId} />
                </Stack>

                <Stack sx={{ width: '50%', height: '100%', flexDirection: 'column'}}>
                    <Stack sx={{ height: '85%' }} className={classes.mainContent}>
                        <ChatWindow sx={{ flexGrow: 1 }} />
                    </Stack>
                    <Stack sx={{ height: '15%' }} className={classes.actions}>
                        <Actions currentAgentId={currentAgentId} />
                    </Stack>
                </Stack>

                <Stack sx={{ width: '25%', height: '85%' }} className={classes.agentState}>
                    <AgentState currentAgent={currentAgent} />
                </Stack>
            </Stack>
        </div>
    )
}
