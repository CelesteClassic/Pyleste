import math
import numpy as np
class vector(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self, other):
        return vector(self.x+other.x,self.y+other.y)


def appr(val, target, amount):
    if val>target:
        return max(val-amount,target)
    return min(val+amount,target)
def sign(x):
    if(x>0):
        return 1
    if(x<0):
        return -1
    if(x==0):
        return 0
class player(object):
    def __init__(self,x,y,remx=0,remy=0,spdx=0,spdy=0):
        self.x=x
        self.y=y
        self.rem=vector(remx,remy)
        self.spd=vector(spdx,spdy)
        self.jump=False
    def update(self):
        maxfall=2
        gravity=0.21

        if abs(self.spd.y)<=0.15:
            gravity*=0.5

        on_ground = self.on_grnd(1)
        if not on_ground:
            self.spd.y=appr(self.spd.y,maxfall,gravity)
        if self.jump:
            self.spd.y=-2
            self.jump=False
    def move(self,ox,oy):
        self.rem.x+=ox
        amount=math.floor(self.rem.x+0.5)
        self.rem.x-=amount
        self.move_x(amount,0)
        self.rem.y+=oy
        amount = math.floor(self.rem.y + 0.5)
        self.rem.y -= amount
        self.move_y(amount)
    def move_x(self,amount,start):
        step = sign(amount)
        for i in range(start, abs(amount)+1):
            self.x += step
    def move_y(self,amount):
        step=sign(amount)
        for i in range(abs(amount)+1):
            if not self.on_grnd(step):
                self.y+=step
            else:
                self.spd.y=0
                self.rem.y=0
                break
    def __str__(self):
        return f"""
            ----------------------------------
            position: {self.x}, {self.y}
            rem values: {self.rem.x}, {self.rem.y}
            speed: {self.spd.x}, {self.spd.y}"""
    def on_grnd(self,dir):
        return False

if __name__ == '__main__':
  p = player(0, 0, 0, 0, 0, -2)
  for i in range(60):
    p.update()
    p.move(p.spd.x, p.spd.y)
    print(p.y, p.rem.y)