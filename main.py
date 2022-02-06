import pygame
import random

pygame.init()

GLOBALS = {
    'BG_COLOR': (21, 21, 21),
    'SCREEN_SIZE': (800, 600),
    'TILE_CORRECT_LETTER': (170, 170, 50),
    'TILE_CORRECT_LETTER_COL': (50, 120, 50),
    'TILE_BORDER_HIGHLIGHT': (130, 130, 130),
    'TILE_BORDER_DEFAULT': (50, 50, 50),
    'FONT_COLOR': (220, 220, 220),
    'TILE_SIZE': (80, 80),
    'TILE_MARGIN': 4,
    'TILE_BORDER': 3,
}

win = pygame.display.set_mode(GLOBALS['SCREEN_SIZE'])
pygame.display.set_caption('BtrWorlde v. 1.0')
font = pygame.font.Font('resources/Lato-Black.ttf', 38)


class Tile:
    def __init__(self, x, y):
        self.letter = ''
        self.pos = x, y
        self.body = pygame.surface.Surface(GLOBALS['TILE_SIZE'])
        self.type_letter('')

    def _set_letter(self, char, fill_color, border_color=None):
        if border_color is None:
            border_color = fill_color

        # render background
        self.body.fill(border_color)
        pygame.draw.rect(self.body, fill_color, (
            GLOBALS['TILE_BORDER'],
            GLOBALS['TILE_BORDER'],
            GLOBALS['TILE_SIZE'][0] - GLOBALS['TILE_BORDER'] * 2,
            GLOBALS['TILE_SIZE'][1] - GLOBALS['TILE_BORDER'] * 2,
        ))

        # render text
        self.letter = char
        text = font.render(char.upper(), True, GLOBALS['FONT_COLOR'])
        text_x = GLOBALS['TILE_SIZE'][0] / 2 - text.get_width() // 2
        text_y = GLOBALS['TILE_SIZE'][1] / 2 - text.get_height() // 2
        self.body.blit(text, (text_x, text_y))

    def type_letter(self, letter):
        if letter:
            self._set_letter(letter, GLOBALS['BG_COLOR'], GLOBALS['TILE_BORDER_HIGHLIGHT'])
        else:
            self._set_letter('', GLOBALS['BG_COLOR'], GLOBALS['TILE_BORDER_DEFAULT'])

    def apply_letter(self, correct, correct_column=False):
        if correct:
            if correct_column:
                self._set_letter(self.letter, GLOBALS['TILE_CORRECT_LETTER_COL'])
            else:
                self._set_letter(self.letter, GLOBALS['TILE_CORRECT_LETTER'])
        else:
            self._set_letter(self.letter, GLOBALS['TILE_BORDER_DEFAULT'])

    def draw(self, surface):
        surface.blit(self.body, self.pos)


class Game:
    def __init__(self):
        self.written_words = []
        self.tiles = []
        self.body = pygame.surface.Surface((
            GLOBALS['TILE_SIZE'][0] * 5 + GLOBALS['TILE_MARGIN'] * 6,
            GLOBALS['TILE_SIZE'][1] * 6 + GLOBALS['TILE_MARGIN'] * 7,
        ))
        self.body.fill(GLOBALS['BG_COLOR'])
        self.pos = (
            GLOBALS['SCREEN_SIZE'][0] // 2 - self.body.get_width() // 2,
            GLOBALS['SCREEN_SIZE'][1] // 2 - self.body.get_height() // 2,
        )
        self.word = ''
        self.allowed_guesses = []
        self.allowed_answers = []
        with open('allowed_guesses.txt', 'r') as f:
            for line in f.readlines():
                self.allowed_guesses.append(line.rstrip())
        with open('allowed_answers.txt', 'r') as f:
            for line in f.readlines():
                self.allowed_answers.append(line.rstrip())
        self.guessed = False
        self.cursor_col = 0
        self.cursor_row = 0
        self.reset()

    def reset(self):
        print(self.word)
        self.word = random.choice(self.allowed_answers)
        self.guessed = False
        self.cursor_col = 0
        self.cursor_row = 0
        self.tiles.clear()
        for i in range(6):
            row = []
            for j in range(5):
                row.append(
                    Tile(
                        j * (GLOBALS['TILE_SIZE'][0] + GLOBALS['TILE_MARGIN']) + GLOBALS['TILE_MARGIN'],
                        i * (GLOBALS['TILE_SIZE'][1] + GLOBALS['TILE_MARGIN']) + GLOBALS['TILE_MARGIN']
                    )
                )
            self.tiles.append(row)

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.body)
        surface.blit(self.body, self.pos)

    def handle_click(self, key: str):
        if key == 'reset':
            self.reset()

        elif key == 'backspace':
            if self.cursor_col >= 0:
                self.tiles[self.cursor_row][self.cursor_col - 1].type_letter('')
                self.cursor_col = max(0, self.cursor_col - 1)

        elif key == 'enter':
            word = ''.join([tile.letter for tile in self.tiles[self.cursor_row]])
            if word not in self.allowed_guesses:
                return
            if self.cursor_col == 5:
                for i in range(5):
                    tile = self.tiles[self.cursor_row][i]
                    if self.word[i] == tile.letter:
                        tile.apply_letter(True, True)
                    elif tile.letter in self.word:
                        tile.apply_letter(True)
                    else:
                        tile.apply_letter(False)
                if word == self.word:
                    self.guessed = True
                self.cursor_row = min(5, self.cursor_row + 1)
                if self.cursor_row == 5:
                    self.guessed = True
                self.cursor_col = 0

        elif ord('a') <= ord(key) <= ord('z'):
            if self.cursor_col <= 4:
                self.tiles[self.cursor_row][self.cursor_col].type_letter(key)
                self.cursor_col = min(5, self.cursor_col + 1)


def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    game1 = Game()

    while run:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

            if e.type == pygame.KEYDOWN:
                if ord('a') <= e.key <= ord('z'):
                    game1.handle_click(chr(e.key))
                elif e.key == pygame.K_BACKSPACE:
                    game1.handle_click('backspace')
                elif e.key == pygame.K_RETURN:
                    game1.handle_click('enter')
                elif e.key == pygame.K_ESCAPE:
                    game1.handle_click('reset')

        win.fill(GLOBALS['BG_COLOR'])
        game1.draw(win)
        pygame.display.update()


if __name__ == '__main__':
    main()
