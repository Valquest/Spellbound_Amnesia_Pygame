import pygame


class Button:

    def __init__(self, button_name, x_pos, y_pos, width, height, font_size):
        self.name = button_name
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.btn_font = pygame.font.Font(None, font_size)
        self.font_render = self.btn_font.render(self.name, True, (0, 0, 0))
        self.btn_position = self.font_render.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))

    # draw a button
    def draw(self, canvas):
        pygame.draw.rect(canvas, "white", self.rect)

    def colided(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
