import pygame
import GameUI


class Block:
    default_size = width, height = GameUI.getSize()
    play_area_pos = play_area_x, play_area_y = GameUI.getPlayAreaPos()
    play_area_size = play_area_width, play_area_height = GameUI.getPlayAreaSize()
    num_of_grids = GameUI.getNumOfGrids()
    grid_size = grid_width, grid_height = play_area_width / num_of_grids, play_area_height / num_of_grids
    rect = None

    def __init__(self, x, y, color, size_ratio = 1):
        self.x = x
        self.y = y
        self.color = color
        self.size_ratio = size_ratio

    def __create_rect(self):
        pos = self.__calculate_pos()
        self.rect = pygame.Rect(pos, (self.grid_width * self.size_ratio, self.grid_height * self.size_ratio))

    def updatePos(self, x, y):
        self.__checkExistence()

        self.x += x
        self.y += y
        pos = self.x, self.y
        self.rect.update(pos, self.width * self.size_ratio, self.height * self.size_ratio)

    def getShape(self):
        self.__checkExistence()

        return self.rect

    def getColor(self):
        self.__checkExistence()

        return self.color

    def __checkExistence(self):
        if self.rect is None:
            self.__create_rect()

    def __calculate_pos(self):
        grid_size = self.play_area_width / self.num_of_grids
        x_pos = self.play_area_x + self.x * grid_size
        y_pos = self.play_area_y + self.y * grid_size
        return x_pos, y_pos

