import pygame
import random
import heapq
from dataclasses import dataclass

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


@dataclass
class Position:
    """Represents a position in the maze."""

    x: int
    y: int


class Maze:
    """Represents the maze."""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1] * cols for _ in range(rows)]

    def draw(self, screen):
        """Draws the maze on the screen."""
        for y in range(self.rows):
            for x in range(self.cols):
                color = WHITE if self.grid[y][x] == 0 else BROWN
                pygame.draw.rect(
                    screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )


class Agent:
    """Represents the agent."""

    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        """Draws the agent on the screen."""
        pygame.draw.circle(
            screen,
            GREEN,
            (
                self.position.x * CELL_SIZE + CELL_SIZE // 2,
                self.position.y * CELL_SIZE + CELL_SIZE // 2,
            ),
            CELL_SIZE // 4,
        )


class MazeGenerator:
    """Generates a random maze."""

    def __init__(self, maze):
        self.maze = maze

    def carve_passages(self, cx, cy):
        """Carves passages in the maze using a recursive backtracking algorithm."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            if (
                0 <= nx < self.maze.rows
                and 0 <= ny < self.maze.cols
                and self.maze.grid[ny][nx] == 1
            ):
                self.maze.grid[cy + direction[1]][cx + direction[0]] = 0
                self.maze.grid[ny][nx] = 0
                self.carve_passages(nx, ny)

    def generate(self):
        """Generates the maze."""
        self.carve_passages(1, 1)


class Pathfinding:
    """Finds the shortest path in the maze using the A* algorithm."""

    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end

    def heuristic(self, a, b):
        """Calculates the Manhattan distance between two positions."""
        return abs(a.x - b.x) + abs(a.y - b.y)

    def find_path(self):
        """Finds the shortest path from the start to the end."""
        open_list = []
        heapq.heappush(open_list, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end)}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == self.end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path = path[::-1]
                return path

            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = Position(current.x + direction[0], current.y + direction[1])
                tentative_g_score = g_score[current] + 1

                if (
                    0 <= neighbor.x < self.maze.rows
                    and 0 <= neighbor.y < self.maze.cols
                ):
                    if self.maze.grid[neighbor.y][neighbor.x] == 0:
                        if (
                            neighbor not in g_score
                            or tentative_g_score < g_score[neighbor]
                        ):
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] + self.heuristic(
                                neighbor, self.end
                            )
                            heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Pathfinding")
    clock = pygame.time.Clock()

    maze = Maze(ROWS, COLS)
    generator = MazeGenerator(maze)
    generator.generate()

    start = Position(1, 1)
    end = Position(ROWS - 2, COLS - 2)
    maze.grid[start.y][start.x] = 0
    maze.grid[end.y][end.x] = 0

    pathfinding = Pathfinding(maze, start, end)
    path = pathfinding.find_path()

    agent = Agent(start)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        maze.draw(screen)
        pygame.draw.circle(
            screen,
            BLUE,
            (end.x * CELL_SIZE + CELL_SIZE // 2, end.y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 4,
        )
        agent.draw(screen)

        if path:
            agent.position = path.pop(0)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()
