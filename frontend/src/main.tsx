import React from 'react'
import ReactDOM from 'react-dom/client'
import { createRootRoute, createRoute, createRouter, RouterProvider } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { AppLayout } from './ui/AppLayout'
import Home from './ui/pages/HomePage'
import Orbit from './ui/pages/OrbitPage'
import ImpactMap from './ui/pages/ImpactMapPage'

const rootRoute = createRootRoute({
  component: () => (
    <ThemeProvider theme={createTheme({ palette: { mode: 'dark' } })}>
      <CssBaseline />
      <AppLayout />
      <TanStackRouterDevtools position="bottom-right" />
    </ThemeProvider>
  ),
})

const homeRoute = createRoute({ getParentRoute: () => rootRoute, path: '/', component: Home })
const orbitRoute = createRoute({ getParentRoute: () => rootRoute, path: 'orbit', component: Orbit })
const impactRoute = createRoute({ getParentRoute: () => rootRoute, path: 'impact-map', component: ImpactMap })

const routeTree = rootRoute.addChildren([homeRoute, orbitRoute, impactRoute])

const router = createRouter({ routeTree })

const root = document.getElementById('root') as HTMLElement
ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)


