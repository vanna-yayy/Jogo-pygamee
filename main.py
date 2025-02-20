import pygame as pg
pg.init()

clock = pg.time.Clock()
fps = 60

# Janela
painel = 150
screen_width = 800
screen_height = 400 + painel
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("K.O KOMBAT")

player_image = pg.image.load('Warrior_Idle_0.png')
player_speed = 5
largura = 200
altura = 150
player_image = pg.transform.scale(player_image, (largura, altura))

background_img = pg.image.load("fundo.png").convert_alpha()
painel_img = pg.image.load("menu.jpeg").convert_alpha()

background_img = pg.transform.scale(background_img, (800, 400))
painel_img = pg.transform.scale(painel_img, (800, screen_height - painel))

# Função para desenhar o fundo
def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_painel():
    screen.blit(painel_img, (0, screen_height - painel))

# Botão Play
def draw_play_button():
    font = pg.font.Font(None, 74)
    text = font.render("Play", True, (255, 255, 255))
   
    button_width = 200
    button_height = 80
    button_x = screen_width // 2 - button_width // 2
    button_y = screen_height // 2 - button_height // 2
    button_rect = pg.Rect(button_x, button_y, button_width, button_height)
    
    button_color = (0, 0, 128)  
    hover_color = (0, 0, 255)   
    border_color = (255, 255, 255)  
    border_width = 5  

    mouse_x, mouse_y = pg.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        pg.draw.rect(screen, hover_color, button_rect) 
    else:
        pg.draw.rect(screen, button_color, button_rect)  

    pg.draw.rect(screen, border_color, button_rect, border_width)  

    screen.blit(text, (button_rect.x + (button_width - text.get_width()) // 2,
                       button_rect.y + (button_height - text.get_height()) // 2))

    return button_rect

class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0 - Idle, 1 - Attack, 2 - Run, 3 - Jump
        self.update_time = pg.time.get_ticks()

        # Carregar animações de idle
        self.load_animation('Warrior_Idle', 6)
        self.load_animation('Warrior_Run', 7)

        # Carregar animações de ataque
        self.load_animation('Warrior_Attack', 12)

        # Carregar animações de dor (hurt)
        self.load_animation('Warrior_hurt', 4)

        # Carregar animações de morte
        self.load_animation('Warrior_Death', 10)
   
        # Definir a imagem inicial
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocidade_y = 0
        self.no_chao = False

    def load_animation(self, base_name, num_frames):
        temp_list = []
        for i in range(num_frames):
            img = pg.image.load(f'{base_name}_{i}.png')
            img = pg.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def update_animation(self):
        animation_cooldown = 100  # Controlar o tempo de troca entre os quadros da animação
        self.image = self.animation_list[self.action][self.frame_index]

        # Atualizar o quadro da animação
        if pg.time.get_ticks() - self.update_time >= animation_cooldown:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0  # Reiniciar a animação se chegar ao final

    def set_action(self, action):
        self.action = action
        self.frame_index = 0  # Reiniciar o quadro da animação quando a ação muda

    def aplicar_gravidade(self):
        if not self.no_chao:
            self.velocidade_y += 0.5

        self.rect.y += self.velocidade_y

        # Colisão com o chão
        if self.rect.bottom >= screen_height - 200:
            self.rect.bottom = screen_height - 200
            self.velocidade_y = 0
            self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -10  
            self.no_chao = False



# class Enemy():
#     def __init__(self, x, y, name, max_hp, strength):
#         self.name = name
#         self.max_hp = max_hp
#         self.hp = max_hp
#         self.strength = strength
#         self.alive = True
#         self.animation_list = []
#         self.frame_index = 0
#         self.action = 0  # 0 - Idle, 1 - Attack
#         self.update_time = pg.time.get_ticks()

#         # Carregar animações de idle para o inimigo
#         self.load_animation('Skeleton_Idle', 11)
#         self.load_animation('Skeleton_Attack', 18)

       
#         self.image = self.animation_list[self.action][self.frame_index]
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def load_animation(self, base_name, num_frames):
#         temp_list = []
#         for i in range(num_frames):
#             img = pg.image.load(f'{base_name}_{i}.png')
#             img = pg.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
#             temp_list.append(img)
#         self.animation_list.append(temp_list)

#     def update_animation(self):
#         animation_cooldown = 100  
#         self.image = self.animation_list[self.action][self.frame_index]

       
#         if pg.time.get_ticks() - self.update_time >= animation_cooldown:
#             self.update_time = pg.time.get_ticks()
#             self.frame_index += 1

#             if self.frame_index >= len(self.animation_list[self.action]):
#                 self.frame_index = 0 

#     def set_action(self, action):
#         self.action = action
#         self.frame_index = 0  


fighter = Fighter(400, 200, "Warrior", 100, 10, 3)


# enemy = Enemy(600, 200, "Enemy", 100, 10)


run = False
game_started = False

# Loop de tela de menu
while not game_started:
    clock.tick(fps)

    draw_bg()
    draw_painel()

    button_rect = draw_play_button()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                game_started = True  # Iniciar o jogo ao clicar no botão

    pg.display.update()

# Loop do jogo
while game_started:
    clock.tick(fps)

    draw_bg()
    draw_painel()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_started = False

    keys = pg.key.get_pressed()

    # Movendo o jogador
    if keys[pg.K_d]:
        if fighter.rect.x + largura < screen_width:
            fighter.rect.x += player_speed
        if fighter.action != 1:
            fighter.set_action(1)  
    elif keys[pg.K_a]:
        if fighter.rect.x > 0:
            fighter.rect.x -= player_speed
        if fighter.action != 1:
            fighter.set_action(1)  
    else:
        if fighter.action != 0:
            fighter.set_action(0) 


    # Detecção de ataque
    if keys[pg.K_SPACE]:
        fighter.set_action(2) 

    # Detecção de pulo
    if keys[pg.K_w]:
        fighter.pular()

    fighter.update_animation()
    fighter.aplicar_gravidade()

    screen.blit(fighter.image, fighter.rect)

    pg.display.update()

pg.quit()
