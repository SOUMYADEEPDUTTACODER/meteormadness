import { Box, Stack, Typography, Button, TextField } from "@mui/material";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { useEffect, useRef, useState } from "react";
import { useSimulationStore } from "../../store/simulationStore";
// Use ESM-compatible import for CommonJS prop-types
import * as PropTypes from "prop-types";

function OrbitScene({ result }: { result: any }) {
  const statsRef = useRef<any>(null);

  useEffect(() => {
    // Load Stats.js UMD dynamically
    import("stats.js").then((StatsModule) => {
      const Stats = (StatsModule as any).default || StatsModule;
      const stats = new Stats();
      stats.showPanel(0);
      document.body.appendChild(stats.dom);
      statsRef.current = stats;

      const animate = () => {
        stats.begin();
        stats.end();
        requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
    });

    return () => {
      if (statsRef.current?.dom?.parentNode) {
        statsRef.current.dom.parentNode.removeChild(statsRef.current.dom);
      }
    };
  }, []);

  if (!result) return null;
  const { current, future } = result.heliocentric_coordinates || {};

  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      {/* Sun */}
      <mesh>
        <sphereGeometry args={[0.1, 32, 32]} />
        <meshStandardMaterial color="yellow" />
      </mesh>
      {/* Asteroid positions */}
      {current && (
        <mesh position={[current[0], current[1], current[2]]}>
          <sphereGeometry args={[0.05, 16, 16]} />
          <meshStandardMaterial color="red" />
        </mesh>
      )}
      {future && (
        <mesh position={[future[0], future[1], future[2]]}>
          <sphereGeometry args={[0.05, 16, 16]} />
          <meshStandardMaterial color="blue" />
        </mesh>
      )}
      <OrbitControls />
    </Canvas>
  );
}

OrbitScene.propTypes = {
  result: PropTypes.object,
};

export default function OrbitPage() {
  const { result, run, loading, error } = useSimulationStore();
  const [asteroidId, setAsteroidId] = useState("3542519");
  const [lat, setLat] = useState(28.5);
  const [lon, setLon] = useState(-89.5);

  return (
    <Stack spacing={3}>
      <Typography variant="h4" fontWeight={700}>
        3D Orbit Visualization
      </Typography>

      {/* Control Panel */}
      <Stack direction="row" spacing={2} alignItems="center">
        <TextField
          label="Asteroid ID"
          value={asteroidId}
          onChange={(e) => setAsteroidId(e.target.value)}
          size="small"
        />
        <TextField
          label="Latitude"
          type="number"
          value={lat}
          onChange={(e) => setLat(parseFloat(e.target.value))}
          size="small"
        />
        <TextField
          label="Longitude"
          type="number"
          value={lon}
          onChange={(e) => setLon(parseFloat(e.target.value))}
          size="small"
        />
        <Button
          variant="contained"
          disabled={loading}
          onClick={() => run(asteroidId, lat, lon)}
        >
          {loading ? "Simulating..." : "Run Simulation"}
        </Button>
      </Stack>

      {error && <Typography color="error">{error}</Typography>}

      <Box
        sx={{
          height: 480,
          borderRadius: 2,
          bgcolor: "background.paper",
          border: "1px solid",
          borderColor: "divider",
        }}
      >
        <OrbitScene result={result} />
      </Box>
    </Stack>
  );
}
