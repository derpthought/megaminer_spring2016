# This is where you build your AI for the Spiders game.

from joueur.base_ai import BaseAI
import random
import math

def connected_to(webs, home):
    return  any(True for web in webs if home in (web.nest_a, web.nest_b))
    
class AI(BaseAI):

    def __init__(self, game):
        self._game = game
        self._player = None

        self.side = 0 # 0 denotes left, 1 right
        self.target_nests = []
        self.frontline = []
        self.phil = None
        self.HOMEBASE = None
        self.ENEMYBASE = None
        self.hq_cutters = []
        self.attack_cutters = []
        self.spitters = []

    """ The basic AI functions that are the same between games. """
    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        return "FLABSLAB AKA TEAM KESHTKAR AKA TripD's HEROES"



    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # DEBUGGING
        start = self.player.time_remaining

        self.phil = self.player.brood_mother
        self.HOMEBASE = self.phil.nest
        self.ENEMYBASE = self.player.other_player.brood_mother.nest
        print("phil ONLINE")
        print("HOMEBASE DETERMINED")
        print("MAIN TARGET ACQUIRED")

        # determine our sidedness
        if self.phil.nest.x <= 200:
            self.side = 0
            self.target_nests = list(filter(lambda n: n.x <= 200, self.game.nests))
            print("LEFT")

        else:
            self.side = 1
            self.target_nests = list(filter(lambda n: n.x > 200, self.game.nests))
            print("RIGHT")

        print("TARGET NESTS ACQUIRED")

        # prioritize nests based on distance from HOMEBASE
        sorted(self.target_nests, key=lambda n: n.distance_to(self.HOMEBASE))
        print("TARGETS PRIORITIZED")

        # get top five target nests closest to line of symmetry
        epsilon = 100
        self.frontline = list(filter(lambda tn: abs(tn.x - 200) < epsilon, self.target_nests))
        sorted(self.frontline, key=lambda n: n.distance_to(self.HOMEBASE))

        # remove duplicate values
        for n in self.frontline:
            self.target_nests.remove(n)

        if self.HOMEBASE in self.frontline:
            self.frontline.remove(self.HOMEBASE)

        print("FRONTLINE ESTABLISHED")

        # DEBUGGING
        print(str(start - self.player.time_remaining))


    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        if won:
            print("SUCK IT!")

        else:
            print("CALCULATED")

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # spawn at beginning of turn

        start = self.player.time_remaining

        # DEBUGGING
        start = self.player.time_remaining

        # determine which hq_cutters alive
        self.hq_cutter = list(filter(lambda hqc: not hqc.is_dead, self.hq_cutters))

        # determine which attack_cutters still alive
        self.attack_cutter = list(filter(lambda ac: not ac.is_dead, self.attack_cutters))

        # determine which spitters still alive
        self.spitters = list(filter(lambda sp: not sp.is_dead, self.spitters))

        print("CASUALTIES REMOVED FROM MEMORY (phil SOBS)")

        # DEBUGGING
        print(str(start - self.player.time_remaining))

        # initial turn spawn
        if self.game.current_turn in [0,1]:
            for i in range(self.phil.eggs):
                if i % 3 == 0:
                    self.hq_cutters.append(self.phil.spawn('Cutter'))
                else:
                    self.spitters.append(self.phil.spawn('Spitter'))

                print("INTO THE MEATGRINDER")

            count_front = 0
            count_target = 0
            for spitter in self.spitters:
                if count_front < len(self.frontline):
                    if self.HOMEBASE in self.frontline[count_front].webs:
                        spitter.spit(self.frontline[count_front])
                    count_front += 1

                else:
                    if count_target < len(self.target_nests):
                        if self.HOMEBASE in self.target_nests[count_target].webs:
                            spitter.spit(self.target_nests[-1 - count_target])
                        count_target += 1

                    else:
                        break
        
        else:
            while self.phil.eggs > 0:
               self.attack_cutters.append(self.phil.spawn("Cutter"))
           
           
        # spitters
        for spitter in self.spitters:
            if not spitter.busy:
                for nest in self.frontline:
                    if connected_to(nest.webs, self.HOMEBASE):
                        continue
                    else:
                        spitter.spit(nest)
                        break
            
            
            if not spitter.busy:
                for nest in self.target_nests:
                    if connected_to(nest.webs, self.HOMEBASE):
                        continue
                    else:
                        spitter.spit(nest)
                        break
                        
            # kill spitter if nothing to do
            if len(self.frontline) == 0 and len(self.target_nests) == 0:
                self.phil.consume(spitter)
        
        # attack_cutters
        for cutter in self.attack_cutters:
            if not cutter.busy:
                if cutter.nest != self.HOMEBASE:
                    for path in cutter.nest.webs:
                        for sp in path.spiderlings:
                            if sp.owner != self.player:
                                cutter.cut(path)
                    else:
                        if len(cutter.nest.webs) > 0:
                            cutter.cut(cutter.nest.webs[0])
                else:
                    for path in self.HOMEBASE.webs:
                        if path.load + 1 < path.strength:
                            cutter.move(path)
                            break
                            
        # HQ_cutters
        count = 0
        for line in self.HOMEBASE.webs:
            if line.nest_a not in self.target_nests or line.nest_b not in self.target_nests:
                numNeed = math.ceil(25*line.strength**2/(4*line.length))
                while count < len(self.hq_cutters):
                    if not ((self.hq_cutters)[count]).busy:
                        ((self.hq_cutters)[count]).cut(line)
                        numNeed -= 1
                    count += 1
                    if numNeed <= 0:
                        break
                if count == len(self.hq_cutters):
                    break
                    
        if not cutter.busy:
                if cutter.nest != self.HOMEBASE:
                    for path in cutter.nest.webs:
                        for sp in path.spiderlings:
                            if sp.owner != self.player:
                                cutter.cut(path)
                    else:
                        if len(cutter.nest.webs) > 0:
                            cutter.cut(cutter.nest.webs[0])
                else:
                    for path in self.HOMEBASE.webs:
                        if path.load + 1 < path.strength:
                            cutter.move(path)
                            break
                    

        # DEBUGGING
        print(str(start - self.player.time_remaining))
        print("YOUR MOVE BITCH")

        return True


        """
        spider = random.choice(self.player.spiders)

        if spider.game_object_name == "BroodMother":
            brood_mother = spider
            choice = random.randint(1, 10)

            if choice == 1: # try to consume a spiderling 10% of the time
                if len(brood_mother.nest.spiders) > 1:
                    otherSpider = random.choice(brood_mother.nest.spiders)
                    if otherSpider != brood_mother:
                        print("BroodMother #" + brood_mother.id +
                              " consuming " + otherSpider.game_object_name +
                              " #" + otherSpider.id)
                        brood_mother.consume(otherSpider)
            else: # try to spawn a Spiderling
                if brood_mother.eggs > 0:
                    # get a random spiderling type to spawn a new
                    # Spiderling of that type
                    randomSpiderlingType = random.choice(["Cutter", "Weaver", "Spitter"])
                    print("BroodMother #" + brood_mother.id +
                          " spawning " + randomSpiderlingType)
                    brood_mother.spawn(randomSpiderlingType)
        else: # it is a Spiderling
            spiderling = spider

            if spiderling.busy == "": # then it is NOT busy
                choice = random.randint(0, 2)

                if choice == 0: # try to move somewhere
                    if len(spiderling.nest.webs) > 0:
                        web = random.choice(spiderling.nest.webs)
                        print("Spiderling " + spiderling.game_object_name +
                              " #" + spiderling.id + " moving on Web #" + web.id)
                        spiderling.move(web)
                elif choice == 1: # try to attack something
                    if len(spiderling.nest.spiders) > 1:
                        otherSpider = random.choice(spiderling.nest.spiders)
                        if otherSpider.owner != spiderling.owner: # attack the enemy!
                            spiderling.attack(otherSpider)
                else: # do something unique based on Spiderling type
                    if spiderling.game_object_name == "Spitter":
                        spitter = spiderling
                        enemysNest = self.player.other_player.brood_mother.nest

                        # look for an existing web to the enemy home nest
                        webExists = any(True
                                        for web in enemysNest.webs
                                        if spitter.nest in (web.nest_a, web.nest_b))

                        if not webExists:
                            print("Spitter #" + spitter.id +
                                  " spitting to Nest #" + enemysNest.id)
                            spitter.spit(enemysNest)
                    elif spiderling.game_object_name == "Cutter":
                        cutter = spiderling
                        if len(cutter.nest.webs) > 0:
                            web = random.choice(cutter.nest.webs)
                            print("Cutter #" + cutter.id +
                                  " cutting Web #" + web.id)
                            cutter.cut(web)
                    elif spiderling.game_object_name == "Weaver":
                        weaver = spiderling
                        if len(weaver.nest.webs) > 0:
                            web = random.choice(weaver.nest.webs)
                            if random.randint(0,1) == 1:
                                print("Weaver #" + weaver.id +
                                      " strengthening Web #" + web.id)
                                weaver.strengthen(web)
                            else:
                                print("Weaver #" + weaver.id +
                                      " weakening Web #" + web.id)
                                weaver.weaken(web)
        return True # To signify that we are done with our turn
        """
