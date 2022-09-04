from Direction import Direction
from Snake import Snake


class Node(object):
    def __init__(self, f_value: int, path, direction: Direction):
        self.f_value = f_value
        self.path = path
        self.direction = direction
        self.x, self.y = path[len(path) - 1]    # Path will be a list, the end of the list will be the new head

    def __repr__(self):
        return f'Node with f value: {self.f_value}'

    """
        0.  Close to body   --> Prevent trapping itself
        1.  Up
        2.  Down
        3.  Left
        4   Right
    """
    def __lt__(self, other):
        # If both have the same f-value, then enter tie breaking logic
        if self.f_value == other.f_value:
            # Close to body
            snake_new = Snake.Snake()
            snake_list = snake_new.getBody()

            close_self = False
            close_other = False

            node_neighbour_self = [(self.x + 1, self.y), (self.x - 1, self.y), (self.x, self.y + 1), (self.x, self.y - 1)]
            node_neighbour_other = [(other.x + 1, other.y), (other.x - 1, other.y), (other.x, other.y + 1), (other.x, other.y - 1)]

            # Check if any part of the snake is a neighbour node
            for n in node_neighbour_self:
                for x, y in n:
                    if snake_list[x][y] == 1:
                        close_self = True
                        break

            for n in node_neighbour_other:
                for x, y in n:
                    if snake_list[x][y] == 1:
                        close_other = True
                        break

            # If either close_self or close_other is True, then the one with False is lesser than the other
            if close_self != close_other:
                return close_self
            # Else compare their direction
            else:
                return self.direction.value < other.direction.value

        else:
            return self.f_value < other.f_value

