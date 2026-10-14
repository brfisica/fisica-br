"""Genera las miniaturas del portal a partir del esquema() de cada taller.

Uso (desde la raíz del repositorio):
    python generar_miniaturas.py                 # todos los talleres
    python generar_miniaturas.py Taller_Fluidos.ipynb
    python generar_miniaturas.py --todos         # además, un PNG por punto en revision_miniaturas/

Ejecuta cada taller, toma la primera figura de la celda del punto elegido
(por defecto el Punto 1; ver ELEGIDO) y la guarda junto al taller como <taller>.webp
(560 × 300 px, se muestra a la mitad para pantallas de alta densidad).
"""
import sys, glob, io, base64, os, re
import nbformat
from nbclient import NotebookClient
from PIL import Image

ANCHO, ALTO = 560, 300
# Punto cuyo esquema representa mejor el taller (si no está, se usa el 1)
ELEGIDO = {}
try:
    sys.path.insert(0, os.path.dirname(__file__)); from elegidos import ELEGIDO
except Exception:
    pass

def esquemas(ruta):
    nb = nbformat.read(ruta, as_version=4)
    NotebookClient(nb, timeout=300, kernel_name='python3', allow_errors=True).execute()
    salida, punto = {}, 0
    for c in nb.cells:
        if c.cell_type == 'markdown' and re.search(r'^## Punto (\d+)', c.source, re.M):
            punto = int(re.search(r'^## Punto (\d+)', c.source, re.M).group(1))
        if c.cell_type == 'code' and 'def esquema' in c.source and punto and punto not in salida:
            for o in c.get('outputs', []):
                if 'image/png' in o.get('data', {}):
                    salida[punto] = base64.b64decode(o['data']['image/png']); break
    return salida

def miniatura(png):
    im = Image.open(io.BytesIO(png)).convert('RGB')
    im.thumbnail((ANCHO, ALTO), Image.LANCZOS)
    lienzo = Image.new('RGB', (ANCHO, ALTO), (255, 255, 255))
    lienzo.paste(im, ((ANCHO - im.width) // 2, (ALTO - im.height) // 2))
    return lienzo

if __name__ == '__main__':
    rutas = sys.argv[1:] or sorted(glob.glob('Taller_*.ipynb'))
    todos = '--todos' in rutas
    if todos: os.makedirs('revision_miniaturas', exist_ok=True)
    rutas = [r for r in rutas if r != '--todos']
    for ruta in rutas:
        nombre = ruta[:-6]
        figs = esquemas(ruta)
        if todos:   # modo revisión: guarda el esquema de cada punto
            for p, png in figs.items():
                miniatura(png).save(f'revision_miniaturas/{nombre}__p{p}.png')
        p = ELEGIDO.get(nombre, 1)
        if p in figs:
            miniatura(figs[p]).save(f'{nombre.replace(" ", "_").replace("(", "").replace(")", "")}.webp', 'WEBP', quality=80, method=6)
            print(f'{nombre}: punto {p} de {sorted(figs)}')
        else:
            print(f'{nombre}: SIN esquema para el punto {p} ({sorted(figs)})')
