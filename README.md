# AI Case Viewer (TCNS Portfolio)
## Quickstart

```bash
pip install -r requirements.txt
streamlit run case_viewer.py

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])


# TCNS – AI Case Viewer

## UD Vision & Roadmap

The TCNS Unattended Delivery (UD) Case Viewer demonstrates how operational constraints, parcel-level data, and 3D visualization can be combined to build next-generation last-mile optimization tools. This roadmap outlines the evolution from simple spatial visualization to a full digital-twin environment.

### 1. Operational Insights from DHL
- Real locker constraints, access flows, and time pressure  
- Variability in parcel dimensions and packaging  
- Recurring inefficiencies in manual loading  

### 2. Constraint-Based 3D Packing
- Space-aware placement  
- Collision detection  
- Validation against locker interior geometry  

### 3. Stackability, Fragility & Orientation Rules
- Parcel properties (stackable, fragile, orientation-restricted)  
- Rule-based or ML-informed validation during placement  
- Visual color-coding of constraint violations  

### 4. Vehicle Access Constraints
- Side-door vs. back-door loading options  
- Differences in reachable volume  
- Operational impact on loading strategy  

### 5. Lock Integration, Telemetry & ML
- Integration with digital locks  
- Access logs & real-time telemetry  
- Predictive models for delivery outcomes and incident detection  

### 6. Digital Twin Simulation
- Virtual locker simulation for parcel placement  
- User-adjustable parameters (locker size, parcel set, constraints)  
- Playback of incident scenarios via embeddings  

### 7. Business Value & Partner Integration
- Efficiency gains for carriers  
- Operational predictability for locker operators  
- Integration value for hardware vendors (locks, telematics)  
- Data valorization across the UD ecosystem  

✨ Parcel Schema v1.0 (Logistics & Digital Twin Model)

This schema defines how parcels are represented inside the TCNS UD Case Viewer.
It mirrors real logistics data models used by carriers (DHL, UPS) and locker operators, while remaining flexible for simulation and AI applications.

1. Geometry
Field	Type	Description
width	float (m)	Parcel width
depth	float (m)	Parcel length
height	float (m)	Parcel height
volume_m3	float	Derived: width × depth × height
2. Physics
Field	Type	Description
weight_kg	float	Parcel weight (real or demo fallback)
max_top_load_kg	float	Max load parcel can tolerate on top (real or fallback rule)
3. Stackability & Handling
Field	Type	Description
stackable_flag	bool	True if parcel can be placed under others
fragile_flag	bool	True if parcel must not bear weight
orientation	string	"any", "upright_only", "flat_only"
4. Identification
Field	Type	Description
parcel_id	string	Provided or auto-generated unique parcel code
5. Placement (simulation fields)

(Used for visualization and later optimization)

Field	Type	Description
x, y, z	float	Coordinates of parcel origin inside locker
Schema Purpose

This schema is designed to support:

Digital twin simulations

3D optimization logic

AI-assisted stacking rules

Collision detection

“Fit / No-Fit” evaluations

Operational analytics

Developer onboarding

The schema will evolve as UD_V1.0 matures (e.g., adding service class, delivery type, thermal requirements).

