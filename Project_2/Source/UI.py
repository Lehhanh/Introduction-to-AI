import pygame
import tkinter as tk
from tkinter import filedialog
import sys
from Agent import *
class WumpusWorldApp:
    def __init__(self, input_file_path=None, output_file_path="output.txt"):
        pygame.init()
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

        # Screen dimensions
        self.screen_size = (800, 700)
        self.grid_size, self.cell_size = self.calculate_grid_and_cell_size()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Wumpus World")
        self.clock = pygame.time.Clock()

        # Load images
        self.load_images()

        # Initialize game variables
        self.grid = []
        self.agent_position = (1, 1)
        self.agent_direction = 'N'
        self.health = 100
        self.points = 0
        self.start_game = False
        self.message = None
        self.message_timer = 0
        self.scream_message = None
        self.scream_timer = 0

        # Load the grid and draw
        if self.input_file_path:
            self.load_grid(self.input_file_path)
            self.update_display()

    def calculate_grid_and_cell_size(self):
        if not self.input_file_path:
            return 0, 0
        grid, size = read_input_file(self.input_file_path)
        cell_size = (self.screen_size[0] - 200) // size  # Reserve space for the info panel
        return size, cell_size

    def load_images(self):
        # Load and scale images
        self.agent_image_size = (self.cell_size, self.cell_size)
        self.images = {
            'agent_up': pygame.transform.scale(pygame.image.load("image/agent.png"), self.agent_image_size),
            'agent_right': pygame.transform.scale(pygame.image.load("image/right.png"), self.agent_image_size),
            'agent_down': pygame.transform.scale(pygame.image.load("image/down.png"), self.agent_image_size),
            'agent_left': pygame.transform.scale(pygame.image.load("image/left.png"), self.agent_image_size),
            'heal': pygame.transform.scale(pygame.image.load("image/healing_poison.png"), (self.cell_size // 2, self.cell_size // 2)),
            'wumpus': pygame.transform.scale(pygame.image.load("image/wumpus.png"), (self.cell_size // 2, self.cell_size // 2)),
            'pit': pygame.transform.scale(pygame.image.load("image/pit.png"), (self.cell_size // 2, self.cell_size // 2)),
            'poison': pygame.transform.scale(pygame.image.load("image/poison_gas.png"), (self.cell_size // 2, self.cell_size // 2)),
            'gold': pygame.transform.scale(pygame.image.load("image/gold.png"), (self.cell_size // 2, self.cell_size // 2)),
            'stench': pygame.transform.scale(pygame.image.load("image/stench.jpg"), (self.cell_size // 2, self.cell_size // 2)),
            'breeze': pygame.transform.scale(pygame.image.load("image/breeze.png"), (self.cell_size // 2, self.cell_size // 2)),
            'whiff': pygame.transform.scale(pygame.image.load("image/whiff.jpg"), (self.cell_size // 2, self.cell_size // 2)),
            'glitter': pygame.transform.scale(pygame.image.load("image/glow.png"), (self.cell_size // 2, self.cell_size // 2)),
        }

    def load_grid(self, filename):
        self.grid, _ = read_input_file(filename)
        self.grid = [[self.parse_cell(cell) for cell in row] for row in reversed(self.grid)]  # Reverse rows
        self.add_percepts()  # Add percepts around elements

    def parse_cell(self, cell):
        percepts = {
            'W': 'wumpus',
            'P': 'pit',
            'G': 'gold',
            'P_G': 'poison',
            'H_P': 'heal'
        }
        return [percepts.get(item, '-') for item in cell.split(',') if item]

    def add_percepts(self):
        """
        Thêm percepts cho các ô dựa trên các thành phần còn lại trong lưới.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if 'wumpus' in self.grid[i][j]:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            if 'stench' not in self.grid[ni][nj]:
                                self.grid[ni][nj].append('stench')
                
                if 'pit' in self.grid[i][j]:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            if 'breeze' not in self.grid[ni][nj]:
                                self.grid[ni][nj].append('breeze')
                
                if 'poison' in self.grid[i][j]:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            if 'whiff' not in self.grid[ni][nj]:
                                self.grid[ni][nj].append('whiff')

                if 'heal' in self.grid[i][j]:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            if 'glitter' not in self.grid[ni][nj]:
                                self.grid[ni][nj].append('glitter')

    def update_display(self):
        self.screen.fill((200, 200, 200))
        self.draw_grid()
        self.draw_elements()
        self.draw_agent()
        self.draw_health_and_points()
        self.draw_start_button()
        self.draw_message()
        pygame.display.flip()

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = j * self.cell_size
                y = (self.grid_size - i - 1) * self.cell_size  # Invert y-coordinate
                pygame.draw.rect(self.screen, (150, 150, 150), (x, y, self.cell_size, self.cell_size), 1)

    def remove_component(self, x, y, component):
        """
        Xóa một thành phần cụ thể từ ô (x, y) và cập nhật ô đó.
        """
        # Lấy danh sách các thành phần trong ô (x, y)
        cell_content = self.grid[y - 1][x - 1]
        
        # Nếu thành phần cần xóa tồn tại trong ô
        if component in cell_content:
            # Xóa thành phần
            cell_content.remove(component)
            
            # Cập nhật lại nội dung ô
            self.grid[y - 1][x - 1] = cell_content
            
            # Xóa percepts liên quan đến thành phần bị xóa
            self.remove_related_percepts(x, y, component)
            
            # Cập nhật màn hình
            self.update_cell(x, y)

    def update_cell(self, x, y):
        """
        Vẽ lại một ô cụ thể (x, y) sau khi một thành phần đã bị xóa.
        """
        # Xóa vùng của ô hiện tại để vẽ lại
        cell_x = (x - 1) * self.cell_size
        cell_y = (self.grid_size - y) * self.cell_size
        pygame.draw.rect(self.screen, (255, 255, 255), (cell_x, cell_y, self.cell_size, self.cell_size))  # Màu trắng để xóa
        
        # Vẽ lại tất cả các thành phần còn lại trong ô
        self.draw_elements(x, y)

    def draw_elements(self, x=None, y=None):
        """
        Vẽ tất cả các thành phần trong toàn bộ lưới, hoặc chỉ trong ô cụ thể nếu x, y được cung cấp.
        """
        if x is not None and y is not None:
            # Vẽ lại chỉ một ô cụ thể
            cell_content = self.grid[y - 1][x - 1]
            cell_x = (x - 1) * self.cell_size
            cell_y = (self.grid_size - y) * self.cell_size
            
            # Vẽ từng thành phần trong ô
            for k, item in enumerate(cell_content):
                if item in self.images:
                    image = self.images[item]
                    sub_x = cell_x + (k % 2) * (self.cell_size // 2)
                    sub_y = cell_y + (k // 2) * (self.cell_size // 2)
                    self.screen.blit(image, (sub_x, sub_y))
        else:
            # Vẽ toàn bộ lưới
            for i, row in enumerate(self.grid):
                for j, cell_content in enumerate(row):
                    cell_x = j * self.cell_size
                    cell_y = (self.grid_size - i - 1) * self.cell_size
                    
                    # Vẽ từng thành phần trong ô
                    for k, item in enumerate(cell_content):
                        if item in self.images:
                            image = self.images[item]
                            sub_x = cell_x + (k % 2) * (self.cell_size // 2)
                            sub_y = cell_y + (k // 2) * (self.cell_size // 2)
                            self.screen.blit(image, (sub_x, sub_y))

    def draw_agent(self):
        x, y = self.agent_position
        x_pos = (x - 1) * self.cell_size
        y_pos = (self.grid_size - y) * self.cell_size  # Invert y-coordinate for agent

        if self.agent_direction == 'N':
            image = self.images['agent_up']
        elif self.agent_direction == 'E':
            image = self.images['agent_right']
        elif self.agent_direction == 'S':
            image = self.images['agent_down']
        elif self.agent_direction == 'W':
            image = self.images['agent_left']
        
        self.screen.blit(image, (x_pos, y_pos))

    def draw_health_and_points(self):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))
        points_text = font.render(f"Points: {self.points}", True, (255, 255, 255))

        # Draw info panel
        pygame.draw.rect(self.screen, (100, 100, 100), (self.grid_size * self.cell_size, 0, 200, self.screen_size[1]))
        self.screen.blit(health_text, (self.grid_size * self.cell_size + 10, 10))
        self.screen.blit(points_text, (self.grid_size * self.cell_size + 10, 50))

    def draw_start_button(self):
        button_color = (0, 128, 0)  # Green
        self.start_button_rect = pygame.Rect(self.grid_size * self.cell_size + 50, self.screen_size[1] // 2 - 20, 100, 40)
        pygame.draw.rect(self.screen, button_color, self.start_button_rect)
        
        font = pygame.font.Font(None, 36)
        start_text = font.render("Start", True, (255, 255, 255))
        self.screen.blit(start_text, (self.grid_size * self.cell_size + 65, self.screen_size[1] // 2 - 10))

    def draw_message(self):
        font = pygame.font.Font(None, 36)
        current_time = pygame.time.get_ticks()

        if self.message and current_time < self.message_timer:
            message_text = font.render(self.message, True, (255, 0, 0))
            self.screen.blit(message_text, (self.grid_size * self.cell_size + 10, 90))

        if self.scream_message and current_time < self.scream_timer:
            scream_text = font.render(self.scream_message, True, (255, 0, 0))
            self.screen.blit(scream_text, (self.grid_size * self.cell_size + 10, 130))

    def perform_actions(self):
        """
        Thực hiện các hành động từ tệp tin đầu ra và cập nhật lưới và hiển thị.
        """
        actions = read_output_file(self.output_file_path)

        for position, action, direction, health, points in actions:
            x, y = position
            
            # Cập nhật vị trí và hướng của đại lý
            self.agent_position = (x, y)  # Cập nhật vị trí của đại lý theo chỉ số 1-based
            self.agent_direction = direction
            self.health = health
            self.points = points

            # Xử lý hành động và cập nhật lưới
            if action == 'GRAB_GOLD':
                self.remove_component(x, y, 'gold')
                self.message = "Gold grabbed!"
                self.message_timer = pygame.time.get_ticks() + 2000  # Hiển thị tin nhắn trong 2 giây

            elif action == 'GRAB_HP':
                self.remove_component(x, y, 'heal')
                self.remove_related_percepts(x, y, 'heal')
                self.message = "Healing potion grabbed!"
                self.message_timer = pygame.time.get_ticks() + 2000  # Hiển thị tin nhắn trong 2 giây

            elif action == 'HEAL':
                self.message = "Healing!"
                self.message_timer = pygame.time.get_ticks() + 2000  # Hiển thị tin nhắn trong 2 giây

            elif action == 'CLIMB':
                self.message = "Climbing!"
                self.message_timer = pygame.time.get_ticks() + 2000  # Hiển thị tin nhắn trong 2 giây

            elif action == 'SHOOT':
                self.message = "Shooting!"
                self.message_timer = pygame.time.get_ticks() + 2000  # Hiển thị tin nhắn trong 2 giây
                self.scream_message = "Wumpus is screaming!"
                
                # Xác định tọa độ mục tiêu dựa trên hướng của đại lý
                if self.agent_direction == 'N':
                    target_x, target_y = x, y + 1
                elif self.agent_direction == 'S':
                    target_x, target_y = x, y - 1
                elif self.agent_direction == 'E':
                    target_x, target_y = x + 1, y
                elif self.agent_direction == 'W':
                    target_x, target_y = x - 1, y

                # Xóa Wumpus và percepts liên quan
                if 0 <= target_x - 1 < self.grid_size and 0 <= target_y - 1 < self.grid_size:
                    self.remove_component(target_x, target_y, 'wumpus')
                    self.remove_related_percepts(target_x, target_y, 'wumpus')

                self.scream_timer = pygame.time.get_ticks() + 4000  # Hiển thị tin nhắn trong 4 giây sau khi bắn

            # Cập nhật màn hình và vẽ lại
            self.update_display()
            pygame.time.delay(500)  # Dừng lại một chút để hiển thị cập nhật

    def remove_related_percepts(self, x, y, removed_component):
        """
        Xóa các percepts liên quan đến ô (x, y) dựa trên loại thành phần bị xóa.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for di, dj in directions:
            ni, nj = x + di, y + dj
            if 0 <= ni - 1 < self.grid_size and 0 <= nj - 1 < self.grid_size:
                neighbor_cell_content = self.grid[nj - 1][ni - 1]
                
                # Xóa percepts liên quan dựa trên loại thành phần bị xóa
                if removed_component == 'wumpus':
                    neighbor_cell_content = [item for item in neighbor_cell_content if item != 'stench']
                elif removed_component == 'pit':
                    neighbor_cell_content = [item for item in neighbor_cell_content if item != 'breeze']
                elif removed_component == 'poison':
                    neighbor_cell_content = [item for item in neighbor_cell_content if item != 'whiff']
                elif removed_component == 'heal':
                    neighbor_cell_content = [item for item in neighbor_cell_content if item != 'glitter']
                
                self.grid[nj - 1][ni - 1] = neighbor_cell_content
                
                # Cập nhật ô sau khi xóa percepts
                self.update_cell(ni, nj)

    def update_grid_percepts(self):
        """
        Cập nhật percepts cho toàn bộ lưới.
        """
        # Reset percepts cho tất cả các ô
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_content = self.grid[i][j]
                # Loại bỏ percepts cũ
                self.grid[i][j] = [item for item in cell_content if item not in ('stench', 'breeze', 'whiff', 'glitter')]
        
        # Thêm percepts mới dựa trên các thành phần hiện có
        self.add_percepts()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check "Start" button
                if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                    self.start_game = True
                    if self.input_file_path:
                        self.perform_actions()  # Call perform_actions when game starts

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_agent('N')
                elif event.key == pygame.K_DOWN:
                    self.move_agent('S')
                elif event.key == pygame.K_LEFT:
                    self.move_agent('W')
                elif event.key == pygame.K_RIGHT:
                    self.move_agent('E')
                elif event.key == pygame.K_r:
                    self.rotate_agent('TURN_RIGHT')
                elif event.key == pygame.K_l:
                    self.rotate_agent('TURN_LEFT')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.grid_size * self.cell_size + 50 <= event.pos[0] <= self.grid_size * self.cell_size + 150 and self.screen_size[1] // 2 - 20 <= event.pos[1] <= self.screen_size[1] // 2 + 20:
                        self.start_game = True
                        self.perform_actions()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_agent('N')
                    elif event.key == pygame.K_DOWN:
                        self.move_agent('S')
                    elif event.key == pygame.K_LEFT:
                        self.move_agent('W')
                    elif event.key == pygame.K_RIGHT:
                        self.move_agent('E')
                    elif event.key == pygame.K_r:
                        self.rotate_agent('TURN_RIGHT')
                    elif event.key == pygame.K_l:
                        self.rotate_agent('TURN_LEFT')

            self.update_display()
            self.clock.tick(30)

def read_input_file(filename):
    with open(filename, 'r') as file:
        # Đọc kích thước lưới từ dòng đầu tiên
        grid_size = int(file.readline().strip())
           
        # Đọc các dòng còn lại để xây dựng ma trận lưới
        grid = []
        for line in file:
            line = line.strip()
            if line:  # Kiểm tra nếu dòng không trống
                grid.append(line.split('.'))
                   
    return grid, grid_size

def open_file_dialog():
    """
    Open a file dialog to select the input file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path

def read_output_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        results = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(': ')
                position_str = parts[0].strip('()')
                action = parts[1].strip()
                direction = parts[2].strip()
                health = float(parts[3].strip())
                points = int(parts[4].strip())

                x, y = map(int, position_str.split(', '))
                results.append(((x, y), action, direction, health, points))

        return results

file_path = open_file_dialog()
i = Interface(file_path, 'result1.txt')
a = Agent(i) 
a.explore_world()
print('complete explore')
app = WumpusWorldApp(file_path, "result1.txt")
app.run()
#position, action, direction, health, points = read_output_file("result1.txt")
