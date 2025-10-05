import { Link } from '@tanstack/react-router'
import { Box, Button, Card, CardContent, Grid, Stack, Typography } from '@mui/material'
import { keyframes } from '@emotion/react'
import { useEffect, useRef, useState } from 'react'
import * as React from "react";

const asteroidStyle: React.CSSProperties = {
  position: "absolute",
  left: "40%",
  top: "90%",
  transform: "translate(-50%, -50%)",
  width: "300px",      // Increased size
  height: "300px",     // Increased size
  zIndex: 2,
};

const motionStyle: React.CSSProperties = {
  animation: "asteroid-float 2s infinite ease-in-out",
};

const waveStyle: React.CSSProperties = {
  position: "absolute",
  left: "75%",
  top: "80%",
  transform: "translate(-50%, -50%)",
  width: "280px",      // Increased width
  height: "210px",     // Increased height
  zIndex: 2,
  animation: "wave-motion 2.5s infinite ease-in-out",
};

const rocketStyle: React.CSSProperties = {
  position: "absolute",
  left: "15%",         // Left of asteroid
  top: "120%",
  transform: "translate(-50%, -50%)",
  width: "300px",
  height: "300px",
  zIndex: 2,
  animation: "rocket-float 2s infinite ease-in-out",
};

export default function Home() {
  const heroRef = useRef<HTMLDivElement | null>(null)
  const headlineRef = useRef<HTMLHeadingElement | null>(null)
  const ctasRef = useRef<HTMLDivElement | null>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Scroll reveal animation
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )
    
    if (heroRef.current) {
      observer.observe(heroRef.current)
    }

    if (!heroRef.current || !headlineRef.current || !ctasRef.current) return

    ;(async () => {
      let animeLib: any = (window as any).anime
      if (!animeLib) {
        try {
          const mod: any = await import('animejs')
          animeLib = mod.default ?? mod
        } catch {
          animeLib = null
        }
      }
      if (!animeLib || typeof animeLib.timeline !== 'function') return

      animeLib.set([headlineRef.current, ctasRef.current], { opacity: 0, translateY: 12 })
      animeLib.timeline({ easing: 'easeOutQuad', duration: 600 })
        .add({ targets: headlineRef.current, opacity: 1, translateY: 0 })
        .add({ targets: ctasRef.current, opacity: 1, translateY: 0 }, '-=300')

      animeLib({
        targets: heroRef.current,
        translateY: [0, -6, 0, 6, 0],
        duration: 6000,
        easing: 'easeInOutSine',
        loop: true,
      })
    })()

    return () => observer.disconnect()
  }, [])

  return (
    <Grid container spacing={6} alignItems="center" sx={{ position: 'relative' }}>
      {/* Animated aurora blobs */}
      <AuroraBlobs />
      <Grid item xs={12} md={6}>
        <Stack spacing={2}>
          <Typography ref={headlineRef} variant="h2" fontWeight={800} lineHeight={1.1}
            sx={{
              textShadow: '0 2px 20px rgba(99, 102, 241, 0.35)',
              letterSpacing: 0.5,
              animation: isVisible ? `${headlineReveal} 1.2s ease-out forwards` : 'none',
              opacity: 0,
              transform: 'translateY(30px)',
            }}
          >
            Defend Earth with data‑driven simulations
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Explore 3D orbital paths, simulate impacts, and test mitigation strategies. Built for scientists, policymakers, and the public.
          </Typography>
          <Stack ref={ctasRef} direction="row" spacing={2}
            sx={{ '& .MuiButton-root': { transition: 'transform .2s ease, box-shadow .3s ease' }, '& .MuiButton-root:hover': { transform: 'translateY(-2px)', boxShadow: '0 10px 30px rgba(99,102,241,.25)' } }}
          >
            <Button component={Link} to="/orbit" size="large" variant="contained">Explore 3D Orbit</Button>
            <Button component={Link} to="/impact-map" size="large" variant="outlined">View Impact Map</Button>
          </Stack>
        </Stack>
      </Grid>
      <Grid item xs={12} md={6}>
        <Box ref={heroRef}
          sx={{ height: 420, borderRadius: 3, background: 'radial-gradient(closest-corner at 70% 30%, #1e3a8a, #0b1020)', position: 'relative', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.35)' }}>
          <StarsCanvas />
          <Box sx={{ position: 'absolute', inset: 0, background: 'url(https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?q=80&w=1200&auto=format&fit=crop) center/cover', opacity: 0.28, mixBlendMode: 'screen' }} />
          <Typography variant="h3" sx={{ position: 'absolute', bottom: 16, left: 16, fontWeight: 700, textShadow: '0 4px 30px rgba(99,102,241,.35)' }}>Meteor Defender</Typography>
        </Box>
      </Grid>
      {/* Small Rocket Motion Picture */}
      <div style={rocketStyle}>
        <svg width="300" height="300" viewBox="0 0 80 80">
          <g>
            <ellipse cx="40" cy="55" rx="10" ry="18" fill="#ccc" stroke="#888" strokeWidth="2"/>
            <rect x="35" y="20" width="10" height="35" rx="5" fill="#eee" stroke="#888" strokeWidth="2"/>
            <polygon points="40,10 35,20 45,20" fill="#f44336" />
            <rect x="37" y="55" width="6" height="12" rx="3" fill="#fbc02d" />
            <polygon points="40,67 37,67 40,80 43,67" fill="#ff9800" />
            <circle cx="40" cy="40" r="4" fill="#90caf9" stroke="#1976d2" strokeWidth="1"/>
          </g>
        </svg>
      </div>

      {/* Asteroid SVG */}
      <div style={{ ...asteroidStyle, ...motionStyle }}>
        <svg width="300" height="300" viewBox="0 0 120 120">
          <ellipse
            cx="60"
            cy="60"
            rx="45"
            ry="35"
            fill="#888"
            stroke="#444"
            strokeWidth="4"
          />
          <circle cx="80" cy="50" r="8" fill="#666" />
          <circle cx="50" cy="80" r="6" fill="#555" />
          <circle cx="70" cy="70" r="4" fill="#444" />
          <circle cx="40" cy="55" r="3" fill="#333" />
        </svg>
      </div>

      {/* Ocean Wave Motion Picture */}
      <div style={waveStyle}>
        <svg width="280" height="210" viewBox="0 0 160 120">
          <defs>
            <linearGradient id="simpleWaveGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#aef" />
              <stop offset="60%" stopColor="#2e5c8a" />
              <stop offset="100%" stopColor="#0a2e4c" />
            </linearGradient>
          </defs>
          <path
            d="M0,100 Q40,60 80,100 Q120,140 160,100"
            stroke="#2e5c8a"
            strokeWidth="6"
            fill="none"
          />
          <path
            d="M0,100 Q40,60 80,100 Q120,140 160,100 L160,120 L0,120 Z"
            fill="url(#simpleWaveGradient)"
          />
          <path
            d="M30,110 Q50,95 70,110"
            stroke="#fff"
            strokeWidth="3"
            fill="none"
            opacity="0.7"
          />
          <path
            d="M100,115 Q120,100 140,115"
            stroke="#fff"
            strokeWidth="3"
            fill="none"
            opacity="0.7"
          />
        </svg>
      </div>
      <style>
        {`
          @keyframes asteroid-float {
            0%   { transform: translate(-50%, -50%) scale(1); }
            50%  { transform: translate(-50%, -55%) scale(1.08) rotate(-5deg); }
            100% { transform: translate(-50%, -50%) scale(1); }
          }
          @keyframes wave-motion {
            0%   { transform: translate(-50%, -50%) scale(1); }
            50%  { transform: translate(-50%, -54%) scale(1.04) rotate(2deg); }
            100% { transform: translate(-50%, -50%) scale(1); }
          }
          @keyframes rocket-float {
            0%   { transform: translate(-50%, -50%) scale(1); }
            50%  { transform: translate(-50%, -54%) scale(1.08) rotate(-6deg); }
            100% { transform: translate(-50%, -50%) scale(1); }
          }
        `}
      </style>
      {/* Developer Card - Bottom Left */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 300,
          left: 0, // Move further left
          zIndex: 10,
        }}
      >
        <Card elevation={6} sx={{ minWidth: 220, bgcolor: 'rgba(255,255,255,0.97)', borderRadius: 3 }}>
          <CardContent>
            <Typography variant="subtitle1" fontWeight={700} color="black" gutterBottom>
              Developers
            </Typography>
            <Typography variant="body2" sx={{ color: 'black' }}>
              Shauly Chakraborty<br />
              Subhadip Das<br />
              Soumyadeep Dutta
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Grid>
  )
}

// Simple starfield canvas
function StarsCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let raf = 0
    const DPR = Math.min(window.devicePixelRatio || 1, 2)
    const resize = () => {
      const parent = canvas.parentElement!
      canvas.width = parent.clientWidth * DPR
      canvas.height = parent.clientHeight * DPR
    }
    resize()
    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random(), y: Math.random(), r: Math.random() * 1.8 + 0.2, s: Math.random() * 0.4 + 0.1
    }))
    const loop = () => {
      raf = requestAnimationFrame(loop)
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.fillStyle = 'rgba(255,255,255,0.85)'
      for (const star of stars) {
        star.x += star.s / canvas.width * 60
        if (star.x > 1) star.x = 0
        ctx.beginPath()
        ctx.arc(star.x * canvas.width, star.y * canvas.height, star.r, 0, Math.PI * 2)
        ctx.fill()
      }
    }
    loop()
    const onResize = () => resize()
    window.addEventListener('resize', onResize)
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', onResize) }
  }, [])
  return <Box sx={{ position: 'absolute', inset: 0 }}><canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} /></Box>
}

// Soft animated color blobs behind content
const float = keyframes({
  '0%': { transform: 'translate3d(0,0,0) scale(1)' },
  '50%': { transform: 'translate3d(10px,-20px,0) scale(1.05)' },
  '100%': { transform: 'translate3d(0,0,0) scale(1)' },
})

const headlineReveal = keyframes({
  '0%': { opacity: 0, transform: 'translateY(30px) scale(0.95)' },
  '50%': { opacity: 0.8, transform: 'translateY(-5px) scale(1.02)' },
  '100%': { opacity: 1, transform: 'translateY(0) scale(1)' },
})

function AuroraBlobs() {
  return (
    <>
      <Box sx={{ position: 'absolute', top: -80, right: -80, width: 260, height: 260, filter: 'blur(80px)', background: 'linear-gradient(135deg,#6366f1,#22d3ee)', opacity: 0.35, borderRadius: '50%', animation: `${float} 10s ease-in-out infinite` }} />
      <Box sx={{ position: 'absolute', bottom: -60, left: -60, width: 220, height: 220, filter: 'blur(70px)', background: 'linear-gradient(135deg,#f43f5e,#6366f1)', opacity: 0.25, borderRadius: '50%', animation: `${float} 12s ease-in-out infinite 1s` }} />
    </>
  )
}


