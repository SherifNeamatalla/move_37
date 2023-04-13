// ChatWindow.tsx
import React, { useEffect, useRef, useState } from 'react'
import {
    Divider,
    IconButton,
    List,
    ListItem,
    ListItemAvatar,
    ListItemIcon,
    ListItemSecondaryAction,
    Stack,
    Tooltip,
    useTheme,
} from '@mui/material'
import { Avatar, ListItemText } from '@material-ui/core'
import './ChatWindow.css'
import ReactTypingEffect from 'react-typing-effect'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
    faBan,
    faBrain,
    faCalendarAlt,
    faCheckCircle,
    faCircleXmark,
    faCog,
    faExclamationTriangle,
    faLightbulb,
    faMicrophone,
    faSpinner,
    faUserTie,
} from '@fortawesome/free-solid-svg-icons'
import AudioPlayer from '../components/AudioPlayer'
import { AGENT_ROLE, PERMISSION_DENIED, PERMISSION_GRANTED, SYSTEM_ROLE, USER_ROLE } from '../config/Constants'

function ChatWindow
({
     audioUrl,
     agentState,
     command,
     chatHistory,
     onResendMessage,
     onAgentAct,
     showHal,
 }) {
    const messagesEndRef = useRef(null)
    const theme = useTheme()
    const [messages, setMessages] = useState([])
    const containerRef = useRef(null)
    const [typingSpeed, setTypingSpeed] = useState(10)


    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight
        }
    }, [chatHistory])
    useEffect(() => {
        if (agentState?.response) {
            setMessages((prevMessages) => [
                ...prevMessages,
                `> ${agentState?.response}`,
            ])
        }


    }, [agentState])

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(scrollToBottom, [messages])


    function planComponent(plan) {
        if (!plan) {
            return null
        }

        const plans = (plan || '').split('\n')

        const plansComponents = plans.map((p, index) => (
            <ListItem key={index} disablePadding>
                <ListItemText>
                    <PlanText>{index + 1}. {p}</PlanText>
                </ListItemText>
            </ListItem>
        ))
        return (<Stack>
            <ListItem>
                <ListItemIcon>
                    <FontAwesomeIcon icon={faCalendarAlt} />
                </ListItemIcon>
                <List>
                    {plansComponents}
                </List>
            </ListItem>
        </Stack>)
    }

    function contentEntryComponent(textComponent, icon) {
        return (
            <ListItem>
                <ListItemIcon>
                    <FontAwesomeIcon icon={icon} />
                </ListItemIcon>
                <ListItemText>
                    {textComponent}
                </ListItemText>
            </ListItem>
        )
    }


    function systemMessageComponent(content, index) {
        return (<ListItem key={index}>
            <ListItemAvatar>
                <FontAwesomeIcon icon={faCog} />
            </ListItemAvatar>

            <ListItemText>
                {content}
            </ListItemText>
        </ListItem>)
    }

    function speakComponent(thoughts, index) {
        if (!thoughts?.['speak']) {
            return null
        }
        if (index === chatHistory.length - 1) {
            return (contentEntryComponent((<MatrixText>
                <ReactTypingEffect text={thoughts['speak']} eraseDelay={9999999} speed={typingSpeed} />
            </MatrixText>), faMicrophone))
        }
        return (contentEntryComponent((<MatrixText>
            {thoughts['speak']}
        </MatrixText>), faMicrophone))
    }

    function agentMessageComponent(content, index) {
        const thoughts = content['thoughts']

        if (!thoughts) {
            return null
        }
        return (
            <ListItem key={index}>
                <ListItemAvatar>
                    <Avatar src={process.env.PUBLIC_URL + '/agent_avatar.png'} />
                </ListItemAvatar>

                <List>
                    {thoughts['text'] && contentEntryComponent((<ThoughtText>
                        {thoughts['text']}
                    </ThoughtText>), faLightbulb)}
                    {thoughts['criticism'] && contentEntryComponent((<CriticismText>
                        {thoughts['criticism']}
                    </CriticismText>), faBan)}
                    {thoughts['reasoning'] && contentEntryComponent((<ReasoningText>
                        {thoughts['reasoning']}
                    </ReasoningText>), faBrain)}
                    {planComponent(thoughts['plan'])}
                    {speakComponent(thoughts, index)}
                </List>
            </ListItem>
        )

    }


    const renderIcon = (confirmedStatus) => {
        if (confirmedStatus === 'error') {
            return (<Tooltip title='Woops! Message did not go through!'>
                <FontAwesomeIcon
                    icon={faExclamationTriangle}
                    onClick={() => onResendMessage()}
                    style={{ cursor: 'pointer' }}
                />
            </Tooltip>)
        } else if (confirmedStatus === 'pending') {
            return <FontAwesomeIcon icon={faSpinner} spin />
        }
        return null
    }

    function userMessageComponent(content, confirmedStatus, index) {

        return (<ListItem key={index}>
            <ListItemAvatar>
                <FontAwesomeIcon icon={faUserTie} />
            </ListItemAvatar>

            <ListItemText>
                {(content || '').replace('Human feedback:', '')}
            </ListItemText>

            {renderIcon(confirmedStatus) && (
                <ListItemSecondaryAction>
                    {renderIcon(confirmedStatus)}
                </ListItemSecondaryAction>
            )}
        </ListItem>)
    }

    function messageComponent(message, index) {
        if (!message) {
            return null
        }

        const role = message.role
        const content = message.content
        const confirmedStatus = message.confirmed || null


        switch (role) {
            case USER_ROLE:
                return userMessageComponent(content, confirmedStatus, index)

            case AGENT_ROLE:
                return agentMessageComponent(content, index)

            case SYSTEM_ROLE:
                return systemMessageComponent(content, index)
            default:
                return 'This message has no role, this is a bug !!!'
        }
    }

    const ChatWindowContainer = (props) => (
        <div
            {...props}
            style={{
                backgroundColor:  theme.palette.matrix.main,
                height: '100%',
                overflowY: 'auto',
                display: 'flex',
                flexDirection: 'column',
                borderRadius: '10px',
                position: 'unset',
            }}
        />
    )

    const MatrixText = (props) => (
        <div
            {...props}
            style={{
                color:  theme.palette.customColors.brightGreen,
                fontFamily: 'Roboto Mono',
                whiteSpace: 'pre-wrap',
                fontSize: '14px',
                lineHeight: '20px',
            }}
        />
    )

    const ThoughtText = (props) => (
        <div
            {...props}
            style={{
                color:  theme.palette.customColors.darkViolet,
                fontFamily: 'Roboto Mono',
                whiteSpace: 'pre-wrap',
                fontSize: '14px',
                lineHeight: '20px',
            }}
        />
    )

    const CriticismText = (props) => (
        <div
            {...props}
            style={{
                color:  theme.palette.customColors.brightOrange2,
                fontFamily: 'Roboto Mono',
                whiteSpace: 'pre-wrap',
                fontSize: '14px',
                lineHeight: '20px',
            }}
        />
    )

    const ReasoningText = (props) => (
        <div
            {...props}
            style={{
                color:  theme.palette.customColors.brightOrange,
                fontFamily: 'Roboto Mono',
                whiteSpace: 'pre-wrap',
                fontSize: '14px',
                lineHeight: '20px',
            }}
        />
    )

    const PlanText = (props) => (
        <div
            {...props}
            style={{
                color:  theme.palette.customColors.brightBlueGreen,
                fontFamily: 'Roboto Mono',
                whiteSpace: 'pre-wrap',
                fontSize: '14px',
                lineHeight: '20px',
            }}
        />
    )

    const Hal = (props) => (
        <div
            {...props}
            style={{
                position: 'absolute',
                top: '50%',
                right: '50%',
                left: '50%',
                bottom: '50%',
                width: '100px',
                height: '100px',
                backgroundColor: 'red',
                borderRadius: '50%',
                transform: 'translate(-50%, -50%)',
                opacity: 0,
                animation: 'pulse 5s infinite',
            }}
        />
    )

    function commandMessageComponent() {
        if (!command || showHal) {
            return null
        }


        return (<ListItem>
            <ListItemAvatar>
                <Tooltip title={'Waiting for user permission!'}>
                    <FontAwesomeIcon icon={faExclamationTriangle} />
                </Tooltip>
            </ListItemAvatar>

            <ListItemText>
                Your response to the command (Send a message instead to provide feedback)
            </ListItemText>

            <ListItemSecondaryAction>
                <IconButton>
                    <FontAwesomeIcon icon={faCheckCircle}
                                     style={{ color: theme.palette.matrix.contrastText }}
                                     onClick={() => {
                                         onAgentAct(PERMISSION_GRANTED)
                                     }}
                    />
                </IconButton>

                <IconButton>
                    <FontAwesomeIcon icon={faCircleXmark}
                                     onClick={() => {
                                         onAgentAct(PERMISSION_DENIED)
                                     }}
                                     style={{ color: theme.palette.customColors.brightOrange2 }}
                    />
                </IconButton>
            </ListItemSecondaryAction>
        </ListItem>)
    }

    function body() {
        const content = (<>
            {(chatHistory || []).map((message, index) => (
                <>
                    {messageComponent(message, index)}
                    <Divider />
                </>
            ))}
            <div ref={messagesEndRef} />
        </>)


        return <ChatWindowContainer className={'scrollable-container'} ref={containerRef}>
            <List className={'scrollable-content'}>
                {content}
                {commandMessageComponent()}
            </List>
            {showHal && <Hal />}
            {audioUrl && (
                <AudioPlayer audioStreamUrl={audioUrl} />
            )}
        </ChatWindowContainer>

    }

    return (
        <>
            {body()}
        </>
    )
}

export default ChatWindow
