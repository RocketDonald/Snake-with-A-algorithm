import Snake
import pygame
import random
from Direction import Direction


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
    max_score = 0
    scoreIncrement = 100
    scoreDecrement = 1
    food = None
    end_game = False

    def __init__(self, size):
        self.size = size
        self.snake = Snake.Snake(self.size)

    def start(self):
        self.__generateFood()

    # Reset all the variables and restart the game
    def restart(self):
        self.snake.reset()
        self.foodPos = None
        self.food = None
        self.score = 0
        self.end_game = False
        self.start()

    # This function runs the logics
    # This function takes a queue of event as input
    # Return specific int values to represent different scenarios:
    #       0 = Normal
    #       1 = Quit
    #       2 = Dead
    #       3 = Win
    def keyHandler(self, event):
        if not self.__isFoodExist():
            self.__generateFood()

        # Change Direction
        self.__changeDir(event)

    def __changeDir(self, keyQueue):
        direction = None
        key = keyQueue.get()
        cont = True

        while cont:
            if key == pygame.K_w:
                direction = Direction.UP
                cont = False
            elif key == pygame.K_s:
                direction = Direction.DOWN
                cont = False
            elif key == pygame.K_a:
                direction = Direction.LEFT
                cont = False
            elif key == pygame.K_d:
                direction = Direction.RIGHT
                cont = False

        self.snake.changeDirection(direction)

    def move(self):
        foodAte = self.snake.move(self.getFoodPos())

        # Check if the snake collide with its body or the wall after moving
        head = self.getSnakeHead()
        if self.isCollide(head, False):
            self.end_game = True

        if foodAte:
            self.__generateFood()
            self.score += self.scoreIncrement
            if self.score > self.max_score:
                self.max_score = self.score
        else:
            if self.score > 0:
                self.score -= self.scoreDecrement

    def isEndGame(self):
        return self.end_game

    def __generateFood(self):
        Collide = True
        rdm = (None, None)
        while Collide:
            rdm = random.randrange(0, self.size), random.randrange(0, self.size)
            Collide = self.isCollide(rdm, True)

        self.foodPos = rdm

    # This function checks if a position is collide with the snake
    def isCollide(self, pos, checkHead):
        if checkHead:
            if pos == self.getSnakeHead():
                return True

        if self.getSnakeBody().__contains__(pos):
            return True

        return self.__isOutOfBound(pos)

    def __isOutOfBound(self, pos):
        x = pos[0]
        y = pos[1]

        if x < 0 or x >= self.size:
            return True
        if y < 0 or y >= self.size:
            return True
        return False

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

    def getScore(self):
        return self.score

    def getMaxScore(self):
        return self.max_score

