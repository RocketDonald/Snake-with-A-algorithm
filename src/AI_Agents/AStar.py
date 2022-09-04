"""
This class is an AI agent using A* to find a solution path
Characteristics:
    -   Multi-threading to process different paths
    -   Communicate the result with GameUI
    -   Time the computational time
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
from Node import Node
from Direction import Direction


class AStar:
    def __init__(self):
        self.frontier = []  # This frontier will be a heap queue

    def find_path(self, beginning_pos, goal_pos, direction: Direction, snake_2d):
        # Create a node for beginning pos
        dis = self.__manhattan_distance(beginning_pos, goal_pos)
        beginning_node = Node(dis, [beginning_pos], direction)
        self.frontier.append(beginning_node)

        # Loop until the frontier is empty
        while not self.frontier:
            # Select a path
            path_node = heapq.heappop(self.frontier)
            path = path_node.path
            head_pos = path[len(path) - 1]

            # Check is the path valid (i.e., does not collide with anything)
            # Prune this path if invalid
            if self.__isCollide(head_pos, snake_2d, path):
                continue

            # Return the solution path if it meets the goal
            if self.__isGoal(head_pos, goal_pos):
                return path

            # Add neighbour nodes to the frontier
            # Add every direction except the opposite direction
            dir_list = self.__prune_opposite_direction(direction)

            for d in dir_list:
                # Generate a new path and create a node with the new path
                path_new = path.copy()
                head_new = self.__new_head(head_pos, d)
                path_new.append(head_new)
                node_new = Node(self.__f_value(head_new, len(path)), path_new, d)   # The cost = length of path

                # Add the new node to frontier
                heapq.heappush(self.frontier, node_new)

        return []

    def __isCollide(self, head_pos, snake_2d, path):
        return not self.__isCollide_old_body(head_pos, snake_2d) and not self.__isCollide_new_body(head_pos, path)

    def __isCollide_old_body(self, head_pos, snake_2d):
        return snake_2d[head_pos[0]][head_pos[1]]

    def __isCollide_new_body(self, head_pos, path):
        return head_pos in path

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

    def __prune_opposite_direction(self, direction):
        dir_list = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        if direction == Direction.UP:
            dir_list.pop(1)
        elif direction == Direction.DOWN:
            dir_list.pop(0)
        elif direction == Direction.RIGHT:
            dir_list.pop(3)
        else:
            dir_list.pop(2)

        return dir_list

    def __isGoal(self, head_pos, goal_pos):
        return head_pos == goal_pos

    def __manhattan_distance(self, node_pos, goal_pos):
        node_x, node_y = node_pos
        goal_x, goal_y = goal_pos

        return abs(goal_x - node_x) + abs(goal_y - node_y)


if __name__ == '__main__':
    a = AStar()
    a.create()
