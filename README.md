# Física BR — entorno de Binder

Esta rama solo define el **entorno** (Python y paquetes) con el que Binder ejecuta los talleres.
Los talleres viven en la rama `main` y se traen al abrir cada enlace con
[nbgitpuller](https://github.com/jupyterhub/nbgitpuller).

Así, corregir un taller en `main` **no** obliga a Binder a reconstruir el entorno: los enlaces
siguen abriendo en el caso rápido. Esta rama solo debe cambiar si cambian las versiones de los paquetes.

Formato de enlace de un taller:

    https://mybinder.org/v2/gh/brfisica/fisica-br/entorno?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fbrfisica%252Ffisica-br%26branch%3Dmain%26urlpath%3Dvoila%252Frender%252Ffisica-br%252FTaller_Fluidos.ipynb

© 2026 Juan David Betancur Ríos y Nora Yamile Rojas Cataño. Todos los derechos reservados.
