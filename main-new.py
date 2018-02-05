import sys, pygame, time
pygame.init()
pygame.font.init()


class TItem:
    def __init__(self, ItemKind, ItemImage, ItemHeight = None, screen = None):
        self.kind = ItemKind
        self.image = ItemImage
        self.height = ItemHeight
        self.ImageLoad = pygame.image.load(self.image)
        self.screen = screen

    def Draw(self, coord):
        if self.height != None:
            PromCoord = list(coord)
            PromCoord[1] -= self.height
            coord = tuple(PromCoord)
        self.screen.blit(self.ImageLoad, coord )

class TPlayer:
    def __init__(self,ItemImage, speed = 1, screen = None, BoardArray = None):
        self.BoardArray = BoardArray
        self.image = ItemImage
        self.speed = speed
        self.ImageLoad = pygame.image.load(self.image)
        self.screen = screen
        self.PlayerX = 1
        self.PlayerY = 1
        self.PlayerIsoX = 0
        self.PlayerIsoY = 0
        self.PlayerFont = pygame.font.Font('./OpenSans-Italic.ttf', 30)

    def Draw(self):
        self.screen.blit(self.ImageLoad, (self.PlayerIsoX, self.PlayerIsoY) )

    def UpdatePos(self, x, y):
        self.PlayerX = x
        self.PlayerY = y

    def ShowPos(self):
        PosText = str(self.PlayerX) + "," + str(self.PlayerY) + ' Isometric: ' + str(self.PlayerIsoX) + ',' + str(self.PlayerIsoY)
        PositionText = self.PlayerFont.render(PosText, True, (200, 0, 0))
        self.screen.blit(PositionText, (10,10))

    def Move(self, direction):
        if direction == 'r':
            if self.BoardArray[self.PlayerY][self.PlayerX + self.speed].kind != 'block':
                self.PlayerX += self.speed
                self.ImageLoad = pygame.image.load("p1.png")
        if direction == 'l':
            if self.BoardArray[self.PlayerY][self.PlayerX - self.speed].kind != 'block':
                self.PlayerX -= self.speed
                self.ImageLoad = pygame.image.load("p.png")
        if direction == 'u':
            if self.BoardArray[self.PlayerY - self.speed][self.PlayerX].kind != 'block':
                self.PlayerY -= self.speed
        if direction == 'd':
            if self.BoardArray[self.PlayerY + self.speed][self.PlayerX].kind != 'block':
                self.PlayerY += self.speed
                self.ImageLoad = pygame.image.load("p1.png")

class TCollectionItem:
    def __init__(self, BoardX = 10, BoardY = 10 ):
        self.BoardArray =[[]]
        self.BoardSize = [BoardX*42, BoardY*32] 
        self.size = x, y = 1280, 800
        self.tilesize = 64
        self.BoardX = BoardX
        self.BoardY = BoardY
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.Items = [ TItem('grass', 'tile.png', screen = self.screen), TItem('block', 'block1.png', 32, screen = self.screen), TItem('block', 'piramid.png', screen = self.screen), TItem('block', 'piramid1.png', 32, screen = self.screen) ]
        self.Player = TPlayer('p1.png', 1, screen = self.screen, BoardArray = self.BoardArray)
    
    def CreateBoard(self, ConfigBoardArray):
        MaxY = len(ConfigBoardArray[0])
        MaxX = len(ConfigBoardArray[1])
        for i in range(MaxY):
            self.BoardArray.append([])
            for j in range(MaxX):
                if ConfigBoardArray[i][j] == 0:
                    self.BoardArray[i].append(self.Items[0])
                elif ConfigBoardArray[i][j] == 1:
                    self.BoardArray[i].append(self.Items[1])
                elif ConfigBoardArray[i][j] == 2:
                    self.BoardArray[i].append(self.Items[2])
                elif ConfigBoardArray[i][j] == 3:
                    self.BoardArray[i].append(self.Items[3])

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
        self.Player.ShowPos()
        pygame.display.flip()

    def toiso(self, x, y):
        res = {x: '', y: ''}
        res["x"] = x*self.tilesize - y*self.tilesize
        res["y"] = (x*self.tilesize + y*self.tilesize)/2
        return res
       
cl = TCollectionItem(10,10)
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
cl.CreateBoard(levelArr)

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
    
   # if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
   #     cl.Player.Move('r')
   # if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
   #     cl.Player.Move('l')
   # if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
   #     cl.Player.Move('u')
   # if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
   #     cl.Player.Move('d')

    cl.ReDrawScreen()
