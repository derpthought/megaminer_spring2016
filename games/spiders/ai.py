# This is where you build your AI for the Spiders game.

from joueur.base_ai import BaseAI
import random
    
class AI(BaseAI):
    
    def __init__(self, game):
        self._game = game
        self._player = None
        
        self.side = 0 # 0 denotes left, 1 right
        self.target_nests = []
        self.phil = None
        self.HOMEBASE = None
        
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
        self.phil = self.player.brood_mother
        self.HOMEBASE = self.phil.nest
        print("phil ONLINE")
        print("HOMEBASE DETERMINED")
        
        # determine our sidedness
        if self.phil.nest.x <= 200:
            self.side = 0
            self.target_nests = filter(lambda n: n.x <= 200, self.game.nests)
            print("LEFT")
            
        else:
            self.side = 1
            self.target_nests = filter(lambda n: n.x > 200, self.game.nests)
            print("RIGHT")
            
        print("TARGETS ACQUIRED")
        
        # prioritize nests based on distance from HOMEBASE
        sorted(self.target_nests, key=lambda n: n.distance_to(self.HOMEBASE))
        print("TARGETS PRIORITIZED")
        
        
    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """


    def run_turn(self):
        """ This is called every time it is this AI.player's turn.
        
        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        
        return True
        """"
        # get broodmother home neste
        phil = self.player.brood_mother
        HOMEBASE = phil.nest
        
        if HOMEBASE:
          # webs inbound to HOMEBASE
          INBOUND = HOMEBASE.webs
          BITCH_ASS_WEB = None
          # find nestes with connection to HOMEBASE
          # find min distance neste
          if INBOUND:
              BITCH_ASS_WEB = INBOUND[0]
              for web in INBOUND:
                  if  web.length < BITCH_ASS_WEB.length :
                      BITCH_ASS_WEB = web
            
        # TODO update spawn cause sux
        # spawn spiders 50/50 W/C
        while phil.eggs > 0:
            if phil.eggs % 2 == 0:
                phil.spawn("Weaver")

            phil.spawn("Cutter")

        # finish current work if not completed
        # if no work, then choose nearest web to start work

        if BITCH_ASS_WEB:
            for sp in self.player.spiders:
                if sp == phil:
                    continue
                if sp.busy == "":
                    if sp.game_object_name == "Weaver":
                        sp.weaken(BITCH_ASS_WEB)
                    elif sp.game_object_name == "Cutter":
                        sp.cut(BITCH_ASS_WEB)
                    else: # lol get that bitch outta hurr
                        phil.consume(sp)

        return True
        """
        
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
