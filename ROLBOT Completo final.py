# -*- coding: utf-8 -*-
"""
TRABAJO PRACTICO INTEGRADOR
ROLBOT - Descubri tu proximo juego de rol

Partes integradas:
1. Carga de datos y clase Juego.
2. Busqueda secuencial y analisis de complejidad.
3. Arbol binario de busqueda (ABB).
4. Arbol AVL, rotaciones y comparacion con el ABB desbalanceado.\n5. Arbol general n-ario, busquedas y recorridos.\n6. Cola de prioridad con heap binaria maxima.
7. Grafo no dirigido y ponderado de juegos relacionados.
8. Recorridos BFS y DFS sobre el grafo.
"""

import time
from collections import deque
import pandas as pd


# =========================================================
# PARTE 1: CARGA DE DATOS Y CLASE JUEGO
# =========================================================

juegos = pd.read_csv("rolbot_juegos_200.csv")
datos_reales = juegos["juego"].dropna().astype(str).tolist()


class Juego:
    def __init__(self, id, juego, genero, jugadores_min, jugadores_max,
                 dificultad, duracion, sistema, popularidad):
        self.__id = id
        self.__juego = juego
        self.__genero = genero
        self.__jugadores_min = jugadores_min
        self.__jugadores_max = jugadores_max
        self.__dificultad = dificultad
        self.__duracion = duracion
        self.__sistema = sistema
        self.__popularidad = popularidad


# =========================================================
# FUNCIONES PRINCIPALES DE ROLBOT
# =========================================================

def buscar_por_nombre(nombre):
    resultado = juegos[
        juegos["juego"].astype(str).str.casefold() == nombre.strip().casefold()
    ]

    if resultado.empty:
        print("\nNo se encontro ese juego.")
    else:
        print("\nInformacion del juego:")
        print(resultado.to_string(index=False))


def listar_juegos():
    print(juegos["juego"].to_string(index=False))


def filtrar_por_genero(genero):
    resultado = juegos[
        juegos["genero"].astype(str).str.casefold() == genero.strip().casefold()
    ]

    if resultado.empty:
        print("\nNo se encontraron juegos de ese genero.")
    else:
        print(resultado.to_string(index=False))



# =========================================================
# PARTE 6: COLA DE PRIORIDAD CON HEAP BINARIA MAXIMA
# =========================================================

def prioridad_juego(juego):
    """
    Devuelve la prioridad de un juego.
    La popularidad es el criterio principal.
    Si hay empate, se utiliza el nombre alfabeticamente.
    """
    try:
        popularidad = float(juego["popularidad"])
        if pd.isna(popularidad):
            popularidad = 0
    except (TypeError, ValueError):
        popularidad = 0

    nombre = str(juego["juego"]).strip()
    return popularidad, nombre.casefold()


class HeapPrioridad:
    """Heap binaria maxima implementada manualmente."""

    def __init__(self, elementos=None):
        self.heap = list(elementos) if elementos is not None else []
        self._construir_heap()

    def _tiene_mayor_prioridad(self, primero, segundo):
        prioridad_primero = prioridad_juego(primero)
        prioridad_segundo = prioridad_juego(segundo)

        if prioridad_primero[0] != prioridad_segundo[0]:
            return prioridad_primero[0] > prioridad_segundo[0]

        # En caso de empate, el nombre alfabeticamente menor va primero.
        return prioridad_primero[1] < prioridad_segundo[1]

    def _flotar(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2

            if self._tiene_mayor_prioridad(self.heap[indice], self.heap[padre]):
                self.heap[indice], self.heap[padre] = (
                    self.heap[padre], self.heap[indice]
                )
                indice = padre
            else:
                break

    def _hundir(self, indice):
        cantidad = len(self.heap)

        while True:
            hijo_izquierdo = 2 * indice + 1
            hijo_derecho = 2 * indice + 2
            mayor = indice

            if (
                hijo_izquierdo < cantidad
                and self._tiene_mayor_prioridad(
                    self.heap[hijo_izquierdo], self.heap[mayor]
                )
            ):
                mayor = hijo_izquierdo

            if (
                hijo_derecho < cantidad
                and self._tiene_mayor_prioridad(
                    self.heap[hijo_derecho], self.heap[mayor]
                )
            ):
                mayor = hijo_derecho

            if mayor == indice:
                break

            self.heap[indice], self.heap[mayor] = (
                self.heap[mayor], self.heap[indice]
            )
            indice = mayor

    def _construir_heap(self):
        # Construccion bottom-up: O(n).
        for indice in range(len(self.heap) // 2 - 1, -1, -1):
            self._hundir(indice)

    def insertar(self, elemento):
        self.heap.append(elemento)
        self._flotar(len(self.heap) - 1)

    def extraer_maximo(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._hundir(0)
        return maximo

    def esta_vacio(self):
        return len(self.heap) == 0


def obtener_top_n(cantidad):
    """Obtiene los N juegos de mayor prioridad usando el heap."""
    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return

    elementos = []
    for _, fila in juegos.iterrows():
        if pd.isna(fila["juego"]):
            continue
        elementos.append(fila.to_dict())

    if not elementos:
        print("No hay juegos disponibles para generar el ranking.")
        return

    heap = HeapPrioridad(elementos)
    cantidad_real = min(cantidad, len(elementos))

    print(f"\nTOP {cantidad_real} JUEGOS POR PRIORIDAD")
    print("----------------------------------------")

    for posicion in range(1, cantidad_real + 1):
        juego = heap.extraer_maximo()
        nombre = str(juego["juego"])
        popularidad = prioridad_juego(juego)[0]
        print(f"{posicion:2}. {nombre:<30} Popularidad: {popularidad:g}")


def consultar_top_n():
    print("\nRANKING DINAMICO DE ROLBOT")
    entrada = input("Cuantos juegos desea consultar? ").strip()

    try:
        cantidad = int(entrada)
    except ValueError:
        print("Ingrese un numero entero valido.")
        return

    obtener_top_n(cantidad)


def mostrar_top_10():
    # La opcion clasica Top 10 tambien utiliza la cola de prioridad.
    obtener_top_n(10)


def recomendar_por_dificultad_y_duracion():
    print("\n--- RECOMENDACION PERSONALIZADA ---")
    print("Dificultades disponibles:")
    print(sorted(juegos["dificultad"].dropna().astype(str).unique()))
    print("Duraciones disponibles:")
    print(sorted(juegos["duracion"].dropna().astype(str).unique()))

    dificultad = input("\nIngrese la dificultad: ").strip()
    duracion = input("Ingrese la duracion: ").strip()

    resultado = juegos[
        (juegos["dificultad"].astype(str).str.casefold() == dificultad.casefold())
        & (juegos["duracion"].astype(str).str.casefold() == duracion.casefold())
    ]

    if resultado.empty:
        print("\nNo se encontraron juegos con esos criterios.")
    else:
        print(f"\nSe encontraron {len(resultado)} juegos recomendados:")
        print(
            resultado[
                ["juego", "genero", "dificultad", "duracion", "popularidad"]
            ].to_string(index=False)
        )


# =========================================================
# PARTE 2: BUSQUEDA SECUENCIAL
# =========================================================

def busqueda_secuencial(nombre, datos):
    comparaciones = 0

    for elemento in datos:
        comparaciones += 1
        if elemento.casefold() == nombre.strip().casefold():
            return elemento, comparaciones

    return None, comparaciones


# =========================================================
# PARTE 3: ARBOL BINARIO DE BUSQUEDA (ABB / BST)
# =========================================================

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return

        actual = self.raiz

        while True:
            if valor.casefold() < actual.valor.casefold():
                if actual.izquierda is None:
                    actual.izquierda = Nodo(valor)
                    return
                actual = actual.izquierda
            elif valor.casefold() > actual.valor.casefold():
                if actual.derecha is None:
                    actual.derecha = Nodo(valor)
                    return
                actual = actual.derecha
            else:
                return  # No insertar nombres duplicados.

    def buscar(self, nombre):
        actual = self.raiz
        comparaciones = 0
        nombre = nombre.strip().casefold()

        while actual is not None:
            comparaciones += 1

            if nombre == actual.valor.casefold():
                return actual.valor, comparaciones

            if nombre < actual.valor.casefold():
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None, comparaciones

    def altura(self):
        return altura_abb(self.raiz)


def altura_abb(nodo):
    if nodo is None:
        return 0

    altura_maxima = 0
    pila = [(nodo, 1)]

    while pila:
        actual, nivel = pila.pop()
        altura_maxima = max(altura_maxima, nivel)

        if actual.izquierda is not None:
            pila.append((actual.izquierda, nivel + 1))

        if actual.derecha is not None:
            pila.append((actual.derecha, nivel + 1))

    return altura_maxima


def cargar_arbol_balanceado(arbol, datos):
    """Carga un ABB insertando primero el elemento central."""
    if not datos:
        return
    medio = len(datos) // 2
    arbol.insertar(datos[medio])
    cargar_arbol_balanceado(arbol, datos[:medio])
    cargar_arbol_balanceado(arbol, datos[medio + 1:])


arbol_rolbot = ArbolBusqueda()
cargar_arbol_balanceado(arbol_rolbot, datos_reales)


def buscar_por_arbol():
    nombre = input("\nIngrese el nombre del juego: ").strip()
    resultado, comparaciones = arbol_rolbot.buscar(nombre)

    if resultado is None:
        print("No se encontro ese juego en el ABB.")
    else:
        print("Juego encontrado:", resultado)
    print("Comparaciones en el ABB:", comparaciones)


# =========================================================
# PARTE 4: ARBOL AVL
# =========================================================

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1


def altura_avl(nodo):
    if nodo is None:
        return 0
    return nodo.altura


def factor_balance(nodo):
    if nodo is None:
        return 0
    return altura_avl(nodo.izquierda) - altura_avl(nodo.derecha)


def rotacion_derecha(y):
    """Rotacion para corregir un desequilibrio izquierda-izquierda."""
    x = y.izquierda
    subarbol = x.derecha

    x.derecha = y
    y.izquierda = subarbol

    y.altura = 1 + max(altura_avl(y.izquierda), altura_avl(y.derecha))
    x.altura = 1 + max(altura_avl(x.izquierda), altura_avl(x.derecha))
    return x


def rotacion_izquierda(x):
    """Rotacion para corregir un desequilibrio derecha-derecha."""
    y = x.derecha
    subarbol = y.izquierda

    y.izquierda = x
    x.derecha = subarbol

    x.altura = 1 + max(altura_avl(x.izquierda), altura_avl(x.derecha))
    y.altura = 1 + max(altura_avl(y.izquierda), altura_avl(y.derecha))
    return y


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        # 1. Insercion normal de un arbol binario de busqueda.
        if nodo is None:
            return NodoAVL(valor)

        if valor.casefold() < nodo.valor.casefold():
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        elif valor.casefold() > nodo.valor.casefold():
            nodo.derecha = self._insertar(nodo.derecha, valor)
        else:
            return nodo  # No insertar duplicados.

        # 2. Actualizar la altura del nodo.
        nodo.altura = 1 + max(
            altura_avl(nodo.izquierda),
            altura_avl(nodo.derecha)
        )

        # 3. Calcular el factor de balance y rotar si hace falta.
        balance = factor_balance(nodo)

        # Caso izquierda-izquierda (LL).
        if balance > 1 and valor.casefold() < nodo.izquierda.valor.casefold():
            return rotacion_derecha(nodo)

        # Caso derecha-derecha (RR).
        if balance < -1 and valor.casefold() > nodo.derecha.valor.casefold():
            return rotacion_izquierda(nodo)

        # Caso izquierda-derecha (LR).
        if balance > 1 and valor.casefold() > nodo.izquierda.valor.casefold():
            nodo.izquierda = rotacion_izquierda(nodo.izquierda)
            return rotacion_derecha(nodo)

        # Caso derecha-izquierda (RL).
        if balance < -1 and valor.casefold() < nodo.derecha.valor.casefold():
            nodo.derecha = rotacion_derecha(nodo.derecha)
            return rotacion_izquierda(nodo)

        return nodo

    def buscar(self, nombre):
        actual = self.raiz
        comparaciones = 0
        nombre = nombre.strip().casefold()

        while actual is not None:
            comparaciones += 1

            if nombre == actual.valor.casefold():
                return actual.valor, comparaciones

            if nombre < actual.valor.casefold():
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None, comparaciones

    def altura(self):
        return altura_avl(self.raiz)


avl_rolbot = ArbolAVL()
for nombre_juego in datos_reales:
    avl_rolbot.insertar(nombre_juego)


def buscar_por_avl():
    nombre = input("\nIngrese el nombre del juego: ").strip()
    resultado, comparaciones = avl_rolbot.buscar(nombre)

    if resultado is None:
        print("No se encontro ese juego en el AVL.")
    else:
        print("Juego encontrado:", resultado)
    print("Comparaciones en el AVL:", comparaciones)


def comparar_abb_vs_avl():
    print("\nCOMPARACION: ABB DESBALANCEADO VS AVL")
    print("Insertamos nombres en orden alfabetico ascendente.")
    print("El ABB comun puede formar una cadena; el AVL se reequilibra.")
    print()
    print("Elementos | Altura ABB | Altura AVL | Comp. ABB | Comp. AVL")

    # Estos tamaños permiten ver claramente la diferencia sin hacer
    # que el experimento cuadratico del ABB tarde demasiado.
    for cantidad in (100, 500, 1000, 2000):
        datos = [f"Juego {i:05d}" for i in range(1, cantidad + 1)]

        abb = ArbolBusqueda()
        avl = ArbolAVL()

        # Mismo orden de insercion para ambos arboles.
        for dato in datos:
            abb.insertar(dato)
            avl.insertar(dato)

        objetivo = datos[-1]
        _, comp_abb = abb.buscar(objetivo)
        _, comp_avl = avl.buscar(objetivo)

        print(
            f"{cantidad:9} | {abb.altura():10} | {avl.altura():10} |"
            f" {comp_abb:9} | {comp_avl:9}"
        )

    print("\nLas alturas se cuentan en cantidad de niveles.")
    print("En el ABB ordenado, la altura puede llegar a n.")
    print("El AVL mantiene una altura proporcional a log2(n).")




# =========================================================
# PARTE 5: ARBOL GENERAL (N-ARIO)
# =========================================================

class NodoGeneral:
    def __init__(self, dato, tipo):
        self.dato = dato
        self.tipo = tipo
        self.hijos = []


class ArbolGeneral:
    def __init__(self, dato_raiz):
        self.raiz = NodoGeneral(dato_raiz, "raiz")

    def agregar_hijo(self, padre, dato, tipo):
        nuevo = NodoGeneral(dato, tipo)
        padre.hijos.append(nuevo)
        return nuevo

    def buscar(self, dato, nodo=None):
        if nodo is None:
            nodo = self.raiz

        if str(nodo.dato).casefold() == str(dato).strip().casefold():
            return nodo

        for hijo in nodo.hijos:
            resultado = self.buscar(dato, hijo)
            if resultado is not None:
                return resultado

        return None

    # Recorrido en profundidad: raiz, hijos y descendientes.
    def preorden(self, nodo=None, resultado=None):
        if resultado is None:
            resultado = []
        if nodo is None:
            nodo = self.raiz

        resultado.append(nodo.dato)
        for hijo in nodo.hijos:
            self.preorden(hijo, resultado)

        return resultado

    # Recorrido en profundidad: primero los descendientes.
    def postorden(self, nodo=None, resultado=None):
        if resultado is None:
            resultado = []
        if nodo is None:
            nodo = self.raiz

        for hijo in nodo.hijos:
            self.postorden(hijo, resultado)
        resultado.append(nodo.dato)

        return resultado

    # Recorrido por niveles: primero la raiz y luego cada nivel.
    def por_niveles(self):
        resultado = []
        cola = deque([self.raiz])

        while cola:
            actual = cola.popleft()
            resultado.append(actual.dato)
            for hijo in actual.hijos:
                cola.append(hijo)

        return resultado

    def mostrar_jerarquia(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        if nivel == 0:
            print(str(nodo.dato))
        else:
            print("    " * (nivel - 1) + "|-- " + str(nodo.dato))

        for hijo in nodo.hijos:
            self.mostrar_jerarquia(hijo, nivel + 1)


def construir_arbol_general():
    arbol = ArbolGeneral("Juegos de rol")
    nodos_genero = {}

    for _, fila in juegos.dropna(subset=["juego", "genero"]).iterrows():
        genero = str(fila["genero"]).strip()
        nombre = str(fila["juego"]).strip()

        if not genero or not nombre:
            continue

        clave_genero = genero.casefold()

        if clave_genero not in nodos_genero:
            nodos_genero[clave_genero] = arbol.agregar_hijo(
                arbol.raiz, genero, "categoria"
            )

        arbol.agregar_hijo(
            nodos_genero[clave_genero], nombre, "juego"
        )

    return arbol


# El arbol se construye una sola vez al iniciar ROLBOT.
arbol_general = construir_arbol_general()


def explorar_categorias():
    while True:
        print("""
========== EXPLORAR CATEGORIAS ==========
1. Mostrar jerarquia completa
2. Buscar categoria o juego
3. Ver recorridos del arbol
4. Filtrar juegos por genero
0. Volver al menu principal
=========================================
""")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            print("\nJERARQUIA DE ROLBOT")
            arbol_general.mostrar_jerarquia()

        elif opcion == "2":
            termino = input("Ingrese el nombre de una categoria o juego: ").strip()
            encontrado = arbol_general.buscar(termino)

            if encontrado is None:
                print("No se encontro la categoria o el juego.")
            else:
                print("Elemento encontrado:", encontrado.dato)
                if encontrado.tipo == "categoria":
                    print("Juegos de esta categoria:")
                    for hijo in encontrado.hijos:
                        print("-", hijo.dato)
                elif encontrado.tipo == "raiz":
                    print("Se encontro la raiz del arbol.")

        elif opcion == "3":
            print("\nRECORRIDO PREORDEN:")
            print(" -> ".join(map(str, arbol_general.preorden())))

            print("\nRECORRIDO POSTORDEN:")
            print(" -> ".join(map(str, arbol_general.postorden())))

            print("\nRECORRIDO POR NIVELES:")
            print(" -> ".join(map(str, arbol_general.por_niveles())))

        elif opcion == "4":
            print("\nGeneros disponibles:")
            print(sorted(juegos["genero"].dropna().astype(str).unique()))
            genero = input("Ingrese el genero: ").strip()
            filtrar_por_genero(genero)

        elif opcion == "0":
            break

        else:
            print("Opcion invalida. Ingrese un numero del menu.")



# =========================================================
# PARTE 7: GRAFO DE JUEGOS RELACIONADOS
# =========================================================

class GrafoJuegos:
    """Grafo no dirigido y ponderado, implementado con lista de adyacencia."""

    def __init__(self):
        # Cada juego apunta a un diccionario {juego_vecino: peso}.
        self.adyacencia = {}

    def agregar_vertice(self, juego):
        if juego not in self.adyacencia:
            self.adyacencia[juego] = {}

    def agregar_arista(self, juego_a, juego_b, peso):
        if juego_a == juego_b:
            return
        self.agregar_vertice(juego_a)
        self.agregar_vertice(juego_b)
        # Al ser no dirigido, guardamos la relacion en ambos sentidos.
        self.adyacencia[juego_a][juego_b] = peso
        self.adyacencia[juego_b][juego_a] = peso

    def obtener_relacionados(self, juego):
        clave = self._buscar_nombre(juego)
        if clave is None:
            return None
        return self.adyacencia[clave]

    def _buscar_nombre(self, nombre):
        buscado = str(nombre).strip().casefold()
        for juego in self.adyacencia:
            if juego.casefold() == buscado:
                return juego
        return None

    def estan_conectados(self, juego_a, juego_b):
        primero = self._buscar_nombre(juego_a)
        segundo = self._buscar_nombre(juego_b)
        if primero is None or segundo is None:
            return None
        return segundo in self.adyacencia[primero]

    def mas_conectados(self, cantidad=10):
        ranking = sorted(
            self.adyacencia.items(),
            key=lambda elemento: (-len(elemento[1]), elemento[0].casefold())
        )
        return ranking[:cantidad]

    def cantidad_aristas(self):
        # Cada arista aparece dos veces en la lista de adyacencia.
        return sum(len(vecinos) for vecinos in self.adyacencia.values()) // 2

    def _buscar_camino_bfs(self, inicio, destino):
        """Devuelve el camino con menor cantidad de aristas usando BFS."""
        origen = self._buscar_nombre(inicio)
        objetivo = self._buscar_nombre(destino)

        if origen is None or objetivo is None:
            return None

        cola = deque([origen])
        visitados = {origen}
        anterior = {origen: None}

        while cola:
            actual = cola.popleft()
            if actual == objetivo:
                camino = []
                paso = objetivo
                while paso is not None:
                    camino.append(paso)
                    paso = anterior[paso]
                camino.reverse()
                return camino

            for vecino in sorted(self.adyacencia[actual], key=str.casefold):
                if vecino not in visitados:
                    visitados.add(vecino)
                    anterior[vecino] = actual
                    cola.append(vecino)

        return []

    def recorrido_dfs(self, inicio):
        """Recorre en profundidad todos los vertices alcanzables desde inicio."""
        origen = self._buscar_nombre(inicio)
        if origen is None:
            return None

        visitados = set()
        recorrido = []
        pila = [origen]

        while pila:
            actual = pila.pop()
            if actual in visitados:
                continue

            visitados.add(actual)
            recorrido.append(actual)

            # Se invierte el orden alfabetico para que la pila visite primero
            # el vecino alfabeticamente menor.
            vecinos = sorted(self.adyacencia[actual], key=str.casefold, reverse=True)
            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)

        return recorrido


def construir_grafo_juegos():
    """Conecta juegos que comparten genero y/o sistema de juego.

    Peso 1: comparten una caracteristica.
    Peso 2: comparten genero y sistema.
    """
    grafo = GrafoJuegos()
    registros = []

    for _, fila in juegos.iterrows():
        if pd.isna(fila.get("juego")):
            continue
        nombre = str(fila["juego"]).strip()
        if not nombre:
            continue

        genero = "" if pd.isna(fila.get("genero")) else str(fila["genero"]).strip()
        sistema = "" if pd.isna(fila.get("sistema")) else str(fila["sistema"]).strip()
        grafo.agregar_vertice(nombre)
        registros.append((nombre, genero.casefold(), sistema.casefold()))

    # Comparamos pares de juegos para descubrir sus caracteristicas comunes.
    for i in range(len(registros)):
        nombre_a, genero_a, sistema_a = registros[i]
        for j in range(i + 1, len(registros)):
            nombre_b, genero_b, sistema_b = registros[j]

            comparte_genero = bool(genero_a) and genero_a == genero_b
            comparte_sistema = bool(sistema_a) and sistema_a == sistema_b
            peso = int(comparte_genero) + int(comparte_sistema)

            if peso > 0:
                grafo.agregar_arista(nombre_a, nombre_b, peso)

    return grafo


# Se construye una vez al iniciar el sistema.
grafo_rolbot = construir_grafo_juegos()


def explorar_grafo():
    while True:
        print("""
========== GRAFO DE JUEGOS RELACIONADOS ==========
1. Ver juegos relacionados
2. Comprobar relacion entre dos juegos
3. Ver juegos con mas conexiones
4. Mostrar estadisticas del grafo
5. BFS: camino mas corto entre dos juegos
6. DFS: explorar la red en profundidad
0. Volver al menu principal
==================================================
""")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            nombre = input("Ingrese el nombre del juego: ").strip()
            relacionados = grafo_rolbot.obtener_relacionados(nombre)
            if relacionados is None:
                print("No se encontro ese juego en el grafo.")
            elif not relacionados:
                print("El juego no tiene conexiones con otros juegos.")
            else:
                print(f"\nJuegos relacionados con {nombre}:")
                ordenados = sorted(
                    relacionados.items(),
                    key=lambda elemento: (-elemento[1], elemento[0].casefold())
                )
                for vecino, peso in ordenados:
                    coincidencias = "genero y sistema" if peso == 2 else "genero o sistema"
                    print(f"- {vecino} | peso: {peso} | comparte: {coincidencias}")

        elif opcion == "2":
            primero = input("Primer juego: ").strip()
            segundo = input("Segundo juego: ").strip()
            conectado = grafo_rolbot.estan_conectados(primero, segundo)
            if conectado is None:
                print("No se encontro uno o ambos juegos en el grafo.")
            elif conectado:
                peso = grafo_rolbot.obtener_relacionados(primero)
                print(f"Si, estan conectados. Peso de la relacion: {peso[grafo_rolbot._buscar_nombre(segundo)]}")
            else:
                print("No existe una conexion directa entre esos juegos.")

        elif opcion == "3":
            cantidad_txt = input("Cuantos juegos desea mostrar? (por defecto 10): ").strip()
            try:
                cantidad = 10 if not cantidad_txt else int(cantidad_txt)
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                print("Ingrese un numero entero mayor que cero.")
                continue
            print("\nJUEGOS CON MAS CONEXIONES")
            for posicion, (nombre, vecinos) in enumerate(grafo_rolbot.mas_conectados(cantidad), 1):
                print(f"{posicion}. {nombre} - {len(vecinos)} conexiones")

        elif opcion == "4":
            vertices = len(grafo_rolbot.adyacencia)
            aristas = grafo_rolbot.cantidad_aristas()
            grado_medio = (2 * aristas / vertices) if vertices else 0
            print("\nESTADISTICAS DEL GRAFO")
            print("Vertices (juegos):", vertices)
            print("Aristas (relaciones):", aristas)
            print(f"Grado promedio: {grado_medio:.2f}")
            print("Representacion: lista de adyacencia")
            print("Tipo: no dirigido y ponderado")
            print("BFS: usa una cola y encuentra el camino con menos aristas.")
            print("DFS: usa una pila y explora cada rama antes de retroceder.")
            print("Ambos recorridos: O(V + E) con lista de adyacencia.")

        elif opcion == "5":
            primero = input("Juego de origen: ").strip()
            destino = input("Juego de destino: ").strip()
            camino = grafo_rolbot._buscar_camino_bfs(primero, destino)

            if camino is None:
                print("No se encontro uno o ambos juegos en el grafo.")
            elif not camino:
                print("No existe un camino entre esos juegos.")
            elif len(camino) == 1:
                print("El origen y el destino son el mismo juego.")
            else:
                print("\nCAMINO MAS CORTO EN CANTIDAD DE CONEXIONES (BFS)")
                print(" -> ".join(camino))
                print("Cantidad de aristas recorridas:", len(camino) - 1)
                print("BFS minimiza la cantidad de aristas, no la suma de sus pesos.")

        elif opcion == "6":
            nombre = input("Juego desde el que desea explorar: ").strip()
            recorrido = grafo_rolbot.recorrido_dfs(nombre)

            if recorrido is None:
                print("No se encontro ese juego en el grafo.")
            else:
                print("\nRECORRIDO EN PROFUNDIDAD (DFS)")
                for posicion, juego in enumerate(recorrido, 1):
                    print(f"{posicion}. {juego}")
                print("Total de juegos alcanzables:", len(recorrido))

        elif opcion == "0":
            break
        else:
            print("Opcion invalida. Ingrese un numero del menu.")


# =========================================================
# ANALISIS DE COMPLEJIDAD (SE EJECUTA AL SALIR)
# =========================================================

def realizar_experimento_balanceado(cantidad):
    datos = [f"Juego {i:06d}" for i in range(cantidad)]
    abb = ArbolBusqueda()
    avl = ArbolAVL()

    # Cargar ambos en orden ascendente: caso problematico para el ABB.
    for dato in datos:
        abb.insertar(dato)
        avl.insertar(dato)

    objetivo = datos[-1]

    inicio = time.perf_counter()
    _, comp_abb = abb.buscar(objetivo)
    tiempo_abb = (time.perf_counter() - inicio) * 1000

    inicio = time.perf_counter()
    _, comp_avl = avl.buscar(objetivo)
    tiempo_avl = (time.perf_counter() - inicio) * 1000

    return cantidad, abb.altura(), avl.altura(), comp_abb, comp_avl, tiempo_abb, tiempo_avl


def analizar_complejidad():
    print("\n========================================")
    print("       ANALISIS DE COMPLEJIDAD")
    print("========================================")

    print("\nPrueba con los datos reales de ROLBOT:")
    if datos_reales:
        objetivo = datos_reales[-1]
        _, comp_seq = busqueda_secuencial(objetivo, datos_reales)
        _, comp_abb = arbol_rolbot.buscar(objetivo)
        _, comp_avl = avl_rolbot.buscar(objetivo)
        print("Cantidad de juegos:", len(datos_reales))
        print("Juego buscado:", objetivo)
        print("Comparaciones busqueda secuencial:", comp_seq)
        print("Comparaciones ABB de ROLBOT:", comp_abb)
        print("Comparaciones AVL:", comp_avl)

    print("\nExperimento con insercion ordenada:")
    print("Elementos | Altura ABB | Altura AVL | Comp. ABB | Comp. AVL | Tiempo ABB ms | Tiempo AVL ms")

    for cantidad in (100, 500, 1000, 2000):
        n, ha, hv, ca, cv, ta, tv = realizar_experimento_balanceado(cantidad)
        print(
            f"{n:9} | {ha:10} | {hv:10} | {ca:9} | {cv:9} |"
            f" {ta:13.6f} | {tv:13.6f}"
        )

    print("\nAnalisis teorico:")
    print("- Busqueda secuencial: mejor caso O(1), peor caso O(n).")
    print("- ABB equilibrado: busqueda O(log n); desbalanceado: O(n).")
    print("- AVL: busqueda e insercion O(log n), porque conserva el balance.")
    print("- Las rotaciones del AVL reacomodan nodos sin perder el orden.")
    print("- Heap: construir la estructura cuesta O(n).")
    print("- Heap: extraer el maximo cuesta O(log n).")
    print("- Top-N: construir el heap y extraer N elementos cuesta O(n + N log n).")
    print("- Grafo: lista de adyacencia; recorrer vecinos cuesta O(grado del vertice).")
    print("- Construccion del grafo: se comparan pares de juegos, O(V^2) en esta version.")
    print("- BFS: O(V + E) con lista de adyacencia; encuentra caminos con")
    print("  la menor cantidad de aristas en grafos no ponderados.")
    print("- DFS: O(V + E) con lista de adyacencia; explora cada vertice y")
    print("  arista alcanzable para recorrer la red en profundidad.")
    print("- BFS usa una cola; DFS usa una pila (implementada aqui manualmente).")
    print("\nConclusion: el balance evita que el arbol se convierta en una cadena.")
    print("La cola de prioridad permite obtener los mejores juegos sin ordenar")
    print("todo el conjunto de datos en cada consulta.")


# =========================================================
# MENU PRINCIPAL INTEGRADO
# =========================================================

def menu_principal():
    while True:
        print("""
========================================
                 ROLBOT
========================================
       Descubri tu proximo juego de rol
----------------------------------------
1. Buscar juego y ver sus datos
2. Explorar categorias
3. Ver Top 10
4. Buscar juego mediante el ABB
5. Buscar juego mediante el AVL
6. Obtener recomendaciones
7. Comparar ABB desbalanceado vs AVL
8. Consultar Top-N mediante cola de prioridad
9. Explorar grafo de juegos relacionados
0. Salir y ejecutar analisis de complejidad
----------------------------------------
""")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            nombre = input("Ingrese el nombre del juego: ")
            buscar_por_nombre(nombre)
        elif opcion == "2":
            explorar_categorias()
        elif opcion == "3":
            mostrar_top_10()
        elif opcion == "4":
            buscar_por_arbol()
        elif opcion == "5":
            buscar_por_avl()
        elif opcion == "6":
            recomendar_por_dificultad_y_duracion()
        elif opcion == "7":
            comparar_abb_vs_avl()
        elif opcion == "8":
            consultar_top_n()
        elif opcion == "9":
            explorar_grafo()
        elif opcion == "0":
            print("\nCerrando ROLBOT...")
            analizar_complejidad()
            print("\nGracias por usar ROLBOT.")
            break
        else:
            print("Opcion invalida. Ingrese un numero del menu.")


if __name__ == "__main__":
    menu_principal()