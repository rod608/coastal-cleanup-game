import pygame
import asyncio
from PIL import Image

pygame.init()

async def main():
    # screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    # colors
    sand_color = (238, 214, 175)
    yellow = (255, 255, 0)
    black = (0, 0, 0)

    # images
    pil_image_recycle = Image.open("img/recycle-bin.png")
    image_recycle = pygame.image.fromstring(pil_image_recycle.tobytes(), pil_image_recycle.size, pil_image_recycle.mode)

    pil_image_trash = Image.open("img/trash-bin.png")
    image_trash = pygame.image.fromstring(pil_image_trash.tobytes(), pil_image_trash.size, pil_image_trash.mode)

    pil_image_water = Image.open("img/water-bottle.png")
    image_water = pygame.image.fromstring(pil_image_water.tobytes(), pil_image_water.size, pil_image_water.mode)

    pil_image_soda = Image.open("img/can.png")
    image_soda = pygame.image.fromstring(pil_image_soda.tobytes(), pil_image_soda.size, pil_image_soda.mode)

    pil_image_bubble = Image.open("img/bubblewrap.png")
    image_bubble = pygame.image.fromstring(pil_image_bubble.tobytes(), pil_image_bubble.size, pil_image_bubble.mode)

    pil_image_glass = Image.open("img/glass.png")
    image_glass = pygame.image.fromstring(pil_image_glass.tobytes(), pil_image_glass.size, pil_image_glass.mode)

    # draggable items
    rects = [
        {"rect": pygame.Rect(50, 50, 55, 55), "type": "Recyclable"},
        {"rect": pygame.Rect(150, 100, 55, 55), "type": "Trash"},
        {"rect": pygame.Rect(200, 300, 55, 55), "type": "Recyclable"},
        {"rect": pygame.Rect(550, 50, 55, 55), "type": "Trash"}
    ]

    # bins
    recycle_bin = pygame.Rect(width // 4, height - 100, 55, 55)
    trash_bin = pygame.Rect(3 * width // 4, height - 100, 55, 55)

    # game variables
    selected_rect = None
    fact = False
    level = 1
    game_won = False  # Game state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    for rect_data in rects:
                        if rect_data["rect"].collidepoint(event.pos):
                            selected_rect = rect_data["rect"]
                            rect_offset = (event.pos[0] - selected_rect.x, event.pos[1] - selected_rect.y)
                            fact = True
                            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_rect = None
                    # check for correct bin drop and remove if necessary
                    rects_to_remove = []
                    for i, rect_data in enumerate(rects):
                        rect = rect_data["rect"]
                        rect_type = rect_data["type"]
                        if (rect_type == "Recyclable" and rect.colliderect(recycle_bin)) or \
                        (rect_type == "Trash" and rect.colliderect(trash_bin)):
                                rects_to_remove.append(i)

                    for index in sorted(rects_to_remove, reverse=True):
                        del rects[index]
                        level = level + 1
                        fact = False

            elif event.type == pygame.MOUSEMOTION:
                if selected_rect:
                    selected_rect.x = event.pos[0] - rect_offset[0]
                    selected_rect.y = event.pos[1] - rect_offset[1]

        screen.fill(sand_color)
        
        # draw bins
        screen.blit(image_recycle, (width // 4, height - 100, 55, 55))
        screen.blit(image_trash, (3 * width // 4, height - 100, 55, 55))
        if level == 1:
            screen.blit(image_water, (rects[0]["rect"].x, rects[0]["rect"].y, 55, 55))
            rect = rects[0]["rect"]
            if selected_rect is None and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, yellow, rect, 2)
        elif level == 2:
            screen.blit(image_bubble, (rects[0]["rect"].x, rects[0]["rect"].y, 55, 55))
            rect = rects[0]["rect"]
            if selected_rect is None and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, yellow, rect, 2)
        elif level == 3:
            screen.blit(image_soda, (rects[0]["rect"].x, rects[0]["rect"].y, 55, 55))
            rect = rects[0]["rect"]
            if selected_rect is None and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, yellow, rect, 2)
        elif level == 4:
            screen.blit(image_glass, (rects[0]["rect"].x, rects[0]["rect"].y, 55, 55))
            rect = rects[0]["rect"]
            if selected_rect is None and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, yellow, rect, 2)

        # draw facts
        if fact and level == 1:
            font = pygame.font.Font(None, 32)
            text = font.render("8 million tons of plastic bottles enter our oceans every year.", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
        elif fact and level == 2:
            font = pygame.font.Font(None, 32)
            text = font.render("Ocean species mistake trash in the ocean as prey.", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
        elif fact and level == 3:
            font = pygame.font.Font(None, 32)
            text = font.render("Aluminum is a non-biodegradable material", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2 - 25))
            screen.blit(text, text_rect)
            font = pygame.font.Font(None, 32)
            text = font.render("that can take hundreds of years to decompose", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2 + 25))
            screen.blit(text, text_rect)
        elif fact and level == 4:
            font = pygame.font.Font(None, 32)
            text = font.render("Glass harms sea species and humans.", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)

        # check for win condition
        if not rects:
            game_won = True

        # display win message
        if game_won:
            font = pygame.font.Font(None, 32)
            text = font.render("Great Job, You have successfully helped our beaches stay clean!", True, black)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
