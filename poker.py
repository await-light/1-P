import random

BRAND_LIST = (
    (0, '3', 4),
    (1, '4', 4),
    (2, '5', 4),
    (3, '6', 4),
    (4, '7', 4),
    (5, '8', 4),
    (6, '9', 4),
    (7, '10', 4),
    (8, 'J', 4),
    (9, 'Q', 4),
    (10, 'K', 4),
    (11, 'A', 4),
    (12, '2', 4),
    (13, 'SMALL', 1),
    (14, 'BIG', 1)
)

########################  BRAND  #########################

class Brand:
    '''
    easy brand object
    :the brand which is called NAME values SIZE
    '''
    reprfmt = "[%s]"
    def __init__(self, size, name):
        self.size = size
        self.name = name

    def __gt__(self, another_brand):
        if self.size > another_brand.size:
            return True
        else:
            return False # <=

    def __repr__(self):
        return Brand.reprfmt % (self.name)

    def __str__(self):
        return self.__repr__()

class BrandList:
    '''
    some of brands gather here
    '''
    def __init__(self, *brands):
        self._brandlist = []
        self._brandlist += brands
        self.autosort()

    def remove_brands(self, delbrandlist:__name__):
        '''
        remove all brands in DELBRANDLIST
        '''
        for delbrand in delbrandlist:
            i = self._index_by_brandname(delbrand.name)
            if i != None:
                self._brandlist.pop(i)

    @property
    def countdict(self):
        '''
        countdict
        :return dict -> brand.name: count
        '''
        d = {}
        for i in self._brandlist:
            if (not d.get(i.name)):
                d[i.name] = 0
            d[i.name] += 1
        return d

    def matchsort(self):
        '''
        sort according to count of brands
        '''
        # 8 8 8 9 2 9 7 9 7 7 2 1
        self._brandlist = sorted(
            self._brandlist, 
            key=lambda x:[i.name for i in self._brandlist].count(x.name), 
            reverse=True
        )
        if len(self._brandlist) == 1:
            # 8 8 8 9 9 9 7 7 7 2 2 1
            start = 0
            lastone = self._brandlist[0].size
            for index, brand in enumerate(self._brandlist):
                if brand.size != lastone:
                    self._brandlist[start:index] = \
                        sorted(
                            self._brandlist[start:index], 
                            key=lambda x:x.size
                        )
                    start = index

    def autosort(func):
        def wrap(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._sort()
        return wrap

    def _sort(self):
        self._brandlist = sorted(self._brandlist, key=lambda x:x.size)

    def _index_by_brandname(self, brandname):
        index = None
        for i, brand in enumerate(self._brandlist):
            if brand.name == brandname:
                index = i
                break
        return index

    @autosort
    def append(self, *args, **kwargs):
        self._brandlist.append(*args, **kwargs)

    def pop(self, *args, **kwargs):
        self._brandlist.pop(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self._brandlist.remove(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self._brandlist.count(*args, **kwargs)

    def __iter__(self):
        return iter(self._brandlist)

    def __getitem__(self, *args, **kwargs):
        return self._brandlist.__getitem__(*args, **kwargs)

    def __repr__(self):
        return ' '.join([str(i) for i in self._brandlist])

    def __len__(self):
        return len(self._brandlist)

##########################################################

######################  BRAND TYPE  ######################

class ComplicatedJudge:
    '''
    ComplicatedJudge
    :just for replacing unreadable lambda expression
    
    RETURN
    :True or False
    '''
    @staticmethod
    def straight(brandlist:BrandList):
        bl = [i.size for i in brandlist] # sorted already
        minbr, maxbr = min(bl), max(bl)
        # the scope 'straight' specifies
        if not ((0 <= minbr <= 11) and (0 <= minbr <= 11)): # from 3 to A
            return False
        # length scope
        if not (5 <= len(bl) <= 12):
            return False
        # if it's continuous
        if (len(set(bl)) < len(bl)):
            return False
        return True

    @staticmethod
    def continuouspairs(brandlist:BrandList):
        bl = [i.size for i in brandlist] # sorted already
        minbr, maxbr = min(bl), max(bl)
        # the scope 'continuouspairs' specifies
        if not ((0 <= minbr <= 11) and (0 <= maxbr <= 11)): # from 3 to A
            return False
        # length scope
        if (not (6 <= len(bl) <= 24)) or (len(bl) % 2 != 0):
            return False
        # if it's continuous
        if ( (bl[::-2][::-1] != bl[::2]) or (len(set(bl[::2])) < len(bl[::2])) ): 
            return False
        return True

BRAND_TYPE = (
    # king bomb -> (SMALL BIG)
        ( lambda T:(len(T)==2) and (T[0].size+T[1].size)==27 ,
          lambda A:A[0],
          lambda AB:True),
    # bomb -> (A A A A)
        ( lambda T:(len(T)==4) and (T[0].size==T[1].size==T[2].size==T[3].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # single -> (A)
        ( lambda T:len(T)==1,
          lambda A:A[0],
          lambda AB:AB[0]>AB[1] ),
    # pair -> (A A)
        ( lambda T:(len(T)==2) and (T[0].size==T[1].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # three -> (A A A)
        ( lambda T:(len(T)==3) and (T[0].size==T[1].size==T[2].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # three + one -> (A A A B)
        ( lambda T:(len(T)==4) and (T[0].size==T[1].size==T[2].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # three + two -> (A A A B B)
        ( lambda T:(len(T)==5) and (T[0].size==T[1].size==T[2].size) and (T[3].size==T[4].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # four + two-single -> (A A A A B C)
        ( lambda T:(len(T)==6) and (T[0].size==T[1].size==T[2].size==T[3].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # four + two-pair -> (A A A A B B C C)
        ( lambda T:(len(T)==8) and (T[0].size==T[1].size==T[2].size==T[3].size) and (T[4].size==T[5]) and (T[6].size==T[7].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # plane-single -> (A A A B B B C D)
        ( lambda T:(len(T)==8) and (T[0].size+1==T[3].size) and (T[0].size==T[1].size==T[2].size) and (T[3].size==T[4].size==T[5].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # plane-pair -> (A A A B B B C C D D)
        ( lambda T:(len(T)==10) and (T[0].size+1==T[3].size) and (T[0].size==T[1].size==T[2].size) and (T[3].size==T[4].size==T[5].size) and (T[6].size==T[7].size) and (T[8].size==T[9].size),
          lambda A:A[0],
          lambda AB:AB[0]>AB[1]),
    # straight -> (A B C D E F G ...)
        ( ComplicatedJudge.straight,
          lambda A:A,
          lambda AB:(AB[0][0]>AB[1][0]) if (len(AB[0])==len(AB[1])) else "Your straight's length must be %d" % len(AB[1])),
    # continuouspairs -> (A A B B C C ...)
        ( ComplicatedJudge.continuouspairs,
          lambda A:A,
          lambda AB:(AB[0][0]>AB[1][0]) if (len(AB[0])==len(AB[1])) else "Your continuouspairs's length must be %d" % len(AB[1]))
)
BRAND_TYPE_KINGBOMB = 0
BRAND_TYPE_BOMB = 1

##########################################################

# identity
LANDOWNER = 1
FARMER = 2

#######################  PLAYER  #########################

class Player:
    '''
    player
    :which IDENTITY is 'landowner' or 'farmer'
     and have BRANDS
    '''
    def __init__(self, identity:int, name):
        self.name = name
        self.identity = identity
        self.brandlist = BrandList()

    def __repr__(self):
        return "name:%s\nidentity:%s\nbrands:%s\n" % (
            self.name,
            "farmer" if self.identity == FARMER else "landowner",
            self.brandlist
        )

##########################################################

#######################  MATCH  ##########################

class Match:
    def __init__(self, match:BrandList, player:Player):
        self._match = match
        self.index, self.mainbody, self.compsize = self._typeit()
        self.player = player

    def _typeit(self):
        match = self._match
        # judge what kind the match is
        # if the match is known, return INDEX of type in BRAND_TYPE
        # and MAINBODY and COMPSIZE
        for index, (is_type, main_body, comp_size) in enumerate(BRAND_TYPE):
            if is_type(match):
                return (index, main_body(match), comp_size)
        # the kind of the match is unknown
        return (None, None, None)

##########################################################

def handout(landowner, farmer1, farmer2):
    '''
    hand out brands
    farmer: 17
    landowner: 20
    '''
    all_brands = [] # all brands
    for i in BRAND_LIST:
        for j in range(i[2]):
            all_brands.append(Brand(i[0], i[1]))
    # hand out brands
    for player in (farmer1, farmer2, landowner):
        for i in range(17 if player.identity == FARMER else 20):
            index = random.randrange(0, len(all_brands))
            player.brandlist.append(all_brands[index])
            all_brands.pop(index)

class Scene:
    def __init__(self, landowner, farmer1, farmer2):
        self.landowner = landowner
        self.farmer1 = farmer1
        self.farmer2 = farmer2
        self.run()

    def prompt(self, *args):
        print(*args)

    def promptquietly(self, playername, *args):
        print(*args)

    def getinput(self, playername):
        return input()

    def run(self):
        players = (
            Player(LANDOWNER, self.landowner), # landowner
            Player(FARMER, self.farmer1), # farmer
            Player(FARMER, self.farmer2), # farmer
        )

        handout(*players)

        for pl in players:
            self.promptquietly(pl.name, "%s's brands: %s" % (pl.name, pl.brandlist))

        count = 0
        last_match = None

        while True:
            # self.prompt("")
            player = players[count % 3]

            # self.prompt(player.name, player.brandlist)
            self.prompt(
                "It's `%s %s`'s turn." % (
                    "Farmer" if player.identity==FARMER else "Landowner",
                    player.name
                )
            )
            strmatch = self.getinput(player.name).strip() # string match

            if strmatch == ".": # skip
                if (last_match == None or player == last_match.player):
                    self.prompt("You must play instead of skipping")
                    continue
                else:
                    count += 1
                    continue
            elif strmatch == "?": # look up brands
                self.promptquietly(player.name, "%s's brands: %s" % (player.name, player.brandlist))
                continue

            brandl = BrandList() # the brandl player plays

            formatted = True # if wrong brand exists or misformatted, will become False
            while formatted:
                if not strmatch:
                    formatted = False
                for i in strmatch.split():
                    # i -> name
                    for j in BRAND_LIST:
                        if i == j[1]:
                            brandl.append(Brand(j[0], i))
                            break
                    else:
                        self.prompt("wrong brand exists `%s`" % i)
                        formatted = False
                        break
                break
            if not formatted:
                continue

            # sort the brandl as match
            brandl.matchsort()
            # print("matchsort brandl:", brandl)

            # whether player has enough brands
            enough = True
            for brandname, num in brandl.countdict.items():
                if (num > player.brandlist.countdict.setdefault(brandname, 0)):
                    enough = False
                    break
            if not enough:
                self.prompt("You don't have enough brands :(")
                continue
            
            # self.prompt("brandl found:", brandl)
            match = Match(brandl, player)
            # self.prompt("typeindex:", match.index)
            # self.prompt("mainbody:", match.mainbody)
            # self.prompt("compsize:", match.compsize)
            
            if (match.index == None): # unknown
                self.prompt("Your match is unknown")
                continue
            if (last_match == None or player == last_match.player): 
                    # 1 you are biggest of last round
                    # 2 if player is last round's biggest, set last_match None
                    # new match will overwrite the original match(LAST_MATCH)
                pass
            else:
                if (last_match.index == BRAND_TYPE_KINGBOMB): # if last one is king bomb
                                                              # match will be smaller than last one anyway
                    self.prompt("Your match must be bigger than last one!")
                    continue
                if (match.index != BRAND_TYPE_KINGBOMB): # not kingbomb
                    if (match.index == last_match.index or match.index == BRAND_TYPE_BOMB): # same index as last one
                        comp = match.compsize((match.mainbody, last_match.mainbody))
                        if type(comp) == bool:
                            if comp: # bigger
                                pass
                            else: # smaller or equal
                                self.prompt("Your match must be bigger than last one!")
                                continue
                        else:
                            self.prompt(comp)
                    else: # not same  
                        self.prompt("Your match's type must be same as last one")
                        continue

            player.brandlist.remove_brands(brandl)
            # someone wins?
            if len(player.brandlist) == 0:
                self.prompt("# %s win%s!" % ("farmers", "") if (player.identity == FARMER) else ("landowner", "s"))
                break
            last_match = match
            count += 1 # next player's turn

if __name__ == '__main__':
    scene = Scene("Sam", "Jack", "Tom")