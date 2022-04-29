from cgitb import text
import pygame
from pygame.math import Vector2 
import random



pygame.init()

ALTO = 480
ANCHO = 720
WIN = pygame.display.set_mode((ANCHO,ALTO))
SCORE_TEXT = pygame.font.SysFont("Russo One",15)

class Snake: #Serpiente.
    def __init__(self):
        self.body = [Vector2(10,100),Vector2(10,110),Vector2(10,120)]
        self.direction = Vector2(0,-10)
        self.add = False

    def draw(self):
        for bloque in self.body:
            pygame.draw.rect(WIN,(0,255,0),(bloque.x,bloque.y,10,10))

    def move(self): #Movimiento

        #[0,1,2] --> [0,1] --> [None,0,1] --> [-1,0,1]
        if  self.add == True:
             body_copy = self.body
             body_copy.insert(0,body_copy[0]+self.direction)
             self.body = body_copy[:]
             self.add = False
        else:
             body_copy = self.body[:-1]
             body_copy.insert(0,body_copy[0]+self.direction)
             self.body = body_copy[:]

    def move_up(self):
        self.direction = Vector2(0,-10)

    def move_down(self):
        self.direction = Vector2(0,10)

    def move_right(self):
        self.direction = Vector2(10,0)

    def move_left(self):
        self.direction = Vector2(-10,0)
    
    def die(self): #Muerte 
        if self.body[0].x >= ANCHO+10 or self.body[0].y >= ALTO+10 or self.body[0].x <= -10 or self.body[0].y <= -10:
            return True

        #Snake se toca a si misma.
        for i in self.body[1:]:
            if self.body[0] == i:
                return True 

class Apple:
    def __init__(self):
        self.generate()

    def draw(self):
        pygame.draw.rect(WIN,(255,0,0),(self.pos.x,self.pos.y,10,10))

    def generate(self):
        self.x = random.randrange(0,ANCHO/10)
        self.y = random.randrange(0,ALTO/10)
        self.pos = Vector2(self.x*10,self.y*10)

    def check_collision(self,snake):
        if snake.body[0] == self.pos:

            self.generate()
            snake.add = True

            return True

        for bloque in snake.body[1:]:
            if bloque == self.pos:
                self.generate()

        return False

        
def main (): #Configuracion.

    snake = Snake()
    apple = Apple()
    score = 0

    fps = pygame.time.Clock()

    while True:

        fps.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN and snake.direction.y != 10:
                if event.key == pygame.K_UP:
                    snake.move_up()
            
            if event.type == pygame.KEYDOWN and snake.direction.y != -10:
                if event.key == pygame.K_DOWN:
                    snake.move_down()

            if event.type == pygame.KEYDOWN and snake.direction.x != -10:
                if event.key == pygame.K_RIGHT:
                    snake.move_right()

            if event.type == pygame.KEYDOWN and snake.direction.x != 10:
                if event.key == pygame.K_LEFT:
                    snake.move_left()



        WIN.fill((0,0,0))
        snake.draw()
        apple.draw()

        snake.move()

        if snake.die():
            quit()

        if apple.check_collision(snake):
            score+=1
            
        text = SCORE_TEXT.render("Score: {}".format(score),1,(255,255,255))
        WIN.blit(text,(ANCHO-text.get_width()-10,10))
        pygame.display.update()        

main ()