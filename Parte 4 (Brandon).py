# -*- coding: utf-8 -*-
"""
TRABAJO PRÁCTICO INTEGRADOR
ROLBOT - Descubrí tu próximo juego de rol

Parte 4: Grafo de Juegos Relacionados y Recomendaciones Avanzadas
Desarrollado por: Brandon Ezequiel Arismendis Vega
"""

import pandas as pd


# ==========================================
# CARGA DE DATOS
# ==========================================

juegos = pd.read_csv("rolbot_juegos_200.csv")



# ==========================================
# PARTE 4 - CLASE GRAFO DE JUEGOS RELACIONADOS
# ESTRUCTURA DE DATOS PARA RECOMENDACIONES
# ==========================================

class GrafoJuegos:
    """
    Grafo no dirigido que conecta juegos que comparten
    el mismo genero o sistema de juego.
    """
    def __init__(self):
        self.adjacencia = {}

    def agregar_juego(self,juego):
        if juego not in self.adjacencia:
            self.adjacencia[juego] = set()

    def agregar_relacion(self, juego1, juego2):
        self.agregar_juego(juego1)
        self.agregar_juego(juego2)
        if juego1 != juego2:
            self.adjacencia[juego1].add(juego2)
            self.adjacencia[juego2].add(juego1)

def obtener_relaciones(self, juego):
    nombre_buscado = juego.strip().casefold()
    for nodo in self.adjacencia:
        if nodo.casefold() == nombre_buscado:
            return list(self.adjacencia[nodo])
        return []


# ==========================================
# CONSTRUCCIÓN Y POBLADO DEL GRAFO
# ==========================================

def construir_grafo_juegos(df):
    grafo = GrafoJuegos()
    lista_juegos = df.to_dict("records")

    for i in range(len(lista_juegos)):
        j1 = lista_juegos[i]
        nombre1 = str(j1["juego"])
        grafo.agregar_juego(nombre1)

        for j in range(i + 1, len(lista_juegos)):
            j2 = lista_juegos[j]
            nombre2 = str(j2["juego"])

            # Conectamos juegos si comparten genero o sistema
            mismo_genero = str(j1["genero"]).casefold() == str(j2["genero"]).casefold()
            mismo_sistema = str(j1["sistema"]).casefold() = str(j2["sistema"]).casefold()

            if mismo_genero or mismo_sistema:
                grafo.agregar_relacion(nombre1, nombre2)

    return grafo


# Inicializamos el grafo con el dataset real
grafo_rolbot = construir_grafo_juegos(juegos)



# ==========================================
# FUNCIONES DE LA PARTE 4
# ==========================================

def buscar_relacionados_por_grafo():
    nombre = input("\nIngrese el nombre del juego para buscar relacionados: ").strip()
    relacionados = grafo_rolbot.obtener_relacionados(nombre)

    if relacionados:
        print(f"\nJuegos relacionados con '{nombre}' (Via Grafo):")
        for idx, rel in enumerate(relacionados[:10], start=1):
            print(f"{idx}. {rel}")
        if len(relacionados) > 10:
            print(f"... y {len(relacionados) - 10} juegos mas.")
        else:
            print(f"\nNo se encontraron juegos relacionados o el juego '{nombre}' no existe.")


    def recomendar_por_dificultad_y_duracion():
        print("\n--- RECOMENDACION PERSONALIZADA ---")
        dificultad = input("Ingrese la dificultad (ej. Baja, Media, Alta): ").strip()
        duracion = input("Ingrese la duracion aproximada (ej. Corta, Media, Larga): ").strip()

        resultado = juegos[
        (juegos["dificultad"].astype(str).str.casefold() == dificultad.casefold()) &
        (juegos["duracion"].astype(str).str.casefold() == duracion.casefold())
    ]

    if resultado.empty:
        print("\nNo se encontraron juegos con esos criterios exactos.")
    else:
        print(f"\nSe encontraron {len(resultado)} juegos recomendados:")
        print(resultado[["juego", "genero", "dificultad", "duracion", "popularidad"]].to_string(index=False))



def modulo_parte_4():
    """
    Menu interactivo para probar especificamente la parte 4.
    """
    while True:
        print("""========================================
    ROLBOT - PARTE 4 (Brandon)
========================================
1. Ver juegos relacionados (Grafo)
2. Recomendación por Dificultad y Duración
0. Volver / Salir
----------------------------------------
""")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            buscar_relacionados_por_grafo()
        elif opcion == "2":
            recomendar_por_dificultad_y_duracion()
        elif opcion == "0":
            print("Saliendo del modulo Parte 4.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    modulo_parte_4()