import React from 'react'
import { createTheme, ThemeProvider } from '@mui/material'
import darkTheme from '../theme'

function AppThemeProvider({ children }) {


    // @ts-ignore
    const theme = createTheme(darkTheme)

    console.debug({theme});

    return (
        <ThemeProvider theme={theme}>
            {children}
        </ThemeProvider>
    )
}

export default AppThemeProvider
