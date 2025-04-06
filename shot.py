from pygame import *
from random import randint

init()

# Створення вікна
win_height = 500
win_width = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("1660294647_4-kartinkin-net-p-fon-dlya-igri-kosmos-krasivo-4.jpg"),
                             (win_width, win_height))
speed = 10

# Створення музики
mixer.init()
mixer.music.load("stranger-things-124008 (1).mp3")
mixer.music.play()
fire_sound = mixer.Sound("vyistrel-pistoleta-36125.mp3")

clock = time.Clock()

# Створення лічильника
max_lost = 6
lost = 0
number = 0
img_bullet = "3207692.png"
font.init()
font1 = font.Font(None, 36)
goal = 6

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (35, 35))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("png-clipart-football-player-zombie-mechanic-sprite-sprite-game-building-removebg-preview.png", 250, 400, speed)
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy("images-removebg-preview.png", randint(80, win_width - 80), 0, 2)
    monsters.add(monster)

bullets = sprite.Group()

# Ігровий цикл
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        # Оновлення тексту
        text_lose = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
        score = font1.render("Рахунок: " + str(number), True, (255, 255, 255))

        # Перевірка зіткнень
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            number += 1
            monster = Enemy("images-removebg-preview.png", randint(80, win_width - 80), 0, 2)
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True

        if number >= goal:
            finish = True
      
        # Оновлення екрану
        window.blit(background, (0, 0))
        window.blit(score, (10, 10))
        window.blit(text_lose, (10, 60))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        bullets.update()
        bullets.draw(window)

    else:
        if lost >= max_lost:
            window.blit(font1.render("YOU LOSE", True, (180, 0, 0)), (200, 200))
            import subprocess
            subprocess.run(["python", "lvl2.py"])

            
        elif number >= goal:
            window.blit(font1.render("YOU WIN", True, (0, 180, 0)), (200, 200))

    display.update()
    clock.tick(60)

quit()
