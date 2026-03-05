import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import heapq
import time

# Nodo para A* 
class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.costo_g = 0
        self.costo_h = 0
        self.costo_f = 0

    def __lt__(self, otro):
        return self.costo_f < otro.costo_f

# Funciones 
def heuristica(a, b):
    """Calcula distancia Euclidiana"""
    return np.linalg.norm(np.array(a)-np.array(b))

def a_estrella(mapa, inicio, destino, animacion=False):
    """Algoritmo A* que encuentra la ruta óptima"""
    lista_abierta = []
    conjunto_cerrado = set()
    nodo_inicio = Nodo(inicio)
    nodo_destino = Nodo(destino)
    heapq.heappush(lista_abierta, nodo_inicio)
    pasos_animacion = []

    while lista_abierta:
        actual = heapq.heappop(lista_abierta)
        if actual.posicion == nodo_destino.posicion:
            ruta = []
            while actual:
                ruta.append(actual.posicion)
                actual = actual.padre
            return ruta[::-1], pasos_animacion

        conjunto_cerrado.add(actual.posicion)

        # Revisar vecinos (incluyendo diagonales)
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                vecino_pos = (actual.posicion[0]+dx, actual.posicion[1]+dy)
                if 0 <= vecino_pos[0] < mapa.shape[0] and 0 <= vecino_pos[1] < mapa.shape[1]:
                    if mapa[vecino_pos] == 1 or vecino_pos in conjunto_cerrado:
                        continue
                    vecino = Nodo(vecino_pos, actual)
                    vecino.costo_g = actual.costo_g + (1.4 if dx!=0 and dy!=0 else 1)
                    vecino.costo_h = heuristica(vecino_pos, nodo_destino.posicion)
                    vecino.costo_f = vecino.costo_g + vecino.costo_h
                    heapq.heappush(lista_abierta, vecino)
                    if animacion:
                        pasos_animacion.append(vecino_pos)
    return None, pasos_animacion

# Interfaz Streamlit 
st.set_page_config(page_title="🚗 A* Pathfinding", layout="wide")
st.title("A* Pathfinding - Ciudad Cuadrícula Estética")

# Layout: Inputs a la izquierda, visualización a la derecha
col_entrada, col_visual = st.columns([1,2])

with col_entrada:
    st.header("Configuración del mapa")
    tamaño_mapa = st.slider("Tamaño del mapa", 5, 30, 12)
    inicio = st.text_input("Posición de inicio (x,y)", "0,0")
    destino = st.text_input("Posición de destino (x,y)", f"{tamaño_mapa-1},{tamaño_mapa-1}")
    bloqueadas_input = st.text_area("Casillas bloqueadas ejemplo: 1,3;2,4;2,1", "")
    animar = st.checkbox("Mostrar animación paso a paso")
    calcular = st.button("Calcular Ruta")

with col_visual:
    area_grafico = st.empty()

if calcular:
    mapa = np.zeros((tamaño_mapa, tamaño_mapa))
    if bloqueadas_input:
        try:
            for pos in bloqueadas_input.split(";"):
                x, y = map(int, pos.split(","))
                mapa[x,y] = 1
        except:
            st.error("Formato de casillas bloqueadas incorrecto")
    
    try:
        inicio_pos = tuple(map(int,inicio.split(",")))
        destino_pos = tuple(map(int,destino.split(",")))
        ruta, pasos = a_estrella(mapa, inicio_pos, destino_pos, animar)
        if ruta:
            st.success(f"Ruta encontrada con {len(ruta)} pasos")
            
            # Visualización 
            for idx, paso in enumerate([*pasos,ruta[-1]]):
                plt.figure(figsize=(6,6))
                for i in range(tamaño_mapa):
                    for j in range(tamaño_mapa):
                        color = "#e0f7fa" 
                        if mapa[i,j]==1:
                            color = "#212121"
                        if (i,j) in ruta[:idx]:
                            color = "#00e676"  
                        if (i,j)==inicio_pos:
                            color = "#2979ff" 
                        if (i,j)==destino_pos:
                            color = "#ff1744"  
                        plt.gca().add_patch(plt.Rectangle((j,tamaño_mapa-1-i),1,1,color=color,ec="white"))
                plt.xlim(0,tamaño_mapa)
                plt.ylim(0,tamaño_mapa)
                plt.gca().set_aspect('equal')
                plt.gca().invert_yaxis()
                plt.axis('off')
                area_grafico.pyplot(plt)
                if animar:
                    time.sleep(0.05)
        else:
            st.warning("No se encontró ruta")
    except Exception as e:
        st.error(f"Error: {e}")