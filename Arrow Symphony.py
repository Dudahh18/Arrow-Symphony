import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Dimensões da janela do jogo
WIDTH, HEIGHT = 800, 450
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Ritmo")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define a fonte
font = pygame.font.Font("fonts\\Zilla_Slab\\ZillaSlab-Bold.ttf", 20)

# Carrega as imagens das setas
arrow_left_image = pygame.image.load("imagens\\esquerda1.png").convert_alpha()
arrow_right_image = pygame.image.load("imagens\\direita1.png").convert_alpha()
arrow_up_image = pygame.image.load("imagens\\cima1.png").convert_alpha()
arrow_down_image = pygame.image.load("imagens\\baixo1.png").convert_alpha()

# Carrega a imagem de fundo
background_image = pygame.image.load("imagens\\FundoJogo.jpg").convert()
menu_background_image = pygame.image.load("imagens\\fundo1.jpg").convert()
modos_background = pygame.image.load("imagens\\fundo2.jpg").convert()
music_background = pygame.image.load("imagens\\fundo2.jpg").convert()
nome_background = pygame.image.load("imagens\\fundo 3.jpg").convert()
ranking_background = pygame.image.load("imagens\\fundo4.jpg").convert()


# Classe para representar uma seta
class Arrow:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.hit = False
        self.speed = speed

        # Define a imagem de acordo com a direção
        if self.direction == "left":
            self.image = arrow_left_image
        elif self.direction == "right":
            self.image = arrow_right_image
        elif self.direction == "up":
            self.image = arrow_up_image
        elif self.direction == "down":
            self.image = arrow_down_image

    def draw(self, win):
        # Desenha a imagem da seta na tela
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= self.speed

    def off_screen(self):
        return self.y < 0

# Função para reproduzir música
def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

# Função principal do jogo
def game_loop(difficulty, music_file):
    run = True
    clock = pygame.time.Clock()
    arrows = []
    score = 0
    combo = 0
    show_message = False  # Flag para exibir a mensagem "Acertou" ou "Errou"
    message_timer = 0  # Timer para controlar o tempo de exibição da mensagem

    # Velocidade de acordo com a dificuldade
    speed = 5
    if difficulty == "médio":
        speed = 7
    elif difficulty == "difícil":
        speed = 10

    # Posições das setas
    positions = {
        "left": WIDTH // 12,
        "down": WIDTH // 5 * 2,
        "up": WIDTH // 5 * 3,
        "right": WIDTH - arrow_right_image.get_width()  # Corrigido para alinhar a seta direita
    }

    # Reproduz a música escolhida
    play_music(music_file)

    # Aguarde a música começar
    while not pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(60)  # Mantenha a atualização da tela

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Adiciona uma nova seta de forma aleatória
        if len(arrows) == 0 or arrows[-1].y < HEIGHT - 200:
            direction = random.choice(["left", "right", "up", "down"])
            arrows.append(Arrow(positions[direction], HEIGHT, direction, speed))

        for arrow in arrows:
            arrow.move()
            if arrow.off_screen():
                arrows.remove(arrow)

            if not arrow.hit:
                # Verifica se a seta foi acertada corretamente
                if keys[pygame.K_LEFT] and arrow.direction == "left" and 50 < arrow.y < 100:
                    arrow.hit = True
                    score += 1
                    combo += 1
                    show_message = True
                    message_timer = 0
                    message_text = font.render("ACERTOU!", 1, GREEN)
                elif keys[pygame.K_RIGHT] and arrow.direction == "right" and 50 < arrow.y < 100:
                    arrow.hit = True
                    score += 1
                    combo += 1
                    show_message = True
                    message_timer = 0
                    message_text = font.render("ACERTOU!", 1, GREEN)
                elif keys[pygame.K_UP] and arrow.direction == "up" and 50 < arrow.y < 100:
                    arrow.hit = True
                    score += 1
                    combo += 1
                    show_message = True
                    message_timer = 0
                    message_text = font.render("ACERTOU!", 1, GREEN)
                elif keys[pygame.K_DOWN] and arrow.direction == "down" and 50 < arrow.y < 100:
                    arrow.hit = True
                    score += 1
                    combo += 1
                    show_message = True
                    message_timer = 0
                    message_text = font.render("ACERTOU!", 1, GREEN)

                # Se a seta saiu da tela sem ser acertada:
                if arrow.y < 0 and not arrow.hit:
                    combo = 0  # Reseta o combo ao errar uma seta
                    show_message = True
                    message_timer = 0
                    message_text = font.render("ERRO", 1, RED)

        # Desenhar na tela
        win.blit(background_image, (0, 0))

        # Desenhar a área de acerto e erro
        pygame.draw.rect(win, WHITE, (0, 70, WIDTH, 10))

        for arrow in arrows:
            arrow.draw(win)

        score_text = font.render(f"Pontos: {score}", 1, WHITE)
        combo_text = font.render(f"Combo: {combo}", 1, WHITE)
        win.blit(score_text, (27, 12))
        win.blit(combo_text, (WIDTH - combo_text.get_width() - 45, 12))

        # Exibe a mensagem "Acertou" e "Errou"
        if show_message:
            win.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - 50))
            message_timer += clock.get_time()  # Aumenta o timer
            if message_timer >= 500:  # Tempo de exibição da mensagem
                show_message = False

        # Verifica se a música terminou
        if not pygame.mixer.music.get_busy():
            # Tela de pontuação final
            run = False
            enter_name_screen(score)

        pygame.display.update()

    pygame.quit()

def enter_name_screen(score):
    run = True
    clock = pygame.time.Clock()
    input_box = pygame.Rect(WIDTH // 20 + 250, HEIGHT // 2 + 30, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font("fonts\\Zilla_Slab\\ZillaSlab-Bold.ttf", 25)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Se o clique estiver dentro da caixa de texto, ative-a
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Salva o nome e a pontuação
                        save_score(text, score)
                        show_leaderboard()
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        win.blit(nome_background, (0, 0))
        # Renderiza o texto atual
        txt_surface = font.render(text, True, color)
        # Altera a largura da caixa de texto se o texto for muito longo
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Desenha o texto
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Desenha a caixa de texto
        pygame.draw.rect(win, color, input_box, 2)

        # Ajusta o tamanho da caixa de texto para ajustar o texto
        input_box.w = max(100, txt_surface.get_width() + 10)

        # Desenha a mensagem de pontuação final
        score_text = font.render(f"Sua pontuação: {score}", 1, WHITE)
        win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 120))

        # Desenha a instrução de entrada de nome
        name_text = font.render("Digite seu nome:", 1, WHITE)
        win.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 - 40))

        pygame.display.flip()

# Função para salvar a pontuação
def save_score(name, score):
    try:
        with open('leaderboard.txt', 'r') as f:
            scores = {}
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    scores[parts[0]] = int(parts[1])
    except FileNotFoundError:
        scores = {}

    scores[name] = score

    with open('leaderboard.txt', 'w') as f:
        for name, score in scores.items():
            f.write(f"{name},{score}\n")

def show_leaderboard():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font("fonts\\Zilla_Slab\\ZillaSlab-Bold.ttf", 25)

    try:
        with open('leaderboard.txt', 'r') as f:
            scores = {}
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    scores[parts[0]] = int(parts[1])

        # Ordena o dicionário de scores por pontuação em ordem decrescente
        sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    except FileNotFoundError:
        sorted_scores = {}

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    run = False

        # Desenha a tela
        win.blit(ranking_background, (0, 0))
        title_text = font.render("Ranking", 1, WHITE)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        y = 150
        for i, (name, score) in enumerate(sorted_scores.items()):
            entry_text = font.render(f"{i+1}. {name}: {score}", 1, WHITE)
            win.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, y))
            y += 50

        # Desenha a instrução para voltar ao menu
        back_text = font.render("Pressione Esc para voltar ao menu", 1, WHITE)
        win.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

def select_difficulty():
    run = True
    clock = pygame.time.Clock()
    difficulties = ["fácil", "médio", "difícil"]
    selected_index = 0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(difficulties)
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(difficulties)
                if event.key == pygame.K_SPACE:
                    select_music(difficulties[selected_index])

        win.blit(modos_background, (0, 0))  # Desenha a imagem de fundo do menu
        title_text = font.render("Selecione a Dificuldade", 1,  WHITE)
        difficulty_text = font.render(f"Dificuldade: {difficulties[selected_index]}", 1, WHITE)
        instruction_text = font.render("Use as setas para mudar, Espaço para selecionar", 1, WHITE)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 147))
        win.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 2 - 2))
        win.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 140))

        pygame.display.update()

    pygame.quit()

def select_music(difficulty):
    run = True
    clock = pygame.time.Clock()
    music_options = ["Alone", "M4", "Mtg Quero Te Encontrar", "Coração de Gelo", "Passei de Nave", "Música Teste"]
    selected_index = 0
    music_files = {
        "Alone": "musicas\\musica1.mp3",
        "M4": "musicas\\musica2.mp3",
        "Quero Te Encontrar": "musicas\\musica3.mp3",
        "Coração de Gelo": "musicas\\musica4.mp3",
        "Passei de Nave": "musicas\\musica5.mp3",
        "Música Teste": "musicas\\musicaTeste.mp3"
    }

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(music_options)
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(music_options)
                if event.key == pygame.K_SPACE:
                    game_loop(difficulty, music_files[music_options[selected_index]])

        win.blit(music_background, (0, 0))  # Desenha a imagem de fundo do menu
        title_text = font.render("Selecione a Música", 1, WHITE)
        music_text = font.render(f"Música: {music_options[selected_index]}", 1, WHITE)
        instruction_text = font.render("Use as setas para mudar, Espaço para selecionar", 1, WHITE)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 147))
        win.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, HEIGHT // 2 - 2))
        win.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 140))

        pygame.display.update()

    pygame.quit()

def main_menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    select_difficulty()

        win.blit(menu_background_image, (0, 0))  # Desenha a imagem de fundo do menu

        start_text = font.render("Pressione Espaço para iniciar", 1, WHITE)
        win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 120))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()