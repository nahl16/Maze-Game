import pygame
import random
from collections import deque

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()

        self.player_pos = (0, 0)
        self.destination_pos = (COLS - 1, ROWS - 1)
        self.maze = self.generate_maze()

    def generate_maze(self):
        maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        stack = []

        # Initialize maze with walls (0: wall, 1: path)
        for row in range(ROWS):
            for col in range(COLS):
                if random.random() < 0.3:  # 30% chance to place a wall
                    maze[row][col] = 0
                else:
                    maze[row][col] = 1

        # Ensure there is a path from start to destination using BFS
        start = (0, 0)
        destination = (ROWS - 1, COLS - 1)
        queue = deque([start])
        visited = set([start])

        while queue:
            current = queue.popleft()
            x, y = current

            if current == destination:
                break

            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random.shuffle(neighbors)

            for nx, ny in neighbors:
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited and maze[ny][nx] == 1:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    stack.append((current, (nx, ny)))

        # Mark the path from start to destination in the maze
        while stack:
            current, next_cell = stack.pop()
            maze[next_cell[1]][next_cell[0]] = 1

        # Mark the destination within the maze
        maze[self.destination_pos[1]][self.destination_pos[0]] = 2

        maze[0][0] = 1  # Starting point
        return maze

    def draw_maze(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.maze[row][col] == 0:
                    color = BLACK
                elif self.maze[row][col] == 1:
                    color = WHITE
                elif self.maze[row][col] == 2:
                    color = BLUE  # Mark destination with blue color
                pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_player(self):
        pygame.draw.circle(self.screen, GREEN, (self.player_pos[0] * CELL_SIZE + CELL_SIZE // 2,
                                                 self.player_pos[1] * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 4)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        new_pos = self.player_pos  # Default to current player position if no movement keys are pressed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_pos = ((self.player_pos[0] - 1) % COLS, self.player_pos[1])
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_pos = ((self.player_pos[0] + 1) % COLS, self.player_pos[1])
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            new_pos = (self.player_pos[0], (self.player_pos[1] - 1) % ROWS)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_pos = (self.player_pos[0], (self.player_pos[1] + 1) % ROWS)

        # Check if the new position is a valid path cell (not a wall)
        if self.maze[new_pos[1]][new_pos[0]] != 0:
            self.player_pos = new_pos

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()

            self.screen.fill(WHITE)
            self.draw_maze()
            self.draw_player()

            # Check if player reached the destination
            if self.player_pos == self.destination_pos:
                font = pygame.font.Font(None, 36)
                text = font.render("You Reached the Destination!", True, RED)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)
                self.player_pos = (0, 0)  # Reset player position
                self.maze = self.generate_maze()  # Regenerate maze
                continue

            pygame.display.flip()
            self.clock.tick(10)  # Adjust game speed (frames per second)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.run_game()
