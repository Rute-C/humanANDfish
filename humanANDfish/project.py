import pygame
from pygame.locals import *
from sys import exit

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
    objetos_fundo = [
        {'image': tapete, 'rect': tapete.get_rect(topleft=(-10,-10))},
        {'image': cama, 'rect': cama.get_rect(topleft=(0,0))},
        {'image': mesa, 'rect': mesa.get_rect(topleft=(0,0))},
        {'image': espelho, 'rect': espelho.get_rect(topleft=(0,0))},
        {'image': poster, 'rect': poster.get_rect(topleft=(0,0))},
    ]

    # Objetos de frente
    objetos_frente = [
        
        {'image': computer, 'rect': computer.get_rect(topleft=(0,0))},
        {'image': lixo, 'rect': lixo.get_rect(topleft=(0,0))},
        {'image': armario, 'rect': armario.get_rect(topleft=(0,0))}
    ]

    objetos_background = [
        objetos_quarto
    ]
    # Estados do jogo
    game_status = 'capa'
    preto = ajustar('camara/preto.png', h, w).convert_alpha()


    # Botão Start
    font = pygame.font.Font("Minecraftia-Regular.ttf", 32)
    botao_start = pygame.Rect(200, 440, 150, 50)

    # Botão Exit
    font_small = pygame.font.Font("Minecraftia-Regular.ttf", 20)
    botao_quit = pygame.Rect(450, 520, 70, 25)

    # Botão Acerca
    botao_credit = pygame.Rect(220, 500, 100, 25)

    running = True
    while running:
        clock.tick(4)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if game_status == 'capa' and botao_start.collidepoint(event.pos):
                    game_status = 'quarto'
                    aparecer = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_quit.collidepoint(event.pos):  # Se clicou dentro do botão QUIT
                    running = False
                    exit()

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

        # JOGO
        elif game_status == 'quarto':

            player_hitbox = pygame.Rect(x_pos + 95, y_pos + 80, 25, 70)

            screen.blit(background1, (0, 0)) # quarto

            for obj in objetos_fundo:
                screen.blit(obj['image'], obj['rect'].topleft)

            if aparecer:
                screen.blit(parado, (x_pos, y_pos))

            left, up, down, right, aparecer, x_pos, y_pos, walk_count, player_hitbox, objetos_background, colidiu = movimento_personagem(
                left, up, down, right, aparecer, vel, x_pos, y_pos, walk_count, player_hitbox, objetos_background)

            for obj in objetos_frente:
                screen.blit(obj['image'], obj['rect'].topleft)

            keys = pygame.key.get_pressed()
            if colidiu:
                screen.blit(preto, (0, 0)) # tela de conversa preta
                colidiu = True
                if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    colidiu = False

            pygame.draw.rect(screen, (0, 0, 0), player_hitbox, -1)
            for obs in objetos_quarto:
                pygame.draw.rect(screen, (0, 0, 0), obs, -1)

        pygame.display.update()

def ajustar(caminho, w, h):
    load = pygame.image.load(f'imagens/{caminho}')
    ajuste = pygame.transform.scale(load, (w, h))
    return ajuste

def movimento_personagem(left, up, down, right, aparecer, vel, x_pos, y_pos, walk_count, player_hitbox, objetos_background):
    keys = pygame.key.get_pressed()
    colidiu = False
    dx = 0
    dy = 0
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
    # Movimento eixo X
    player_hitbox.x += dx
    for comodo in objetos_background:  # cada comodo é uma lista de Rects
        for obj in comodo:
            if player_hitbox.colliderect(obj):
                if dx > 0:  # movendo para a direita
                    player_hitbox.right = obj.left
                elif dx < 0:  # movendo para a esquerda
                    player_hitbox.left = obj.right
                colidiu = True

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
    
    return left, up, down, right, aparecer, x_pos, y_pos, walk_count, player_hitbox, objetos_background, colidiu


if __name__ == "__main__":
    main()