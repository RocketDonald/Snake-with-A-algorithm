"""
This class is an AI agent using A* to find a solution path
Characteristics:
    -   Multi-threading to process different paths
    -   Communicate the result with GameUI
    -   Time the computational time
    -   Check will the snake collide right after reaching the goal
    -   Make emergency decision (Low priority)  --> Avoid colliding while computing

Representation of Node:
    -   Tuple:  (pos, direction)    --> Direction is used for outputting final result

Heuristic (Need to determine the weighting):
    -   Manhattan distance from p to goal (i.e., food)
    -   How many block is sticking to its body  (low-priority)

Cost:
    -   Distance moved from beginning to p

Heap Queue (Priority Queue):
    -   Lower f(p) first
    -   f(p) = Heuristic(p) + Cost(p)
    -   If tie:
        0.  Close to body   --> Prevent trapping itself
        1.  Up
        2.  Down
        3.  Left
        4   Right

Methods:
    Public:
        -   create()
        -   find_path(beginning_pos, goal_pos, snake)
        -   end_game() --> Stops all threads and reset

    Private:
        -   manhattan_distance(node_pos, goal_pos)
        -   isGoal(pos)
        -   isCollide(pos) --> Prune
        -   isCollide_old_body(pos)
        -   isCollide_new_body(pos)
        -   isClose_to_body(pos)
        -   prune_direction(direction)
        -   addFrontier(frontier, direction)    --> add valid paths into the frontier
"""
import heapq
import queue
import threading

import GameUI
from AI_Agents.Node import Node
from Direction import Direction


class AStar:
    def __init__(self):
        self.frontier = []  # This frontier will be a heap queue
        self.result = queue.Queue()
        self.borderSize = GameUI.getNumOfGrids()

    # This function find the path and returns it
    # Return a list of directions
    # Return an empty list if no solution found
    def find_path(self, beginning_pos, goal_pos, direction: Direction, snake_whole_body, snake_length):
        print(f'Finding a path from {beginning_pos[0]} , {beginning_pos[1]} to {goal_pos[0]}, {goal_pos[1]}')
        # Reset
        self.frontier = queue.PriorityQueue()

        # Create a node for beginning pos
        # This the direction of the first movement cannot be changed
        dis = self.__manhattan_distance(beginning_pos, goal_pos)
        beginning_node = Node(dis, [beginning_pos], [direction])
        self.frontier.put(beginning_node)

        # Loop until the frontier is empty
        while not self.frontier.empty():
            thread1 = threading.Thread(target=self.a_star_logic, args= (snake_whole_body, snake_length, goal_pos, direction))
            thread2 = threading.Thread(target=self.a_star_logic, args= (snake_whole_body, snake_length, goal_pos, direction))
            thread3 = threading.Thread(target=self.a_star_logic, args= (snake_whole_body, snake_length, goal_pos, direction))
            thread4 = threading.Thread(target=self.a_star_logic, args= (snake_whole_body, snake_length, goal_pos, direction))

            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()

            if not self.result.empty():
                return self.result.get()

        print("No solution found")
        return []

    def a_star_logic(self, snake_whole_body, snake_length, goal_pos, direction):
        # Select a path
        path_node = self.frontier.get()

        if not path_node or path_node is None:
            return

        path = path_node.path
        head_pos = path[len(path) - 1]
        # print(f"Path with f-value {path_node.f_value} has been selected")

        # Prune if the path length is too long (i.e., over the size of the board)
        if self.__path_too_long(path):
            # print("Pruned because of too long")
            return

        # Check is the path valid (i.e., does not collide with anything)
        # Prune this path if invalid
        if self.__isCollide(head_pos, snake_whole_body, path, snake_length):
            return

        # Return the solution path if it meets the goal
        if self.__isGoal(head_pos, goal_pos):
            return self.result.put(path_node.directions[1:])

        # Add neighbour nodes to the frontier
        # Add every direction except the opposite direction
        dir_list = self.__prune_direction(direction, head_pos)

        for d in dir_list:
            # Generate a new path and create a node with the new path
            path_new = path.copy()
            head_new = self.__new_head(head_pos, d)
            path_new.append(head_new)

            directions_new = path_node.directions.copy()
            directions_new.append(d)
            # The cost = length of path
            node_new = Node(self.__f_value(head_new, goal_pos, len(path_new)), path_new, directions_new)

            # Add the new node to frontier
            self.frontier.put(node_new)

        return


    def __path_too_long(self, path):
        path_limit = self.borderSize * self.borderSize
        if len(path) > path_limit:
            return True
        return False

    def __isCollide(self, head_pos, snake_whole_body, path, length):
        return self.__isCollide_wall(head_pos) or self.__isCollide_new_body(head_pos, path, length) or \
               self.__isCollide_old_body(head_pos, snake_whole_body, length)

    def __isCollide_old_body(self, head_pos, snake_whole_body, length):
        snake_whole_body_in_length = snake_whole_body[-length:]
        if head_pos in snake_whole_body_in_length:
            print("Pruned because of colliding old body")
            return True
        return False

    def __isCollide_new_body(self, head_pos, path, length):
        path_in_length = path[-length + 1:0]
        if head_pos in path_in_length:
            print("Pruned because of colliding new body")
            return True
        return False

    def __isCollide_wall(self, head_pos):
        x, y = head_pos
        if x < 0 or x >= self.borderSize or y < 0 or y >= self.borderSize:
            print("Pruned because of colliding wall")
            return True
        return False

    def __f_value(self, head_pos, goal_pos, cost):
        return self.__manhattan_distance(head_pos, goal_pos) + cost

    def __new_head(self, pos, direction):
        x, y = pos
        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.RIGHT:
            x += 1
        else:
            x -= 1

        return x, y

    def __prune_direction(self, direction, head_pos):
        dir_list = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        x, y = head_pos
        limit = self.borderSize - 1

        if direction == Direction.UP or y >= limit:
            dir_list.remove(Direction.DOWN)
        if direction == Direction.DOWN or y <= 0:
            dir_list.remove(Direction.UP)
        if direction == Direction.RIGHT or x >= limit:
            dir_list.remove(Direction.LEFT)
        if direction == Direction.LEFT or x <= 0:
            dir_list.remove(Direction.RIGHT)

        return dir_list

    def __isGoal(self, head_pos, goal_pos):
        return head_pos == goal_pos

    def m(self, a, b):
        return self.__manhattan_distance(a, b)

    def __manhattan_distance(self, node_pos, goal_pos):
        node_x, node_y = node_pos
        goal_x, goal_y = goal_pos

        return abs(goal_x - node_x) + abs(goal_y - node_y)


