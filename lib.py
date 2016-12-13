import pygame, itertools, time, sys, unittest


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Box(object):
    state = 0
    
    def __init__(self, x, y, size, board):
        """
        Box where the x's and o's are drawn

        :param x:
        :param y:
        :param size:
        :param board:
        """
        self.size = size
        self.line_width = int(self.size / 40) if self.size > 40 else 1
        self.radius = (self.size / 2) - (self.size / 8)
        self.rect = pygame.Rect(x, y, size, size)
        self.board = board
    
    def mark_x(self):
        pygame.draw.line(self.board.surface, GREEN, (self.rect.centerx - self.radius, self.rect.centery - self.radius), (self.rect.centerx + self.radius, self.rect.centery + self.radius), self.line_width)
        pygame.draw.line(self.board.surface, GREEN, (self.rect.centerx - self.radius, self.rect.centery + self.radius), (self.rect.centerx + self.radius, self.rect.centery - self.radius), self.line_width)
    
    def mark_o(self):
        pygame.draw.circle(self.board.surface, RED, (int(self.rect.centerx), int(self.rect.centery)), int(self.radius), int(self.line_width))


class Board(object):
    turn = 1
    
    def __init__(self, grid_size=3, box_size=200, border=20, line_width=5):
        self.grid_size = grid_size
        self.box_size = box_size
        self.border = border
        self.line_width = line_width
        surface_size = (self.grid_size * self.box_size) + (self.border * 2) + (self.line_width * (self.grid_size - 1))
        self.surface = pygame.display.set_mode((surface_size, surface_size), 0, 32)
        self.setup()

        
    def setup(self):
        """
        Initializes the board, including setting game_over variable to False
        :return:
        """
        pygame.display.set_caption('Tic Tac Toe - Player 1 Start')
        self.surface.fill(BLACK)
        self.draw_lines()
        self.initialize_boxes()
        self.calculate_winners()
        self.game_over = False

    def draw_lines(self):
        for i in range(1, self.grid_size):
            start_position = ((self.box_size * i) + (self.line_width * (i - 1))) + self.border
            width = self.surface.get_width() - (2 * self.border)
            pygame.draw.rect(self.surface, WHITE, (start_position, self.border, self.line_width, width))
            pygame.draw.rect(self.surface, WHITE, (self.border, start_position, width, self.line_width))
    
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
    
    def process_click(self, x, y):
        """
        Checks if box is empty, if not fills it with an x or an o, then checks if game is over. if game is over calls ending_menu method
        :param x: x position of cursor
        :param y: y position of cursor
        :return: nothing
        """
        box = self.get_box_at_pixel(x, y)
        if box is not None and not self.game_over:
            self.play_turn(box)
            self.check_game_over()
        if self.game_over:
            self.ending_menu(x, y)

    def display_end_menu(self):
        """
        Makes rectangles that act as ending menu buttons with options -Play again- or -Quit game-
        :return: nothing
        """
        surface_size = self.surface.get_height()
        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 16))

        text1 = font.render("Play again", True, YELLOW, BLUE)
        text2 = font.render("Quit game", True, YELLOW, BLUE)

        self.rect1 = text1.get_rect()
        self.rect2 = text2.get_rect()
        self.rect1.center = (surface_size / 3, surface_size / 12)
        self.rect2.center = ((surface_size * 2) / 3, surface_size / 12)
        self.surface.blit(text1, self.rect1)
        self.surface.blit(text2, self.rect2)

    def ending_menu(self, x, y):
        """
        Calls method if mouse cursor click falls within ending menu buttons, if -Play again- clicked, refreshes the game,
        if -Quit game- clicked, exits the program
        :param x: x position of cursor
        :param y: y position of cursor
        :return: nothing
        """
        if self.rect1.collidepoint(x, y):
            self.setup()
        elif self.rect2.collidepoint(x, y):
            pygame.quit()
            sys.exit()

    def play_sound(self):
        """
        Loads the mixer with a sound corresponding to the player whose turn it is, then plays sound
        :return:
        """
        if self.turn == 1:
            pygame.mixer.music.load('limit.wav')
        elif self.turn == 2:
            pygame.mixer.music.load('bolt2.wav')
        pygame.mixer.music.play()

    def play_turn(self, box):
        """
        Marks x or o if cursor clicks empty box, calls play_sound method with each drawn x or o
        changes caption to display whose turn it currently is
        :param box: box object
        :return:
        """
        if box.state != 0:
            return
        if self.turn == 1:
            box.mark_x()
            box.state = 1
            self.play_sound()
            self.turn = 2
        elif self.turn == 2:
            box.mark_o()
            box.state = 2
            self.play_sound()
            self.turn = 1
        pygame.display.set_caption('Tic Tac Toe - Player %d Turn' % self.turn)
        return
    
    def calculate_winners(self):
        self.winning_combinations = []
        indices = [x for x in range(0, self.grid_size * self.grid_size)]
        
        # Vertical combinations
        self.winning_combinations += ([tuple(indices[i:i+self.grid_size]) for i in range(0, len(indices), self.grid_size)])
        
        # Horizontal combinations
        self.winning_combinations += [tuple([indices[x] for x in range(y, len(indices), self.grid_size)]) for y in range(0, self.grid_size)]
        
        # Diagonal combinations
        self.winning_combinations.append(tuple(x for x in range(0, len(indices), self.grid_size + 1)))
        self.winning_combinations.append(tuple(x for x in range(self.grid_size - 1, len(indices), self.grid_size - 1)))
    
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
        return winner
    
    def check_game_over(self):
        winner = self.check_for_winner()
        if winner:
            self.game_over = True
        elif all(box.state in [1, 2] for box in self.boxes):
            self.game_over = True
        if self.game_over:
            self.display_game_over(winner)
    
    def display_game_over(self, winner):
        """
        Makes rectangle to display game over, plays victory or draw sound
        :param winner: Winner of game, type int = 1 or 2
        :return:
        """
        surface_size = self.surface.get_height()
        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 8))

        if winner:
            text = 'Player %s won!' % winner
            pygame.display.set_caption('Tic Tac Toe - Player %s Won' % winner)
            pygame.mixer.music.load('victory.wav')
        else:
            text = 'Draw!'
            pygame.display.set_caption('Tic Tac Toe - Draw Game')
            pygame.mixer.music.load('aww.wav')

        text = font.render(text, True, YELLOW, BLUE)
        rect = text.get_rect()
        rect.center = (surface_size / 2, surface_size / 2)

        pygame.mixer.music.play()

        self.surface.blit(text, rect)
        self.display_end_menu()

class TicTacTest(unittest.TestCase):
    def test_init(self):
        """
        Initializes board object with not default sizes, checks to see that the sizes are correct
        :return:
        """
        board = Board(5, 100, 10, 3)
        self.assertTrue(board.grid_size == 5)
        self.assertFalse(board.box_size == 200)
        self.assertTrue(board.border == 10)
        self.assertTrue(board.line_width == 3)

    def test_setup(self):
        """
        Initializes board object, checks to see if game_over initalized to 0
        :return:
        """
        board = Board()
        self.assertTrue(board.game_over == False)

    def test_initialize_boxes(self):
        """
        Initializes board object, checks to see if there are 9 box objects, iteratures through self.boxes to make sure
        all the items are box objects
        :return:
        """
        board = Board()
        self.assertTrue(len(board.boxes) == 9)
        for i in board.boxes:
            self.assertIsInstance(i, Box)

    def test_get_box_at_pixel(self):
        """
        Initializes a board object, checks to see if pos 0,0 is a not a box and 30, 30 is a box
        :return:
        """
        board = Board()
        self.assertNotIsInstance(board.get_box_at_pixel(0, 0), Box)
        self.assertIsInstance(board.get_box_at_pixel(30, 30), Box)

    def test_process_click(self):
        """
        Initializes board object, plays a turn, checks to see if it is player two's turn
        :return:
        """
        board = Board()
        pygame.init()
        board.process_click(30, 30)
        self.assertTrue(board.turn == 2)

    def test_play_sound(self):
        """
        Initializes a board object, calls the play sound method and checks if sound is playing, pauses for 3 seconds
        to check if the sound isn't playing
        :return:
        """
        board = Board()
        pygame.init()
        board.play_sound()
        self.assertTrue(pygame.mixer.music.get_busy() == True)
        time.sleep(3)
        self.assertFalse(pygame.mixer.music.get_busy())


if __name__ == "__main__":
    unittest.main()
    pygame.tests.run()
