import { create } from "zustand"
import { runSimulation } from "../api/simulate"

interface SimulationState {
  loading: boolean
  error: string | null
  result: any | null
  run: (asteroidId: string, lat: number, lon: number) => Promise<void>
}

export const useSimulationStore = create<SimulationState>((set) => ({
  loading: false,
  error: null,
  result: null,

  run: async (asteroidId: string, lat: number, lon: number) => {
    set({ loading: true, error: null })
    try {
      const data = await runSimulation(asteroidId, lat, lon)
      set({ result: data.output, loading: false })
    } catch (err: any) {
      set({ error: err.message, loading: false })
    }
  },
}))
