import unittest
import os
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,son_matriz_y_misma_dimension,estado_valido, es_matriz,
                               reiniciar_juego, caminos_descubiertos, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)



class es_matrizTest(unittest.TestCase):
    def test_ejemplo(self):
        a = []
        b = [[1,2],[3]]
        self.assertFalse(es_matriz(a))
        self.assertFalse(es_matriz(b))

class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0,-1]]

        calcular_numeros(tablero)
        self.assertEqual(tablero, [[2,-1],
                                   [2,-1]])

class estado_validoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado : EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, 1],
                [1, -1]
            ],
            'tablero_visible': [
                [BOMBA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True
        }
        self.assertFalse(estado_valido(estado))

        estado["juego_terminado"] = False
        self.assertFalse(estado_valido(estado))

        estado["tablero_visible"] = [[VACIO,VACIO],
                                     ["2", VACIO]]
        self.assertFalse(estado_valido(estado))
        
        
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False }
        self.assertTrue(estado_valido(estado))
        
        estado['columnas'] = 1.2
        self.assertFalse(estado_valido(estado))

class son_matriz_y_misma_dimensionTest(unittest.TestCase):
    def test_ejemplo(self):
        a = [[1,2],[3,4]]
        b = [[4,3],[2,1]]
        c = [[1,2],[1]]
        d = []
        self.assertTrue(son_matriz_y_misma_dimension(a,b))
        self.assertFalse(son_matriz_y_misma_dimension(b,c))
        self.assertFalse(son_matriz_y_misma_dimension(d,b))


class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False


        }
        #t###esteamos que si ya hay bandera, devuleve vacio
        marcar_celda(estado,0,0)
        self.assertEqual(estado['tablero_visible'],
            [[VACIO, VACIO],
            [VACIO, VACIO]])
        
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado["tablero_visible"], [[BANDERA, VACIO],
                [VACIO, VACIO]])
        
       
        ####testeamos que si el juego se termino
        estado["tablero_visible"] = [[BOMBA, VACIO],
                                     [VACIO, VACIO]]
        estado["juego_terminado"] = True
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado["tablero_visible"],
                                    [[BOMBA, VACIO],
                                    [VACIO, VACIO]])
        estado['juego_terminado'] = False
        estado["tablero_visible"] = [[VACIO, VACIO],
                                     ["1", VACIO]]
        marcar_celda(estado, 1, 0)
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],
                                                    ["1", VACIO]])


class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        descubrir_celda(estado,0,2)
        descubrir_celda(estado,2,0)

        
        #si se elije una bomba
        self.assertTrue(estado["juego_terminado"])
        self.assertEqual(estado["tablero_visible"],[[VACIO, VACIO, "1"],
            [VACIO, "3", "1"],
            [BOMBA, "2", "0"]])
        estado["juego_terminado"] = True
        self.assertEqual(descubrir_celda(estado,0,0), estado) 

        estado2: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, "1"],
                [VACIO, "3", "1"],
                [VACIO, "2", "0"]
            ],
            'juego_terminado': False }
        
        descubrir_celda(estado2, 0, 0)
        self.assertTrue(estado["juego_terminado"])

        estado5: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [0, 1, -1, 1, 1],
                [1, 2, 1, 2, 1],
                [-1, 1, 0, 1, -1],
                [1, 2, 1, 2, 1],
                [0, 1, -1, 1, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO]],
            'juego_terminado': False }
        
        descubrir_celda(estado5, 2, 2)
        self.assertEqual(estado5["tablero_visible"],[
                [VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, "2", "1", "2", VACIO],
                [VACIO, "1", "0", "1", VACIO],
                [VACIO, "2", "1", "2", VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO]] )
        
        estado4: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False }
        
        descubrir_celda(estado4, 1, 1)
        self.assertEqual(estado4["tablero_visible"],[["1", "1", "1"],
                                                    ["1", "0", "1"],
                                                    ["1", "1", "1"]] )

class caminos_descubiertosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero:list[list[int]] = [
            [0, 0, 0, 0], 
            [0, 0, 0, 0], 
            [1, 1, 0, 0], 
            [-1, 1, 0, 0]]
        tablero_visible:list[list[str]] = [
            [VACIO, VACIO, VACIO, VACIO], 
            [VACIO, VACIO, BANDERA, VACIO], 
            [VACIO, VACIO, VACIO, VACIO], 
            [VACIO, VACIO, VACIO, VACIO]]
        fila = 0
        columna = 3

        caminos_descubiertos(tablero, tablero_visible, fila, columna)
        self.assertEqual(tablero_visible,
                        [["0", "0", "0", "0"], 
                        ["0", "0", BANDERA, "0"], 
                        ["1", "1", "0", "0"], 
                        [VACIO, "1", "0", "0"]])


class guardar_estadoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1],
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                ["1", "1"],
                
            ],
            'juego_terminado': False }
        ruta ="carpeta_test_1_guardar_estado"
        guardar_estado(estado, ruta)
        self.assertTrue(os.path.exists(os.path.join(ruta, "tablero.txt")))
        self.assertTrue(os.path.exists(os.path.join(ruta, "tablero_visible.txt")))

       
class cargar_estadoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado : EstadoJuego = {}
        ruta_inv = "ruta_invalida"
        res: bool = cargar_estado(estado, ruta_inv)
        self.assertFalse(res)

        ruta = "carpeta_test_2_cargar_estado"

        x = open(os.path.join(ruta,"tablero.txt"), "w")
        x.write ("0,2,1\n1,2,0\n0,1,1\n")
        x.close()

        y = open(os.path.join(ruta,"tablero_visible.txt"), "w")
        y.write("*,2,1\n1,2,*\n?,?,?\n")
        y.close()
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1],
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                ["1", "1"],
                
            ],
            'juego_terminado': False }
        res:bool = cargar_estado(estado, ruta)
        self.assertFalse(res)

        f = open(os.path.join(ruta,"tablero.txt"), "w")
        f.write ("-1,2,1\n1,2,-1\n0,1,1\n")
        f.close()

        g = open(os.path.join(ruta,"tablero_visible.txt"), "w")
        g.write("*,2,1\n1,2,*\n?,?,?\n")
        g.close()
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1],
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                ["1", "1"],
                
            ],
            'juego_terminado': False }
        res: bool = cargar_estado(estado, ruta)
        self.assertTrue(res)
        self.assertEqual(estado["filas"],3)
        self.assertEqual(estado["columnas"], 3)
        self.assertEqual(estado["minas"], 2)
        self.assertFalse(estado["juego_terminado"])
        self.assertEqual(estado["tablero"], [[-1, 2, 1],
                                             [1, 2, -1],
                                             [0, 1, 1]])
        self.assertEqual(estado["tablero_visible"], [[BANDERA, "2", "1"],
                                                     ["1","2", BANDERA],
                                                     [VACIO, VACIO, VACIO]])


if __name__ == '__main__':
 unittest.main(verbosity=2)

