import os
import queue
import time

import pygame
import Block
import Game

pygame.font.init()

size = width, height = 780, 780
playAreaSize = playAreaWidth, playAreaHeight = 660, 660
playAreaX = (width - playAreaWidth) / 2
playAreaY = (height - playAreaHeight) / 2 + 40
numOfGrids = 30
fps = 4
timePerFrame = 1 / fps
foodSizeRatio = 0.8

white = 255, 255, 255
black = 0, 0, 0
space_grey = 50, 50, 50
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


# draws text in the middle
def draw_scoreboard(score, max_score, text_size, color, surface):
    font = pygame.font.Font(fontPath, text_size, bold=False, italic=True)
    label = font.render(max_score, 1, color)
    label_2 = font.render(score, 1, color)

    surface.blit(label, (width/2 - (label.get_width()/2), label.get_height()/2))
    surface.blit(label_2, (width/2 - (label_2.get_width()/2), label_2.get_height()/2 + label.get_height()))


def draw_playArea(surface):
    playArea = pygame.Rect((playAreaX, playAreaY), (playAreaWidth, playAreaHeight))
    pygame.draw.rect(surface, black, playArea)


def draw_rect(surface, rect):
    pygame.draw.rect(surface, rect.getColor(), rect.getShape())


def draw_snake_head(surface, snake_pos):
    rect = Block.Block(snake_pos[0], snake_pos[1], deepGreen)
    draw_rect(surface, rect)


def draw_snake_body(surface, snake_pos):
    rect = Block.Block(snake_pos[0], snake_pos[1], lightGreen)
    draw_rect(surface, rect)


def draw_food(surface, food_pos):
    rect = Block.Block(food_pos[0], food_pos[1], red)
    draw_rect(surface, rect)


def main(window):
    gameHandler = Game.Game(numOfGrids)
    gameHandler.start()

    clock = pygame.time.Clock()

    run = True
    currentTime = 0

    play_area_rect = Block.Block(0, 0, white, numOfGrids)

    draw_playArea(window)

    keyPressQueue = queue.Queue()

    end_game = False

    end_game_wait_time = 10
    wait_time = 0

    while run:
        # Handle time
        currentTime += clock.get_rawtime() / 1000   # Convert raw time from millisecond to second

        clock.tick()

        # Draw Background
        window.fill(space_grey)
        draw_rect(window, play_area_rect)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                keyPressQueue.put_nowait(event.key)

        # Logic that perform every timePerFrame seconds
        if currentTime >= timePerFrame:
            # Reset the time countdown
            currentTime = 0

            # Pass the event to gameHandler if there is any
            if not keyPressQueue.empty():
                gameHandler.keyHandler(keyPressQueue)

            # Move when the game is still continue
            if end_game is False:
                gameHandler.move()

            end_game = gameHandler.isEndGame()

            # Check if the game ends
            if end_game:
                # Ends the game and restarts
                gg_msg = "GG! Score " + str(gameHandler.getScore())
                print(gg_msg)
                draw_text_middle(gg_msg, 50, black, window)
                pygame.display.update()
                # Show the GG message for wait_time, then restart the game
                wait_time += 1
                if wait_time >= end_game_wait_time:
                    wait_time = 0
                    gameHandler.restart()
            else:
                # Draw the new graph
                # Draw snake
                headPos = gameHandler.getSnakeHead()    # Head
                draw_snake_head(window, headPos)

                bodyPosList = gameHandler.getSnakeBody()    # Body
                for body in bodyPosList:
                    draw_snake_body(window, body)

                # Draw Food
                foodPos = gameHandler.getFoodPos()
                draw_food(window, foodPos)

                # Draw Scoreboard
                score = gameHandler.getScore()
                score_text = "Score " + str(score)
                score_max = gameHandler.getMaxScore()
                score_max_text = "Highest Score " + str(score_max)
                draw_scoreboard(score_text, score_max_text, 30, white, window)

                # Update
                pygame.display.update()

    pygame.quit()


def main_menu(window):
    run = True
    while run:
        draw_text_middle('Press any key to begin', 50, white, window)
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
    win = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake')

    main_menu(win)  # start game
