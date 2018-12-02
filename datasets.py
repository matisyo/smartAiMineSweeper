import numpy as np

class DataSets(object):
    memory = []        
    def __init__(self,max_memory=10,gamma=.95):
        self.max_memory=max_memory
        self.gamma = gamma
    def remember(self,episode):        
        self.memory.append(episode)
        if len(self.memory) > self.max_memory:            
            del self.memory[0]

    def get_data(self,model,data_size=10,last_few=10):
        a,b,c,d = self.memory[0][0].shape#alto por ancho
        mem_size = len(self.memory)
        last_few = min(mem_size, last_few)
        data_size = min(last_few, data_size)

        inputs = np.zeros((data_size, b,c,d))
        targets = np.zeros((data_size, b*c))

        for i, j in enumerate(np.random.choice(range(last_few), data_size, replace=False)):
            envstate, action, reward, envstate_next, game_over = self.memory[mem_size-last_few+j]
            inputs[i] = envstate
            targets[i] = model.predict(envstate)[0]
            if game_over:
                targets[i, action] = reward
            else:
                targets[i, action] = reward + self.gamma * np.max(model.predict(envstate_next)[0])
        return inputs, targets