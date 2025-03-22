import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Web")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AZUL = (0, 102, 204)

font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 60)

# Entrada de nombre con cuadro
nombre_jugador = ""
input_active = True
input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)

# Fondo y música
try:
    fondo = pygame.image.load("fondo_pingpong.png")
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
except:
    fondo = None

try:
    pygame.mixer.music.load("musica_fondo.mp3")
    musica_disponible = True
except:
    musica_disponible = False

pygame.mixer.music.set_volume(0.4)

# Ingreso del nombre
while input_active:
    screen.fill(BLACK)
    prompt = font.render("Ingresa tu nombre:", True, WHITE)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 100))
    pygame.draw.rect(screen, WHITE, input_box, 2)
    nombre_surface = input_font.render(nombre_jugador, True, WHITE)
    screen.blit(nombre_surface, (input_box.x + 10, input_box.y + 10))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and nombre_jugador.strip():
                input_active = False
                if musica_disponible:
                    pygame.mixer.music.play(-1)
            elif event.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            else:
                if len(nombre_jugador) < 15:
                    nombre_jugador += event.unicode

if not nombre_jugador:
    nombre_jugador = "Jugador"

BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5 * random.choice((1, -1))
ball_dy = 5 * random.choice((1, -1))

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
paddle_speed = 7

player1_x = 30
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_x = WIDTH - 45
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

score1 = 0
score2 = 0

inicio_tiempo = time.time()
paused = False
pause_button = pygame.Rect(WIDTH - 70, 10, 40, 40)

running = True
start_time = time.time()
max_duration = 150

while running:
    if fondo:
        screen.blit(fondo, (0, 0))
    else:
        screen.fill((20, 20, 40))

    pygame.draw.circle(screen, WHITE, pause_button.center, 20, 2)
    pygame.draw.rect(screen, WHITE, (pause_button.centerx - 6, pause_button.centery - 10, 4, 20))
    pygame.draw.rect(screen, WHITE, (pause_button.centerx + 2, pause_button.centery - 10, 4, 20))

    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, y, 4, 10))

    pygame.draw.rect(screen, AZUL, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, AZUL, (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    if not paused:
        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
            ball_dy *= -1

        if (ball_x - BALL_RADIUS <= player1_x + PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or            (ball_x + BALL_RADIUS >= player2_x and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
            ball_dx *= -1

        if ball_x < 0:
            score2 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = 5 * random.choice((1, -1))
            ball_dy = 5 * random.choice((1, -1))
            paddle_speed = 7
            inicio_tiempo = time.time()

        if ball_x > WIDTH:
            score1 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = 5 * random.choice((1, -1))
            ball_dy = 5 * random.choice((1, -1))
            paddle_speed = 7
            inicio_tiempo = time.time()

        if time.time() - inicio_tiempo >= 10:
            ball_dx += 1 if ball_dx > 0 else -1
            ball_dy += 1 if ball_dy > 0 else -1
            paddle_speed += 1
            inicio_tiempo = time.time()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= paddle_speed
    if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
        player1_y += paddle_speed

    delay = random.randint(0, 5)
    if random.random() < 0.05:
        pass
    elif random.random() < 0.05:
        player2_y += random.choice([-1, 1]) * paddle_speed
    elif ball_x > WIDTH // 2:
        if ball_y > player2_y + PADDLE_HEIGHT // 2 + delay:
            player2_y += paddle_speed
        elif ball_y < player2_y + PADDLE_HEIGHT // 2 - delay:
            player2_y -= paddle_speed

    score_text = font.render(f"{nombre_jugador} {score1} - {score2} IA", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    if paused:
        pause_text = font.render("PAUSA", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 25))

    tiempo_restante = max(0, int(max_duration - (time.time() - start_time)))
    tiempo_texto = font.render(f"Tiempo: {tiempo_restante // 60}:{tiempo_restante % 60:02}", True, WHITE)
    screen.blit(tiempo_texto, (20, 20))

    if time.time() - start_time >= max_duration:
        ganador = "Empate" if score1 == score2 else nombre_jugador if score1 > score2 else "IA"
        end_text = font.render(f"Ganador: {ganador}", True, WHITE)
        screen.fill(BLACK)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 25))
        pygame.display.flip()
        pygame.time.wait(4000)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos):
                paused = not paused

    pygame.display.flip()
    clock.tick(60)

if musica_disponible:
    pygame.mixer.music.stop()
pygame.quit()
