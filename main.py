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

        self.rect_X = 300
        self.rect_Y = 650

        self.rect_Width = 60
        self.rect_Height = 30

        self.enemies_rect_Width = 40
        self.enemies_rect_Height = 32

        self.enemies_red_image = pygame.image.load("assets/red.png")

        self.enemies_green_image = pygame.image.load("assets/green.png")

        self.enemies_yellow_image = pygame.image.load("assets/yellow.png")

        self.player_image = pygame.image.load("assets/player.png")

        self.counter = 0

        self.ruch = random.randint(30,60)

        self.shoot_counter = 0

        self.shoot_possible = True

        self.bullet_table = []

        self.space_pressed = 0

        self.enemies_table = [
            #[35,1000],[115,1000],[195,1000],[275,1000],[355,1000],[435,1000],

            #[35,50],[115,50],[195,50],[275,50],[355,50],[435,50],

            #[70,150],[150,150],[230,150],[310,150],[390,150],[470,150],

            #[35,250],[115,250],[195,250],[275,250],[355,250],[435,250]
        ]
        self.start_leyer(35,1000)

        self.start_leyer(35, typ="y")
        self.start_leyer(75,90,typ="g")
        self.start_leyer(35,130,"g")
        self.start_leyer(75,170,"r")
        self.start_leyer(35,210,"r")

        self.znak = "plus"

        self.punkty = 0

        
        

        self.typ_pietra = 0


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

            #pygame.draw.rect(self.screen,(0,0,0),self.kwadrat)

            self.screen.blit(self.player_image,self.kwadrat)


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

            
            

            pygame.display.flip()

            self.clock.tick(60)
    def shoot(self):
        if self.shoot_possible:
                self.bullet_table.append([self.rect_X+(self.rect_Width//2),self.rect_Y])
                self.shoot_possible=False
                self.shoot_counter=20
            

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
            
            
            print(self.punkty)           

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
        

        if self.enemies_table[39][0] + self.enemies_rect_Width*2 > self.window_width:
            self.znak = "minus"
            print(self.enemies_table[20])
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
        pass
    def game_over(self):
        pass
            




                
            




game = Game()

game.main_loop()