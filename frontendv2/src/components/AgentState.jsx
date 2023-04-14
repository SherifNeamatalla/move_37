import React from 'react'
import { Divider, List, ListItem, ListItemText, TextField, useTheme } from '@mui/material'


function AgentState({ currentAgent }) {

    const theme = useTheme()

    console.debug({currentAgent})

    const AgentStateContainer = (props) => (
        <div
            {...props}
            style={{
                backgroundColor: theme.palette.agentState.background,
                color: theme.palette.customColors.brightGreen2,
                padding: theme.spacing(2),
                height: '100%',
                borderRadius: '10px',
                overflowY: 'auto',
            }}
        />
    )

    const CommandTextField = (props) => (
        <TextField
            {...props}
            style={{
                '& input': {
                    color: theme.palette.text.primary,
                },
                '& .Mui-disabled': {
                    color: theme.palette.text.secondary,
                },
                '& .MuiInputLabel-root': {
                    color: theme.palette.customColors.brightGreen2,
                },
            }}
        />
    )

    return (
        <AgentStateContainer>
            <List>
                {(currentAgent?.goals || []) && (
                    <>
                        <ListItem>
                            <ListItemText
                                style={{
                                    color: theme.palette.customColors.brightYellow,
                                    fontWeight: 'bold',
                                    textAlign: 'center',
                                }}
                                primary='Agent Goals' />
                        </ListItem>
                        {(currentAgent?.goals || []).map((goal, index) => (
                            <ListItem key={index}>
                                <ListItemText primary={(index + 1) + '. ' + goal} />
                            </ListItem>
                        ))}
                        <Divider />
                    </>
                )}
            </List>
        </AgentStateContainer>
    )
}

export default AgentState
