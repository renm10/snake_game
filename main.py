import pygame
import random
import sys #For sys.exit() -> quitting the program

SIZE = 10 #Size of the snake block
WIDTH, HEIGHT = 720, 480 #Width / Height of window
FPS = 10 #Frame per second

#Snake Class
class Snake:
    def __init__(self):
        self.x, self.y = (WIDTH / 2), (HEIGHT / 2)
        self.velocityx = 10 # Move to the right by default
        self.velocityy = 0 # Doesn't move up or down 
        self.head = [WIDTH / 2, HEIGHT / 2] #Starting Position
        self.body = [[(WIDTH / 2) - SIZE, HEIGHT / 2]] #Starting Position of body (moving right)

    def updateHead(self):
        self.head[0] += self.velocityx
        self.head[1] += self.velocityy

    def updateBody(self):
        self.body.insert(0, [self.head[0], self.head[1]])
        self.body.pop()
       
def drawSnakeHead(snake_head):
    pygame.draw.rect(screen, dgreen, pygame.Rect(snake_head[0], snake_head[1], SIZE, SIZE))

def drawSnakeBody(snake_body):
    for body in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(body[0], body[1], SIZE, SIZE))

#Colors 
white = (255, 255, 240)
green = (152, 216, 170)
dgreen = (123, 173, 137)
red = (255, 109, 96)
orange = (255,144,0)
lightyellow = (243, 233, 159)
yellow = (247, 208, 96)

#Setup pygame
pygame.init()
pygame.font.init()

#Font
scorefont = pygame.font.Font(None, 36)
fontbig = pygame.font.Font(None, 120)
fontmed = pygame.font.Font(None, 60)
fontsmall = pygame.font.Font(None, 50)

#Displays a given text to the screen
def displayText(msg, font, color, y):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH / 2, y))
    screen.blit(text, text_rect)

#Initialize window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

#Snake Game main loop
def playGame():
    score = 0
    clock = pygame.time.Clock()
    gameOver = False
    fruit_pos = [random.randint(0, (WIDTH - SIZE) / 10) * 10, random.randint(0, (HEIGHT - SIZE) / 10) * 10] #-10 bc block is itself 10 units
    snake = Snake()

    #Direction (For preventing users to move the opposite (180 degrees) way when moving in a direction)
    right = True
    left = False
    up = False
    down = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #When user x's out of the window
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: #Checks the opposite direction of the current direction
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and right != True:
                    snake.velocityx = -10
                    snake.velocityy = 0
                    right = False
                    left = True
                    up = False
                    down = False
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and left != True:
                    snake.velocityx = 10
                    snake.velocityy = 0
                    right = True
                    left = False
                    up = False
                    down = False
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and down != True:
                    snake.velocityx = 0
                    snake.velocityy = -10
                    right = False
                    left = False
                    up = True
                    down = False
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and up != True:
                    snake.velocityx = 0
                    snake.velocityy = 10
                    right = False
                    left = False
                    up = False
                    down = True


        # Player gets Fruit => Grow the snake and increase score by 10
        if snake.head == fruit_pos: # When player gets the fruit, move it somewhere else randomly
            fruit_pos = [random.randint(0, (WIDTH - SIZE) / 10) * 10, random.randint(0, (HEIGHT - SIZE) / 10) * 10]
            score += 10
            snake.body.append([(snake.body[-1][0] + SIZE), (snake.body[-1][1] + SIZE)])

        # Update Head and Body
        snake.updateBody()
        snake.updateHead()
        

        # Check player if it doesn't hit the boundaries
        if snake.head[0] < 0 or snake.head[0] > WIDTH or snake.head[1] < 0 or snake.head[1] > HEIGHT:
            gameOver = True
        
        # Check player if it doesn't hit his own body
        for body in snake.body: 
            if snake.head[0] == body[0] and snake.head[1] == body[1]:
                gameOver = True

        screen.fill(white)

        #Draw player
        drawSnakeHead(snake.head)
        drawSnakeBody(snake.body)

        #Spawn Fruit
        pygame.draw.rect(screen, red, pygame.Rect(fruit_pos[0], fruit_pos[1], SIZE, SIZE))

        # Draw the score to the screen
        score_text = scorefont.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if gameOver:
            screen.fill(white)
            displayText('Game Over!', fontbig, green, 230)
            displayText('BACK [SPACE]', fontsmall, red, 300)
            displayText('QUIT [Q]', fontsmall, red, 350)
    
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type ==  pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_SPACE:
                            mainMenu()

        pygame.display.update()

        clock.tick(FPS)

#Main Menu Loop 
def mainMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If player x's out of the window
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #Start the game 
                    playGame()
        
        screen.fill(white)
        displayText('SNAKE GAME', fontbig, green, 200)
        displayText('- Press \'Space\' to Start -', fontmed, red, 300)

        pygame.display.update()

mainMenu()

pygame.quit()
sys.exit()