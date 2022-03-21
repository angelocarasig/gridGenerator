import pygame
pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Grid Generator")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Node():
    """ Class Node represents single cell in the grid """
    def __init__(self, row, col, width, total_rows):
        """ Init function """
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.neighbours = []
        self.total_rows = total_rows

    def get_pos(self):
        """ Returns the position in the grid """
        return self.row, self.col

    def is_color(self, color):
        """ Checks the type of node by color """
        return self.color == color

    def set_color(self, color):
        """ Sets the type of node by color """
        self.color = color

    def draw(self, win):
        """ Drawing the individual nodes """
        pygame.draw.rect(win, self.color, (self.x, self.y , self.width, self.width))

def get_clicked_pos(pos, rows, width):
    """ Get the row and column based on click position """
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

def make_grid(rows, width):
    """ Initializng the grid """
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows) # Adding nodes to every cell
            grid[i].append(node)

    return grid

def draw_grid(win, width, rows):
    """ Draws the grid """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))

def draw(win, grid, width, rows):
    """ Draws elements on the screen """
    win.fill(WHITE)

    """ Drawing the nodes """
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, width, rows) # Drawing the grid

    pygame.display.update()

def flipMatrix(matrix):
    new_matrix = []

    while len(matrix) > 0:
        new_matrix.append(matrix.pop(-1))
    return new_matrix
        
def rotateMatrix(N, mat): 
    for x in range(0, int(N / 2)):
        for y in range(x, N-x-1):
            temp = mat[x][y]
            mat[x][y] = mat[y][N-1-x]
            mat[y][N-1-x] = mat[N-1-x][N-1-y]
            mat[N-1-x][N-1-y] = mat[N-1-y][x]
            mat[N-1-y][x] = temp

def main(win):
    """ Main method which handles the function calls, also handles the input """
    run = True

    ROWS = 20 # Rows val

    # Start and end nodes
    start = None
    end = None

    grid = make_grid(ROWS, WIDTH)

    # Main loop
    while run:
        # Drawing the screen
        draw(win, grid, WIDTH, ROWS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.set_color(BLUE)
                elif not end and node != start:
                    end = node
                    end.set_color(YELLOW)
                elif node != end and node != start:
                    node.set_color(BLACK)

            if pygame.mouse.get_pressed()[2]: # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.set_color(WHITE)

                if node == start:
                    start = None
                elif node == end:      
                    end = None

            if event.type == pygame.KEYDOWN:

                output = []

                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        curr_row = []
                        for node in row:
                            if node.is_color(WHITE):
                                curr_row.append(".")
                            elif node.is_color(BLACK):
                                curr_row.append("=")
                            elif node.is_color(BLUE):
                                curr_row.append("S")
                            elif node.is_color(YELLOW):
                                curr_row.append("E")
                        output.append(curr_row)
                        
                    #Manipulating and saving to file

                    #Because it reads column by column:
                    rotateMatrix(ROWS, output)
                    new_matrix = flipMatrix(output)

                    final = ""
                    for i in new_matrix:
                        for j in i:
                            final += j
                        final += "\n"

                    with open("grid.txt", "w+") as f:
                        f.write(final)

                    pygame.quit()
                    return

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    # Game quit
    pygame.quit()

if __name__ == "__main__":
    main(WIN)