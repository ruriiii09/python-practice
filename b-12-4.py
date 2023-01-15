import pyxel

class Ball:
    speed = 1

    def __init__(self):
        self.x = pyxel.rndi(0, 199)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self):
        self.x += self.vx * Ball.speed
        self.y += self.vy * Ball.speed
        if self.x<=0 or self.x>= 200:
            self.vx= -self.vx

    def restart(self):
        self.x = pyxel.rndi(0, 199)    #0から画面の横幅-1の間
        self.y = 0
        angle = pyxel.rndi(30, 150)    #30度から150度の間
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

class Pad:
    def __init__(self):
        self.size =40
        self.x = 100

    def catch(self, ball):
        if ball.y >= 195:
            if self.x - self.size/2 <= ball.x:
                if ball.x <= self.x + self.size/2:
                    return True
        else:
            return False

class App:
    def __init__(self):
        pyxel.init(200,200)
        self.pad = Pad()
        self.score=0
        self.a=0
        self.i=0
        self.m=0
        self.pad.x = pyxel.mouse_x
        self.state = True
        self.balls =[Ball(), Ball(), Ball()]
        pyxel.run(self.update, self.draw)


    def update(self):
        if self.state == False:
           return
        self.pad.x = pyxel.mouse_x
        for b in self.balls:
            b.move()
            if self.pad.catch(b):
                self.score += 1
                Ball.speed += 1
                b.restart()

            if b.y >= 200:
                b.restart()
                self.m += 1
                if self.m == 5:
                    self.state = False

    def draw(self):
        pyxel.cls(7)
        if self.state ==False:
            pyxel.text(100, 100,'Game Over',0)
        self.r='SCORE:'
        self.s=self.r+str(self.score)
        for b in self.balls:
            pyxel.circ(b.x,b.y,10,6)
        pyxel.text(10, 10, self.s, 0)
        pyxel.rect(self.pad.x-20, 195, 40, 5, 14)

App()
