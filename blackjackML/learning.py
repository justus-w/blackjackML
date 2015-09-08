"""

This file is NOT directly used in the project. It only makes existing code
available which might prove useful. This machine learning strategy was written
by Jonas Peters in Neubeuern and I suppose that this is the latest version.
"""
class ServanPlayer(StrategicPlayer):
    def __init__(self, name = "Servan", cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = "Servan"
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.strategy = Strategy()
        self.default = [0.1,0.3,0.5,0.5]
             # insurance o/wise not
             # split o/wise not
             # doubledown o/wise not
             # hit o/wise stand       
        self.game = Game()
        self.history = History()
    
    def add_gradient_to_strategy(self):
        step_size = 0.002
        tab_tmp = deepcopy(self.strategy.table)
        avec = []
        for g in self.history.game:
            prod_probvec_0 = 1.0
            probvec_tilde = []
            for dec in range(len(g.game_state)):
                a = GameState(g.game_state[dec][0], g.game_state[dec][1], g.game_state[dec][2], g.game_state[dec][3], g.game_state[dec][4]).__hash__()
                prod_probvec_0 = prod_probvec_0 * g.prob[dec]
                if g.action[dec]:
                    probvec_tilde.append(self.strategy.table[a])
                else:
                    probvec_tilde.append(1 - self.strategy.table[a])
                if (prod_probvec_0 == 0.0):
                    print g.prob
            for dec in range(len(g.game_state)):
                if g.action[dec]:
                    sign = 1.0
                else:
                    sign = -1.0
                a = GameState(g.game_state[dec][0], g.game_state[dec][1], g.game_state[dec][2], g.game_state[dec][3], g.game_state[dec][4]).__hash__()
                #if ((self.strategy.table[a] > 0.0) & (self.strategy.table[a] < 1.0)): 
                if ((self.strategy.table[a] > 0.0) & (self.strategy.table[a] < 1.0)): 
                    # tab_tmp[a] = min(max(tab_tmp[a] + step_size * g.gain * sign * np.prod(probvec_tilde[:dec] + probvec_tilde[(dec+1):])/prod_probvec_0,0),1)
                    tab_tmp[a] = tab_tmp[a] + step_size * g.gain * sign * np.prod(probvec_tilde[:dec] + probvec_tilde[(dec+1):])/prod_probvec_0
                    if ((tab_tmp[a] > 0.0) & (tab_tmp[a] < 1.0)): 
                        #everything fine
                        True
                    else:
                        avec.append(a)
                if False:
                    if (a == GameState(3,3,0,['2', '4'], ['A']).__hash__()):
                        print "\n found one"
                        print "gain: ", g.gain
                        print "game state", g.game_state
                        print "actions", g.action
                        print "probabilities under playing strategy", probvec_tilde
                        print "factor", np.prod(probvec_tilde[:dec] + probvec_tilde[(dec+1):])/prod_probvec_0
                        a = GameState(g.game_state[dec][0], g.game_state[dec][1], g.game_state[dec][2], g.game_state[dec][3], g.game_state[dec][4]).__hash__()
                        print "old: ", self.strategy.table[a]
                        print "new: ", tab_tmp[a]
#                if ((tab_tmp[a] == 0) & (self.strategy.table[a] > 0)):
#                    print "state became deterministic"
#                if ((tab_tmp[a] == 1) & (self.strategy.table[a] < 1)):
#                    print "state became deterministic"
        self.strategy.table = deepcopy(tab_tmp)
        for a in avec:
            self.strategy.table[a] = min(max(self.strategy.table[a], 0), 1)
    
    def update_strategy(self,numGames):
        if True:
            if (numGames % 1000 == 0):
                if(numGames > 20000):
                    self.add_gradient_to_strategy()
                    if True:
                        print "strategy upgedated!"
            if (numGames % 1000 == 0):
                if(numGames > 40000):
                    self.history.remove_almost_all_games(40000)
                    print "history cleared"
                    

class StrategicPlayer(Player):
    """ A player with different strategies. """
    #has an object strategy, which is a look-up table and defines all actions
    def __init__(self, name, cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = name
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.strategy = Strategy()
        self.default = [0.5,0,0,0.5]
             # insurance o/wise not
             # split o/wise not
             # doubledown o/wise not
             # hit o/wise stand       
        self.game = Game()
        self.history = History()

    def get_state(self, h):
        #ins = 1 => insurance bought; ins = 2 => insurance offered but not bought; ins = 0 => make choice; ins = 3 => option not available
        #ddo = 1 => double down; ddo = 2 => not double down; ddo = 0 => make choice
        #spl = 1 => split; spl = 2 => split possible but not done; spl = 0 => make choice; spl = 3 => option not available
        #check double down status

        #        ddo1 = self.hand[0].dd
        #ddo2 = 0
        #hand2 = Hand()
        #if len(self.hand) != 1:
        #    ddo2 = self.hand[1].dd
        #    hand2 = self.hand[1]
        #s = GameState(self.ins,self.spl,ddo1,ddo2,self.hand[0].cards,hand2.cards,dh)
 
        if output:
            print "complete game sate: (ins, spl, dd, hand, dealer)", self.ins, self.spl, self.hand[h].dd, self.hand[h].sorted_list(), dealer.hand[0].sorted_list()
        s = GameState(self.ins,self.spl,self.hand[h].dd,self.hand[h].sorted_list(),dealer.hand[0].sorted_list())
        
        return s.__hash__()
    
    def get_state_non_hash(self, h):
        #ins = 1 => insurance bought; ins = 2 => insurance offered but not bought; ins = 0 => make choice; ins = 3 => option not available
        #ddo = 1 => double down; ddo = 2 => not double down; ddo = 0 => make choice
        #spl = 1 => split; spl = 2 => split possible but not done; spl = 0 => make choice; spl = 3 => option not available
        #check double down status
        s = [self.ins,self.spl,self.hand[h].dd,self.hand[h].sorted_list(),dealer.hand[0].sorted_list()]
        return s
    
    def action(self, h):
        #if self.strategy.table.has_key(self.get_state()):
        gstmp = self.get_state(h)
        if gstmp in self.strategy.table:
            p = self.strategy.table[gstmp]
        else:
            if output:
                print "ins. status: ", self.ins, " --splt status: " , self.spl, " -- double down status of hand ",h,self.hand[h].dd
            if self.ins == 0:
                p = self.default[0] #insurance o/wise not
            elif self.spl == 0:
                p = self.default[1] #split o/wise not
            elif self.hand[h].dd == 0:
                p = self.default[2] # doubledown o/wise not
            else:
                p = self.default[3] # hit o/wise stand   
            self.strategy.table[gstmp] = p
            
        act = p > random.random()
        if act:
            self.game.prob.append(p)
        else:
            self.game.prob.append(1-p)            

        self.game.game_state.append(self.get_state_non_hash(h))
        self.game.action.append(act)
        return act
        
    def double_down(self,h=0):
        dd = self.action(h)
        if dd:
            if output:
                print(self.name + " chose double down.")
            self.hand[h].dd = 1
        else:
            self.hand[h].dd = 2
        return dd
        
    def hit_otherwise_stand(self,io,h=0):
        hit = self.action(h)        
        self.hand[h].stand = not hit
        if hit:
            if output:
                print(self.name + " chose to hit.")
        else:
            if output:
                print(self.name + " chose to stand.")
        return hit
    
    def buys_insurance(self,io):
        self.ins = 0
        res = self.action(h)
        if res:
            self.ins = 1
        else:
            self.ins = 2
    
    def split_hand(self,h=0):
        if self.hand[h].can_split():
            self.spl = 0
            res = self.action(h)
            if res:
                self.spl = 1
                if output:
                    print(self.name + " chose to split.")
                return True
            else:
                self.spl = 2
                if output:
                    print(self.name + " chose not to split.")
                return False
        else:
            self.spl = 3
            return False
        
    def bet(self,io,h=0):
        b = 10
        self.hand[h].bet = b
        self.credits -= b
        self.game.gain -= b
        
    def update_strategy(self,games):
        return True
    
class History(object):
    def __init__(self):
        self.game = []
        
    def add_game(self, g):
        self.game.append(deepcopy(g)) 
        
    def remove_almost_all_games(self, nn):
        self.game = self.game[(-nn):(-1)]

class Game(object):
    def __init__(self):
        self.prob = []
        self.game_state = []
        self.action = []
        self.gain = 0
        
    def reset(self):
        self.prob = []
        self.game_state = []
        self.action = []
        self.gain = 0

class GameState(object):
    def __init__(self,ins,spl,ddo,h1,dh):
        self.ins = ins
        self.spl = spl
        self.ddo = ddo
        self.h1 = h1
        self.dh = dh
        
    def __hash__(self):
        return hash((self.ins,self.spl,self.ddo,self.h1.__str__(),"-",self.dh.__str__()))
    
class Strategy(object):
    def __init__(self):
        self.table = {}