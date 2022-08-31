from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Snake:
    # Stores position of head and body
    # Snake can move within 30*30 grid
    # Positional Data will be stored in a list
    # The list will be a cyclist list, a head pointer will be used to indicate the head position
    # Provide methods to:
    #       change direction
    #       move forward
    #       get head
    #       get bodies
    #       get live/dead (call after each move)
    #       eat food (+1 length)
    #       get win (tailIdx == headIdx + 1)

    snake = []
    head = ()
    headIdx = 0
    tailIdx = 0
    snakeMaxSize = 30 * 30
    boardSize = 30
    direction = Direction.LEFT

    # Constructor
    def __init__(self, boardSize):
        self.boardSize = boardSize

        self.snakeMaxSize = boardSize * boardSize

        self.reset()

    def reset(self):
        self.snake = []
        self.headIdx = 0
        self.tailIdx = 0
        middle = self.boardSize / 2
        head = (middle, middle)
        self.snake.append(head)  # Set the snake starts in the middle
        self.direction = Direction.LEFT

        # Instantiate a list with the size of snakeMaxSize
        for i in range(1, self.snakeMaxSize):
            self.snake.append((None, None))

    # Plus 1 to the direction
    # A default moving action will add a new head and remove the tail, such that the length of the snake remains
    # If the snake eats a food, the head grow but tail remains, such that the length +1
    # Will check isAlive() at the end and returns the value
    def move(self, foodPos):
        currentPos = self.snake[self.headIdx]
        # print("Moving from " + str(currentPos[0]) + ", " + str(currentPos[1]))  # TODO - remove this
        x = currentPos[0]
        y = currentPos[1]
        foodX = foodPos[0]
        foodY = foodPos[1]

        if self.direction is Direction.UP:
            y -= 1
        elif self.direction is Direction.DOWN:
            y += 1
        elif self.direction is Direction.LEFT:
            x -= 1
        else:
            x += 1

        ate = True

        # Add head and remove tail if food is not eaten
        self.__addHead(x, y)
        if x != foodX or y != foodY:
            self.__removeTail()
            ate = False

        # print("Head: " + str(self.headIdx) + " | Tail: " + str(self.tailIdx))   # TODO - remove this

        return ate

    # This function updates the head position and add head into the list
    def __addHead(self, x, y):
        h = (x, y)
        self.head = h
        self.headIdx = (self.headIdx + 1) % self.snakeMaxSize
        self.snake[self.headIdx] = h

    # This function removes the tail and replace it as (None, None) tuple
    # Then plus one to the tail index
    def __removeTail(self):
        self.snake[self.tailIdx] = (None, None)
        self.tailIdx = (self.tailIdx + 1) % self.snakeMaxSize

    # This method changes the direction of the snake as long as the change is valid
    # Snake cannot change direction 180 Degree
    def changeDirection(self, newDirection):
        oldDirection = self.direction

        if oldDirection is Direction.UP and newDirection is Direction.DOWN:
            return
        elif oldDirection is Direction.RIGHT and newDirection is Direction.LEFT:
            return
        elif oldDirection is Direction.DOWN and newDirection is Direction.UP:
            return
        elif oldDirection is Direction.LEFT and newDirection is Direction.RIGHT:
            return
        else:
            self.direction = newDirection

    # This function returns true iff tailIdx == headIdx + 1 (i.e., filled the whole array)
    def isWin(self):
        i = (self.headIdx + 1) % self.snakeMaxSize
        return self.tailIdx == i

    def getHead(self):
        return self.head

    # This function returns the body (exclude the head)
    def getBody(self):
        beginning = self.headIdx
        ending = self.tailIdx

        # Case 1: beginning < ending
        if beginning < ending:
            res = self.snake[beginning + 1:]
            res.append(self.snake[:ending - 1])
            return res
        # Case 2: beginning > ending
        elif beginning > ending:
            return self.snake[ending : beginning]
        # Case 3: beginning == ending
        else:
            return []

    def __cyclicIdx(self, i):
        return (i+1) % self.snakeMaxSize

    def __repr__(self):
        return "Snake()"

    def __str__(self):
        head = self.snake[self.headIdx]
        tail = self.snake[self.tailIdx]
        result = "Snake Length: " + str(len(self.snake)) + " | Head Pos: [" + str(head[0]) + ", " + str(head[1]) + \
                 "] | Tail Pos: [" + str(tail[0]) + ", " + str(tail[1]) + "]"
        return result
