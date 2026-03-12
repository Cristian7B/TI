import heapq
import math

# Esta clase nos ayudará a construir los códigos uniendo las probabilidades menores
class Nodo:
    def __init__(self, prob, simbolo, izq=None, der=None):
        self.prob = prob
        self.simbolo = simbolo
        self.izq = izq
        self.der = der
        self.direccion = '' # Guardará '0' o '1'

    def __lt__(self, otro):
        return self.prob < otro.prob

# Función recursiva para recorrer el árbol y asignar los 0s y 1s
def generarCodigos(nodo, codigo_actual='', diccionario_codigos=None):
    if diccionario_codigos is None:
        diccionario_codigos = {}
        
    nuevo_codigo = codigo_actual + str(nodo.direccion)
    
    if nodo.izq:
        generarCodigos(nodo.izq, nuevo_codigo, diccionario_codigos)
    if nodo.der:
        generarCodigos(nodo.der, nuevo_codigo, diccionario_codigos)
        
    # Si es un nodo hoja (tiene un símbolo), guardamos el código
    if not nodo.izq and not nodo.der:
        diccionario_codigos[nodo.simbolo] = nuevo_codigo
        
    return diccionario_codigos

# --- FUNCIÓN PRINCIPAL DEL DIAGRAMA ---
def codificarFuente(simbolos_probabilidades):
    print("--- INICIANDO ALGORITMO ---")
    
    # 1. Inputs
    simbolos = list(simbolos_probabilidades.keys())
    probabilidades = list(simbolos_probabilidades.values())
    
    # Validar que la suma de probabilidades sea 1 (con un pequeño margen de error por los decimales)
    suma_probs = sum(probabilidades)
    if not math.isclose(suma_probs, 1.0, abs_tol=1e-5):
        print(f"Error: Las probabilidades deben sumar 1. Suma actual: {suma_probs}")
        return

    # 2. Análisis de Equiprobabilidad
    es_equiprobable = all(math.isclose(p, probabilidades[0], abs_tol=1e-5) for p in probabilidades)
    if es_equiprobable:
        print("-> Análisis: Los símbolos SON equiprobables.")
    else:
        print("-> Análisis: Los símbolos NO son equiprobables. Se requiere codificación de longitud variable.")

    # 3. Verificar si son probabilidades díadas (potencias negativas de 2, ej. 0.5, 0.25)
    son_diadas = all(math.log2(p).is_integer() for p in probabilidades if p > 0)
    if son_diadas:
        print("-> Nota: Las probabilidades son díadas. ¡Se espera una eficiencia teórica del 100%!")

    """
    4. Construir el árbol para generar los códigos (La parte central de la imagen)
    Ordenar de mayor a menor probabilidad está implícito en el uso de la cola de prioridad (heap)
    Usamos un árbol y asignams de abajo hacia arriba, abajo se encuentran los nodos con mayor probabilidad, 
    nodos que deberan tener la menor cantidad de digitos
    """ 
    nodos = [Nodo(prob, sim) for sim, prob in simbolos_probabilidades.items()]
    heapq.heapify(nodos)
    while len(nodos) > 1:
        izq = heapq.heappop(nodos)
        der = heapq.heappop(nodos)
        
        izq.direccion = '0'
        der.direccion = '1'
        
        nuevo_nodo = Nodo(izq.prob + der.prob, izq.simbolo + der.simbolo, izq, der)
        heapq.heappush(nodos, nuevo_nodo)
        
    raiz = nodos[0]
    codigos = generarCodigos(raiz)

    # 5. Calcular Eficiencia y Redundancia (Outputs)
    entropia = sum(-p * math.log2(p) for p in probabilidades if p > 0)
    longitud_media = sum(simbolos_probabilidades[sim] * len(codigo) for sim, codigo in codigos.items())
    
    eficiencia = (entropia / longitud_media) * 100
    redundancia = 100 - eficiencia

    # --- OUTPUTS ---
    print("\n--- OUTPUTS (RESULTADOS) ---")
    print("Símbolo\tProbabilidad\tCódigo\tLongitud")
    print("-" * 45)
    # Mostramos los resultados ordenados de mayor a menor probabilidad como pide la imagen
    por_prob_descendente = sorted(simbolos_probabilidades.items(), key=lambda x: x[1], reverse=True)
    for sim, prob in por_prob_descendente:
        print(f"{sim}\t{prob:.4f}\t\t{codigos[sim]}\t{len(codigos[sim])} bits")
        
    print("-" * 45)
    print(f"Entropía (H): \t\t{entropia:.4f} bits/símbolo")
    print(f"Longitud Media (L): \t{longitud_media:.4f} bits/símbolo")
    print(f"Eficiencia: \t\t{eficiencia:.2f}%")
    print(f"Redundancia: \t\t{redundancia:.2f}%")


# ==========================================
# CASO DE PRUEBA
# ==========================================
if __name__ == "__main__":
    datos_entrada = {
        'A': 0.2,
        'B': 0.2,
        'C': 0.2,
        'D': 0.2,
        '1': 0.2
    }
    
    codificarFuente(datos_entrada)
