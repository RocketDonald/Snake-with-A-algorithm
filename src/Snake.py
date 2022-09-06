from Direction import Direction


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
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

    snake = []      # This will be a cyclic list, so that obtaining body, adding head and removing tail will be O(1)
    snake_2d = [[]]
    head = ()
    headIdx = 0
    tailIdx = 0
    length = 0
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
        self.snake_2d = [[]]
        self.headIdx = 0
        self.tailIdx = 0
        self.length = 1
        middle = self.boardSize / 2
        self.head = (middle, middle)
        self.snake.append(self.head)  # Set the snake starts in the middle
        self.direction = Direction.LEFT

        # Instantiate a list with the size of snakeMaxSize
        for i in range(1, self.snakeMaxSize):
            self.snake.append((None, None))

        # Instantiate a 2d list with the size of snakeMaxSize * snakeMaxSize
        self.snake_2d = [[0] * self.snakeMaxSize for i in range(self.snakeMaxSize)]

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

        print(f"Moved from {currentPos[0]}, {currentPos[1]} to {x}, {y}")
        return ate

    # This function updates the head position and add head into the list
    def __addHead(self, x, y):
        # Handle cyclic list
        h = (x, y)
        self.head = h
        self.headIdx = (self.headIdx + 1) % self.snakeMaxSize
        self.snake[self.headIdx] = h

        # Handle 2d list
        self.snake_2d[int(x)][int(y)] = 1

        # Increase the length
        self.length += 1

    # This function removes the tail and replace it as (None, None) tuple
    # Then plus one to the tail index
    def __removeTail(self):
        x, y = self.snake[self.tailIdx]
        # Handle cyclic list
        self.snake[self.tailIdx] = (None, None)
        self.tailIdx = (self.tailIdx + 1) % self.snakeMaxSize

        # Handle 2d list
        self.snake_2d[int(x)][int(y)] = 0

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
            res = self.snake[ending:]
            res.extend(self.snake[:beginning])
            return res
        # Case 2: beginning > ending
        elif beginning > ending:
            return self.snake[ending : beginning]
        # Case 3: beginning == ending
        else:
            return []

    def getWholeSnake(self):
        result = []
        result.extend(self.getBody())
        result.append(self.getHead())
        return result

    def getWholeSnake_2d(self):
        return self.snake_2d

    def get_snake_length(self):
        return self.length

    def getDirection(self):
        return self.direction

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

    def __iter__(self):
        return self.getWholeSnake()
