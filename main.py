import pygame
import random
import time
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
WIDTH = HEIGHT = 600
RESOLUTION = (WIDTH, HEIGHT)
GRID_LINE_WIDTH = 2
INNER_CIRCLE = WIDTH / 8.5
OUTER_CIRCLE = WIDTH / 7.5
SLASH_LENGTH = int(WIDTH / 8.5)
SLASH_THICKNESS = int(WIDTH / 35.3)
FONT_SIZE = int(WIDTH / 17)
WIN_CONDITIONS = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
CORNER_NUMBERS = [1, 3, 7, 9]
EVEN_NUMBERS = [2, 4, 6, 8]
TILE_COORD = {
    1: (WIDTH / 6, WIDTH / 6),
    2: (WIDTH / 2, WIDTH / 6),
    3: (WIDTH / 6 * 5, WIDTH / 6),
    4: (WIDTH / 6, WIDTH / 2),
    5: (WIDTH / 2, WIDTH / 2),
    6: (WIDTH / 6 * 5, WIDTH / 2),
    7: (WIDTH / 6, WIDTH / 6 * 5),
    8: (WIDTH / 2, WIDTH / 6 * 5),
    9: (WIDTH / 6 * 5, WIDTH / 6 * 5)
}
# Line coordinates
X_1 = Y_1 = WIDTH / 3
X_2 = Y_2 = WIDTH / 3 * 2
X_3 = Y_3 = WIDTH


# Checks win condition
def check_win_condition(tiles):
    for con in WIN_CONDITIONS:
        if all(i in tiles for i in con):
            return True
    return False


# Main application
def main():
    def event_msg(string):
        pygame.draw.rect(screen, BLACK, (0, WIDTH / 2.5, WIDTH, WIDTH / 5))
        font_style = pygame.font.Font(None, FONT_SIZE)
        msg = font_style.render(string, True, WHITE)
        msg_rect = msg.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(msg, msg_rect)
        pygame.display.flip()
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        time.sleep(2.5)
        pygame.event.set_allowed(pygame.MOUSEMOTION)

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("The Unbeatable Tic-Tac-Toe")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Player tiles & Computer tiles

    # Event loop
    while 1:
        tiles_to_draw = [i for i in TILE_COORD.keys()]
        user_tiles = []
        comp_tiles = []
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT))

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            # Draw grid lines
            pygame.draw.line(screen, BLACK, (X_1, 0), (X_1, Y_3), GRID_LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (X_2, 0), (X_2, Y_3), GRID_LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (0, Y_1), (X_3, Y_1), GRID_LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (0, Y_2), (X_3, Y_2), GRID_LINE_WIDTH)
            pygame.display.flip()

            # User's Turn -
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Detects User Mouse click and gets the coordinates of the click
                clicked_pos = pygame.mouse.get_pos()
                # Finds the center point of the clicked tile
                tolerance = WIDTH / 6
                is_valid_pick = False
                for tile in tiles_to_draw:
                    ref_tile = TILE_COORD[tile]
                    if ref_tile[0] + tolerance > clicked_pos[0] > ref_tile[0] - tolerance and \
                            ref_tile[1] + tolerance > clicked_pos[1] > ref_tile[1] - tolerance:
                        # Drawing O mark on the tile
                        pygame.draw.circle(screen, BLACK, ref_tile, OUTER_CIRCLE)
                        pygame.draw.circle(screen, WHITE, ref_tile, INNER_CIRCLE)
                        pygame.display.flip()
                        # The tile is given to User, and is no longer selectable.
                        user_tiles.append(tile)
                        tiles_to_draw.remove(tile)
                        is_valid_pick = True

                # Check User's win condition
                if check_win_condition(user_tiles):
                    event_msg("You win!")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        break

                time.sleep(0.5)

                # Detects tie
                if not tiles_to_draw:
                    event_msg("It's a tie!")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        break

                # Computer's Turn -
                if is_valid_pick and tiles_to_draw:
                    computer_pick = None

                    # Blocks special tricks
                    if len([pick for pick in CORNER_NUMBERS if pick in user_tiles]) == 2:
                        computer_pick = 2
                    if (1 in user_tiles and 6 in user_tiles) or (2 in user_tiles and 9 in user_tiles):
                        computer_pick = 3
                    if (3 in user_tiles and 8 in user_tiles) or (6 in user_tiles and 7 in user_tiles):
                        computer_pick = 9
                    if (4 in user_tiles and 9 in user_tiles) or (8 in user_tiles and 1 in user_tiles):
                        computer_pick = 7
                    if (7 in user_tiles and 2 in user_tiles) or (4 in user_tiles and 3 in user_tiles) or (
                            5 in user_tiles):
                        computer_pick = 1

                    # Basic defense algorithm
                    for condition in WIN_CONDITIONS:
                        check = [pick for pick in condition if pick in user_tiles]
                        if len(check) == 2:
                            choice = [pick for pick in condition if pick not in check]
                            if choice:
                                if choice[0] in tiles_to_draw:
                                    computer_pick = choice[0]

                    # Basic offense algorithm:
                    for condition in WIN_CONDITIONS:
                        check = [pick for pick in condition if pick in comp_tiles]
                        if len(check) == 2:
                            choice = [pick for pick in condition if pick not in check]
                            if choice:
                                if choice[0] in tiles_to_draw:
                                    computer_pick = choice[0]

                    # Picks 5 if not taken
                    if 5 in tiles_to_draw:
                        computer_pick = 5

                    # The tile is given to Computer, and is no longer selectable.
                    try:
                        tiles_to_draw.remove(computer_pick)

                    except ValueError:
                        computer_pick = random.choice(tiles_to_draw)
                        tiles_to_draw.remove(computer_pick)

                    finally:
                        comp_tiles.append(computer_pick)

                    # Drawing X mark on the tile
                    chosen_tile = TILE_COORD[computer_pick]
                    pygame.draw.line(screen, BLACK,
                                     (chosen_tile[0] - SLASH_LENGTH, chosen_tile[1] - SLASH_LENGTH),
                                     (chosen_tile[0] + SLASH_LENGTH, chosen_tile[1] + SLASH_LENGTH),
                                     SLASH_THICKNESS)
                    pygame.draw.line(screen, BLACK,
                                     (chosen_tile[0] - SLASH_LENGTH, chosen_tile[1] + SLASH_LENGTH),
                                     (chosen_tile[0] + SLASH_LENGTH, chosen_tile[1] - SLASH_LENGTH),
                                     SLASH_THICKNESS)
                    pygame.display.flip()

                    # Check Computer's win condition
                    if check_win_condition(comp_tiles):
                        event_msg("You lost!")
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            break

                    time.sleep(0.25)


if __name__ == "__main__":
    main()
