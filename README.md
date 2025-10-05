# Asteroid Impact Simulation and Visualization Tool

## Competition Summary

This project is designed for the interactive simulation and visualization of asteroid impacts on Earth, integrating real scientific datasets and communicating complex impact science to diverse audiences.

**Key Features:**
- Integrates NASA’s Near-Earth Object (NEO) API for real-time asteroid data (characteristics, orbits).
- Simulates impact effects using USGS environmental and geological data (topography, seismic, tsunami).
- Models trajectories, impact energy, crater size, tsunamis, and both atmospheric and seismic consequences.
- Allows users to explore mitigation and “defense” strategies (deflection, gravity tractors, etc.).
- Provides visualizations for scientists, policymakers, educators, and the public.

---

## Project Roadmap

### Phase 1: Research & Data Collection

- Understand asteroid trajectories, impact physics.
- Source NASA NEO and USGS datasets for real simulation and consequence modeling.
- Supplement with relevant environmental and population datasets.

### Phase 2: Backend Development

- Orbit simulation using Keplerian elements (with Python libraries like Astropy, Poliastro).
- Impact energy calculations and crater size estimation.
- Tsunami and seismic modeling using USGS data.
- Mitigation engine for simulating defense actions.

### Phase 3: Frontend Development

- 3D visualization of orbital paths (Three.js/CesiumJS).
- 2D maps for impact zones, craters, tsunamis (Leaflet/D3.js).
- Interactive controls and options for mitigation simulations.
- Educational overlays: tooltips, infographics, gamified “Defend Earth” mode.

### Phase 4: User Testing & Accessibility

- Ensure results are intuitive and accessible to non-experts.
- Add accessibility features such as colorblind palettes and multilingual tooltips.
- Optimize for web/mobile performance.

---


## Installation

1. **Backend**:  
   - Install Python dependencies:  
     `pip install -r requirements.txt`

2. **Frontend**:  
   - Install Node dependencies:  
     `cd frontend`  
     `npm install`
**Backend** (API & simulations):  
  `python backend/app.py`

- **Frontend** (User Interface):  
  `cd frontend`  
  `npm start` or `npm run dev`

## Contributing

Feel free to open issues or submit pull requests for new features, bug fixes, or improvements!  

---

## License

MIT License (or specify your preferred license here)
