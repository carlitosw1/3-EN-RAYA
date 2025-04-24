import json
import os

print("BIENVENIDOS AL JUEGO 3 EN RAYA")

RANKING_FILE = "ranking.json"

def limpiar_pantalla():
    print("\n" * 50)

def mostrar_tablero(tablero):
    print("   1   2   3")
    for i, fila in enumerate(tablero):
        fila_str = " | ".join(fila)
        print(f"{i + 1}  {fila_str}")
        if i < 2:
            print("  ---+---+---")

def verificar_ganador(tablero, simbolo):
    for i in range(3):
        if all([casilla == simbolo for casilla in tablero[i]]) or \
           all([tablero[j][i] == simbolo for j in range(3)]):
            return True
    if all([tablero[i][i] == simbolo for i in range(3)]) or \
       all([tablero[i][2 - i] == simbolo for i in range(3)]):
        return True
    return False

def tablero_lleno(tablero):
    return all(casilla != " " for fila in tablero for casilla in fila)

def obtener_posicion(tablero):
    while True:
        try:
            fila = int(input("Fila (1, 2, 3): ")) - 1
            col = int(input("Columna (1, 2, 3): ")) - 1
            if tablero[fila][col] == " ":
                return fila, col
            else:
                print("Casilla ocupada.")
        except (ValueError, IndexError):
            print("Entrada inválida.")

def registrar_jugadores():
    jugadores = cargar_ranking()
    print("=== Registro de todos los jugadores ===")
    while True:
        nombre = input("Ingresa nombre (o escribe 'fin' para terminar): ").strip()
        if nombre.lower() == 'fin':
            if len(jugadores) >= 2:
                break
            else:
                print("Necesitas al menos 2 jugadores.")
                continue
        if nombre.lower() in (n.lower() for n in jugadores):
            print("Ese nombre ya está registrado. Elige otro.")
        else:
            jugadores[nombre] = jugadores.get(nombre, 0)
    guardar_ranking(jugadores)
    return jugadores

def elegir_jugadores(jugadores):
    nombres = list(jugadores.keys())
    while True:
        print("=== Jugadores disponibles ===")
        for idx, nombre in enumerate(nombres):
            print(f"{idx + 1}. {nombre}")
        try:
            p1 = int(input("Jugador 1 (elige número): ")) - 1
            p2 = int(input("Jugador 2 (elige número): ")) - 1
            if p1 == p2:
                print("Deben ser jugadores distintos.")
            elif 0 <= p1 < len(nombres) and 0 <= p2 < len(nombres):
                return nombres[p1], nombres[p2]
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

def mostrar_ranking(jugadores):
    print("\n=== 🏆 Ranking de jugadores 🏆 ===")
    ranking = sorted(jugadores.items(), key=lambda x: x[1], reverse=True)
    for nombre, puntos in ranking:
        print(f"{nombre}: {puntos} puntos")
    print()

def jugar_ronda(jugador1, jugador2, jugadores):
    simbolos = {jugador1: "X", jugador2: "O"}
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    turno = jugador1

    limpiar_pantalla()
    print(f"{jugador1} (X) vs {jugador2} (O)\n")

    while True:
        print(f"Turno de {turno} ({simbolos[turno]})")
        mostrar_tablero(tablero)
        fila, col = obtener_posicion(tablero)
        tablero[fila][col] = simbolos[turno]

        if verificar_ganador(tablero, simbolos[turno]):
            limpiar_pantalla()
            print(f"¡{turno} ha ganado esta ronda!\n")
            jugadores[turno] += 1
            guardar_ranking(jugadores)
            mostrar_tablero(tablero)
            break
        elif tablero_lleno(tablero):
            limpiar_pantalla()
            print("¡Empate!\n")
            mostrar_tablero(tablero)
            break

        turno = jugador1 if turno == jugador2 else jugador2
        limpiar_pantalla()

def cargar_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_ranking(jugadores):
    with open(RANKING_FILE, "w") as f:
        json.dump(jugadores, f)

def menu_principal():
    jugadores = registrar_jugadores()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ver ranking")
        print("2. Jugar nueva ronda")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_ranking(jugadores)
        elif opcion == "2":
            jugador1, jugador2 = elegir_jugadores(jugadores)
            jugar_ronda(jugador1, jugador2, jugadores)
        elif opcion == "3":
            print("¡Gracias por jugar! 🕹️")
            break
        else:
            print("Opción no válida.")

menu_principal()