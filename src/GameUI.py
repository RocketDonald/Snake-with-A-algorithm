import os
import pygame
import Block
import Game

pygame.font.init()

size = width, height = 780, 780
playAreaSize = playAreaWidth, playAreaHeight = 660, 660
playAreaX = (width - playAreaWidth) / 2
playAreaY = (height - playAreaHeight) / 2 + 40
numOfGrids = 30
fps = 2
timePerFrame = 1 / fps
foodSizeRatio = 0.8

white = 255, 255, 255
black = 0, 0, 0
lightGreen = 100, 160, 50
deepGreen = 70, 125, 35
red = 175, 80, 80

currDir = os.path.dirname(__file__)
fontFile = 'arcade.TTF'
fontPath = os.path.join(currDir, fontFile)


# draws text in the middle
def draw_text_middle(text, text_size, color, surface):
    font = pygame.font.Font(fontPath, text_size, bold=False, italic=True)
    label = font.render(text, 1, color)

    surface.blit(label, (width/2 - (label.get_width()/2), height/2 - (label.get_height()/2)))


def draw_playArea(surface):
    playArea = pygame.Rect((playAreaX, playAreaY), (playAreaWidth, playAreaHeight))
    pygame.draw.rect(surface, black, playArea)


def draw_rect(surface, rect):
    pygame.draw.rect(surface, rect.getColor(), rect.getShape())


def main(window):
    gameHandler = Game.Game()
    gameHandler.start()
    clock = pygame.time.Clock()

    run = True
    currentTime = 0

    colors = [deepGreen, lightGreen]
    index = 0

    play_area_rect = Block.Block(0, 0, white, numOfGrids)
    temp_food = Block.Block(0, 0, red)

    draw_playArea(window)

    while run:
        # Handle time
        currentTime += clock.get_rawtime() / 1000   # Convert raw time from millisecond to second

        clock.tick()

        window.fill(colors[index])
        draw_rect(window, play_area_rect)

        if currentTime >= timePerFrame:
            index = (index + 1) % 2
            currentTime = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                gameHandler.keyHandler(event)

        gameHandler.move()


        pygame.display.update()

    pygame.quit()


def main_menu(window):
    run = True
    while run:
        draw_text_middle('Press any key to begin', 50, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(window)

    pygame.quit()


def getSize():
    return size


def getPlayAreaPos():
    return playAreaX, playAreaY


def getPlayAreaSize():
    return playAreaSize


def getNumOfGrids():
    return numOfGrids


if __name__ == '__main__':
    print(str(playAreaX) + " " + str(playAreaY))
    win = pygame.display.set_mode(size)
    pygame.display.set_caption('Tetris')

    main_menu(win)  # start game