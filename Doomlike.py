#-*-coding:UTF-8-*-

import pygame
import random
# import os


class Utils():  # Utilitarios
    def getScores(self, file_name):  # Le a lista de highscores
        List = []
        f = open(file_name, "r")
        for line in f:
            if line[0] != "\n" and line[0] != "":
                List.append(line.rstrip().split(';'))
        f.close()
        return (List)

    def sortScores(self, file_name):  # Organiza a lista
        List = self.getScores(file_name)
        sortedList = sorted(List, key=lambda score: int(score[1]))
        sortedList.reverse()
        f = open(file_name, "w")
        for line in sortedList:
            f.write(line[0] + ';' + line[1] + '\n')
        f.close()
        return (List)

    def addToFile(self, newline, file_name):  # Adiciona um novo nome a lista
        f = open(file_name, "a")
        f.write(newline)
        f.close()


class Shoot():  # Classe do tiro
    def __init__(self, screen, shoot_img):  # Inicia a classe

        self.screen = screen

        self.Orig_img = shoot_img
        self.Orig_img = pygame.transform.scale(
            self.Orig_img, (self.Orig_img.get_width() * 3, self.Orig_img.get_height() * 3))

        self.timer = 0
        self.pos_z = 0
        self.pos_x = screen.get_width() / 2

        self.rect = pygame.Rect(self.pos_x, self.pos_x, 10, 10)

    def refreshX(self, add):  # Atualiza sua posição em X
        self.pos_x += add

    def refresh(self):  # Atualiza sua posição em Z

        size = self.pos_z / 5

        self.img = pygame.transform.scale(
            self.Orig_img, (int(self.Orig_img.get_width() - size), int(self.Orig_img.get_height() - size)))

        self.rect = pygame.Rect(self.pos_x - 10 + int(self.Orig_img.get_width() / 2 - self.img.get_width() / 2),
                                self.screen.get_rect().height / 2 + 20 - int(self.pos_z / 10), self.img.get_width(), self.img.get_height())

        self.timer = (self.timer + 1) % 5
        if self.timer == 0:
            self.pos_z += 60


class Enemy():  # Classe de inimigos
    def __init__(self, screen, orig_img, hit_imgs, orig_death, orig_explo, sound_explo, sound_pain, sound_roam, sound_death):  # Inicializa a classe
        self.screen = screen

        self.Orig_imgs = orig_img
        self.Hit_imgs = hit_imgs
        self.Orig_death = orig_death
        self.Orig_explo = orig_explo

        self.hit = False
        self.isAlive = True

        self.currsprite = 0
        self.life = 3

        # Carrega os sons
        self.explo_sound = sound_explo
        self.pain = sound_pain
        self.roam_sound = sound_roam
        self.death_sound = sound_death

        self.roam_sound.play(0)

        # Definição de variáveis
        self.pos_z = 100
        self.pos_x = random.randint(100, 700)
        self.timer = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_x, 10, 10)

        # Flags
        self.dying = False
        self.exploding = False
        self.dead = False

    def refreshX(self, add):  # Atualiza posição em X
        self.pos_x += add
        if self.pos_x > 2650:
            self.pos_x = -50
        elif self.pos_x < -1800:
            self.pos_x = 850

    def deadAnim(self):  # Ativa animação de morte
        self.dying = True
        self.currsprite = 0

    def refresh(self):  # Atualiza posição em Z e as sprites para cada flag
        if self.dying:  # Morrendo
            size = self.pos_z / 5
            self.img = pygame.transform.scale(
                self.Orig_death[self.currsprite], (int(self.Orig_death[0].get_width() - size), int(self.Orig_death[0].get_height() - size)))

            self.rect = pygame.Rect(self.pos_x - 10 + int(self.Orig_death[0].get_width() / 2 - self.img.get_width() / 4),
                                    self.screen.get_rect().height / 4 - int(self.pos_z / 20) + 110, self.img.get_width() / 2, self.img.get_height() / 2)

            self.timer = (self.timer + 1) % 5
            if self.timer == 0:
                self.currsprite += 1
                if self.currsprite == len(self.Orig_death):
                    self.dead = True

        elif self.exploding:  # Explodindo
            size = self.pos_z / 5

            self.img = pygame.transform.scale(
                self.Orig_explo[self.currsprite], (int(self.Orig_explo[0].get_width() - size) * 2, int(self.Orig_explo[0].get_height() - size) * 2))

            self.rect = pygame.Rect(self.pos_x - 10 + int(self.Orig_explo[0].get_width() / 2 - self.img.get_width() / 4),
                                    self.screen.get_rect().height / 4 - int(self.pos_z / 20) + 110, self.img.get_width() / 2, self.img.get_height() / 2)

            self.timer = (self.timer + 1) % 5
            if self.timer == 0:
                self.currsprite += 1
                if self.currsprite == len(self.Orig_explo):
                    self.dead = True
        else:  # Andando normal
            size = self.pos_z / 5

            if self.hit:
                self.img = pygame.transform.scale(
                    self.Hit_imgs[self.currsprite], (int(self.Hit_imgs[0].get_width() - size), int(self.Hit_imgs[0].get_height() - size)))
            else:
                self.img = pygame.transform.scale(
                    self.Orig_imgs[self.currsprite], (int(self.Orig_imgs[0].get_width() - size), int(self.Orig_imgs[0].get_height() - size)))

            self.rect = pygame.Rect(self.pos_x - 10 + int(self.Orig_imgs[0].get_width() / 2 - self.img.get_width() / 4),
                                    self.screen.get_rect().height / 4 - int(self.pos_z / 20) + 110, self.img.get_width() / 2, self.img.get_height() / 2)

            self.timer = (self.timer + 1) % 5
            if self.timer == 0:
                self.currsprite += 1
                self.currsprite = self.currsprite % 5
                self.pos_z -= 10

            if self.hit:
                self.hittimer = (self.hittimer + 1) % 15
                if self.hittimer == 0:
                    self.hit = False


class Player():  # Classe do jogador
    def __init__(self):

        # Carrega imagens
        self.sprites = []
        for img in range(3):
            self.sprites.append(pygame.image.load(
                'hand0' + str(img + 1) + '.png'))

        for index, img in enumerate(self.sprites):
            self.sprites[index] = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3))

        self.faces = []
        for img in range(6):
            self.faces.append(pygame.image.load(
                'faces/face' + str(img) + '.png'))

        # Define variáveis
        self.life = 5
        self.currsprite = 0
        self.timer = 0

    def shootAnim(self):  # Gerencia animação de tiro
        self.timer = (self.timer + 1) % 5
        if self.timer == 0:
            self.currsprite = (self.currsprite + 1) % 3
            if self.currsprite == 0:
                return (False)
        return(True)


class Game():  # Classe principal
    def __init__(self, screen):
        # Definições da tela
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        # Carregar fonte
        font = 'fonts/AmazDooMLeft.ttf'
        font_size = 60
        self.font = pygame.font.Font(font, font_size)
        self.title = pygame.font.Font(font, 80)

        self.menuItems = ['PLAY', 'HIGHSCORES']
        self.menu_pos = 0

        # Carregar Audio
        pygame.mixer.music.load('sounds/music0.ogg')
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
        self.player_death = pygame.mixer.Sound('sounds/PlayerDeath.wav')
        self.player_hurt = pygame.mixer.Sound('sounds/PlayerHurt.wav')

        # Carregar imagem de fundo
        self.background = pygame.image.load('bg.jpg')
        self.hs_bg = pygame.image.load('highscore.png')
        self.menu = pygame.image.load('menu.png')
        self.bg_size = self.background.get_width()

        # Sprites
        self.shootImg = pygame.image.load('shoot.png')

        self.Orig_imgs = []
        self.Hit_imgs = []
        self.Orig_death = []
        self.Orig_explo = []

        # Carrega os sprites
        for i in range(5):
            self.Orig_imgs.append(pygame.image.load(
                'enemy/enemy' + str(i) + '.png'))

        for i in range(5):
            self.Hit_imgs.append(pygame.image.load(
                'enemy/enemyhit' + str(i) + '.png'))

        for i in range(10):
            self.Orig_death.append(pygame.image.load(
                'enemy/death' + str(i) + '.png'))

        for i in range(5):
            self.Orig_explo.append(pygame.image.load(
                'enemy/explosion' + str(i) + '.png'))

        # Carrega os sons
        self.explo_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.pain = pygame.mixer.Sound('sounds/ImpPain.wav')
        self.roam_sound = pygame.mixer.Sound('sounds/ImpRoam.wav')
        self.death_sound = [pygame.mixer.Sound('sounds/ImpDeath1.wav'),
                            pygame.mixer.Sound('sounds/ImpDeath2.wav')]

        self.name = 'AAA'

        self.enemyRespaw = 1

    def drawCounter(self):  # Desenha o contador de mortes
        text = 'Kills: ' + str(self.counter)
        text = self.font.render(text, True, (250, 250, 250))

        t_w = text.get_rect().width

        self.screen.blit(text, (self.scr_width / 2 - t_w / 2, 20))

    def drawHS(self):  # Desenha os HighScores
        text = self.title.render('HIGHSCORES', True, (200, 200, 200))
        t_w = text.get_rect().width
        self.screen.blit(text, (self.scr_width / 2 - t_w / 2, 20))

        self.canEdit = True
        isHigh = False
        sumHigh = 0
        HS_List = Utils().getScores('highscores')

        if self.counter is 0:
            self.canEdit = False
        else:
            # Verifica se a pontuação entra nos highscores
            if len(HS_List) > 5:
                if self.counter > int(HS_List[5][1]):
                    isHigh = True
            else:
                isHigh = True

            # Se não entrar, só exibe no fim da lista
            if isHigh is False:
                if len(HS_List) > 5:
                    size = 5
                else:
                    size = len(HS_List)
                name = self.font.render('You', True, (150, 150, 150))
                score = self.font.render(
                    str(self.counter), True, (150, 150, 150))
                s_w = score.get_rect().width
                size += 1
                self.screen.blit(
                    name, (self.scr_width / 2 - 200, 50 * size + 120))
                self.screen.blit(
                    score, (self.scr_width / 2 + 200 - s_w, 50 * size + 120))
                self.canEdit = False

        text = self.font.render(
            'press <ENTER> to continue', True, (250, 250, 250))
        t_w = text.get_rect().width
        self.screen.blit(text, (self.scr_width / 2 -
                                t_w / 2, self.scr_height - 80))

        # Desenha toda lista
        for index, hscore in enumerate(HS_List):
            if index > 5:
                break
            if isHigh:  # Posiciona a pontuação corretamente na lista, caso ela entre
                if self.counter > int(hscore[1]):
                    name = self.font.render(self.name, True, (250, 50, 50))
                    score = self.font.render(
                        str(self.counter), True, (250, 50, 50))
                    s_w = score.get_rect().width
                    self.screen.blit(
                        name, (self.scr_width / 2 - 200, 50 * index + sumHigh + 120))
                    self.screen.blit(
                        score, (self.scr_width / 2 + 200 - s_w, 50 * index + sumHigh + 120))
                    sumHigh = 60
                    isHigh = False

            name = self.font.render(hscore[0], True, (250, 250, 250))
            score = self.font.render(hscore[1], True, (250, 250, 250))
            s_w = score.get_rect().width
            self.screen.blit(
                name, (self.scr_width / 2 - 200, 50 * index + sumHigh + 120))
            self.screen.blit(
                score, (self.scr_width / 2 + 200 - s_w, 50 * index + sumHigh + 120))

    def drawMenu(self):
        for index, item in enumerate(self.menuItems):
            if self.menu_pos == index:
                item = self.title.render(
                    self.menuItems[index], True, (250, 0, 0))
            else:
                item = self.title.render(
                    self.menuItems[index], True, (250, 250, 250))
            item_w = item.get_rect().width
            self.screen.blit(
                item, (self.scr_width / 2 - item_w / 2, 80 * index + 420))

    def checkEvents(self):  # Eventos de input
        if self.Menu:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.menu_pos = abs(
                            self.menu_pos - 1) % len(self.menuItems)
                    elif event.key == pygame.K_UP:
                        self.menu_pos = abs(
                            self.menu_pos + 1) % len(self.menuItems)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_pos == 0:
                            self.Menu = False
                            self.isRunning = True
                        elif self.menu_pos == 1:
                            self.Menu = False
                            self.isRunning = False

        elif self.isRunning:
            pressed = pygame.key.get_pressed()
            # Movimentação lateral
            if pressed[pygame.K_d]:
                for shoot in self.shootList:
                    shoot.refreshX(-10)
                for enemy in self.enemyList:
                    enemy.refreshX(-10)
                self.bg_pos[0] -= 10
            if pressed[pygame.K_a]:
                for shoot in self.shootList:
                    shoot.refreshX(10)
                for enemy in self.enemyList:
                    enemy.refreshX(10)
                self.bg_pos[0] += 10

            # Fix da posição do background
            if self.bg_pos[0] == -2650:
                self.bg_pos[0] = 0
            elif self.bg_pos[0] == 800:
                self.bg_pos[0] = -1880

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    # Tiros
                    if event.key == pygame.K_SPACE:

                        if self.shoot is False:
                            self.shoot_sound.play(0)
                            self.shoot = True
                            self.shootList.append(
                                Shoot(self.screen, self.shootImg))
                    elif event.key == pygame.K_w:
                        self.enemyList.append(Enemy(self.screen, self.Orig_imgs, self.Hit_imgs, self.Orig_death,
                                                    self.Orig_explo, self.explo_sound, self.pain, self.roam_sound, self.death_sound))

        else:
            if self.canEdit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key >= 97 and event.key <= 122:
                            if len(self.name) < 3:
                                letter = chr(event.key)
                                letter = letter.upper()
                                self.name = self.name + letter

                        elif event.key == pygame.K_SPACE:
                            self.name = self.name + ' '
                        elif event.key == pygame.K_BACKSPACE:
                            self.name = self.name[:-1]
                        elif event.key == pygame.K_RETURN:
                            Utils().addToFile(self.name + ';' + str(self.counter), 'highscores')
                            Utils().sortScores('highscores')
                            self.Menu = True
                            self.reset()
                        elif event.key == pygame.K_ESCAPE:
                            exit()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.Menu = True
                            self.reset()

    def blitChar(self, player):  # Printa a mão do personagem na tela
        player_size = player.sprites[player.currsprite].get_rect().width / 2

        if self.shoot is True:
            self.shoot = player.shootAnim()

        self.screen.blit(
            player.sprites[player.currsprite], (self.scr_width / 2 - player_size, self.scr_height - player.sprites[player.currsprite].get_height()))

    def drawLifes(self, player):  # Printa as faces e a quantidade de vidas do personagem
        text = 'Lifes: ' + str(player.life)
        text = self.font.render(text, True, (250, 250, 250))
        img = pygame.transform.scale(
            player.faces[4 - (player.life - 1)], (player.faces[4 - (player.life - 1)].get_width() * 3, player.faces[4 - (player.life - 1)].get_height() * 3))
        self.screen.blit(img, (10, 500))
        self.screen.blit(text, (100, 530))

    def reset(self):  # Reseta todas as flags e variaveis para posição inicial
        self.counter = 0
        self.shoot = False
        self.bg_pos = [0, 0]
        self.shootList = []
        self.enemyList = []
        self.isRunning = True

        self.player = Player()

    def run(self):
        self.isRunning = True
        while True:  # Loop principal
            global mainloop
            mainloop = True
            pygame.mixer.music.play(-1)
            self.reset()
            self.Menu = True
            while mainloop:  # Loop da partida
                if self.Menu:
                    self.screen.blit(self.menu, (0, 0))
                    self.drawMenu()
                else:
                    if self.isRunning:
                        # Printa o background
                        self.screen.blit(self.background, self.bg_pos)

                        if self.bg_pos[0] < -1950:
                            self.screen.blit(
                                self.background, (self.bg_pos[0] + 1880 + self.scr_width, self.bg_pos[1]))
                        elif self.bg_pos[0] > 0:
                            self.screen.blit(
                                self.background, (self.bg_pos[0] - 2685, self.bg_pos[1]))

                        # Printa os Tiros
                        for index, shoot in enumerate(self.shootList):
                            shoot.refresh()
                            self.screen.blit(shoot.img, (shoot.pos_x - 10 + int(shoot.Orig_img.get_width() / 2 - shoot.img.get_width() / 2),
                                                         self.scr_height / 2 + 20 - int(shoot.pos_z / 10)))

                            if shoot.pos_z >= self.scr_height / 2:
                                self.shootList.pop(index)

                        # Gera inimigos

                        self.enemyRespaw = (
                            self.enemyRespaw + 1) % (300 - self.counter * 1.5)

                        if int(self.enemyRespaw) == 0:
                            self.enemyList.append(Enemy(self.screen, self.Orig_imgs, self.Hit_imgs, self.Orig_death,
                                                        self.Orig_explo, self.explo_sound, self.pain, self.roam_sound, self.death_sound))

                        # Verifica colisão entre Shoot() e Enemy()
                        for enemy_index, enemy in enumerate(self.enemyList):
                            for shoot_index, shoot in enumerate(self.shootList):

                                enemy_dist = abs(enemy.pos_z) / 1000
                                shoot_dist = abs(shoot.pos_z) / 240

                                if enemy.rect.colliderect(shoot.rect) and abs(enemy_dist - shoot_dist) < 0.1:
                                    self.shootList.pop(shoot_index)
                                    enemy.pain.play(0)
                                    enemy.life -= 1
                                    enemy.hit = True
                                    enemy.hittimer = 0
                                    if enemy.life == 0:
                                        enemy.death_sound[random.randint(
                                            0, 1)].play(0)
                                        enemy.deadAnim()
                            if enemy.dead is True:
                                self.counter += 1
                                self.enemyList.pop(enemy_index)

                        # Printa os inimigos
                        if len(self.enemyList) > 0:
                            for enemy in reversed(self.enemyList):
                                enemy.refresh()
                                self.screen.blit(enemy.img, (enemy.pos_x - 10 + int(enemy.Orig_imgs[0].get_width() / 2 - enemy.img.get_width() / 2),
                                                             self.scr_height / 2 - 90 - int(enemy.pos_z / 20)))

                            # Dano no personagem baseado na pos_z do inimigo
                            for enemy in self.enemyList:
                                if enemy.pos_z < -1000:
                                    if enemy.exploding is False:
                                        enemy.explo_sound.play(0)
                                        enemy.exploding = True
                                        enemy.currsprite = 0
                                        self.player_hurt.play(0)
                                        self.player.life -= 1

                        # Chama as funções de printar
                        self.blitChar(self.player)
                        self.drawCounter()
                        self.drawLifes(self.player)

                        # Verifica se o personagem está vivo
                        if self.player.life <= 0:
                            self.player_death.play(0)
                            self.isRunning = False
                            self.canEdit = True
                    else:
                        self.screen.blit(self.hs_bg, (0, 0))
                        self.drawHS()

                self.checkEvents()
                pygame.display.flip()


# Inicializa pygame e mixer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

# Roda o programa
if __name__ == "__main__":
    # Cria a tela
    clock = pygame.time.Clock()
    clock.tick(30)

    screen = pygame.display.set_mode((800, 600), 0, 32)
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Doomlike')

    # Roda a classe Game()
    Game = Game(screen)
    Game.run()
