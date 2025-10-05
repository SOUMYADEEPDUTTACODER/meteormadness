// src/api/simulate.ts
export async function runSimulation(asteroidId: string, lat: number, lon: number) {
  const resp = await fetch("http://localhost:8000/api/simulate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      asteroid_id: asteroidId,
      impact_lat: lat,
      impact_lon: lon,
      propagate_days: 30,
    }),
  })

  if (!resp.ok) {
    throw new Error(`Simulation failed: ${resp.status}`)
  }
  return resp.json()
}
