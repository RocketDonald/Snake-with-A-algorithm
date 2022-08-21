import sys
import pygame
import Game



def main():
    pygame.init()

    size = width, height = 600, 600

    display = pygame.display
    screen_surface = display.set_mode(size)
    display.set_caption("Snake Game")

    gameSize = 540, 540
    numOfGrids = 30
    game = Game.Game(numOfGrids)

    running = True

    while running:
        events = pygame.event.get()

        value = game.run(events)
        running = __handleValue(value)

        food = game.getFoodPos()
        head = game.getSnakeHead()
        body = game.getSnakeBody()

        drawBoard(screen_surface, food, head, body, size, gameSize, numOfGrids)

        display.flip()

    pygame.quit()


def __handleValue(value):
    if value is 1:
        return False
    if value is 2:
        __restart()
        return False
    if value is 3:
        __win()
        return False
    return True


def __restart():
    print("Restart")


def __win():
    print("You win")
    __restart()
    

def drawBoard(surface, food, head, body, windowSize, gameSize, numOfGrids):
    black = 0, 0, 0
    white = 255, 255, 255
    red = 200, 30, 30


    # Fill background
    surface.fill(white)

    # Draw boarder
    boarderPosX = (windowSize - gameSize) / 2
    boarderPosY = (windowSize - gameSize) * 0.7
    boarderPos = (boarderPosX, boarderPosY)

    gridSize = gameSize / numOfGrids

    pygame.draw.rect(surface, black, (boarderPos, (gameSize, gameSize)), 3)

    # Draw food
    foodX = food[0]
    foodY = food[1]
    foodPos = calculatePos(foodX, foodY)
    foodSize = 30

    pygame.draw.rect(surface, red, (foodPos, (foodSize, foodSize)), 5)

    # Draw Snake
    # Head
    pygame.draw.rect(surface, red, (food, (foodSize, foodSize)), foodSize)



def calculatePos(x, y, gameZone, gridSize):
    posX = (x * gridSize) + gameZone[0]
    posY = (y * gridSize) + gameZone[1]

    return posX, posY


if __name__ == "__main__":
    main()
