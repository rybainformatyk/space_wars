import pygame
import random

pygame.init()


class Game():
    def __init__(self) -> None:

        self.window_width = 1280
        self.window_height = 720

        self.screen = pygame.display.set_mode((self.window_width,self.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("space_wars")
        
        pygame.font.init()
        #pygame.font.SysFont("cabrit",32)
        self.font30 = pygame.font.Font(None,30)
        self.font60 = pygame.font.Font(None,60)
        self.font100 = pygame.font.Font(None,100)

        self.rect_Width = 60
        self.rect_Height = 30

        self.enemies_rect_Width = 40
        self.enemies_rect_Height = 32

        self.enemies_red_image = pygame.image.load("assets/red.png")

        self.enemies_green_image = pygame.image.load("assets/green.png")

        self.enemies_yellow_image = pygame.image.load("assets/yellow.png")

        self.player_image = pygame.image.load("assets/player.png")

        self.heart =  pygame.image.load("assets/heart.png")

        pygame.display.set_icon(self.enemies_red_image)

        self.rect_X = 300
        self.rect_Y = 650

        self.counter = 0

        self.counter2 = 0

        self.ruch = random.randint(30,60)

        self.shoot_counter = 0

        self.shoot_possible = True

        self.bullet_table = []

        self.bullet_enemy_table = []

        self.space_pressed = 0

        self.escape_pressed = 0

        self.enemies_table = []
        self.start_leyer(35,1000)

        self.start_leyer(35, typ="y")
        self.start_leyer(75,90,typ="g")
        self.start_leyer(35,130,"g")
        self.start_leyer(75,170,"r")
        self.start_leyer(35,210,"r")

        self.znak = "plus"

        self.punkty = 0

        self.play = 1
        

        self.typ_pietra = 0


        self.live = 3

        self.killed = 0

        self.best = 0

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                if self.rect_X != 0:
                    self.rect_X -= 10
            if key[pygame.K_RIGHT]:
                if self.rect_X+self.rect_Width != self.window_width:
                    self.rect_X += 10
    
            if key[pygame.K_SPACE]:
            
                if self.space_pressed == 0:
                    self.shoot()
                    self.space_pressed = 1
                if self.play==0:
                    self.reset()
            else:
                self.space_pressed = 0
            
            if key[pygame.K_ESCAPE]:
                if self.escape_pressed == 0:

                    print("escape")
                    if self.play == 1:
                        self.play =0
                        print("stop")
                    elif self.play == 0:
                        if self.live != 0:
                            self.play = 1
                            print("start")
                    self.escape_pressed = 1
            else:
                self.escape_pressed = 0


            self.screen.fill("purple")

            if self.play:
            
                self.gracz()

                self.shoot_update()

                self.shoot_enemy_update()
            
                self.enemies()

                self.liczniki()

                self.wskazniki()
            else:
                if self.live == 0:
                    self.game_over()
                else:
                    self.przerwa()

            
            
            

            pygame.display.flip()

            self.clock.tick(60)
    def shoot(self):
        if self.shoot_possible:
                self.bullet_table.append([self.rect_X+(self.rect_Width//2),self.rect_Y])
                self.shoot_possible=False
                self.shoot_counter=20
    def przerwa(self):
        pp = self.font60.render("PAUSED",True,(0,0,0))
        self.screen.blit(pp,(self.window_width//2-pp.get_width()//2 , self.window_height//2-pp.get_height()//2))

        hel = self.font60.render("HELP",True,(0,0,0))
        self.screen.blit(hel,(20,20))

        lewo = self.font30.render("<-- - w lewo",True,(0,0,0))
        self.screen.blit(lewo,(20,80))

        prawo = self.font30.render("--> - w prawo",True,(0,0,0))
        self.screen.blit(prawo,(20,100))

        strzal = self.font30.render("space - strzał",True,(0,0,0))
        self.screen.blit(strzal,(20,120))
    
    def gracz(self):
        self.kwadrat = pygame.Rect(self.rect_X,self.rect_Y,self.rect_Width,self.rect_Height)

        #pygame.draw.rect(self.screen,(0,0,0),self.kwadrat)

        self.screen.blit(self.player_image,self.kwadrat)
    
    def liczniki(self):
        self.counter +=1

        self.counter2 +=1

        self.shoot_counter-=1


        if self.counter == self.ruch:
                self.enem_move()
                self.counter = 0
                self.ruch = random.randint(30,60)
            
            
        if self.shoot_counter <=0:
                self.shoot_possible=True

            
        if self.counter2 == 60:
                self.shoot_enemies()
                self.counter2=0
        if self.killed ==100:
            self.reset(self.punkty)
            self.killed=0
    def wskazniki(self):
        punk = self.font30.render(f"SCORE: {str(self.punkty)}",True,(0,0,0))
        self.screen.blit(punk,(self.window_width//2-punk.get_width()//2,20))

        zycia = self.font30.render(str(self.live),True,(0,0,0))
        self.screen.blit(zycia,(self.window_width -20 -zycia.get_width(),20))

        for i in range(self.live,0,-1):
            self.screen.blit(self.heart,(self.window_width -20 -(45*i) -20,5))

        
        ll = open("best.txt").readline().strip()
        self.best = int(ll)
        
        zycia = self.font30.render(f"BEST SCORE: {str(self.best)}",True,(0,0,0))
        self.screen.blit(zycia,(20,20))

    


    def shoot_update(self):
        z1 = 0
        z2 = 0
        for i in range(len(self.bullet_table)):
            
            self.bullet_table[i][-1]-=5
            pocisk = pygame.Rect(self.bullet_table[i][0],self.bullet_table[i][1],8,8)
            pygame.draw.rect(self.screen,(0,0,0),pocisk)
            for j in range(len(self.enemies_table)):
                if self.bullet_table[i][0] >= self.enemies_table[j][0] and self.bullet_table[i][0] <= self.enemies_table[j][0]+self.enemies_rect_Width:
                    if self.bullet_table[i][1] >= self.enemies_table[j][1] and self.bullet_table[i][1] <= self.enemies_table[j][1] +self.enemies_rect_Width:
                        z1 = i
                        z2 = j
        if z2!= 0:
            self.bullet_table.pop(z1)
            self.enemies_table.pop(z2) 
            self.punkty +=1
            self.killed +=1
            
            
            
            print("punkty: ",self.punkty)  
            print("zab ",self.killed)          

    def enemies(self):
        for i in range(len(self.enemies_table)):
            enem = pygame.Rect(self.enemies_table[i][0],self.enemies_table[i][1],self.enemies_rect_Width,self.enemies_rect_Height)
            #pygame.draw.rect(self.screen,(0,254,0),enem)
            if self.enemies_table[i][2] == "r":
                self.screen.blit(self.enemies_red_image,enem)
            elif self.enemies_table[i][2] == "g":
                self.screen.blit(self.enemies_green_image,enem)
            elif self.enemies_table[i][2] == "y":
                self.screen.blit(self.enemies_yellow_image,enem)
            
    def enem_move(self):
        

        if self.enemies_table[19][0] + self.enemies_rect_Width*2 > self.window_width:
            self.znak = "minus"
            self.down()
            
        elif self.enemies_table[0][0] < 0:
            self.znak = "plus"
            self.down()
            
        for i in range(len(self.enemies_table)):
                if self.znak == "plus":
                    self.enemies_table[i][0] +=10
                else: 
                    self.enemies_table[i][0] -=10
                if self.enemies_table[i][1] >=self.window_width:
                    self.game_over()
    def down(self):
        for i in range(len(self.enemies_table)):
            self.enemies_table[i][1] +=20

                


    # def add_leyer(self):         
    #             for i in range(len(self.enemies_table)):
    #                 self.enemies_table[i][1] +=50


    #             if self.typ_pietra == 0:
    #                 self.start_leyer(105)
    #                 self.typ_pietra =1
    #             elif self.typ_pietra ==1:
    #                 self.start_leyer(35)
    #                 self.typ_pietra = 0
            
                
                
    def start_leyer(self,start,wysokosc=50,typ="r"):
        for i in range(20):
            self.enemies_table.append([start+i*60,wysokosc,typ])

                

    def shoot_enemies(self):
        przeciwnik = random.choice(self.enemies_table)
        self.bullet_enemy_table.append([przeciwnik[0]+(self.enemies_rect_Width//2),przeciwnik[1]])
    def shoot_enemy_update(self):
        z1 = 0
        z2 = 0
        for i in range(len(self.bullet_enemy_table)):
            
            self.bullet_enemy_table[i][-1]+=5
            pocisk = pygame.Rect(self.bullet_enemy_table[i][0],self.bullet_enemy_table[i][1],8,8)
            pygame.draw.rect(self.screen,(0,0,0),pocisk)
            
            if self.bullet_enemy_table[i][0] >= self.rect_X and self.bullet_enemy_table[i][0] <= self.rect_X+self.rect_Width:
                    if self.bullet_enemy_table[i][1] >= self.rect_Y and self.bullet_enemy_table[i][1] <= self.rect_Y+self.rect_Height:
                        z1 = i
                        z2 = 1
                        
        if z2!= 0:
            self.bullet_enemy_table.pop(z1)
            
            self.live-=1
            print("zycia: ",self.live)
            if self.live==0:
                self.game_over()

    def game_over(self):
        napis = self.font100.render("Game Over",True,(0,0,0))
        self.screen.blit(napis,(self.window_width//2 - napis.get_width()//2,300))

        napis2 = self.font60.render(f"score: {self.punkty}",True,(0,0,0))
        self.screen.blit(napis2,(self.window_width//2 - napis2.get_width()//2,380))

        napis3 = self.font60.render(f"press SPACE to replay",True,(0,0,0))
        self.screen.blit(napis3,(self.window_width//2 - napis3.get_width()//2,450))

        self.play=0

        if self.punkty > self.best:
            open("best.txt","w").write(f"{self.punkty}")
            

    def reset(self,punk = 0):

        self.rect_X = 300
        self.rect_Y = 650

        self.counter = 0

        self.counter2 = 0

        self.ruch = random.randint(30,60)

        self.shoot_counter = 0

        self.shoot_possible = True

        self.bullet_table = []

        self.bullet_enemy_table = []

        self.space_pressed = 0

        self.enemies_table = []
        self.start_leyer(35,1000)

        self.start_leyer(35, typ="y")
        self.start_leyer(75,90,typ="g")
        self.start_leyer(35,130,"g")
        self.start_leyer(75,170,"r")
        self.start_leyer(35,210,"r")

        self.znak = "plus"

        self.punkty = punk

        self.play = 1
        

        self.typ_pietra = 0



        
            




                
            




game = Game()

game.main_loop()