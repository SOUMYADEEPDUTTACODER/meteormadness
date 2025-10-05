import { AppBar, Box, Container, IconButton, Toolbar, Typography, Button, Stack } from '@mui/material'
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch'
import { Link, Outlet, useRouter } from '@tanstack/react-router'
import { keyframes } from '@emotion/react'

export function AppLayout() {
  const router = useRouter()
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="sticky" color="transparent" elevation={0}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Stack direction="row" spacing={1} alignItems="center">
            <RocketLaunchIcon color="primary" sx={{ animation: `${rocketPulse} 2s ease-in-out infinite` }} />
            <Typography variant="h6" fontWeight={700} sx={{ animation: `${textGlow} 3s ease-in-out infinite` }}>Meteor Defender</Typography>
          </Stack>
          <Stack direction="row" spacing={1}>
            <Button component={Link} to="/" variant="text">Home</Button>
            <Button component={Link} to="orbit" variant="text">3D Orbit</Button>
            <Button component={Link} to="impact-map" variant="contained">Impact Map</Button>
          </Stack>
        </Toolbar>
      </AppBar>
      <Container maxWidth="xl" sx={{ flex: 1, py: 4 }}>
        <Outlet />
      </Container>
      <Box component="footer" sx={{ py: 3, textAlign: 'center', opacity: 0.7 }}>
        <Typography variant="body2">© {new Date().getFullYear()} Meteor Defender</Typography>
        <Typography variant="body2" sx={{ mt: 1, opacity: 0.6 }}>Developed by team SpaceTraveller</Typography>
      </Box>
    </Box>
  )
}

const rocketPulse = keyframes({
  '0%, 100%': { transform: 'scale(1)', filter: 'drop-shadow(0 0 8px rgba(99, 102, 241, 0.5))' },
  '50%': { transform: 'scale(1.1)', filter: 'drop-shadow(0 0 16px rgba(99, 102, 241, 0.8))' },
})

const textGlow = keyframes({
  '0%, 100%': { textShadow: '0 0 8px rgba(99, 102, 241, 0.3)' },
  '50%': { textShadow: '0 0 16px rgba(99, 102, 241, 0.6), 0 0 24px rgba(99, 102, 241, 0.4)' },
})


