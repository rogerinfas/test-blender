# test-blender

Machu Picchu + tecla mecánica en Blender, con visor web interactivo en Next.js.

## Contenido

- `blender/machu_picchu.blend` — escena Machu Picchu (terreno, Huayna Picchu, andenes, ruinas, Templo del Sol, Intihuatana)
- `blender/tecla.blend` — tecla mecánica (placa + switch + keycap) con animación de 3 pulsaciones (frames 1–90)
- `blender/tecla.mp4` — video de la animación
- `blender/renders/` — renders de referencia
- `blender/scripts/` — scripts Python para regenerar las escenas en Blender (`machu.py`, `machu2.py`, `tecla.py`, `bclient.py` para pilotar Blender por socket)
- `web/` — proyecto Next.js 16 + Tailwind + react-three-fiber con el visor 3D (`/modelo` y `/teclado` interactivo)

## Web: cómo correr

```bash
cd web
npm install
npm run dev   # http://localhost:3000
```

Rutas: `/` (hero con 3D de fondo) · `/tours` · `/nosotros` · `/contacto` · `/modelo` (Machu Picchu 3D) · `/teclado` (tecla interactiva: clic o ESPACIO)
