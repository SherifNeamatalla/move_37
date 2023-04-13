import React from 'react'

import AppThemeProvider from './AppThemeProvider'

export function AppProviders({ children }) {
    return (
        <AppThemeProvider>
            {children}
        </AppThemeProvider>
    )
}
