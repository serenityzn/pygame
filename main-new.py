import sys, pygame, time
from random import randrange
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
        self.PlayerX = 0
        self.PlayerY = 0
        self.PlayerIsoX = 0
        self.PlayerIsoY = 0
        self.screenOffsetX = 9
        self.screenOffsetY = 1
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
        self.size = x, y = 640, 480
        self.tilesize = 12
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.Walls = [ TItem('floor', 'room1_floor_tile24x12_1.png', screen = self.screen), TItem('floor', 'room1_floor_tile24x12_2.png', screen = self.screen), TItem('floor', 'room1_floor_tile24x12_3.png', screen = self.screen), TItem('wall', 'room1_table1_24x34_p1.png', 22, screen = self.screen), TItem('wall', 'room1_table1_24x34_p2.png', 22, screen = self.screen), TItem('wall', 'room1_table1_24x34_p3.png', 22, screen = self.screen), TItem('wall', 'room1_table1_24x34_p3.png', 16, screen = self.screen), ]
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
                elif ConfigBoardArray[i][j] == 4:
                    self.BoardArray[i].append(self.Walls[4])
                elif ConfigBoardArray[i][j] == 5:
                    self.BoardArray[i].append(self.Walls[5])
                elif ConfigBoardArray[i][j] == 6:
                    self.BoardArray[i].append(self.Walls[6])

    def CreatePickItems(self, ItemsArray):
        maxX = len(ItemsArray[1])
        maxY = len(ItemsArray[0])
        for i in range(maxY):
            self.PItemsArray.append([])
            for j in range(maxX):
                if ItemsArray[i][j] == 0:
                    self.PItemsArray[i].append(self.Items[0])
                else:
                    self.PItemsArray[i].append(None)
    def ReDrawScreen(self):
        self.screen.fill(self.black)
        PlayerCoord = self.toiso(self.Player.PlayerX, self.Player.PlayerY)
        self.Player.PlayerIsoX = PlayerCoord["x"]+self.Player.screenOffsetX*self.tilesize+self.tilesize/2
        self.Player.PlayerIsoY = PlayerCoord["y"]-self.tilesize*2+self.tilesize/2
        for i in range(10):
            for j in range(10):
                DrawCoord = self.toiso(i,j)
                if self.BoardArray[j][i].kind == 'wall':
                    self.Walls[2].Draw((DrawCoord["x"]+self.Player.screenOffsetX*self.tilesize, DrawCoord["y"]+self.Player.screenOffsetY*self.tilesize))
                else:
                    self.BoardArray[j][i].Draw((DrawCoord["x"]+self.Player.screenOffsetX*self.tilesize, DrawCoord["y"]+self.Player.screenOffsetY*self.tilesize))
        for i in range(10):
            for j in range(10):
                DrawCoord = self.toiso(i,j)
                if self.BoardArray[j][i].kind == 'wall':
                    self.BoardArray[j][i].Draw((DrawCoord["x"]+self.Player.screenOffsetX*self.tilesize, DrawCoord["y"]+self.Player.screenOffsetY*self.tilesize))
        self.Player.Draw()
        self.Player.ShowPos()
        pygame.display.flip()

    def toiso(self, x, y):
        res = {x: '', y: ''}
        res["x"] = x*self.tilesize - y*self.tilesize
        res["y"] = (x*self.tilesize + y*self.tilesize)/2
        return res
       
levelArr = [[0,1,1,0,2,0,1,2,1,0],
            [2,1,1,2,0,1,2,0,2,2],
            [0,0,0,2,2,0,2,0,0,1],
            [2,1,0,1,1,2,1,0,0,2],
            [0,1,2,1,0,0,1,2,1,1],
            [2,1,1,0,1,2,2,2,1,1],
            [1,1,2,1,0,5,0,1,2,2],
            [2,0,1,0,0,4,0,2,1,0],
            [0,1,1,0,2,3,0,0,1,2],
            [0,2,0,1,1,0,2,0,0,0]]
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
