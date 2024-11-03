import pygame
import random
import heapq

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Pathfinding")

def main():
    print("Generating maze...")
    maze = [[1] * COLS for _ in range(ROWS)]
    
    def carve_passages(cx, cy, grid):
        print(f"Carving passages at ({cx}, {cy})")
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            if 0 <= nx < ROWS and 0 <= ny < COLS and grid[ny][nx] == 1:
                grid[cy + direction[1]][cx + direction[0]] = 0
                grid[ny][nx] = 0
                carve_passages(nx, ny, grid)
    
    carve_passages(1, 1, maze)
    
    start = (1, 1)
    end = (ROWS - 2, COLS - 2)
    
    print(f"start: {start}, end: {end}")
    maze[start[1]][start[0]] = 0
    maze[end[1]][end[0]] = 0
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    print("running algorithm...")
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        current = heapq.heappop(open_list)[1]
        print(f"current: {current}")

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            tentative_g_score = g_score[current] + 1

            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                if maze[neighbor[1]][neighbor[0]] == 0:
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
                        print(f"added to open list: {neighbor}")

    agent_pos = start
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        
        for y in range(ROWS):
            for x in range(COLS):
                color = WHITE if maze[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.circle(screen, BLUE, (end[0] * CELL_SIZE + CELL_SIZE // 2, end[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.draw.circle(screen, GREEN, (agent_pos[0] * CELL_SIZE + CELL_SIZE // 2, agent_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

        if path:
            print(f"moving agent to: {agent_pos}")
            agent_pos = path.pop(0)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()