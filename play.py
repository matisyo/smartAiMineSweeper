from keras.models import model_from_json
from buscaminas import MineSweeper as ms
import numpy as np
from random import randint

def set_smart_ohe(tmp):
    tmp = tmp+2
    next_turno = np.zeros((*tmp.shape,12))
    next_turno[:,np.arange(25),11]=1
    for i,x in enumerate(tmp):
        next_turno[i,range(x.shape[0]),x] = 1
    return next_turno.reshape(-1,5,5,12)
def reformat():
    m = load_model()    
    data = np.loadtxt(open("prueba.csv", "rb"), delimiter=",").astype(int)
    n = (data.shape[1]-3)//2
    mapa = set_smart_ohe(data[:,:n])
    mapa_prox = set_smart_ohe(data[:,n:n*2])
    action,reward,end = data[:,n*2],data[:,n*2+1],1-data[:,n*2+2]
    target = m.predict(mapa)
    res_next = m.predict(mapa_prox)
    target[range(action.shape[0]),action ] = reward + .95 * end * np.max(res_next,axis=1)
    np.save('entrada.npy', mapa)
    np.save('salida.npy', target)

def load_model():
    with open('model.json', 'r') as json_file:     
        loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    loaded_model.compile(optimizer='adam', loss='mse')
    return loaded_model

def to_file(lista,name):
    with open(name, "a+") as f:
        for t in lista:
            frase = ",".join(map(lambda x : str(int(x)),t))+"\n"
            f.write(frase)
def to_ohe(a,alto,ancho):
    este_turno = np.zeros((len(a),12))
    este_turno[np.arange(len(a)), np.array(a+2).astype(int)] = 1
    este_turno[np.arange(len(a)),11]=1
    este_turno = este_turno.reshape(1,alto,ancho,12)
    return este_turno

def jugar(alto,ancho,bombas,epsilon=.1,cant_juegos=1,filename='prueba.csv'):    
    model = load_model()
    open(filename, 'w').close()
    for juego in range(cant_juegos):
        #Creo Juego        
        game = ms(alto,ancho,bombas,True)
        duracion = 0
        cant_turnos = 0
        resultado = "gano"
        bombas_click=0
        mal_click=0
        bien_click=0
        lista = []
        while not game.gameover:
            a = game.matriz_usuario.copy()
            este_turno = a
            # Genereo proximo movimiento
            al_azar = (np.random.rand() <= epsilon)
            if not al_azar:                
                action = np.argmax(model.predict(to_ohe(este_turno,alto,ancho))[0])
            else:
                action = randint(0,alto*ancho-1)
            
            t1,t2 = game.get_loc(action) 
            cant = game.click(t1,t2)
            
            if game.gameover:                
                reward = 100            
            elif cant==-1:
                reward = -100
                resultado="perdio"
                bombas_click+=1
            elif cant==0:
                reward = -1
                mal_click+=1
            else:
                reward = 10
                bien_click+=1
            
            next_turno = game.matriz_usuario.copy()
            
            episode = [este_turno, 
                       next_turno,
                       action, 
                       reward,                       
                       game.gameover]
            episode_final = list(episode[0])+list(episode[1])
            episode_final += [episode[2],episode[3],int(episode[4])]
            lista.append(episode_final)
        to_file(lista,filename)