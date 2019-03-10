#import random
#import os
import time

class envir:
    def __init__(self, size = 5):
        self.size = size
        self.agent = agent(1, 1, self)
        self.enemies = [enemy(2, 3, self)]
        
    def create_map(self):
        self.map = [[0 for i in range(self.size)] for i in range(self.size)]
        for e in self.enemies:
            self.map[e.y][e.x] = 2
            
        self.map[self.agent.y][self.agent.x] = 1

    def print_map(self):
        for i in self.map:
            print(i)

    def step(self):
        for e in self.enemies:
            e.step()
        self.agent.step()
        self.create_map()

class alive:
    def __init__(self, x, y, env):
        self.x = x
        self.y = y
        self.env = env
        self.mode = "runner"

    def move(self, dx, dy):
        if (0 <= self.x + dx < self.env.size) and (0 <= self.y + dy < self.env.size):
            self.x += dx
            self.y += dy

    def see_map(self):#hunter or runner
        self.env.create_map()
        seen_map = self.env.map
        #hunt agent
        if self.mode == "hunter":
            self.reward_map = [[-1 for i in range(self.env.size)] for i in range(self.env.size)]
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    self.reward_map[self.env.agent.y+i][self.env.agent.x+j] = 1
            self.reward_map[self.env.agent.y][self.env.agent.x] = 2

        #run from enemies
        if self.mode == "runner":
            self.reward_map = [[1 for i in range(self.env.size)] for i in range(self.env.size)]
            for e in self.env.enemies:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        self.reward_map[e.y+i][e.x+j] = -1
                self.reward_map[e.y][e.x] = -2
            self.reward_map[self.y][self.x] = -3

    #get max reward
    def strategy(self):
        #max_reward_total = 0
        rmax1 = -100
        rmax1_move = (0, 0)
        rmax2 = -100
        rmax2_move = (0, 0)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                for dy2 in [-1, 0, 1]:
                    for dx2 in [-1, 0, 1]:
                        if (0 <= self.x + dx < self.env.size) and (0 <= self.y + dy < self.env.size):
                            if self.reward_map[self.y + dy][self.x + dx] > rmax1:
                                rmax1 = self.reward_map[self.y + dy][self.x + dx]
                                rmax1_move = (dx, dy)
                                
                        if (0 <= self.x + rmax1_move[0] + dx2 < self.env.size) and (0 <= self.y + rmax1_move[1] + dy2 < self.env.size):    
                            if self.reward_map[self.y + rmax1_move[1] + dy2][self.x + rmax1_move[0] + dx2] > rmax2:
                                rmax2 = self.reward_map[self.y + rmax1_move[1] + dy2][self.x + rmax1_move[0] + dx2]
                                rmax2_move = (dx2, dy2)
                            
        self.strategy_move1 = rmax1_move
        self.strategy_move2 = rmax2_move

    def step(self):
        self.see_map()
        self.strategy()
        self.move(self.strategy_move1[0], self.strategy_move1[1])

class enemy(alive):
    def __init__(self, x, y, env):
        alive.__init__(self, x, y, env)
        self.mode = "hunter"

class agent(alive):
    def __init__(self, x, y, env):
        alive.__init__(self, x, y, env)
        self.mode = "runner"

e = envir()
e.create_map()
e.print_map()
while True:
    print("\n--------\n")
    time.sleep(1)
    e.step()
    e.print_map()
    #print("\nAgent reward map:\n")
    #for i in e.agent.reward_map:
    #    print(i)
