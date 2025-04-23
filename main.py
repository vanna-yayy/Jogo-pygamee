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
painel_img = pg.image.load("menu.jfif").convert_alpha()

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
def draw_barra_vida(current_hp, max_hp):
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10

        # Calcula a largura da barra de vida com base na vida atual
        fill_width = int((current_hp / max_hp) * bar_width)

        # Desenha a barra de fundo (vida máxima)
        pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Desenha a barra de vida atual
        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

        # Desenha a borda da barra de vida
        pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  

def draw_barra_vida_inimigo(enemy):
    bar_width = 60  
    bar_height = 10  
    bar_x = enemy.rect.centerx - bar_width // 2  
    bar_y = enemy.rect.top - 2  
    # Calcula a largura da barra de vida com base na vida atual
    fill_width = int((enemy.hp / enemy.max_hp) * bar_width)

    # Desenha a barra de fundo (vida máxima)
    pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

    # Desenha a barra de vida atual
    pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

    # Desenha a borda da barra de vida
    pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  # Borda branca


def verificar_colisao(fighter, enemies):
    for enemy in enemies:
        if fighter.rect.colliderect(enemy.rect):
            if fighter.action == 2 and pg.time.get_ticks() - fighter.attack_cooldown > 500:  
                enemy.hp -= fighter.strength
                fighter.attack_cooldown = pg.time.get_ticks()
                if enemy.hp <= 0:      
                    enemy.alive = False
                    enemy.set_action(4)  # Animação de morte do inimigo
            if enemy.action == 2 and pg.time.get_ticks() - enemy.attack_cooldown > 500:  # Se o inimigo está atacando
                fighter.hp -= enemy.strength
                enemy.attack_cooldown = pg.time.get_ticks()
                if fighter.hp <= 0:
                    fighter.alive = False  # O jogador morre




def verificar_colisao_inimigo_ataque(enemy, fighter):
    if not enemy.alive:
        return 
    
    if enemy.action == 2:  # Se o inimigo está atacando
        if pg.time.get_ticks() - enemy.attack_cooldown > 300:  
            attack_rect = pg.Rect(enemy.rect.x + 50, enemy.rect.y, enemy.rect.width, enemy.rect.height)  # Ajuste a posição do ataque
            if attack_rect.colliderect(fighter.rect):
                # Só aplica dano se o jogador não estiver pulando
                if fighter.no_chao:  
                    fighter.hp -= enemy.strength
                    enemy.attack_cooldown = pg.time.get_ticks()  
                    if fighter.hp <= 0:
                        fighter.alive = False
                        fighter.set_action(4)  # Animação de morte do jogador



def verificar_colisao_ataque(fighter, enemy):
    if fighter.action == 2:  # Se o jogador está atacando
        if fighter.rect.colliderect(enemy.rect):  # Verificar colisão
            dano = fighter.strength * 0.2  # Aplica 50% do dano original (exemplo)
            enemy.hp -= dano  # Dano reduzido
            if enemy.hp <= 0:
                enemy.alive = False  # O inimigo morre
                enemy.set_action(4)  # Animação de morte do inimigo



def verificar_vitoria(enemies):
    # Verificar se todos os inimigos estão mortos
    for enemy in enemies:
        if enemy.alive:
            return False  # Se algum inimigo ainda estiver vivo, não há vitória
    return True 

def exibir_mensagem(texto, cor, tamanho, x, y):
    font = pg.font.Font(None, tamanho)
    mensagem = font.render(texto, True, cor)
    screen.blit(mensagem, (x - mensagem.get_width() // 2, y - mensagem.get_height() // 2))


class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0 - Idle, 1 - Run, 2 - Attack, 3 - Jump
        self.update_time = pg.time.get_ticks()
        self.attack_cooldown = 5  # Adicione um cooldown para a animação de ataque
        self.is_dead = False  
        self.dead_animation_played = False 
       

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
        animation_cooldown = 100  
        self.image = self.animation_list[self.action][self.frame_index]
        self.image = pg.transform.flip(self.image, self.flip, False)  

        # Atualizar o quadro da animação
        if pg.time.get_ticks() - self.update_time >= animation_cooldown:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0  
                if self.action == 2:  
                    self.set_action(0)

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame_index = 0  
            self.update_time = pg.time.get_ticks()  

    def aplicar_gravidade(self):
        if not self.no_chao:
            self.velocidade_y += 0.5

        self.rect.y += self.velocidade_y

        # Colisão com o chão
        if self.rect.bottom >= screen_height - 200:
            self.rect.bottom = screen_height - 200
            self.velocidade_y = 0
            self.no_chao = True

    def play_death_animation(self):
        # definir a animação de morte
        print("Animação de morte do personagem está sendo exibida!")
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Exemplo de animação

    def kill(self):
        # Função para "matar" o personagem
        self.is_dead = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -10  
            self.no_chao = False


class Enemy:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.flip = True  # O inimigo começa virado para a esquerda
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0 - Idle, 1 - Run, 2 - Attack, 3 - Hurt, 4 - Die
        self.update_time = pg.time.get_ticks()
        self.attack_cooldown = 3
        self.attack_range = 50  # Distância mínima para começar o ataque

        # Carregar animações do inimigo
        self.load_animation('Cogumelo-Idle', 7)
        self.load_animation('Cogumelo-Run', 8)
        self.load_animation('Cogumelo-Attack', 10)
        self.load_animation('Cogumelo-Hit', 5)
        self.load_animation('Cogumelo-Die', 15)

        # Definir a imagem inicial
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocidade_y = 0
        self.no_chao = False

    def load_animation(self, base_name, num_frames):
        sprite_sheet = pg.image.load(f'{base_name}.png')
        sprite_width = 80
        sprite_height = 64
        temp_list = []
        for i in range(num_frames):
            x = i * sprite_width
            y = 0
            frame = sprite_sheet.subsurface(pg.Rect(x, y, sprite_width, sprite_height))
            frame = pg.transform.scale(frame, (int(sprite_width * 2), int(sprite_height * 2)))  # Alterando o fator de escala (ex: 2x menor)
            temp_list.append(frame)
        self.animation_list.append(temp_list)
        
    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        self.image = pg.transform.flip(self.image, self.flip, False)  # Inverter a imagem
        if pg.time.get_ticks() - self.update_time >= animation_cooldown:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            if self.action == 2:  # Se for a ação de ataque, muda para idle
                self.set_action(0)
            

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def aplicar_gravidade(self):
        if not self.no_chao:
            self.velocidade_y += 0.5
        self.rect.y += self.velocidade_y
        if self.rect.bottom >= screen_height - 200:
            self.rect.bottom = screen_height - 200
            self.velocidade_y = 0
            self.no_chao = True

    def mover(self, fighter):
        if self.alive and fighter.alive:
            # Calculando a distância entre o inimigo e o jogador
            distancia = abs(self.rect.x - fighter.rect.x)

            if distancia > self.attack_range:  # Se estiver fora do alcance de ataque, o inimigo se aproxima
                if self.rect.x > fighter.rect.x:
                    self.rect.x -= 1  # Movimenta o inimigo para a direita
                    self.flip = False  # Inverte a imagem para a direita
                elif self.rect.x < fighter.rect.x:
                    self.rect.x += 1  # Movimenta o inimigo para a esquerda
                    self.flip = True  # Inverte a imagem para a esquerda
                self.set_action(1)  # Corrida
            else:
                # Quando estiver dentro do alcance de ataque, o inimigo ataca
                self.set_action(2)  # Ataque




fighter = Fighter(400, 200, "Warrior", 100, 3, 3)
enemy = Enemy(600, 200, "Cogumelo", 50, 2, 2) 
enemy2 = Enemy(650, 200, "Cogumelo2", 50, 2, 2)  
enemy3 = Enemy(700, 200, "Cogumelo3", 50, 2, 2)  
enemy4 = Enemy(500, 200, "Cogumelo4", 50, 2, 2) 
enemy5 = Enemy(550, 200, "Cogumelo5", 50, 2, 2) 
enemy6 = Enemy(600, 200, "Cogumelo6", 50, 2, 2)  

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
def new_func(screen_width, player_speed, largura, fighter):
    if not fighter.alive:
        return  # Se o jogador não estiver vivo, não faz nada.
    
    keys = pg.key.get_pressed()

    # Movendo o jogador
    if keys[pg.K_d]:
        if fighter.rect.x + largura < screen_width:
            fighter.rect.x += player_speed
        if fighter.action != 1:
            fighter.set_action(1)  
        fighter.flip = False
    elif keys[pg.K_a]:
        if fighter.rect.x > 0:
            fighter.rect.x -= player_speed
        if fighter.action != 1:
            fighter.set_action(1)  
        fighter.flip = True
            
    if keys[pg.K_w]:
        fighter.pular()

    if keys[pg.K_SPACE] and fighter.action != 2:
        fighter.set_action(2)
        fighter.attack_cooldown = pg.time.get_ticks()

    if not (keys[pg.K_d] or keys[pg.K_a] or keys[pg.K_w] or keys[pg.K_SPACE]):
        if fighter.action != 0:
            fighter.set_action(0)

while game_started:
    clock.tick(fps)

    draw_bg()
    draw_painel()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_started = False

    new_func(screen_width, player_speed, largura, fighter)

    fighter.update_animation()
    fighter.aplicar_gravidade()

    enemies = [enemy, enemy2, enemy3, enemy4, enemy5, enemy6]
    verificar_colisao(fighter, enemies)

    # Verificar colisões e aplicar dano entre o jogador e os inimigos
    verificar_colisao_ataque(fighter, enemy)
    verificar_colisao_ataque(fighter, enemy2)
    verificar_colisao_ataque(fighter, enemy3)
    verificar_colisao_ataque(fighter, enemy4)
    verificar_colisao_ataque(fighter, enemy5)
    verificar_colisao_ataque(fighter, enemy6)



    verificar_colisao_inimigo_ataque(enemy, fighter)
    verificar_colisao_inimigo_ataque(enemy2, fighter)
    verificar_colisao_inimigo_ataque(enemy3, fighter)
    verificar_colisao_inimigo_ataque(enemy4, fighter)
    verificar_colisao_inimigo_ataque(enemy5, fighter)
    verificar_colisao_inimigo_ataque(enemy6, fighter)

    draw_barra_vida(fighter.hp, fighter.max_hp)

    if not fighter.alive:
        exibir_mensagem("Você morreu!!", (255, 0, 0), 100, screen_width // 2, screen_height // 2)
    else:
        screen.blit(fighter.image, fighter.rect)

    if verificar_vitoria(enemies):
        font = pg.font.Font(None, 74)
        victory_text = font.render("VOCÊ VENCEU!", True, (0, 255, 0))  # Texto verde
        screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 2 - victory_text.get_height() // 2))

    screen.blit(fighter.image, fighter.rect)

    for enemy in enemies:
        enemy.mover(fighter)
        enemy.update_animation()
        enemy.aplicar_gravidade()
        screen.blit(enemy.image, enemy.rect)

        draw_barra_vida_inimigo(enemy)   

    pg.display.update()

pg.quit()
