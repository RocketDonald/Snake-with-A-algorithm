import Snake
import pygame
import random
import Block


class Game:
    """
    This class handles all the game logics
    This class will be called in UI class
    This class provides methods to:
        generate food
        handle user input
        calculate score
        end game if needed

    """
    size = 30
    snake = None
    foodPos = None
    score = 0
    scoreIncrement = 100
    scoreDecrement = 1

    def __init__(self, size):
        self.size = size
        self.snake = Snake.Snake(self.size)

    def start(self):
        self.__generateFood()

    # This function runs the logics
    # This function takes a queue of event as input
    # Return specific int values to represent different scenarios:
    #       0 = Normal
    #       1 = Quit
    #       2 = Dead
    #       3 = Win
    def keyHandler(self, event):
        # Generate food if food not exist
        pass

    def __changeDir(self, key):
        direction = None
        if key == pygame.K_w:
            direction = Snake.Direction.UP
        elif key == pygame.K_s:
            direction = Snake.Direction.DOWN
        elif key == pygame.K_a:
            direction = Snake.Direction.LEFT
        elif key == pygame.K_d:
            direction = Snake.Direction.RIGHT

        self.snake.changeDirection(direction)

    def move(self):
        self.snake.move(self.getFoodPos())

    def __generateFood(self):
        self.foodPos = (random.randrange(0, self.size), random.randrange(0, self.size))

    def __isFoodExist(self):
        return self.foodPos is not None

    def __increaseScore(self):
        self.score += self.scoreIncrement

    def __decreaseScore(self):
        self.score -= self.scoreDecrement

    def getFoodPos(self):
        return self.foodPos

    def getSnakeHead(self):
        return self.snake.getHead()

    def getSnakeBody(self):
        return self.snake.getBody()

