
# -*- coding: utf-8 -*-
"""
TRABAJO PRÁCTICO INTEGRADOR
ROLBOT - Descubrí tu próximo juego de rol

Parte 1: Carga de datos
Parte 2: Búsqueda y análisis de complejidad
Parte 3: Árbol binario de búsqueda
"""

import pandas as pd
import time


# ==========================================
# PARTE 1 - CARGA DE DATOS
# ==========================================

juegos = pd.read_csv("rolbot_juegos_200.csv")


# ==========================================
# PARTE 2 - CLASE JUEGO
# ==========================================

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


# ==========================================
# FUNCIONES DE BÚSQUEDA Y FILTRADO
# ==========================================

def buscar_por_nombre(nombre):

    resultado = juegos[
        juegos["juego"].str.casefold() == nombre.strip().casefold()
    ]

    if resultado.empty:
        print("No se encontró el juego.")
    else:
        print(resultado.to_string(index=False))


def listar_juegos():

    print(juegos["juego"].to_string(index=False))


def filtrar_por_genero(genero):

    resultado = juegos[
        juegos["genero"].str.casefold() == genero.strip().casefold()
    ]

    if resultado.empty:
        print("No se encontraron juegos de ese género.")
    else:
        print(resultado.to_string(index=False))


# ==========================================
# PARTE 3 - NODO DEL ÁRBOL
# ==========================================

class Nodo:

    def __init__(self, valor):

        self.valor = valor
        self.izquierda = None
        self.derecha = None


# ==========================================
# PARTE 3 - ÁRBOL BINARIO DE BÚSQUEDA
# La clave de ordenamiento es el nombre del juego.
# ==========================================

class ArbolBusqueda:

    def __init__(self):

        self.raiz = None

    def insertar(self, valor):

        nuevo = Nodo(valor)

        if self.raiz is None:
            self.raiz = nuevo
            return

        actual = self.raiz

        while True:

            if valor.casefold() < actual.valor.casefold():

                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return

                actual = actual.izquierda

            elif valor.casefold() > actual.valor.casefold():

                if actual.derecha is None:
                    actual.derecha = nuevo
                    return

                actual = actual.derecha

            else:
                # Evitamos insertar nombres duplicados.
                return

    def buscar(self, nombre):

        actual = self.raiz
        comparaciones = 0
        nombre = nombre.strip().casefold()

        while actual is not None:

            comparaciones += 1
            valor_actual = actual.valor.casefold()

            if nombre == valor_actual:
                return actual.valor, comparaciones

            elif nombre < valor_actual:
                actual = actual.izquierda

            else:
                actual = actual.derecha

        return None, comparaciones

    # Recorrido inorder: izquierda, raíz, derecha.
    def inorder(self, nodo):

        if nodo is not None:
            self.inorder(nodo.izquierda)
            print(nodo.valor)
            self.inorder(nodo.derecha)

    # Recorrido preorder: raíz, izquierda, derecha.
    def preorder(self, nodo):

        if nodo is not None:
            print(nodo.valor)
            self.preorder(nodo.izquierda)
            self.preorder(nodo.derecha)

    # Recorrido postorder: izquierda, derecha, raíz.
    def postorder(self, nodo):

        if nodo is not None:
            self.postorder(nodo.izquierda)
            self.postorder(nodo.derecha)
            print(nodo.valor)


# ==========================================
# CARGAR UN ÁRBOL BALANCEADO
# Los datos deben estar ordenados previamente.
# ==========================================

def cargar_arbol_balanceado(arbol, datos):

    if len(datos) == 0:
        return

    medio = len(datos) // 2

    arbol.insertar(datos[medio])

    cargar_arbol_balanceado(arbol, datos[:medio])
    cargar_arbol_balanceado(arbol, datos[medio + 1:])


# ==========================================
# CONSTRUIR EL ÁRBOL CON LOS JUEGOS REALES
# ==========================================

datos_reales = sorted(
    juegos["juego"].dropna().astype(str).tolist(),
    key=str.casefold
)

arbol_real = ArbolBusqueda()

cargar_arbol_balanceado(arbol_real, datos_reales)


# ==========================================
# FUNCIONES QUE UTILIZA EL MENÚ
# ==========================================

def buscar_en_arbol(nombre):

    resultado, comparaciones = arbol_real.buscar(nombre)

    if resultado is not None:

        print("\n¡Juego encontrado!")

        # Buscamos los datos completos del juego en el CSV.
        datos_juego = juegos[
            juegos["juego"].str.casefold()
            == resultado.casefold()
        ]

        print(datos_juego.to_string(index=False))

    else:

        print("\nNo se encontró el juego:", nombre)

    print("\nComparaciones realizadas en el árbol:", comparaciones)


def mostrar_top_10():

    print("\nTOP 10 JUEGOS")

    top_10 = juegos.sort_values(
        "popularidad",
        ascending=False
    ).head(10)

    print(top_10[["juego", "popularidad"]].to_string(index=False))


def mostrar_juegos_relacionados():

    genero = input("Ingrese el género: ")
    filtrar_por_genero(genero)


def mostrar_recomendaciones():

    dificultad = input("Ingrese una dificultad: ")

    resultado = juegos[
        juegos["dificultad"].str.casefold()
        == dificultad.strip().casefold()
    ]

    if resultado.empty:
        print("No se encontraron juegos con esa dificultad.")
    else:
        print(
            resultado[
                ["juego", "genero", "dificultad", "duracion"]
            ].to_string(index=False)
        )


def recorrer_arbol():

    print("\nTIPO DE RECORRIDO")
    print("1. Inorder (orden alfabético)")
    print("2. Preorden")
    print("3. Postorden")

    opcion_recorrido = input("Opción: ").strip()

    if opcion_recorrido == "1":
        print("\nJUEGOS ORDENADOS ALFABÉTICAMENTE")
        arbol_real.inorder(arbol_real.raiz)

    elif opcion_recorrido == "2":
        print("\nRECORRIDO PREORDEN")
        arbol_real.preorder(arbol_real.raiz)

    elif opcion_recorrido == "3":
        print("\nRECORRIDO POSTORDEN")
        arbol_real.postorder(arbol_real.raiz)

    else:
        print("Opción de recorrido inválida.")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def ejecutar_menu():

    while True:

        print("""
========================================
               ROLBOT
========================================
      Descubrí tu próximo juego de rol
----------------------------------------

1. Buscar juego
2. Explorar categorías
3. Ver Top 10
4. Ver juegos relacionados
5. Obtener recomendaciones
6. Recorrer el árbol

0. Salir y ejecutar análisis de complejidad

----------------------------------------
""")

        opcion = input("Opción: ").strip()

        if opcion == "1":

            nombre = input("Ingrese el nombre del juego: ")
            buscar_en_arbol(nombre)

        elif opcion == "2":

            print("\nGÉNEROS DISPONIBLES:")
            generos = sorted(
                juegos["genero"].dropna().astype(str).unique()
            )
            print(", ".join(generos))

            genero = input("Ingrese el género: ")
            filtrar_por_genero(genero)

        elif opcion == "3":

            mostrar_top_10()

        elif opcion == "4":

            mostrar_juegos_relacionados()

        elif opcion == "5":

            mostrar_recomendaciones()

        elif opcion == "6":

            recorrer_arbol()

        elif opcion == "0":

            print("¡Hasta luego!")
            break

        else:

            print("Opción inválida. Intentá nuevamente.")


# ==========================================
# PARTE 2 - BÚSQUEDA SECUENCIAL
# ==========================================

def busqueda_secuencial(nombre, datos):

    comparaciones = 0
    nombre_buscado = nombre.strip().casefold()

    for juego in datos:

        comparaciones += 1

        if str(juego).casefold() == nombre_buscado:
            return juego, comparaciones

    return None, comparaciones


# ==========================================
# COMPARAR BÚSQUEDAS CON DATOS REALES
# ==========================================

def comparar_busquedas_reales():

    if not datos_reales:
        print("No hay juegos cargados.")
        return

    juego_buscado = datos_reales[-1]

    resultado_secuencial, comparaciones_secuencial = (
        busqueda_secuencial(juego_buscado, datos_reales)
    )

    resultado_arbol, comparaciones_arbol = (
        arbol_real.buscar(juego_buscado)
    )

    print("\n========================================")
    print(" COMPARACIÓN CON DATOS REALES DE ROLBOT")
    print("========================================")

    print("Cantidad de juegos:", len(datos_reales))
    print("Juego buscado:", juego_buscado)

    print("\nBÚSQUEDA SECUENCIAL")
    print("Resultado:", resultado_secuencial)
    print("Comparaciones:", comparaciones_secuencial)

    print("\nÁRBOL BALANCEADO")
    print("Resultado:", resultado_arbol)
    print("Comparaciones:", comparaciones_arbol)


# ==========================================
# EXPERIMENTO DE COMPLEJIDAD
# ==========================================

def realizar_experimento(cantidad):

    datos = [
        f"Juego {i:06d}"
        for i in range(cantidad)
    ]

    datos_ordenados = sorted(datos, key=str.casefold)

    arbol = ArbolBusqueda()

    cargar_arbol_balanceado(arbol, datos_ordenados)

    # Elegimos el último elemento para exigirle más
    # trabajo a la búsqueda secuencial.
    juego_buscado = datos[-1]

    inicio = time.perf_counter()

    resultado_secuencial, comparaciones_secuencial = (
        busqueda_secuencial(juego_buscado, datos)
    )

    tiempo_secuencial = (
        time.perf_counter() - inicio
    ) * 1000

    inicio = time.perf_counter()

    resultado_arbol, comparaciones_arbol = (
        arbol.buscar(juego_buscado)
    )

    tiempo_arbol = (
        time.perf_counter() - inicio
    ) * 1000

    return (
        cantidad,
        comparaciones_secuencial,
        comparaciones_arbol,
        tiempo_secuencial,
        tiempo_arbol
    )


# ==========================================
# EJECUTAR ANÁLISIS DE COMPLEJIDAD
# ==========================================

def ejecutar_analisis_complejidad():

    comparar_busquedas_reales()

    print("\n========================================")
    print("       RESULTADOS DEL EXPERIMENTO")
    print("========================================")

    resultados = []

    resultados.append(realizar_experimento(100))
    resultados.append(realizar_experimento(1000))
    resultados.append(realizar_experimento(10000))
    resultados.append(realizar_experimento(100000))

    for resultado in resultados:

        cantidad = resultado[0]
        comparaciones_secuencial = resultado[1]
        comparaciones_arbol = resultado[2]
        tiempo_secuencial = resultado[3]
        tiempo_arbol = resultado[4]

        print("\nCantidad de elementos:", cantidad)

        print("Búsqueda secuencial:")
        print("  Comparaciones:", comparaciones_secuencial)
        print("  Tiempo:", round(tiempo_secuencial, 6), "ms")

        print("Árbol balanceado:")
        print("  Comparaciones:", comparaciones_arbol)
        print("  Tiempo:", round(tiempo_arbol, 6), "ms")

        print("----------------------------------------")

    print("\n========================================")
    print("       ANÁLISIS DE COMPLEJIDAD")
    print("========================================")

    print("\nBÚSQUEDA SECUENCIAL")
    print("Mejor caso: Ω(1)")
    print("Peor caso: O(n)")
    print("Caso promedio: Θ(n), bajo el supuesto usual de búsqueda.")

    print("\nÁRBOL BINARIO DE BÚSQUEDA BALANCEADO")
    print("Mejor caso: Ω(1)")
    print("Peor caso: O(log n), si se mantiene balanceado.")
    print("Un ABB no balanceado puede llegar a O(n).")

    print("\n========================================")
    print("             CONCLUSIÓN")
    print("========================================")

    print("Se compararon dos estrategias de búsqueda en ROLBOT.")
    print("La búsqueda secuencial revisa los juegos uno por uno.")
    print("El árbol balanceado permite descartar gran parte")
    print("de los elementos en cada comparación.")
    print("Los tiempos pueden variar según el equipo y la ejecución.")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":

    ejecutar_menu()
    ejecutar_analisis_complejidad()
