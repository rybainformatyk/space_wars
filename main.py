import pygame
import random

pygame.init()


class Game():
    def __init__(self) -> None:

        self.window_width = 600
        self.window_height = 720

        self.screen = pygame.display.set_mode((self.window_width,self.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("space_wars")

        self.rect_X = 300
        self.rect_Y = 650

        self.rect_Width = 50
        self.rect_Height = 50

        self.counter = 0

        self.ruch = random.randint(30,60)

        self.shoot_counter = 0

        self.shoot_possible = True

        self.bullet_table = []

        self.space_pressed = 0

        self.enemies_table = [
            [35,1000],[115,1000],[195,1000],[275,1000],[355,1000],[435,1000],

            [35,50],[115,50],[195,50],[275,50],[355,50],[435,50],

            [70,150],[150,150],[230,150],[310,150],[390,150],[470,150],

            [35,250],[115,250],[195,250],[275,250],[355,250],[435,250]
        ]

        self.znak = "plus"

        self.punkty = 0

        self.platforma = 0

        self.typ_pietra = 0

        self.ammunition = 10

        self.live = 3
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
            else:
                self.space_pressed = 0

            self.screen.fill("purple")


            self.kwadrat = pygame.Rect(self.rect_X,self.rect_Y,self.rect_Width,self.rect_Height)

            pygame.draw.rect(self.screen,(0,0,0),self.kwadrat)


            self.shoot_update()
            
            self.enemies()

            if self.counter == self.ruch:
                self.enem_move()
                self.counter = 0
                self.ruch = random.randint(30,60)
            
            self.shoot_counter-=1
            if self.shoot_counter <=0:
                self.shoot_possible=True

            self.counter +=1

            self.add_leyer()
            

            pygame.display.flip()

            self.clock.tick(60)
    def shoot(self):
        if self.shoot_possible:
            if self.ammunition > 0:
                self.bullet_table.append([self.rect_X+25,self.rect_Y])
                self.shoot_possible=False
                self.shoot_counter=20
                self.ammunition-=1
                print(self.ammunition)
            else:
                print("zabrakło amunicjii")

    def shoot_update(self):
        z1 = 0
        z2 = 0
        for i in range(len(self.bullet_table)):
            
            self.bullet_table[i][-1]-=5
            pocisk = pygame.Rect(self.bullet_table[i][0],self.bullet_table[i][1],8,8)
            pygame.draw.rect(self.screen,(0,0,0),pocisk)
            for j in range(len(self.enemies_table)):
                if self.bullet_table[i][0] >= self.enemies_table[j][0] and self.bullet_table[i][0] <= self.enemies_table[j][0]+50:
                    if self.bullet_table[i][1] >= self.enemies_table[j][1] and self.bullet_table[i][1] <= self.enemies_table[j][1] +50:
                        z1 = i
                        z2 = j
        if z2!= 0:
            self.bullet_table.pop(z1)
            self.enemies_table.pop(z2) 
            self.punkty +=1
            self.platforma +=1
            
            print(self.punkty)           

    def enemies(self):
        for i in range(len(self.enemies_table)):
            enem = pygame.Rect(self.enemies_table[i][0],self.enemies_table[i][1],50,50)
            pygame.draw.rect(self.screen,(0,254,0),enem)
    def enem_move(self):
        

        if self.enemies_table[5][0] + 50 > 600:
            self.znak = "minus"
        elif self.enemies_table[0][0] < 0:
            self.znak = "plus"
        for i in range(len(self.enemies_table)):
                if self.znak == "plus":
                    self.enemies_table[i][0] +=10
                else: 
                    self.enemies_table[i][0] -=10
                if self.enemies_table[i][1] >=600:
                    self.game_over()
    def add_leyer(self):
        if self.platforma >=6:
            if self.enemies_table[0][0] ==35:
            
            
                for i in range(len(self.enemies_table)):
                    self.enemies_table[i][1] +=70


                if self.typ_pietra == 0:
                    self.enemies_table.extend([[70,50],[150,50],[230,50],[310,50],[390,50],[470,50]])
                    self.typ_pietra =1
                elif self.typ_pietra ==1:
                    self.enemies_table.extend([[35,50],[115,50],[195,50],[275,50],[355,50],[435,50]])
                    self.typ_pietra = 0
            
                self.platforma = 0

                self.ammunition +=10

    def shoot_enemies(self):
        pass
    def game_over(self):
        pass
            




                
            




game = Game()

game.main_loop()