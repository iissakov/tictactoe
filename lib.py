import pygame, itertools


FPS = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Box(object):
    state = 0
    
    def __init__(self, x, y, size, board):
        self.size = size
        self.line_width = int(self.size / 40) if self.size > 40 else 1
        self.radius = (self.size / 2) - (self.size / 8)
        self.rect = pygame.Rect(x, y, size, size)
        self.board = board
    
    def mark_x(self):
        pygame.draw.line(self.board.surface, RED, (self.rect.centerx - self.radius, self.rect.centery - self.radius), (self.rect.centerx + self.radius, self.rect.centery + self.radius), self.line_width)
        pygame.draw.line(self.board.surface, RED, (self.rect.centerx - self.radius, self.rect.centery + self.radius), (self.rect.centerx + self.radius, self.rect.centery - self.radius), self.line_width)
    
    def mark_o(self):
        pygame.draw.circle(self.board.surface, BLUE, (self.rect.centerx, self.rect.centery), self.radius, self.line_width)


class Board(object):
    turn = 1
    
    def __init__(self, grid_size=3, box_size=200, border=20, line_width=5):
        self.grid_size = grid_size
        self.box_size = box_size
        self.border = border
        self.line_width = line_width
        surface_size = (self.grid_size * self.box_size) + (self.border * 2) + (self.line_width * (self.grid_size - 1))
        self.surface = pygame.display.set_mode((surface_size, surface_size), 0, 32)
        self.game_over = False
        self.setup()
        
    def setup(self):
        pygame.display.set_caption('Tic Tac Toe')
        self.surface.fill(WHITE)
        self.draw_lines()
        self.initialize_boxes()
        self.calculate_winners()
    
    def draw_lines(self):
        for i in xrange(1, self.grid_size):
            start_position = ((self.box_size * i) + (self.line_width * (i - 1))) + self.border
            width = self.surface.get_width() - (2 * self.border)
            pygame.draw.rect(self.surface, BLACK, (start_position, self.border, self.line_width, width))
            pygame.draw.rect(self.surface, BLACK, (self.border, start_position, width, self.line_width))
    
    def initialize_boxes(self):
        self.boxes = []
        
        top_left_numbers = []
        for i in range(0, self.grid_size):
            num = ((i * self.box_size) + self.border + (i *self.line_width))
            top_left_numbers.append(num)
        
        box_coordinates = list(itertools.product(top_left_numbers, repeat=2))
        for x, y in box_coordinates:
            self.boxes.append(Box(x, y, self.box_size, self))
    
    def get_box_at_pixel(self, x, y):
        for index, box in enumerate(self.boxes):
            if box.rect.collidepoint(x, y):
                return box
        return None
    
    def play_turn(self, box):
        if box.state != 0:
            return
        if self.turn == 1:
            box.mark_x()
            box.state = 1
            self.turn = 2
        elif self.turn == 2:
            box.mark_o()
            box.state = 2
            self.turn = 1
        return
    
    def calculate_winners(self):
        self.winning_combinations = []
        box_combinations = list(itertools.combinations([i for i in xrange(0, len(self.boxes))], self.grid_size))
        for combination in box_combinations:            
            diffs = []
            for i in xrange(0, self.grid_size - 1):
                diff = combination[i + 1] - combination[i]
                diffs.append(diff)
            if all(i == diff for i in diffs):
                # Vertical rows
                if diff == 1 and combination[0] % self.grid_size == 0:
                    self.winning_combinations.append(combination)
                # Horizontal rows
                if diff == self.grid_size:
                    self.winning_combinations.append(combination)
                # Diagonal rows
                if diff == self.grid_size + 1 and combination[0] == 0:
                    self.winning_combinations.append(combination)
                if diff == self.grid_size - 1 and combination[0] == self.grid_size - 1:
                    self.winning_combinations.append(combination)
    
    def check_for_winner(self):
        winner = 0
        for combination in self.winning_combinations:
            states = []
            for index in combination:
                states.append(self.boxes[index].state)
            if all(x == 1 for x in states):
                winner = 1
            if all(x == 2 for x in states):
                winner = 2
        if winner:
            self.game_over = True
            self.display_winner(winner)
    
    def display_winner(self, winner):
        surface_size = self.surface.get_height()
        winner_text = 'Player %s won!' % winner
        font = pygame.font.Font('freesansbold.ttf', surface_size / 8)
        text = font.render(winner_text, True, BLACK)
        rect = text.get_rect()
        rect.center = (surface_size / 2, surface_size / 2)
        self.surface.blit(text, rect)