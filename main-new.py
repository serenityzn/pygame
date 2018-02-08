import sys, pygame, time
pygame.init()
pygame.font.init()


class TItem:
    def __init__(self, ItemKind, ItemImage, ItemHeight = None, screen = None, properties = None):
        self.kind = ItemKind
        self.image = self.ImageLoad(ItemImage)
        self.height = ItemHeight
        self.screen = screen
        self.properties = properties

    def Draw(self, coord):
        if self.height != None:
            PromCoord = list(coord)
            PromCoord[1] -= self.height
            coord = tuple(PromCoord)
        self.screen.blit(self.image, coord )

    def ImageLoad(self, image, colorkey = None):
        try:
            img = pygame.image.load(image)
        except pygame.error, message:
            print 'Cannot load image:', image
            raise SystemExit, message
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return img 
        

class TPlayer:
    def __init__(self,ItemImage, speed = 1, screen = None, BoardArray = None):
        self.BoardArray = BoardArray
        self.image = self.ImageLoad(ItemImage)
        self.speed = speed
        self.screen = screen
        self.PlayerX = 1
        self.PlayerY = 1
        self.PlayerIsoX = 0
        self.PlayerIsoY = 0
        self.Health = 60
        self.MaxHealth = 60
        self.Armor = 0
        self.PlItems = []
        self.ItemsOn = { 'body': None, 'legs': None, 'head': None, 'weapons': None }
        self.PlayerFont = pygame.font.Font('./OpenSans-Italic.ttf', 30)

    def PickItem(self, item):
        if item.properties != None:
            self.PlItems.append(item)

    def ImageLoad(self, image, colorkey = None):
        try:
            img = pygame.image.load(image)
        except pygame.error, message:
            print 'Cannot load image:', image
            raise SystemExit, message
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return img 

    def Draw(self):
        self.screen.blit(self.image, (self.PlayerIsoX, self.PlayerIsoY) )

    def UpdatePos(self, x, y):
        self.PlayerX = x
        self.PlayerY = y

    def ShowPos(self):
        PosText = str(self.PlayerX) + "," + str(self.PlayerY) + ' Isometric: ' + str(self.PlayerIsoX) + ',' + str(self.PlayerIsoY)
        PositionText = self.PlayerFont.render(PosText, True, (200, 0, 0))
        self.screen.blit(PositionText, (10,10))

    def Move(self, direction):
        if direction == 'r':
            if self.BoardArray[self.PlayerY][self.PlayerX + self.speed].kind != 'wall':
                self.PlayerX += self.speed
                self.image = self.ImageLoad("p1.png")
        if direction == 'l':
            if self.BoardArray[self.PlayerY][self.PlayerX - self.speed].kind != 'wall':
                self.PlayerX -= self.speed
                self.image = self.ImageLoad("p.png")
        if direction == 'u':
            if self.BoardArray[self.PlayerY - self.speed][self.PlayerX].kind != 'wall':
                self.PlayerY -= self.speed
        if direction == 'd':
            if self.BoardArray[self.PlayerY + self.speed][self.PlayerX].kind != 'wall':
                self.PlayerY += self.speed
                self.image = self.ImageLoad("p1.png")

class TCollectionItem:
    def __init__(self, LevelArray, PickItemsArray):
        self.BoardArray =[[]]
        self.PItemsArray =[[]]
        self.size = x, y = 1280, 800
        self.tilesize = 64
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.Walls = [ TItem('floor', 'tile.png', screen = self.screen), TItem('wall', 'block1.png', 32, screen = self.screen), TItem('wall', 'piramid.png', screen = self.screen), TItem('wall', 'piramid1.png', 32, screen = self.screen) ]
        self.Items = [ TItem('pants', 'pants.png', screen = self.screen, properties = {'armor': 2, 'durability': '10'})]
        self.Player = TPlayer('p1.png', 1, screen = self.screen, BoardArray = self.BoardArray)
        self.CreateBoard(LevelArray)
        self.CreatePickItems(PickItemsArray)
    
    def CreateBoard(self, ConfigBoardArray):
        MaxY = len(ConfigBoardArray[0])
        MaxX = len(ConfigBoardArray[1])
        for i in range(MaxY):
            self.BoardArray.append([])
            for j in range(MaxX):
                if ConfigBoardArray[i][j] == 0:
                    self.BoardArray[i].append(self.Walls[0])
                elif ConfigBoardArray[i][j] == 1:
                    self.BoardArray[i].append(self.Walls[1])
                elif ConfigBoardArray[i][j] == 2:
                    self.BoardArray[i].append(self.Walls[2])
                elif ConfigBoardArray[i][j] == 3:
                    self.BoardArray[i].append(self.Walls[3])

    def CreatePickItems(self, ItemsArray):
        print ItemsArray
        maxX = len(ItemsArray[1])
        maxY = len(ItemsArray[0])
        for i in range(maxY):
            self.PItemsArray.append([])
            for j in range(maxX):
                print "i={0} j={1}".format(i,j)
                print self.PItemsArray
                print "Array{0},{1} = {2}".format(i,j,ItemsArray[i][j])
                if ItemsArray[i][j] == 0:
                    self.PItemsArray[i].append(self.Items[0])
                else:
                    self.PItemsArray[i].append(None)

    def ReDrawScreen(self):
        self.screen.fill(self.black)
        PlayerCoord = self.toiso(self.Player.PlayerX, self.Player.PlayerY)
        self.Player.PlayerIsoX = PlayerCoord["x"]+9*64+64
        self.Player.PlayerIsoY = PlayerCoord["y"]+1*64
        for i in range(10):
            for j in range(10):
                DrawCoord = self.toiso(i,j)
                if j == self.Player.PlayerY and i == self.Player.PlayerX:
                    self.BoardArray[j][i].Draw((DrawCoord["x"]+9*64, DrawCoord["y"]+1*64))
                    self.Player.Draw()
                else:
                    self.BoardArray[j][i].Draw((DrawCoord["x"]+9*64, DrawCoord["y"]+1*64))
                if self.PItemsArray[j][i] != None:
                    self.PItemsArray[j][i].Draw((DrawCoord["x"]+9*64, DrawCoord["y"]+1*64))
        self.Player.ShowPos()
        pygame.display.flip()

    def toiso(self, x, y):
        res = {x: '', y: ''}
        res["x"] = x*self.tilesize - y*self.tilesize
        res["y"] = (x*self.tilesize + y*self.tilesize)/2
        return res
       
levelArr = [[0,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,1,1,1,2,0,1],
            [1,0,0,1,0,0,0,1,0,1],
            [1,0,0,1,3,3,0,1,0,1],
            [1,0,0,0,0,1,0,1,0,1],
            [1,0,2,0,0,0,0,1,0,1],
            [1,0,0,0,0,1,1,1,0,1],
            [1,0,0,2,0,0,0,0,0,3],
            [1,1,1,1,1,1,1,1,1,1]]
itemsArr = [[1,1,1,1,1,1,1,1,1,1],
            [1,0,0,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1]]
cl = TCollectionItem(levelArr, itemsArr)
#cl.CreateBoard(levelArr)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cl.Player.Move('r')
            if event.key == pygame.K_LEFT:
                cl.Player.Move('l')
            if event.key == pygame.K_UP:
                cl.Player.Move('u')
            if event.key == pygame.K_DOWN:
                cl.Player.Move('d')
    
    cl.ReDrawScreen()
