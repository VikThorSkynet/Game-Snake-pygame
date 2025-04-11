# -*- coding: utf-8 -*-
import pygame
import sys
import random
import json
import math

# --- Configurações ---
pygame.init()
pygame.font.init()
# --- Configuração de Sons ---
pygame.mixer.init()
# Indique o caminho para seus arquivos de som aqui
EAT_SOUND = pygame.mixer.Sound('comer.wav')
WALL_CREATE_SOUND = pygame.mixer.Sound('criarparede.wav')
WALL_DESTROY_SOUND = pygame.mixer.Sound('destruirparede.wav')

# Música de fundo
pygame.mixer.music.load('musicabackgroundmusic.mp3')
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Cores Neon Melhoradas
COLOR_BLACK = (0, 0, 0)
COLOR_DARK_BG = (5, 5, 10)  # Fundo um pouco mais claro que preto puro
COLOR_NEON_GREEN = (0, 255, 100)
COLOR_NEON_GREEN_DARK = (0, 180, 70)  # Para gradiente
COLOR_GRAY = (150, 150, 150)
COLOR_GRAY_GLOW = (180, 180, 180)  # Para efeito de brilho
COLOR_BLUE = (5, 5, 255)
COLOR_BLUE_GLOW = (40, 40, 255)  # Para efeito de brilho
COLOR_RED = (255, 0, 100)
COLOR_RED_GLOW = (255, 40, 140)  # Para efeito de brilho
COLOR_WHITE = (240, 240, 240)
COLOR_BUTTON_TEXT = (200, 200, 200)
COLOR_GRID_LINE = (20, 20, 30)  # Linhas de grade sutis
COLOR_YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Neon Snake Game')
clock = pygame.time.Clock()
INITIAL_FPS = 7
FPS_INCREMENT = 0.17

# Fontes - Tente carregar fontes mais estilizadas se disponíveis
try:
    font_score = pygame.font.Font(None, 35)
    font_title = pygame.font.Font(None, 70)
    font_menu = pygame.font.Font(None, 50)
    font_button = pygame.font.Font(None, 40)
    font_info = pygame.font.Font(None, 28)
    font_input = pygame.font.Font(None, 40)
except pygame.error:
    font_score = pygame.font.SysFont('arial', 25)
    font_title = pygame.font.SysFont('arial', 50)
    font_menu = pygame.font.SysFont('arial', 40)
    font_button = pygame.font.SysFont('arial', 30)
    font_info = pygame.font.SysFont('arial', 20)
    font_input = pygame.font.SysFont('arial', 30)

# --- Configuração do Scoreboard ---
SCOREBOARD_FILE = 'neon_snake_scoreboard.json'
MAX_SCORES = 10

# --- Efeitos visuais ---
# Partículas para efeitos
particles = []
particle_timer = 0

# Pulsação para elementos neon
pulse_value = 0
pulse_direction = 1
pulse_speed = 0.05

# Variável para controlar o estado da música
music_playing = True

# Vinheta para bordas da tela
def create_vignette_surface(width, height, intensity=0.7):
    """Cria uma superfície com efeito de vinheta (escurece as bordas)"""
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        for x in range(width):
            # Calcula distância normalizada do centro
            distance_x = (x / width - 0.5) * 2
            distance_y = (y / height - 0.5) * 2
            distance = min(0.5, math.sqrt(distance_x**2 + distance_y**2))
            # Aplica curva de intensidade
            alpha = int(255 * (distance ** intensity))
            vignette.set_at((x, y), (0, 0, 0, alpha))
    return vignette

# Cria a superfície de vinheta uma vez
vignette_surface = create_vignette_surface(SCREEN_WIDTH, SCREEN_HEIGHT)

# Classe para partículas
class Particle:
    def __init__(self, x, y, color, size=3, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        # Diminui tamanho conforme envelhece
        self.size = max(0, self.size * (self.life / self.max_life))
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(
            surface,
            color_with_alpha,
            (int(self.x), int(self.y)),
            int(self.size)
        )

def add_particles(x, y, color, count=10, size=3, life=30):
    """Adiciona partículas na posição especificada"""
    for _ in range(count):
        particles.append(Particle(x, y, color, size, life))

def update_particles():
    """Atualiza todas as partículas"""
    global particles
    particles = [p for p in particles if p.update()]

def draw_particles(surface):
    """Desenha todas as partículas"""
    for p in particles:
        p.draw(surface)

def load_scoreboard():
    try:
        with open(SCOREBOARD_FILE, 'r') as f:
            board = json.load(f)
            board.sort(key=lambda item: item['score'], reverse=True)
            return board
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_scoreboard(board):
    try:
        with open(SCOREBOARD_FILE, 'w') as f:
            json.dump(board, f, indent=4)
    except IOError as e:
        print(f"Erro ao salvar scoreboard: {e}")

def add_score(board, name, score):
    board.append({'name': name, 'score': score})
    board.sort(key=lambda item: item['score'], reverse=True)
    return board[:MAX_SCORES]

# Carrega o scoreboard ao iniciar
scoreboard = load_scoreboard()

# --- Funções de Desenho Melhoradas ---
def draw_grid(surface):
    """Desenha linhas de grade sutis"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID_LINE, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID_LINE, (0, y), (SCREEN_WIDTH, y), 1)

def draw_element_with_glow(surface, color, glow_color, position, glow_size=0.5):
    """Desenha um elemento com efeito de brilho"""
    x, y = position
    # Desenha o brilho (maior e mais transparente)
    glow_rect = pygame.Rect(
        (x * GRID_SIZE) - (GRID_SIZE * (glow_size-1))/2,
        (y * GRID_SIZE) - (GRID_SIZE * (glow_size-1))/2,
        GRID_SIZE * glow_size,
        GRID_SIZE * glow_size
    )

    # Cria uma superfície para o brilho com canal alpha
    glow_surf = pygame.Surface((int(GRID_SIZE * glow_size), int(GRID_SIZE * glow_size)), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*glow_color[:3], 20), glow_surf.get_rect(), border_radius=int(GRID_SIZE/3))
    surface.blit(glow_surf, glow_rect)

    # Desenha o elemento principal
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect, border_radius=int(GRID_SIZE/5))

def draw_element(surface, color, position):
    """Desenha um bloco do grid."""
    if position[0] < 0 or position[0] >= GRID_WIDTH or position[1] < 0 or position[1] >= GRID_HEIGHT: return
    rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect, border_radius=int(GRID_SIZE/5))

def draw_snake(surface, snake_segments):
    """Desenha a cobra com efeito de gradiente e brilho"""
    # Desenha o brilho para a cabeça
    if snake_segments:
        head = snake_segments[0]
        draw_element_with_glow(surface, COLOR_NEON_GREEN, COLOR_NEON_GREEN, head, 1.5)

    # Desenha o corpo com gradiente
    for i, segment in enumerate(snake_segments[1:], 1):
        # Calcula cor com base na posição (mais escuro conforme se afasta da cabeça)
        fade = min(1.0, i / len(snake_segments) * 1.5)
        r = int(COLOR_NEON_GREEN[0])
        g = int(COLOR_NEON_GREEN[1] * (1 - fade * 0.5))
        b = int(COLOR_NEON_GREEN[2] * (1 - fade * 0.7))
        segment_color = (r, g, b)
        draw_element(surface, segment_color, segment)

def draw_food(surface, food):
    """Desenha a comida (azul ou vermelha) com efeito de brilho e pulsação"""
    if food and food.get('pos'):
        pos = food['pos']
        food_type = food.get('type', 'blue')

        # Aplica pulsação ao tamanho do brilho
        pulse_mod = 0.2 * math.sin(pulse_value) + 1.0

        if food_type == 'blue':
            # Comida azul com brilho pulsante
            draw_element_with_glow(surface, COLOR_BLUE, COLOR_BLUE_GLOW, pos, 1.3 + pulse_mod)
        else:
            # Comida vermelha com brilho pulsante
            draw_element_with_glow(surface, COLOR_RED, COLOR_RED_GLOW, pos, 1.3 + pulse_mod)

def draw_walls(surface, walls):
    """Desenha as paredes com efeito de brilho"""
    for wall_pos in walls:
        draw_element_with_glow(surface, COLOR_GRAY, COLOR_GRAY_GLOW, wall_pos, 1.1)

def draw_text_with_shadow(surface, text, font, color, position, shadow_offset=2, center=False):
    """Desenha texto com sombra para melhor legibilidade"""
    # Sombra
    shadow_pos = (position[0] + shadow_offset, position[1] + shadow_offset)
    shadow_color = (0, 0, 0)
    text_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = shadow_pos
    else:
        text_rect.topleft = shadow_pos
    surface.blit(text_surface, text_rect)

    # Texto principal
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = position
    else:
        text_rect.topleft = position
    surface.blit(text_surface, text_rect)

def draw_text(surface, text, font, color, position, center=False):
    """Desenha texto na tela com sombra para melhor legibilidade"""
    draw_text_with_shadow(surface, text, font, color, position, 2, center)

def draw_button(surface, text, font, text_color, button_color, rect, center_text=True, hover=False):
    """Desenha um botão com efeito hover"""
    # Efeito de brilho se hover
    if hover:
        glow_rect = rect.copy()
        glow_rect.inflate_ip(10, 10)
        pygame.draw.rect(surface, button_color, glow_rect, border_radius=10, width=2)

    # Botão principal
    pygame.draw.rect(surface, button_color, rect, border_radius=8)

    # Gradiente sutil (linha mais clara no topo)
    highlight_rect = rect.copy()
    highlight_rect.height = rect.height // 4
    pygame.draw.rect(surface, (min(255, button_color[0] + 30),
                              min(255, button_color[1] + 30),
                              min(255, button_color[2] + 30)),
                    highlight_rect, border_radius=8, width=0)

    # Texto
    draw_text(surface, text, font, text_color, rect.center, center=center_text)

def draw_scoreboard(surface, board):
    """Desenha o placar no lado esquerdo com estilo melhorado"""
    # Fundo semi-transparente
    score_bg = pygame.Surface((SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 40), pygame.SRCALPHA)
    score_bg.fill((20, 20, 30, 150))
    surface.blit(score_bg, (10, 20))

    # Borda neon
    pygame.draw.rect(surface, COLOR_NEON_GREEN,
                    pygame.Rect(10, 20, SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 40),
                    width=2, border_radius=10)

    title_y = 30
    score_y = title_y + 50
    line_height = 30
    x_pos = 25

    # Título com efeito neon
    draw_text_with_shadow(surface, "HIGH SCORES", font_button, COLOR_NEON_GREEN, (x_pos, title_y))

    # Linha divisória
    pygame.draw.line(surface, COLOR_NEON_GREEN,
                    (x_pos, title_y + 35),
                    (SCREEN_WIDTH // 2 - 35, title_y + 35), 2)

    # Entradas do placar
    for i, entry in enumerate(board):
        name = entry.get('name', '???')[:15]
        score_val = entry.get('score', 0)

        # Destaque para os 3 primeiros
        if i < 3:
            text_color = (255, 255, 100) if i == 0 else (220, 220, 220)
            text = f"{i+1}. {name:<15} {score_val:>5}"
            draw_text_with_shadow(surface, text, font_info, text_color, (x_pos, score_y + i * line_height))
        else:
            text = f"{i+1}. {name:<15} {score_val:>5}"
            draw_text(surface, text, font_info, COLOR_WHITE, (x_pos, score_y + i * line_height))

# --- Funções Lógicas ---
def get_valid_spawn_position(snake_segments, current_walls, current_food):
    position = None
    attempts = 0
    max_attempts = (GRID_WIDTH * GRID_HEIGHT) - len(snake_segments) - len(current_walls) - (1 if current_food else 0)
    max_attempts = max(10, max_attempts)
    food_pos = current_food['pos'] if current_food else None

    while position is None and attempts < max_attempts:
        x = random.randrange(0, GRID_WIDTH)
        y = random.randrange(0, GRID_HEIGHT)
        potential_pos = (x, y)
        is_on_snake = potential_pos in snake_segments
        is_on_wall = potential_pos in current_walls
        is_on_food = potential_pos == food_pos
        if not is_on_snake and not is_on_wall and not is_on_food:
            position = potential_pos
        attempts += 1
    if position is None:
        print("Aviso: Não foi possível encontrar posição válida para spawn.")
    return position

def spawn_food(snake_segments, current_walls, current_food, food_type_to_spawn):
    pos = get_valid_spawn_position(snake_segments, current_walls, current_food)
    if pos is None:
        print("Aviso: Não há espaço para gerar nova comida!")
        return None

    # Adiciona partículas no local da nova comida
    color = COLOR_BLUE_GLOW if food_type_to_spawn == 'blue' else COLOR_RED_GLOW
    add_particles(pos[0] * GRID_SIZE + GRID_SIZE//2,
                 pos[1] * GRID_SIZE + GRID_SIZE//2,
                 color, 15, 4, 40)

    return {'pos': pos, 'type': food_type_to_spawn}

def reset_game_state():
    global snake_pos, snake_direction, current_direction, pending_direction, snake_grow, walls, score, current_fps, last_score_wall_added, food
    snake_pos = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)
    current_direction = snake_direction
    pending_direction = snake_direction
    snake_grow = False
    walls = []
    score = 0
    current_fps = INITIAL_FPS
    last_score_wall_added = -1
    food = spawn_food(snake_pos, walls, None, 'blue')
    print("Estado resetado.")

def move_snake(snake_segments, direction, grow):
    global snake_grow
    if not direction or not snake_segments: return snake_segments

    head_x, head_y = snake_segments[0]
    dir_x, dir_y = direction
    new_head = (head_x + dir_x, head_y + dir_y)
    snake_segments.insert(0, new_head)

    if not grow:
        snake_segments.pop()
    else:
        snake_grow = False
    return snake_segments

def add_wall(snake_segments, current_walls, current_food):
    global walls
    wall_pos = get_valid_spawn_position(snake_segments, current_walls, current_food)
    if wall_pos:
        walls.append(wall_pos)
        # Adiciona partículas no local da nova parede
        add_particles(wall_pos[0] * GRID_SIZE + GRID_SIZE//2,
                     wall_pos[1] * GRID_SIZE + GRID_SIZE//2,
                     COLOR_GRAY_GLOW, 15, 4, 40)
        return True
    return False

def remove_random_wall():
    global walls
    if walls:
        removed_wall = random.choice(walls)
        # Adiciona partículas no local da parede removida
        add_particles(removed_wall[0] * GRID_SIZE + GRID_SIZE//2,
                     removed_wall[1] * GRID_SIZE + GRID_SIZE//2,
                     COLOR_RED_GLOW, 20, 5, 50)
        walls.remove(removed_wall)
        return True
    return False

def check_collisions(snake_segments, current_walls):
    if not snake_segments: return False
    head = snake_segments[0]
    head_x, head_y = head

    # Colisão com Bordas
    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        return True
    # Colisão com Corpo
    if head in snake_segments[1:]:
        return True
    # Colisão com Paredes
    if head in current_walls:
        return True
    return False

def toggle_music():
    global music_playing
    music_playing = not music_playing
    if music_playing:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

# --- Estados do Jogo e Variáveis Globais ---
MENU = 0
PLAYING = 1
GAME_OVER = 2
GETTING_NAME = 3
PAUSED = 4
game_state = MENU

player_name = ""

# --- Definição dos Retângulos dos Botões ---
button_width = 200; button_height = 50
button_y_start = SCREEN_HEIGHT // 2 + 40
button_y_restart = SCREEN_HEIGHT // 2 + 60
start_button_rect = pygame.Rect(0, button_y_start, button_width, button_height)
restart_button_rect = pygame.Rect(0, button_y_restart, button_width, button_height)

# Botão de música
music_button_width = 160; music_button_height = 40
music_button_rect = pygame.Rect(SCREEN_WIDTH - music_button_width - 10, 10, music_button_width, music_button_height)

# Botões da tela de pausa
resume_button_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 - 30, button_width, button_height)
quit_button_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 + 30, button_width, button_height)

# --- Inicializa Variáveis do Jogo ---
food = None
snake_pos = []
snake_direction = None
current_direction = None
pending_direction = None
snake_grow = False
walls = []
score = 0
current_fps = INITIAL_FPS
last_score_wall_added = -1

# --- Loop Principal ---
running = True
while running:
    # --- 1. Tratamento de Eventos ---
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

        # Tratamento da tecla ESC para pausar o jogo
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state == PLAYING:
                game_state = PAUSED
            elif game_state == PAUSED:
                game_state = PLAYING

        # Eventos específicos do estado GETTING_NAME
        if game_state == GETTING_NAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        scoreboard = add_score(scoreboard, player_name, score)
                        save_scoreboard(scoreboard)
                    game_state = GAME_OVER
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 15:
                    if event.unicode.isprintable() and not event.unicode.isspace():
                         player_name += event.unicode.upper()

        # Eventos específicos do estado PLAYING
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and current_direction != (0, 1): pending_direction = (0, -1)
                elif event.key == pygame.K_DOWN and current_direction != (0, -1): pending_direction = (0, 1)
                elif event.key == pygame.K_LEFT and current_direction != (1, 0): pending_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and current_direction != (-1, 0): pending_direction = (1, 0)

        # Eventos específicos do estado MENU
        elif game_state == MENU:
            # Verifica clique no botão de música no menu
            if clicked and music_button_rect.collidepoint(mouse_pos):
                toggle_music()

        # Eventos específicos do estado PAUSED
        elif game_state == PAUSED:
            # Verifica clique nos botões de pausa
            if clicked:
                if resume_button_rect.collidepoint(mouse_pos):
                    game_state = PLAYING
                elif quit_button_rect.collidepoint(mouse_pos):
                    game_state = MENU
                elif music_button_rect.collidepoint(mouse_pos):
                    toggle_music()

    # --- Fim do Tratamento de Eventos ---

    # --- 2. Lógica do Jogo por Estado ---
    # Atualiza efeito de pulsação
    pulse_value += pulse_speed
    if pulse_value > math.pi * 2:
        pulse_value = 0

    # Atualiza partículas
    update_particles()

    # Verifica hover nos botões
    start_button_hover = start_button_rect.collidepoint(mouse_pos)
    restart_button_hover = restart_button_rect.collidepoint(mouse_pos)
    music_button_hover = music_button_rect.collidepoint(mouse_pos)
    resume_button_hover = resume_button_rect.collidepoint(mouse_pos)
    quit_button_hover = quit_button_rect.collidepoint(mouse_pos)

    if game_state == MENU:
        # Verifica clique no botão Iniciar
        if clicked:
            if start_button_rect.collidepoint(mouse_pos):
                reset_game_state()
                game_state = PLAYING

    elif game_state == PLAYING:
        # Atualiza direção e move a cobra
        current_direction = pending_direction
        snake_pos = move_snake(snake_pos, current_direction, snake_grow)

        # Verifica Colisões
        if check_collisions(snake_pos, walls):
            # Adiciona partículas de explosão na cabeça da cobra
            if snake_pos:
                head = snake_pos[0]
                add_particles(head[0] * GRID_SIZE + GRID_SIZE//2,
                             head[1] * GRID_SIZE + GRID_SIZE//2,
                             COLOR_NEON_GREEN, 30, 6, 60)

            # Lógica de transição para GETTING_NAME ou GAME_OVER
            is_high = False
            if score > 0:
                if len(scoreboard) < MAX_SCORES:
                    is_high = True
                elif scoreboard and score > scoreboard[-1]['score']:
                     is_high = True

            if is_high:
                player_name = ""
                game_state = GETTING_NAME
            else:
                game_state = GAME_OVER
        else:
            # Se não colidiu, processa comida
            head = snake_pos[0]
            if food and head == food['pos']:
                food_type_eaten = food['type']
                next_food_type = 'blue'

                # Toca som e adiciona partículas ao comer
                EAT_SOUND.play()
                add_particles(head[0] * GRID_SIZE + GRID_SIZE//2,
                             head[1] * GRID_SIZE + GRID_SIZE//2,
                             COLOR_BLUE_GLOW if food_type_eaten == 'blue' else COLOR_RED_GLOW,
                             20, 5, 40)

                if food_type_eaten == 'blue':
                    # Comeu azul: cresce, pontua, acelera
                    snake_grow = True
                    score += 1
                    current_fps += FPS_INCREMENT
                    # Adiciona parede a cada 3 pontos
                    if score > 0 and score % 3 == 0 and score > last_score_wall_added:
                        if add_wall(snake_pos, walls, food):
                            last_score_wall_added = score
                    # Decide se a PRÓXIMA comida será vermelha
                    if score >= 10 and score % 5 == 0:
                        next_food_type = 'red'

                elif food_type_eaten == 'red':
                    # Comeu vermelha: ação na parede, próxima é azul
                    action = random.choice(['remove', 'add'])

                    if action == 'remove':
                        remove_random_wall()
                        WALL_DESTROY_SOUND.play()
                    else:
                        add_wall(snake_pos, walls, food)
                        WALL_CREATE_SOUND.play()

                    next_food_type = 'blue'

                # Gera a próxima comida com o tipo decidido
                food = spawn_food(snake_pos, walls, food, next_food_type)

            # Segurança: caso a comida suma
            if food is None:
                food = spawn_food(snake_pos, walls, None, 'blue')

    elif game_state == GAME_OVER:
        # Verifica clique no botão Reiniciar
        if clicked:
            if restart_button_rect.collidepoint(mouse_pos):
                game_state = MENU

    # --- 3. Desenho por Estado ---
    screen.fill(COLOR_DARK_BG)

    # Desenha grid em todos os estados
    draw_grid(screen)

    # Aplica efeito de vinheta em todos os estados
    screen.blit(vignette_surface, (0, 0))

    if game_state == MENU:
        draw_scoreboard(screen, scoreboard)

        # Elementos principais à direita - ajustado mais para a direita
        title_x = SCREEN_WIDTH * 0.75
        button_x_menu = title_x
        start_button_rect.centerx = button_x_menu

        # Efeito de título pulsante
        title_glow = int(20 * math.sin(pulse_value * 2) + 20)
        title_color = (0, 255 - title_glow, 100 + title_glow)

        # Desenha Título com efeito de sombra
        shadow_offset = 1
        for offset in range(shadow_offset, 0, -1):
            alpha = 100 - (offset * 30)
            shadow_color = (0, 100, 40, alpha)
            shadow_surf = font_title.render("Neon Snake", True, shadow_color)
            shadow_rect = shadow_surf.get_rect(center=(title_x + offset, SCREEN_HEIGHT // 3 + offset))
            screen.blit(shadow_surf, shadow_rect)

        draw_text(screen, "Neon Snake", font_title, title_color, (title_x, SCREEN_HEIGHT // 3), center=True)

        # Botão com efeito hover
        draw_button(screen, "Iniciar", font_button, COLOR_BUTTON_TEXT, COLOR_NEON_GREEN,
                   start_button_rect, hover=start_button_hover)

        # Instruções
        info_text = "Use as setas para mover"
        draw_text(screen, info_text, font_info, COLOR_WHITE,
                 (title_x, start_button_rect.bottom + 35), center=True)

        info_esc = "ESC para pausar"
        draw_text(screen, info_esc, font_info, COLOR_WHITE,
                 (title_x, start_button_rect.bottom + 65), center=True)

        # Botão de música (apenas no menu e na pausa)
        music_text = "Música: ON" if music_playing else "Música: OFF"
        music_color = COLOR_NEON_GREEN if music_playing else COLOR_RED
        draw_button(screen, music_text, font_info, COLOR_BUTTON_TEXT, music_color,
                   music_button_rect, hover=music_button_hover)

    elif game_state == PLAYING:
        # Desenho do jogo
        draw_walls(screen, walls)
        draw_snake(screen, snake_pos)
        draw_food(screen, food)
        draw_particles(screen)

        # Score no canto superior direito com efeito de brilho
        score_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 150))
        screen.blit(score_bg, (SCREEN_WIDTH - 160, 5))
        pygame.draw.rect(screen, COLOR_NEON_GREEN, pygame.Rect(SCREEN_WIDTH - 160, 5, 150, 40),
                        width=2, border_radius=5)
        draw_text(screen, f"Score: {score}", font_score, COLOR_WHITE, (SCREEN_WIDTH - 85, 25), center=True)

    elif game_state == GETTING_NAME:
        # Tela de entrada de nome com efeitos visuais
        # Fundo semi-transparente
        input_bg = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
        input_bg.fill((20, 20, 40, 200))
        screen.blit(input_bg, (50, 100))

        # Borda neon pulsante
        border_intensity = int(40 * math.sin(pulse_value * 2) + 215)
        border_color = (0, border_intensity, 100)
        pygame.draw.rect(screen, border_color,
                        pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200),
                        width=3, border_radius=15)

        draw_text(screen, "Novo Recorde!", font_menu, COLOR_NEON_GREEN,
                 (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), center=True)
        draw_text(screen, f"Score: {score}", font_button, COLOR_WHITE,
                 (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60), center=True)
        draw_text(screen, "Digite seu nome (Max 15):", font_button, COLOR_WHITE,
                 (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10), center=True)

        # Caixa de input visual com efeito pulsante
        input_rect_width = 350
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - input_rect_width // 2,
                               SCREEN_HEIGHT // 2 + 30, input_rect_width, 50)

        # Fundo da caixa
        pygame.draw.rect(screen, (30, 30, 50), input_rect, border_radius=8)

        # Borda pulsante
        border_width = int(3 + math.sin(pulse_value * 3) * 2)
        pygame.draw.rect(screen, COLOR_NEON_GREEN, input_rect,
                        width=border_width, border_radius=8)

        # Nome digitado
        draw_text(screen, player_name, font_input, COLOR_WHITE, input_rect.center, center=True)

        # Cursor piscante
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            cursor_x = input_rect.centerx + font_input.size(player_name)[0] // 2 + 5
            pygame.draw.line(screen, COLOR_WHITE,
                            (cursor_x, input_rect.centery - 15),
                            (cursor_x, input_rect.centery + 15), 2)

        draw_text(screen, "[ENTER] para confirmar", font_info, COLOR_GRAY,
                 (SCREEN_WIDTH // 2, input_rect.bottom + 20), center=True)

    elif game_state == GAME_OVER:
        draw_scoreboard(screen, scoreboard)
        draw_particles(screen)

        # Elementos principais à direita - ajustado mais para a direita
        center_x_go = SCREEN_WIDTH * 0.75
        restart_button_rect.centerx = center_x_go

        # Fundo semi-transparente
        gameover_bg = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
        gameover_bg.fill((40, 0, 0, 150))
        screen.blit(gameover_bg, (center_x_go - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

        # Borda vermelha pulsante
        border_intensity = int(40 * math.sin(pulse_value * 2) + 215)
        pygame.draw.rect(screen, (border_intensity, 0, 50),
                        pygame.Rect(center_x_go - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4,
                                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                        width=3, border_radius=15)

        # Texto Game Over com efeito de tremor
        tremor_x = random.randint(-2, 2)
        tremor_y = random.randint(-2, 2)
        draw_text(screen, "GAME OVER", font_menu, COLOR_RED,
                 (center_x_go + tremor_x, SCREEN_HEIGHT // 2 - 70 + tremor_y), center=True)

        score_text = f"Score final: {score}"
        draw_text(screen, score_text, font_menu, COLOR_WHITE,
                 (center_x_go, SCREEN_HEIGHT // 2 - 10), center=True)

        # Botão com efeito hover
        draw_button(screen, "Reiniciar", font_button, COLOR_BUTTON_TEXT, COLOR_RED,
                   restart_button_rect, hover=restart_button_hover)

    elif game_state == PAUSED:
        # Desenha o jogo em segundo plano com sobreposição escura
        draw_walls(screen, walls)
        draw_snake(screen, snake_pos)
        draw_food(screen, food)

        # Sobreposição escura semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Cria janela de pausa
        pause_width = 350
        pause_height = 250
        pause_x = SCREEN_WIDTH // 2 - pause_width // 2
        pause_y = SCREEN_HEIGHT // 2 - pause_height // 2

        # Fundo da janela
        pause_bg = pygame.Surface((pause_width, pause_height), pygame.SRCALPHA)
        pause_bg.fill((20, 20, 40, 220))
        screen.blit(pause_bg, (pause_x, pause_y))

        # Borda pulsante
        border_intensity = int(40 * math.sin(pulse_value * 2) + 215)
        border_color = COLOR_YELLOW
        pygame.draw.rect(screen, border_color,
                        pygame.Rect(pause_x, pause_y, pause_width, pause_height),
                        width=3, border_radius=15)

        # Texto de pausa
        draw_text(screen, "PAUSA", font_menu, COLOR_YELLOW,
                 (SCREEN_WIDTH // 2, pause_y + 40), center=True)

        # Centraliza botões na janela de pausa
        center_x = SCREEN_WIDTH // 2
        resume_button_rect.centerx = center_x
        resume_button_rect.centery = pause_y + 110
        quit_button_rect.centerx = center_x
        quit_button_rect.centery = pause_y + 170

        # Botões
        draw_button(screen, "Continuar", font_button, COLOR_BUTTON_TEXT, COLOR_NEON_GREEN,
                   resume_button_rect, hover=resume_button_hover)
        draw_button(screen, "Menu", font_button, COLOR_BUTTON_TEXT, COLOR_RED,
                   quit_button_rect, hover=quit_button_hover)

        # Botão de música (apenas no menu e na pausa)
        music_text = "Música: ON" if music_playing else "Música: OFF"
        music_color = COLOR_NEON_GREEN if music_playing else COLOR_RED
        draw_button(screen, music_text, font_info, COLOR_BUTTON_TEXT, music_color,
                   music_button_rect, hover=music_button_hover)

        # Instruções
        info_text = "Pressione ESC para continuar"
        draw_text(screen, info_text, font_info, COLOR_WHITE,
                 (SCREEN_WIDTH // 2, pause_y + 220), center=True)

    # --- 4. Atualização da Tela ---
    pygame.display.flip()

    # --- 5. Controle de FPS ---
    fps_target = current_fps if game_state == PLAYING else 30
    clock.tick(fps_target)

# --- Fim do Programa ---
pygame.quit()
sys.exit()