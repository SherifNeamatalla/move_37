import React, { useEffect, useState } from 'react'
import SendIcon from '@material-ui/icons/Send'
import { InputAdornment } from '@material-ui/core'
import { TextField, useTheme } from '@mui/material'
import './ChatWindow.css'
import { makeStyles } from '@mui/styles'

const useStyles = makeStyles((theme) => ({
    textField: {
        width: '100%',
        padding: theme.spacing(2),
        backgroundColor: theme.palette.background.default,
        '& .MuiOutlinedInput-root': {
            '& fieldset': {
                borderColor: theme.palette.primary.main,
            },
            '&:hover fieldset': {
                borderColor: theme.palette.primary.light,
            },
            '&.Mui-focused fieldset': {
                borderColor: theme.palette.primary.main,
            },
            '& .MuiInputBase-input': {
                color: theme.palette.customColors.brightGreen2,
            },
            '&.Mui-focused .MuiInputBase-input': {
                color: theme.palette.customColors.brightGreen2,
            },
        },
    },
}))

const Actions = ({ onSendMessage, currentAgentId, command, onAgentAct }) => {
    const theme = useTheme()
    const classes = useStyles()
    const [message, setMessage] = useState('')


    useEffect(() => {
        setMessage('')
    }, [currentAgentId])


    const handleActionClick = async () => {
        setMessage('')

        let result = null

        if (command) {
            result = await onAgentAct(message)
        } else {
            result = await onSendMessage(message)
        }
    }

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleActionClick()
        }
    }


    if (!currentAgentId) {
        return null
    }


    function TextArea() {

        return (<TextField
            sx={{
                borderRadius: '4px',
                border: '2px solid',
                borderColor: 'matrix.contrastText',
                backgroundColor: 'matrix.main',
                color: 'matrix.contrastText',
                fontFamily: 'monospace',
                fontWeight: 'bold',
                letterSpacing: '2px',
                padding: '8px',
                width: '100%',
                '&:hover': {
                    borderColor: 'highlight.main',
                },
                '&:focus': {
                    outline: 'none',
                    borderColor: 'highlight.main',
                    boxShadow: (theme) => `0 0 0 2px ${theme.palette.highlight.main}`,
                },
            }}
            InputProps={{
                endAdornment: (
                    <InputAdornment
                        style={{ cursor: 'pointer' }}
                        onClick={() => handleActionClick()}
                        position='end'
                    >
                        <SendIcon
                            className={'icon-rotator'}
                            style={{ transform: 'rotate(-45deg)' }} />
                    </InputAdornment>
                ),
            }}
            placeholder={command ? 'Type your feedback...' : 'Type your message...'}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyPress={handleKeyPress}
        />)
    }


    return (
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                flexDirection: 'row',
                width: '100%',
                backgroundColor: theme.palette.background.paper,
                borderRadius: '50%',
            }}
        >
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'row',
                    backgroundColor: theme.palette.background.paper,
                    borderRadius: theme.shape.borderRadius,
                    width: '100%',
                }}
            >
                <TextArea/>

            </div>
        </div>
    )
}

export default Actions
