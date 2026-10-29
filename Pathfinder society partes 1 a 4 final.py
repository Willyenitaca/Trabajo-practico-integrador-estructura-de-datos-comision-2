# -*- coding: utf-8 -*-
"""
TRABAJO PRACTICO INTEGRADOR
ROLBOT - Descubri tu proximo juego de rol

Partes integradas:
1. Carga de datos y clase Juego.
2. Busqueda secuencial y analisis de complejidad.
3. Arbol binario de busqueda (ABB).
4. Arbol AVL, rotaciones y comparacion con el ABB desbalanceado.
"""

import time
import pandas as pd


# =========================================================
# PARTE 1: CARGA DE DATOS Y CLASE JUEGO
# =========================================================

juegos = pd.read_csv("rolbot_juegos_200.csv")


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


def mostrar_top_10():
    top_10 = juegos.sort_values("popularidad", ascending=False).head(10)
    print("\nTOP 10 JUEGOS POR POPULARIDAD")
    print(top_10[["juego", "popularidad"]].to_string(index=False))


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
    print("\nConclusion: el balance evita que el arbol se convierta en una cadena.")


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
0. Salir y ejecutar analisis de complejidad
----------------------------------------
""")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            nombre = input("Ingrese el nombre del juego: ")
            buscar_por_nombre(nombre)
        elif opcion == "2":
            print("\nGeneros disponibles:")
            print(sorted(juegos["genero"].dropna().astype(str).unique()))
            genero = input("Ingrese el genero: ")
            filtrar_por_genero(genero)
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
        elif opcion == "0":
            print("\nCerrando ROLBOT...")
            analizar_complejidad()
            print("\nGracias por usar ROLBOT.")
            break
        else:
            print("Opcion invalida. Ingrese un numero del menu.")


if __name__ == "__main__":
    menu_principal()
