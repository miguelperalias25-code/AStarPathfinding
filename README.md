# A* Pathfinding - Ciudad Cuadrícula Estética

## Descripción

Esta aplicación es un **simulador visual del algoritmo A\*** aplicado a un mapa de ciudad en forma de cuadrícula. Permite a los usuarios experimentar cómo A* encuentra la ruta óptima desde un punto de inicio hasta un destino, considerando calles transitables y obstáculos (como edificios o calles cortadas).  

La interfaz es **interactiva y estética**, mostrando la ruta paso a paso con colores y animación opcional.

---

## Funcionalidades

- Selección de **tamaño del mapa** (5x5 hasta 30x30).  
- Definición de **posición de inicio y destino**.  
- Configuración de **casillas bloqueadas** manualmente.  
- **Animación paso a paso** de la búsqueda de la ruta.  
- Visualización estética:
  - Verde: ruta encontrada  
  - Azul: inicio  
  - Rojo: destino  
  - Negro: obstáculos  
  - Blanco/azul claro: calles transitables  

---

## Instalación

1. Clonar este repositorio:

```bash
git clone https://github.com/TU_USUARIO/AstarPathfinding.git
cd AstarPathfinding

Instalar dependencias:

pip install -r requirements.txt

Ejecutar la aplicación:

streamlit run astar_ciudad.py