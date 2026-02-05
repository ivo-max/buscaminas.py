import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def crear_matriz_de_ceros(filas:int, columnas: int) -> list[list[int]]:
    matriz: list[list[int]] = []
    for fila in range(filas):
        filaAux:list[int] = []
        for columna in range(columnas):
            filaAux.append(0)
        matriz.append(filaAux)
    return matriz

def es_matriz (t:list[list[Any]]) -> bool: 
    res: bool = True
    if t == [] or any(fila == [] for fila in t):
        res = False
    else:
        len_de_fila: int = len(t[0])
        for fila in t:
            if len(fila) != len_de_fila:
                res = False
    return res

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    """
    Args:
        filas: es un numero que indica la cantidad de filas deseadas en la matriz
        columnas: es un numero que indica la cantidad de columnas deseadas en la matriz
        minas: es un numero que indica la cantidad de minas deseadas en la matriz
    Return:
        una matriz de 0 y -1 ordenados al azar, usando los parametros para determinar la dimension de la matriz
        y la cantidad de minas
    """
    matriz: list[list[int]] = crear_matriz_de_ceros(filas,columnas)
    posiciones_usadas: list[tuple[int,int]] = []
    while len(posiciones_usadas) < minas:
        fila_random: int = random.randint(0,filas - 1)
        columna_random: int = random.randint(0,columnas - 1)
        if (fila_random,columna_random)  not in posiciones_usadas:
            matriz[fila_random][columna_random] = -1
            posiciones_usadas.append((fila_random,columna_random))
    return matriz

def posiciones_del_tablero (tablero:list[list[int]]) -> list[tuple[int,int]]:
    lista_de_todas_las_posiciones: list[tuple[int,int]] = []
    numero_de_fila: int = 0
    numero_de_columna: int = 0
    for fila in tablero:
        for columna in fila:
            lista_de_todas_las_posiciones.append((numero_de_fila, numero_de_columna))
            numero_de_columna += 1
        numero_de_columna = 0
        numero_de_fila += 1 
    return lista_de_todas_las_posiciones

def posiciones_adyacentes (lista_de_posiciones:list[tuple[int,int]], posicion:tuple[int,int])-> list[tuple[int,int]]:
    posiciones_adyacentes: list[tuple[int,int]] = []
    posibles_posiciones: list[tuple[int,int]] = []
    posicion_fila: int = posicion[0]
    posicion_columna: int = posicion[1]
    for f in range(-1,2):
        for c in range(-1,2):
            if f != 0 or c != 0:
                posibles_posiciones.append((posicion_fila + f, posicion_columna + c))
    for posi in posibles_posiciones:
        if posi in lista_de_posiciones:
            posiciones_adyacentes.append(posi)
    return posiciones_adyacentes

def calcular_numeros(tablero: list[list[int]]):
    """
    Args:
        tablero: es una matriz de enteros
    Return:
        devuelve la misma matriz agregando +1 a los numeros mayores o iguales a 0 
        por cada -1  que tengan en alguna de sus posiciones adyacentes
    """
    posiciones_tablero: list[tuple[int,int]] = posiciones_del_tablero(tablero)
    for posicion in posiciones_tablero:
        if tablero[posicion[0]][posicion[1]] == -1:
            for adyacente in posiciones_adyacentes(posiciones_tablero, posicion):
                if tablero[adyacente[0]][adyacente[1]] != -1:
                    tablero[adyacente[0]][adyacente[1]] += 1
    return

def crear_matriz_de_VACIOS(filas:int, columnas: int) -> list[list[str]]:
    matriz: list[list[str]] = []
    for fila in range(filas):
        filaAux:list[str] = []
        for columna in range(columnas):
            filaAux.append(VACIO)
        matriz.append(filaAux)
    return matriz

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    """
    Args:
        filas: es un numero que indica la cantidad de filas deseadas en el estado de juego
        columnas: es un numero que indica la cantidad de columnas deseadas en el estado de juego 
        minas: es un numero que indica la cantidad de minas deseadas en el estado de juego
    Return:
        devuelve un diccionario con 6 elementos que corresponden a la cantidad de filas, cantidad de columnas,
        cantidad de minas, una matriz de enteros usando las funciones de calcular_numeros y colocar_minas con los 
        parametros de filas, columnas y minas, una matriz de strings que va a funcionar como el tablero visible(se 
        crea con todos elementos VACIOS) y el estado de juego terminado con True si se gano o perdio, en caso contrario False.
    """
    diccionario_estado: EstadoJuego = {}
    diccionario_estado["filas"] = filas
    diccionario_estado["columnas"] = columnas
    diccionario_estado["minas"] = minas
    diccionario_estado["tablero"] = colocar_minas(filas,columnas,minas)
    calcular_numeros(diccionario_estado["tablero"])
    diccionario_estado["tablero_visible"] = crear_matriz_de_VACIOS(filas,columnas)
    diccionario_estado["juego_terminado"] = False
    return diccionario_estado

def  son_matriz_y_misma_dimension( t1: list[list[int]] , t2 : list[list[str]]) -> bool:
    res:bool = False
    filas_t1:int = 0
    columnas_t1:int = 0
    filas_t2:int = 0
    columnas_t2:int = 0
    for fila_t1 in t1:
        for columna_t1 in fila_t1:
            columnas_t1 += 1
        filas_t1 += 1
    for fila_t2 in t2:
        for columna_t2 in fila_t2:
            columnas_t2 += 1
        filas_t2 += 1
    if filas_t2 == filas_t1 and columnas_t1 == columnas_t2 and es_matriz(t1)==True and es_matriz(t2)==True:
        res = True
    return res

def es_entero (num:int) -> bool:
    return num % 1 == 0
       

def  estructura_y_tipos_validos (estado: EstadoJuego) -> bool:
    res: bool = False
    a: bool = estado["filas"] > 0 and es_entero(estado["filas"])
    b: bool = estado["columnas"] > 0 and es_entero(estado["columnas"])
    c: bool = estado["minas"] > 0 and estado["minas"] < (estado["columnas"] *  estado["filas"]) and es_entero(estado["minas"])
    d: bool = estado["juego_terminado"] in (True, False)
    e: bool = es_matriz(estado["tablero"])
    f: bool = es_matriz(estado["tablero_visible"])
    h: bool = len(estado) == 6
    if a and b and c and d and e and f and h:
        res = True
    return res

def estado_valido (estado: EstadoJuego) -> bool:
    res: bool = False
    if estructura_y_tipos_validos(estado):
        minas: int = 0
        for fila in estado["tablero"]:
            for columna in fila:
                if columna == -1:
                    minas += 1
        minas_correctas: bool = minas == estado["minas"]
        tablero_correcto: bool = True
        juego_terminado_correcto: bool = True
        hay_bomba_descubierta: bool = False
        for fila_de_str in estado["tablero_visible"]:
                for stri in fila_de_str:
                    if stri == BOMBA:
                        hay_bomba_descubierta = True
                        if not estado["juego_terminado"]:
                            juego_terminado_correcto = False 
        if estado["juego_terminado"] == True:        
            if todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) != True and hay_bomba_descubierta:
                        juego_terminado_correcto = False
        si_BOMBA_menos1: bool = True
        elems_tablero_visible_correcto: bool = True
        posiciones: list[tuple[int,int]] = posiciones_del_tablero(estado["tablero_visible"])
        for posicion in posiciones:
            if (estado["tablero_visible"])[posicion[0]][posicion[1]] == BOMBA and (estado["tablero"])[posicion[0]][posicion[1]] != -1:
                si_BOMBA_menos1 = False
            if (estado["tablero_visible"])[posicion[0]][posicion[1]] not in (BANDERA,BOMBA,VACIO):
                if str((estado["tablero_visible"])[posicion[0]][posicion[1]]) != str((estado["tablero"])[posicion[0]][posicion[1]]):
                    elems_tablero_visible_correcto = False
        if minas_correctas and tablero_correcto and juego_terminado_correcto and si_BOMBA_menos1 and elems_tablero_visible_correcto:
            res = True
    return res
    
def todas_celdas_seguras_descubiertas (tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    posiciones:list[tuple[int,int]] = posiciones_del_tablero (tablero)
    res: bool = True
    for posicion in posiciones:
        if tablero[posicion[0]][posicion[1]] != -1:
           if tablero_visible[posicion[0]][posicion[1]] != str(tablero[posicion[0]][posicion[1]]):
               res = False
    return res

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]: 
    copia_del_tablero_visible: list[list[str]] = estado["tablero_visible"].copy()
    return copia_del_tablero_visible

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Args:
        estado: es un diccionario con todos los elementos mencionados previamente en la funcion crear_juego
        fila: es un entero que determina una fila de la matriz del "tablero_visible" del estado
        columna: es un entero que determina una columna de la matriz del "tablero_visible" del estado
    Return:
        modifica el estado agregando una bandera en la posicion determinada por la fila y la columnaso quita
        la banndera si ya habia una en esa posicion, todo esto siempre que el juego no haya terminado
    """
    if (estado["juego_terminado"]) == True:
        return estado
    if (estado["tablero_visible"])[fila][columna] == VACIO:
        (estado["tablero_visible"])[fila][columna] = BANDERA
        return estado
    elif (estado["tablero_visible"])[fila][columna] == BANDERA:
        (estado["tablero_visible"])[fila][columna] = VACIO
        return

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Args:
        estado: es un diccionario con todos los elementos mencionados previamente en la funcion crear_juego
        fila: es un entero que determina una fila de la matriz del "tablero_visible" del estado
        columna: es un entero que determina una columna de la matriz del "tablero_visible" del estado
    Return:
        modifica el estado reemplazando en el "tablero_visible", si la posicion dada corresponde a -1 en la "tablero",
        se coloca una BOMBA, si es un numero mayor a 0, devulve el string de ese numero y si es 0, se tienen que desbloquear
        posiciones adyacentes utilizando el mismo concepto
    """
    if estado["juego_terminado"] == True:
        return estado
    if (estado["tablero"])[fila][columna] == -1:
        estado["juego_terminado"] = True
        (estado["tablero_visible"])[fila][columna] = BOMBA
    if (estado["tablero"])[fila][columna] > 0:
        estado["tablero_visible"][fila][columna] = str((estado["tablero"])[fila][columna])
    if (estado["tablero"])[fila][columna] == 0:
       (estado["tablero_visible"]) = caminos_descubiertos(estado["tablero"], estado["tablero_visible"], fila, columna)
    if todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"]):
        estado["juego_terminado"] = True
    return

def caminos_descubiertos (tablero: list[list[int]], tablero_visible: list[list[str]], fila: int, columna: int) -> None:
    posiciones_vistas: list[tuple[int,int]] = []
    posiciones_por_visitar: list[tuple[int,int]] = [(fila,columna)]
    while  len(posiciones_por_visitar) > 0:
        posicion_actual = posiciones_por_visitar[0]
        posiciones_por_visitar.pop(0)
        if posicion_actual not in posiciones_vistas:
            posiciones_vistas.append(posicion_actual)
        valor = tablero[posicion_actual[0]][posicion_actual[1]]
        tablero_visible[posicion_actual[0]][posicion_actual[1]] = str(valor)
        if valor == 0:
            for adya in posiciones_adyacentes(posiciones_del_tablero(tablero), posicion_actual):
                if adya not in posiciones_por_visitar and adya not in posiciones_vistas:
                    if tablero_visible[adya[0]][adya[1]] != BANDERA:
                        posiciones_por_visitar.append(adya)
    return tablero_visible

def verificar_victoria(estado: EstadoJuego) -> bool:
    """
    Verifica si se cumple que todas las celdas seguras fueron descubiertas, oseas todas las posiciones de
    "tablero" diferentes a -1 fueron descubiertas
    Args:
        estado: recibe un diccionario con los elementos mencionados previamente
    Return:
        devulve True si se cumple que todas las celdas seguras fueron descubiertas, en caso contrario False
    """
    return todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"])

def reiniciar_juego(estado: EstadoJuego) -> None:
    """
    Args:
        estado: recibe un diccionario con los elementos mencionados previamente
    Return:
        modifica el estado recibido al cambiar el elemento de "tablero", creando uno diferente random nuevo,
        a "tablero_visible" se reinicia colocando todos valores de VACIO, y se determina que el "juego_terminado
        es False.
    """
    estado["columnas"] = estado["columnas"]
    estado["filas"] = estado["filas"]
    estado["minas"] = estado["minas"]
    tablero: list[list[int]] = (crear_juego(estado["filas"], estado["columnas"],estado["minas"]))["tablero"]
    while tablero == estado["tablero"]:
        tablero = (crear_juego(estado["filas"], estado["columnas"],estado["minas"]))["tablero"]
    estado["tablero"] = tablero
    estado["tablero_visible"] = crear_matriz_de_VACIOS(estado["filas"], estado["columnas"])
    estado["juego_terminado"] = False
    return
    

def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """
    Args:
        estado: recibe un diccionario con los elementos mencionados previamente
        ruta_directorio: una ruta existente en el equipo
    Return:
        genera 2 arhivos en la ruta_directorio, "tablero" y "tablero_visible", en el primero se guardan todos los numeros
        correspondintes a el elemento de estado de "tablero" ,y el segundo toma los valores del estado
        de "tablero_visible", reemplaza los VACIOS por ? , las BANDERA por * y agrega los valores de los strings de numeros
        al segundo archivo, todo separado por comas y con separacion entre lineas
    """
    filas = estado["filas"]
    columnas = estado["columnas"]
    tablero = estado["tablero"]
    tablero_visible = estado["tablero_visible"]
    direc_tablero = os.path.join(ruta_directorio, "tablero.txt")
    direc_tablero_visible = os.path.join(ruta_directorio, "tablero_visible.txt")
    archivo_tablero = open(direc_tablero, 'w')
    for i in range(filas):
        linea:str = ""
        for c in range(columnas):
            elemento:str = str(tablero[i][c])
            linea += elemento
            if c != (columnas - 1):
                linea += ","
        archivo_tablero.write(linea + '\n')
    archivo_tablero.close()
    archivo_tablero_visible = open(direc_tablero_visible, 'w')
    for fila in range(filas):
        linea_visible:str = ""
        for columna in range(columnas):
            elemento_visible = tablero_visible[fila][columna]
            if elemento_visible == BANDERA:
                linea_visible += "*"
            if elemento_visible == VACIO:
                    linea_visible += "?"
            if elemento_visible in ("0","1","2","3","4","5","6","7","8"):
                linea_visible += elemento_visible
            if columna != (columnas - 1):
                    linea_visible += ","
        archivo_tablero_visible.write(linea_visible + '\n')
    archivo_tablero_visible.close()
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:

    """
    Args:
        estado: recibe un diccionario con los elementos mencionados previamente aunque no importan ya que es una variable out
        ruta_directorio: una ruta existente en el equipo
    Return:
        toma 2 archivos "tablero" y "tablero_visible" y hace la funcion guardar estado a la inversa; el primero quita todas las
        comas y lo devuelve en formato de matriz que va a pasar a ser el estado de "tablero", y el segundo reemplaza * por BANDERA,
        ? por VACIO y quita las comas y devulve otra matrsi que va a ser el estado de "tablero_visible"
    """
    if existe_archivo(ruta_directorio, "tablero.txt") == True and existe_archivo(ruta_directorio, "tablero_visible.txt") == True:
        direc_tablero = os.path.join(ruta_directorio, "tablero.txt")
        direc_tablero_visible = os.path.join(ruta_directorio, "tablero_visible.txt")
        
        archivo_tablero = open(direc_tablero, 'r')
        valores_posibles_tablero = ["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8"]
        minas:int = 0
        lineas_tablero:list = archivo_tablero.readlines()
        elementos_tablero:list[list[int]] = []
        for linea in lineas_tablero:
            fila:list[int] = []
            numero:str = ""
            for caracter in linea:
                numero += str(caracter)
                if numero in valores_posibles_tablero:
                    if numero == "-1":
                        minas += 1
                    fila.append(int(numero))
                    numero = ""
                elif numero != "-":
                    numero = ""
            elementos_tablero.append(fila)
        archivo_tablero.close()

        archivo_tablero_visible = open(direc_tablero_visible, 'r')
        valores_posibles_tablero_visible = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        lineas_tablero_visible:list = archivo_tablero_visible.readlines()
        elementos_tablero_visible:list[list] = []
        for linea_visible in lineas_tablero_visible:
            fila_visible:list = []
            numero_visible:str = ""
            for caracter_visible in linea_visible:
                numero_visible += str(caracter_visible)
                if numero_visible in valores_posibles_tablero_visible:
                    fila_visible.append(numero_visible)
                    numero_visible = ""
                elif numero_visible == "?":
                    fila_visible.append(VACIO)
                    numero_visible = ""
                elif numero_visible == "*":
                    fila_visible.append(BANDERA)
                    numero_visible = ""
                else:
                    numero_visible = ""
            elementos_tablero_visible.append(fila_visible)
        archivo_tablero_visible.close()

        estado["filas"] = len(elementos_tablero)
        estado["columnas"] = len(fila)
        estado["minas"] = minas
        estado["juego_terminado"] = False
        estado["tablero"] = elementos_tablero
        estado["tablero_visible"] = elementos_tablero_visible

        if minas > 0 and verificar_victoria(estado) == False and estado_valido(estado) == True:                    
            return True
    else:
        return False


