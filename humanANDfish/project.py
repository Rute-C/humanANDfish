import pygame
from pygame.locals import *
from sys import exit
import random
import time

class RelogioPersonalizado:
    def __init__(self, horas=0, minutos=0):
        self.horas = horas
        self.minutos = minutos
    
    def passa_tempo(self):
        self.minutos += 1        
        if self.minutos >= 59:  # verifica se já passou 59 minutos 
            self.horas += 1     # se sim, acrescenta 1 hora
            self.minutos = 0    # reset

    def tempo(self):
        return self.minutos, self.horas

    def __str__(self):
        return f"{self.horas:02d}:{self.minutos:02d}"



def main():
    pygame.init()

    # Tamanho da tela
    w = 550
    h = 550
    global screen
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption('Human and Fish')


    # personagem
    x_pos = 250
    y_pos = 200
    vel = 10
    tamanho_personagem = 220
    walk_count = 0
    down = False
    up = False
    right = False
    left = False
    aparecer = False


    global walk_left
    global walk_right
    global walk_up
    global walk_down
    walk_right = [
        pygame.transform.scale(
        pygame.image.load("imagens/personagem/andar_direiro00.png").convert_alpha(),
        (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_direiro01.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_direiro02.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        )
    ]      
    walk_left = [
        pygame.transform.scale(
        pygame.image.load("imagens/personagem/andar_esq00.png").convert_alpha(),
        (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_esq01.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_esq02.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        )
    ]      
    walk_down = [
        pygame.transform.scale(
        pygame.image.load("imagens/personagem/andar_frente00.png").convert_alpha(),
        (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_frente01.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_frente02.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        )
    ] 
    walk_up = [
        pygame.transform.scale(
        pygame.image.load("imagens/personagem/andar_tras00.png").convert_alpha(),
        (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_tras01.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        ),
        pygame.transform.scale(
            pygame.image.load("imagens/personagem/andar_tras02.png").convert_alpha(),
            (tamanho_personagem, tamanho_personagem)
        )
    ]  

    parado = pygame.transform.scale(
        pygame.image.load("imagens/personagem/andar_frente00.png").convert_alpha(),
        (tamanho_personagem, tamanho_personagem)
        )    
    
    # player = [parado, walk_left, walk_right, walk_down, walk_up]

    clock = pygame.time.Clock()

    # Imagem da capa
    capa_surface = ajustar('capa.png', h, w)

    
    # Imagem do quarto
    background1 = ajustar('background/quarto.png', h, w).convert_alpha()
    espelho = ajustar('quarto/espelho.png', h, w).convert_alpha()
    poster = ajustar('quarto/poster.png', h, w).convert_alpha()
    mesa = ajustar('quarto/mesa.png', h, w).convert_alpha()
    tapete = ajustar('quarto/tapete.png', h, w).convert_alpha()
    cama = ajustar('quarto/cama.png', h, w).convert_alpha()
    computer = ajustar('quarto/computer.png', h, w).convert_alpha()
    lixo = ajustar('quarto/lixo.png', h, w).convert_alpha()
    armario = ajustar('quarto/armario.png', h, w).convert_alpha()

    # Hitbox do quarto
    mesa_hitbox = pygame.Rect(x_pos + 170, y_pos - 5, 95, 30)
    cama_hitbox = pygame.Rect(x_pos - 150, y_pos + 5, 150, 50)
    computer_hitbox = pygame.Rect(x_pos + 110, y_pos + 300, 150, 30)
    lixo_hitbox = pygame.Rect(x_pos + 20, y_pos + 300, 30, 30)
    armario_hitbox = pygame.Rect(x_pos - 230 , y_pos + 180, 100, 130)
    roupa_hitbox = pygame.Rect(x_pos - 130 , y_pos + 220, 80, 80)

    objetos_quarto = [
        cama_hitbox,
        mesa_hitbox,
        computer_hitbox,
        lixo_hitbox,
        armario_hitbox,
        roupa_hitbox
    ]
    # Objetos de fundo
    objetos_fundo_quarto = [
        {'image': tapete, 'rect': tapete.get_rect(topleft=(-10,-10))},
        {'image': cama, 'rect': cama.get_rect(topleft=(0,0))},
        {'image': mesa, 'rect': mesa.get_rect(topleft=(0,0))},
        {'image': espelho, 'rect': espelho.get_rect(topleft=(0,0))},
        {'image': poster, 'rect': poster.get_rect(topleft=(0,0))},
    ]

    # Objetos de frente
    objetos_frente_quarto = [
        
        {'image': computer, 'rect': computer.get_rect(topleft=(0,0))},
        {'image': lixo, 'rect': lixo.get_rect(topleft=(0,0))},
        {'image': armario, 'rect': armario.get_rect(topleft=(0,0))}
    ]

    # Imagens da cozinha
    background2 = ajustar('background/cozinha.png', h, w).convert_alpha()

    objetos_cozinha = []

    # Estados do jogo
    game_status = 'capa'
    preto = ajustar('camara/preto.png', h, w).convert_alpha()
    colidiu = False

    # Fonte
    font_small_small = pygame.font.Font("Minecraftia-Regular.ttf", 15)
    font_small = pygame.font.Font("Minecraftia-Regular.ttf", 20)
    font_big = pygame.font.Font("Minecraftia-Regular.ttf", 40)
    font = pygame.font.Font("Minecraftia-Regular.ttf", 32)

    # Botão Start
    botao_start = pygame.Rect(200, 440, 150, 50)

    # Botão Exit
    botao_quit = pygame.Rect(450, 520, 70, 25)

    # Botão Acerca
    botao_credit = pygame.Rect(220, 500, 100, 25)
    
    # Warning - tela preta
    alpha = 255

    # time
    relogio = RelogioPersonalizado(7, 0)
    contador = 0

    running = True
    while running:
        clock.tick(4)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if game_status == 'capa' and botao_start.collidepoint(event.pos):
                    game_status = 'tela_preta'
                    aparecer = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_quit.collidepoint(event.pos):  # Se clicou dentro do botão QUIT
                    running = False
                    exit()
            

        random_fifty = random.randint(1, 2)

        # CAPA
        if game_status == 'capa':
            aparecer = False
            screen.blit(capa_surface, (0, 0))

            # Pintar os rectangulos arredondados
            pygame.draw.rect(screen, (22,154,147,255), botao_start, border_radius=30)
            pygame.draw.rect(screen, (22,154,147,255), botao_quit, border_radius=30)
            pygame.draw.rect(screen, (22,154,147,255), botao_credit, border_radius=30)

            texto = font.render("START", True, (0, 0, 0))
            texto_rect = texto.get_rect(center=botao_start.center)  # Centraliza texto no botão
            screen.blit(texto, texto_rect)

            texto1 = font_small.render("QUIT", True, (0, 0, 0))
            texto_rect1 = texto1.get_rect(center=botao_quit.center)  # Centraliza texto no botão
            screen.blit(texto1, texto_rect1)

            texto2 = font_small.render("CREDIT", True, (0, 0, 0))
            texto_rect2 = texto2.get_rect(center=botao_credit.center)  # Centraliza texto no botão
            screen.blit(texto2, texto_rect2)

        elif game_status == 'tela_preta':
            screen.fill((0, 0, 0))
            warning = font_big.render("Content Warning:", True, (255, 0, 0)).convert_alpha()
            warning1 = font_big.render("Sensitive Themes", True, (255, 0, 0)).convert_alpha()
            warning.set_alpha(alpha)
            warning1.set_alpha(alpha)
            screen.blit(warning, (80, 230))
            screen.blit(warning1, (80, 290))
            alpha -= 20
            if alpha <= 0:
                game_status = 'quarto'
        
        # QUARTO
        elif game_status == 'quarto':

            player_hitbox = pygame.Rect(x_pos + 95, y_pos + 80, 25, 70)

            screen.blit(background1, (0, 0)) # quarto

            for obj in objetos_fundo_quarto:
                screen.blit(obj['image'], obj['rect'].topleft)

            if aparecer:
                screen.blit(parado, (x_pos, y_pos))

            left, up, down, right, aparecer, x_pos, y_pos, walk_count, player_hitbox, objetos_background, colidiu, temp, game_status = movimento_personagem(
                left, up, down, right, aparecer, vel, x_pos, y_pos, walk_count, player_hitbox, objetos_background, colidiu, game_status, objetos_quarto, objetos_cozinha)

            for obj in objetos_frente_quarto:
                screen.blit(obj['image'], obj['rect'].topleft)

            pygame.draw.rect(screen, (0, 0, 0), player_hitbox, -1)

            for obs in objetos_quarto:
                pygame.draw.rect(screen, (0, 0, 0), obs, -1)
                 
            quarto_colidiu(colidiu, random_fifty, preto, font_small_small, temp, cama_hitbox, mesa_hitbox, computer_hitbox, lixo_hitbox,
                          armario_hitbox, roupa_hitbox)

            hour, minute, contador = time(font, clock, contador, relogio)
    
        # COZINHA
        elif game_status == 'cozinha':

            player_hitbox = pygame.Rect(x_pos + 95, y_pos + 80, 25, 70)

            screen.blit(background2, (0, 0)) # cozinha

            if aparecer:
                screen.blit(parado, (x_pos, y_pos))

            left, up, down, right, aparecer, x_pos, y_pos, walk_count, player_hitbox, colidiu, temp, game_status = movimento_personagem(
                left, up, down, right, aparecer, vel, x_pos, y_pos, walk_count, player_hitbox, colidiu, game_status, objetos_quarto, objetos_cozinha)

            pygame.draw.rect(screen, (0, 0, 0), player_hitbox, 1)

           
        
        
        pygame.display.update()

def ajustar(caminho, w, h):
    load = pygame.image.load(f'imagens/{caminho}')
    ajuste = pygame.transform.scale(load, (w, h))
    return ajuste

def movimento_personagem(left, up, down, right, aparecer, vel, x_pos, y_pos, walk_count, player_hitbox, 
                         colidiu, game_status, objetos_quarto, objetos_cozinha):
    keys = pygame.key.get_pressed()
    vel_rapid = vel * 2
    velocidade = vel
    colidiu = False
    temp = None
    dx = 0
    dy = 0
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        vel = vel_rapid
    else:
        vel = velocidade
    
    if keys[pygame.K_LEFT] and x_pos > -10:
        dx -= vel                
        left = True
        up = False
        down = False
        right = False
        aparecer = False
    elif keys[pygame.K_RIGHT] and x_pos < 420:
        dx += vel
        left = False
        up = False
        down = False
        right = True
        aparecer = False
    elif keys[pygame.K_UP] and y_pos > 95:
        dy -= vel
        left = False
        up = True
        down = False
        right = False
        aparecer = False
    elif keys[pygame.K_DOWN] and y_pos < 355:
        dy += vel
        left = False
        up = False
        down = True
        right = False
        aparecer = False
    else:
        aparecer = True
        left = False
        up = False
        down = False
        right = False

    # Colisão
    # mudar de cenário
    parede_quarto = pygame.Rect(530, 270, 50, 100)
    pygame.draw.rect(screen, (0, 0, 0), parede_quarto, 1)

    # Movimento eixo X
    player_hitbox.x += dx
    if game_status == 'quarto':
        comodo = objetos_quarto
    if game_status == 'cozinha':
        comodo = objetos_cozinha
    for obj in comodo:
        if player_hitbox.colliderect(obj):
            if dx > 0:  # movendo para a direita
                player_hitbox.right = obj.left
            elif dx < 0:  # movendo para a esquerda
                player_hitbox.left = obj.right
            colidiu = True
            temp = obj
            break

    # Movimento eixo Y
    player_hitbox.y += dy
    for comodo in objetos_background:
        for obj in comodo:
            if player_hitbox.colliderect(obj):
                if dy > 0:  # movendo para baixo
                    player_hitbox.bottom = obj.top
                elif dy < 0:  # movendo para cima
                    player_hitbox.top = obj.bottom
                colidiu = True
                temp = obj
                break

    if player_hitbox.colliderect(parede_quarto):
        if game_status == 'quarto':
            game_status = 'cozinha'
            x_pos = 90   # posição inicial na cozinha
            y_pos = 150
            player_hitbox.topleft = (x_pos, y_pos)
            left = False
            up = False
            down = False
            right = False
            aparecer = True
    
    # Jogador não colidiu, pode se mover livremente
    x_pos += dx    
    y_pos += dy

    x_pos = player_hitbox.x - 95  # Alinha a posição X do sprite com a hitbox 
    y_pos = player_hitbox.y - 80  # Alinha a posição Y do sprite com a hitbox 

    if walk_count + 1 >= 4:
            walk_count = 0

    if right:
        screen.blit(walk_right[walk_count], (x_pos, y_pos))
        walk_count += 1
    elif left:
        screen.blit(walk_left[walk_count], (x_pos, y_pos))
        walk_count += 1
    elif up:
        screen.blit(walk_up[walk_count], (x_pos, y_pos))
        walk_count += 1
    elif down:
        screen.blit(walk_down[walk_count], (x_pos, y_pos))
        walk_count += 1
    else:
        screen.blit(walk_down[0], (x_pos, y_pos))
        walk_count = 0
    
    return left, up, down, right, aparecer, x_pos, y_pos, walk_count, player_hitbox, colidiu, temp, game_status

def quarto_colidiu(colidiu, random_fifty, preto, font_small_small, temp,
                    cama_hitbox, mesa_hitbox, computer_hitbox, lixo_hitbox,
                    armario_hitbox, roupa_hitbox):
     # cena preta com textos diferentes
    text_cama1 = font_small_small.render("It's my bed, I like to sleep", True, (255, 255, 255))
    text_cama1_1 = font_small_small.render("to pass the time...", True, (255, 255, 255))
    text_cama2 = font_small_small.render("I don't feel like sleeping...", True, (255, 255, 255))
    text_mesa = font_small_small.render("Here is my companion!! My Fish ", True, (255, 255, 255))
    text_computer = font_small_small.render("It's only my computer...", True, (255, 255, 255))
    text_lixo = font_small_small.render("Ug!! It smells bad...", True, (255, 255, 255))
    text_armario = font_small_small.render("... ...", True, (255, 255, 255))
    text_roupa = font_small_small.render("I really need to organize", True, (255, 255, 255))
    text_roupa1 = font_small_small.render("these clothes...", True, (255, 255, 255))

    if colidiu:
        screen.blit(preto, (0, 0)) # tela de conversa preta
        if temp == cama_hitbox:
            if random_fifty == 1:
                screen.blit(text_cama1, (150, 450))
                screen.blit(text_cama1_1, (150, 480))
            else:
                screen.blit(text_cama2, (150, 470))
        if temp == mesa_hitbox:
            screen.blit(text_mesa, (150, 470) )
        if temp == computer_hitbox:
            screen.blit(text_computer, (150, 470))
        if temp == lixo_hitbox:
            screen.blit(text_lixo, (150, 470))
        if temp == armario_hitbox:
            screen.blit(text_armario, (150, 470))
        if temp == roupa_hitbox:
            screen.blit(text_roupa, (150, 450))
            screen.blit(text_roupa1, (150, 480))
        pygame.display.update()
        pygame.time.wait(2000)
        colidiu = False

def time(font, clock, contador, relogio):
    intervalo = 500
    contador += clock.tick(4)

    if contador >= intervalo:
        contador = 0
        relogio.passa_tempo()
    minute, hour = relogio.tempo()

    relogio_ver = font.render(str(relogio), True, (0, 0, 0))
    screen.blit(relogio_ver, (440, 0))
    return hour, minute, contador


if __name__ == "__main__":
    main()