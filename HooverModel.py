import threading

class State:
    def __init__(self, action, id):
        self.action = action
        self.id = id

class Rule:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        
class Model:
    def __init__(self, state,  action, perception):
        self.perception = perception
        self.state = state
        self.action = action

class Quadrant:
    def __init__(self, dirty, nombre, id):
        self.dirty = dirty
        self.name = nombre
        self.id = id
        self.side = 10;
        
    

class Space:
    def __init__(self):
        self.lado = 10
        self.environment = []
        self.environment.append(Quadrant( "limpio", "c1", 0))
        self.environment.append(Quadrant( "limpio", 'c2', 1))      

        self.perception = 'espera'
        self.quadrant = 0
        self.state = []        
        self.state.append(State( 'espera', 0))
        self.state.append(State( 'c1', 1))  
        self.state.append(State( 'c2', 2))
        #self.state.append(State( 'aspirar', 3))
        self.state.append(State( 'sucio', 3))
        self.state.append(State( 'limpio', 4))
        #self.state.append(State( 'scanear', 3))
        
        
        self.rule = []
        self.rule.append(Rule( 'esperar', 'c1'))
        self.rule.append(Rule( 'esperar', 'c2'))
        self.rule.append(Rule( 'c2', 'c1'))
        self.rule.append(Rule( 'c1', 'c2'))
        self.rule.append(Rule( 'sucio', 'aspirar'))  
        self.rule.append(Rule( 'limpio', 'esperar'))
        
        self.model = []
        self.model.append(Model('espera', 'mover c1', "c2"))
        self.model.append(Model('espera', 'mover c2', "c1"))
        self.model.append(Model('c1', 'aspirar', "sucio"))
        self.model.append(Model('c2', 'aspirar', "sucio"))
        self.model.append(Model('c1', 'esperar', "limpio"))        
        self.model.append(Model('c2', 'esperar', "limpio"))
        
        self.currentModel = Model(self.state[0].action,  "c1", "")
        
        self.print_enviroment()
                

    def mess(self, quadrant):
        if quadrant == '1':            
            self.environment[0].dirty = 'sucio'
            
        if quadrant == '2':
            self.environment[1].dirty = 'sucio'
        self.print_enviroment()
        
    def clean(self, quadrant):
        if quadrant == 1:
            self.environment[0].dirty = 'limpio'
        if quadrant == 2:
            self.environment[2].dirty = 'limpio'
        self.print_enviroment()
        
    def print_enviroment(self):
        quadrant_hoover_one = 'HOV' if self.quadrant == 1 else '   '
        quadrant_hoover_two = 'HOV' if self.quadrant == 0 else '   '
        
        dirty_one = 'sucio' if self.environment[0].dirty == 'sucio' else '     '
        dirty_two = 'sucio' if self.environment[1].dirty == 'sucio' else '     '
        
        
        quadrant_hoover_one += ' ' + dirty_one
        quadrant_hoover_two += ' ' + dirty_two
        
        print('* ' * self.lado)
        for i in range(self.lado - 2):
            if i == 1:
                print(f'*{quadrant_hoover_one}' + ' ' * (self.lado - 2) + '*')
            else:              
                print('* ' + '  ' * (self.lado - 2) + '*')
        print('* ' * self.lado)
        
        print('* ' * self.lado)
        for i in range(self.lado - 2):
            if i == 1:
                print(f'*{quadrant_hoover_two}' + ' ' * (self.lado - 2) + '*')
            else:              
                print('* ' + '  ' * (self.lado - 2) + '*')
        print('* ' * self.lado)
        
        
    def obtain_action(self, state):
        print()
        if(state == 'espera'):
            self.quadrant = 1 if self.quadrant == 0 else 0
            return "mover-c2" if self.quadrant == 0 else "mover-c1"
        if(state == 'limpio'):
            self.quadrant = 1 if self.quadrant == 0 else 0
            return "mover-c2" if self.quadrant == 0 else "mover-c1"
        if(state == 'sucio'):
            self.clean(self.quadrant)
            return "aspirar"
        
        
    def update_status(self, state, action, perception):
        if(self.exist_model(state, action, perception)):
            return state                  
        return "espera"
    
    def exist_model(self, state, action, perception):
        for i, objet in enumerate(self.model):
            if objet.perception == perception and objet.state == state:
                return True                  
        return False 
    
    def execute_action(self, action):
        print(action)
        
        self.print_enviroment()
                
    
    def obtain_quadrant(self):
        return self.quadrant
    
    def obtain_perception(self, dirty):
        for objeto in self.rule:
            if objeto.state == dirty:
                return objeto
        return self.rule[0]
    
    def check_is_dirty(self, quadrant):      
        return self.environment[quadrant].dirty
    
    

class Hoover(threading.Thread):
    def __init__(self, space):       
        threading.Thread.__init__(self)
            

    def run(self):        
        while True:
            
            current_quadrant = space.obtain_quadrant()
            
            this_suction = space.check_is_dirty(current_quadrant)
            perception = space.obtain_perception(this_suction)
            
            new_state = space.update_status(perception.action, perception.state, this_suction)
            new_action = space.obtain_action(new_state)
            
            space.execute_action(new_action)
            
            
            threading.Event().wait(5)
            
            
                    
            

class User(threading.Thread):
    def __init__(self, cuadrantes):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print('Ingresa el numero de cuadrante a ensuciar:') 
            pos_quadrant = input()
            space.mess(pos_quadrant)
            
            threading.Event().wait(5)


space = Space()

hoover = Hoover(space)
user = User(space)


hoover.start()
user.start()

