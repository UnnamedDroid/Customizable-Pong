import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 700, 500

BALL_RADIUS = 7
BALL_MAXVEL = 5

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

Custom = input("Do you want to customize the game (y/n)\n")
if Custom == "":
    Custom = "n"
elif Custom == "y":
    #colour 
    c_input = input("What colour do you want? (insert answer in all caps) \n-WHITE\n-RED\n-GREEN\n-BLUE\n-YELLOW\n-MAGENTA\n\nDefault : WHITE\n")
    if c_input == "":
        WHITE = (255, 255, 255)
    elif c_input == "RED":
        WHITE = (255, 0, 0)
    elif c_input == "GREEN":
        WHITE = (0, 255, 0)
    elif c_input == "BLUE":
        WHITE = (0, 0, 255)
    elif c_input == "YELLOW":
        WHITE = (255, 255, 0)
    elif c_input == "MAGENTA":
        WHITE = (255, 0, 255)
    # size x
    c_input = input("What scale do you wish the game to be (X scale)\nDefault : 700\n")
    if c_input == "":
        WIDTH = 700
    elif c_input.isdigit():
        WIDTH = int(c_input)
    # y
    c_input = input("What scale do you wish the game to be (Y scale)\nDefault : 500\n")
    if c_input == "":
        HEIGHT = 500
    elif c_input.isdigit():
        HEIGHT = int(c_input)
    # size of ball
    c_input = input("How big do you want the ball to be? (3-18)\nDefault : 7\n")
    if c_input == "":
        BALL_RADIUS = 7
    elif c_input.isdigit():
        BALL_RADIUS = clamp(int(c_input), 3, 18)
    # speed of ball
    c_input = input("How fast do you want the ball to go? (3-20)\nDefault : 7\n")
    if c_input == "":
        BALL_MAXVEL = 5
    elif c_input.isdigit():
        BALL_MAXVEL = clamp(int(c_input), 3, 20)
        



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong in Python")

FPS = 60



PADDLE_WIDTH, PADDLE_HEIGHT = 20,100



LINE_WIDTH = 10

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
       
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

class Ball:
    MAX_VEL = BALL_MAXVEL
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y),self.radius)

    def move(self, win):
        self.x += self.x_vel
        self.y += self.y_vel

def draw(win, paddles, ball, L, R):
    win.fill(BLACK)

    leftScoreText = SCORE_FONT.render(f"{L}", 1, WHITE)
    rightScoreText = SCORE_FONT.render(f"{R}", 1, WHITE)

    win.blit(leftScoreText, (WIDTH//4 - leftScoreText.get_width()//2, 20))
    win.blit(rightScoreText, (WIDTH * (3/4) - rightScoreText.get_width()//2, 20))


    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(WIN, WHITE, (WIDTH//2 - LINE_WIDTH//2, i, LINE_WIDTH, HEIGHT//50))
    ball.draw(win)
    pygame.display.update()

def handle_ball_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        # right paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                dif_in_y = middle_y - ball.y
                red_fact = (left_paddle.height /2) / ball.MAX_VEL
                y_vel = dif_in_y / red_fact
                ball.y_vel = -1 * y_vel
    else: 
        # right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                dif_in_y = middle_y - ball.y
                red_fact = (right_paddle.height /2) / ball.MAX_VEL
                y_vel = dif_in_y / red_fact
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    L_score = 0
    R_score = 0

    while run:
        clock.tick(FPS)

        draw(WIN, [left_paddle, right_paddle], ball, L_score, R_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move(WIN)
        handle_ball_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            R_score += 1
            ball.x, ball.y = WIDTH//2, HEIGHT//2
            ball.y_vel, ball.x_vel = 0, BALL_MAXVEL
        elif ball.x > WIDTH:
            L_score += 1
            ball.x, ball.y = WIDTH//2, HEIGHT//2
            ball.y_vel, ball.x_vel = 0, BALL_MAXVEL * -1

    pygame.quit()

if __name__ == "__main__":
    main()
