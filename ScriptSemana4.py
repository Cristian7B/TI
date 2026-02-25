import math

simbolosRestaurante = {
    1: "★",  2: "●",  3: "▲",  4: "■",  5: "◆",
    6: "♣",  7: "♠",  8: "♥",  9: "♦", 10: "☀",
    11: "☁", 12: "♫", 13: "☕", 14: "❄", 15: "✿",
    16: "⚡", 17: "☾", 18: "✈", 19: "☘", 20: "♨"
}

def calcularEntropia(mensajes):
    if len(mensajes) == 0:
        return 0.0
    
    frecuencias = {}
    
    for simbolo in mensajes:
        frecuencias[simbolo] = frecuencias.get(simbolo, 0) + 1
    
    H = 0.0
    total = len(mensajes)
    
    for frecuencia in frecuencias.values():
        p = frecuencia / total
        H -= p * math.log2(p)
    
    return H
    
x = int(input("Ingrese el valor de x: "))

print("\nMenú disponible:")
for numero, simbolo in simbolosRestaurante.items():
    print(f"{numero} → {simbolo}")

mensajes = []

for i in range(x):
    eleccion = int(input(f"\nSeleccione símbolo #{i+1}: "))
    
    if eleccion in simbolosRestaurante:
        mensajes.append(simbolosRestaurante[eleccion])
    else:
        print("Número inválido.")
        i -= 1  # opcional si quieres repetir intento

H = calcularEntropia(mensajes)

print("Mensajes generados:", mensajes)
print("Entropía:", round(H, 4), "bits")
