import threading
import random

class Quadrant:
    def __init__(self, dirty, nombre, id):
        self.dirty = False
        self.name = nombre
        self.id = id

class Space:
    def __init__(self):
        self.environment = [[Quadrant for i in range(3)] for j in range(3)]        
        for i in range(3):
            for j in range(3):
                dirty = False
                name = 'cuadrante' + str(i) + '' + str(j)
                id = i * 3 + j
                objeto = Quadrant(dirty, name, id)
                self.environment[i][j] = objeto
        posInit = self.environment[0][0]
        posInit.name = 'AS'
        self.printEnvironment()
                

    def mess(self, col, row):
        element = self.environment[col][row]
        element.name = 'sucio'+ str(col) + '' + str(row)
        element.dirty = True
        self.printEnvironment()
        
    def clean(self, col, row):
        element = self.environment[col][row]
        element.name = 'cd' + str(col) + '' + str(row)
        element.dirty = False
        
    def printEnvironment(self):
        for fila in self.environment:
            print("\n")
            row = ''
            for element in fila:
                row += '   ' + str(element.name)                
            print(row)
        print("\n")

class Hoover(threading.Thread):
    def __init__(self, cuadrantes):
        threading.Thread.__init__(self)        

    def run(self):
        
        while True:
            for cuadrante in space.environment:
                row = space.environment.index(cuadrante)
                for i, element in enumerate(cuadrante):                    
                    if not element.dirty:
                        col = i                        
                        if i >= 2:
                            col = 0
                            if row >= 2:
                                row = 0
                            else:
                                row = row + 1
                        else:
                            col = i+1
                        newPos = space.environment[col][row]
                        newPos.name= 'AS'
                        element.name = 'cuadrante' + str(i) + ''+ str(row)
                        space.printEnvironment()
                        threading.Event().wait(4)
                    else:
                        space.clean(i, row)
                    
            threading.Event().wait(10)

class User(threading.Thread):
    def __init__(self, cuadrantes):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print('Ingresa posicion x Donde quieres ensuciar o salir para terminar:') 
            posX = input()
            
            print('Ingresa posicion y Donde quieres ensuciar o salir para terminar:') 
            posY = input()
        
            space.mess(posX,posY)
            
            threading.Event().wait(3)


space = Space()

hoover = Hoover(space)
user = User(space)


hoover.start()
user.start()

