import pygame
import sys
import math
import time

# Afstand tussen twee punten berekenen
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tekst weergeven op het scherm
def draw_text(surface, text, x, y, font_size=20, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Initialisatie van Pygame
pygame.init()

# Instellingen voor het scherm
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("the life saving magic")

# Achtergrond instellingen
background_image = pygame.image.load("afbeeldingen/background.JPG")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Grond instellingen
ground_image = pygame.image.load("afbeeldingen/grond.JPG")
ground_image = pygame.transform.scale(ground_image, (screen_width, ground_image.get_height()))

# Speler instellingen
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - ground_image.get_height()  # Zorg ervoor dat de speler op de grond begint
player_speed = 5
jump = -10  # Spronghoogte

# Variabelen voor het springen
is_jumping = False
jump_count = 10

# Laad speler afbeelding
player_image = pygame.image.load("afbeeldingen/speler.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_image_original = player_image  # Bewaar het origineel voor spiegelen

# Laad poppetje
poppetje_width = 50
poppetje_height = 50
poppetje_image = pygame.image.load("afbeeldingen/poppetje.png")
poppetje_image = pygame.transform.scale(poppetje_image, (poppetje_width, poppetje_height))
poppetje_x = 200
poppetje_y = screen_height - player_height - ground_image.get_height()
poppetje_message = ""
poppetje_message2 = ""
poppetje_message3 = ""

# Platform instellingen
platform_width = 200
platform_height = 20
platform_x = 300
platform_y = screen_height - platform_height - ground_image.get_height() - 50

# Hoofd spel-lus
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Controleer of de speler op het platform staat
    on_platform = (
        player_y + player_height >= platform_y
        and player_y + player_height <= platform_y + 10
        and player_x + player_width > platform_x
        and player_x < platform_x + platform_width
    )

    # Beweging van de speler
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        player_image = player_image_original  # Herstel de originele oriëntatie
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
        player_image = player_image_original
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
        player_image = pygame.transform.flip(player_image_original, True, False)  # Spiegel de speler
    if keys[pygame.K_d] and player_x < screen_width - player_width:
        player_x += player_speed
        player_image = pygame.transform.flip(player_image_original, True, False)  # Spiegel de speler
    if keys[pygame.K_LSHIFT]:
        player_speed = 15
    else:
        player_speed = 5

    # Springen
    if not is_jumping and (keys[pygame.K_SPACE] or keys[pygame.K_w]) and on_platform:
        is_jumping = True

    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Graviteit
    if not on_platform and not is_jumping:
        if player_y < screen_height - player_height - ground_image.get_height():
            player_y += 5  # Simpele graviteitssimulatie
        else:
            player_y = screen_height - player_height - ground_image.get_height()  # Voorkom dat de speler door de grond zakt

    # Controleer afstand tussen speler en poppetje
    distance_to_poppetje = calculate_distance(player_x, player_y, poppetje_x, poppetje_y)

    # Controleer of de speler dichtbij genoeg is en op de "E"-toets drukt
    if distance_to_poppetje < 50 and keys[pygame.K_e]:
        # Voer hier acties uit wanneer de speler interactie heeft met het poppetje
        poppetje_message = "Wow, dus jij bent de tovenaar die ons komt redden"
        poppetje_message2 = "Een monster heeft alle mensen ontvoerd"
        poppetje_message3 = "En jij moet ze vinden en de weg terug vertellen, veel succes"
    else:
        poppetje_message = ""
        poppetje_message2 = ""
        poppetje_message3 = ""

    # Tekenen op het scherm
    screen.blit(background_image, (0, 0))  # Tekenen van de achtergrond
    screen.blit(ground_image, (0, screen_height - ground_image.get_height()))  # Tekenen van de grond

    # Tekenen van het platform
    pygame.draw.rect(screen, (0, 0, 255), (platform_x, platform_y, platform_width, platform_height))

    # Tekenen van de speler
    screen.blit(player_image, (player_x, player_y))
    screen.blit(poppetje_image, (poppetje_x, poppetje_y))

    # Tekenen van het bericht als de speler in de buurt van het poppetje is
    if distance_to_poppetje < 50:
        draw_text(screen, "Houd 'E' ingedrukt voor interactie", poppetje_x - 50, poppetje_y - 20)

    # Tekenen van het poppetje bericht
    draw_text(screen, poppetje_message, 50, 30)  # Aanpassen van de positie indien nodig
    draw_text(screen, poppetje_message2, 50, 40)
    draw_text(screen, poppetje_message3, 50, 50)

    # Scherm bijwerken
    pygame.display.flip()

    # FPS beperken
    clock.tick(30)
