import { Box, Stack, Typography, TextField, Button } from "@mui/material"
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet"
import { useSimulationStore } from "../../store/simulationStore"
import { useState } from "react"

export default function ImpactMapPage() {
  const { result, run, loading } = useSimulationStore()

  const [asteroidId, setAsteroidId] = useState("3542519")
  const [lat, setLat] = useState(28.5)
  const [lon, setLon] = useState(-89.5)

  const impact = result?.impact_location
  const crater = result?.crater?.diameter_km ?? 0

  return (
    <Stack spacing={3}>
      <Typography variant="h4" fontWeight={700}>
        Impact Map
      </Typography>

      {/* --- Control Panel --- */}
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

      <Box
        sx={{
          height: 520,
          borderRadius: 2,
          bgcolor: "background.paper",
          border: "1px solid",
          borderColor: "divider",
        }}
      >
        <MapContainer
          center={[impact?.lat || 0, impact?.lon || 0]}
          zoom={impact ? 6 : 2}
          style={{ height: "100%", width: "100%", borderRadius: "8px" }}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {impact && (
            <>
              <Marker position={[impact.lat, impact.lon]}>
                <Popup>
                  <Typography variant="body2">
                    <b>Impact Site</b> <br />
                    Elevation: {impact.elevation_m?.toFixed(2)} m <br />
                    Crater: {crater.toFixed(2)} km
                  </Typography>
                </Popup>
              </Marker>
              <Circle
                center={[impact.lat, impact.lon]}
                radius={crater * 500} // scale km → m
                pathOptions={{ color: "red", fillOpacity: 0.3 }}
              />
            </>
          )}
        </MapContainer>
      </Box>
    </Stack>
  )
}
