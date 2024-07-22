import tkinter as tk
from queue import PriorityQueue

#import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

window_width = 1000
window_height = 600

#Các nút level
def level1():
    print("Hello")
def level2():
    print("Hello")
def level3():
    print("Hello")
def level4():
    print("Hello")

#Code ghi file 
def save_to_file(text_box):
    # Lấy nội dung từ text_box
    text_content = text_box.get("1.0", tk.END)

    # Ghi nội dung vào file "text.txt"
    with open("text.txt", 'w') as file:
        file.write(text_content)

    # Thông báo hoàn thành
    tk.messagebox.showinfo("Thông báo", "Đã lưu vào file 'text.txt' thành công!")

def start_game(start_button, title_label, exit_button, root):
    #Dừng các nút ban đầu
    start_button.grid_forget()
    title_label.grid_forget()
    exit_button.grid_forget()

    #Các nút xuất hiện trong giao diện Level
    start_label = tk.Label(root, text="Select Level", font=("Arial", 24, "bold italic"), fg="Black")
    start_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/4.5)

    #các nút level
    level1_button = tk.Button(root, text="Level1", width=15, height=5, command= lambda: algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root), bg="Orange", fg="Black")
    level1_button.grid(row=1, column=0, padx=5, pady=3)

    level2_button = tk.Button(root, text="Level2", width=15, height=5, command=level2, bg="Orange", fg="Black")
    level2_button.grid(row=1, column=1, padx=5, pady=3)

    level3_button = tk.Button(root, text="Level3", width=15, height=5, command=level3, bg="Orange", fg="Black")
    level3_button.grid(row=2, column=0, padx=3, pady=3)

    level4_button = tk.Button(root, text="Level4", width=15, height=5, command=level4, bg="Orange", fg="Black")
    level4_button.grid(row=2, column=1, padx=3, pady=3)

    exit_button = tk.Button(root, text="Exit", width=15, height=5, command= lambda: exit_game(root), bg="Orange", fg="Black")
    exit_button.grid(row=3, column=1, padx=3, pady=3)

def algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root):
    #Dừng các nút
    start_label.grid_forget()
    level1_button.grid_forget()
    level2_button.grid_forget()
    level3_button.grid_forget()
    level4_button.grid_forget()

    start1_label = tk.Label(root, text="Select algorithm", font=("Arial", 24, "bold italic"), fg="Black")
    start1_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/4.5)

    BFS_button = tk.Button(root, text="BFS", width=15, height=5, command=lambda: level1_bfs(), bg="Orange", fg="Black")
    BFS_button.grid(row=1, column=0, padx=5, pady=3)

    DFS_button = tk.Button(root, text="DFS", width=15, height=5, command=level2, bg="Orange", fg="Black")
    DFS_button.grid(row=1, column=1, padx=5, pady=3)

    UCS_button = tk.Button(root, text="UCS", width=15, height=5, command=level3, bg="Orange", fg="Black")
    UCS_button.grid(row=2, column=0, padx=3, pady=3)

    GBFS_button = tk.Button(root, text="GBFS", width=15, height=5, command=level4, bg="Orange", fg="Black")
    GBFS_button.grid(row=2, column=1, padx=3, pady=3)   

def exit_game(root):
    root.destroy()

#Hàm tạo cửa sổ
def create_root(string):
    root = tk.Tk()
    root.title(string)
    return root

def create_screen():
    #Tạo cửa sổ
    root = create_root("Searching")

    #Căn giữa màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    # Nhãn tiêu đề
    title_label = tk.Label(root, text="Welcome to My Game", font=("Arial", 24, "bold italic"), fg="Black")
    title_label.grid(row=0, column=0, columnspan=2, padx=window_width/3, pady=window_height/4)

    # Nút bắt đầu trò chơi
    start_button = tk.Button(root, text="Start", width=15, height=5, command= lambda: start_game(start_button, title_label, exit_button, root), bg="Orange", fg="Black")
    start_button.grid(row=1, column=0, padx=10, pady=10)

    # Nút thoát
    exit_button = tk.Button(root, text="Exit", width=15, height=5, command= lambda: exit_game(root), bg="Orange", fg="Black")
    exit_button.grid(row=1, column=1, padx=10, pady=10)
    # Chạy vòng lặp chính của tkinter để hiển thị cửa sổ
    root.mainloop()

#create_screen()

# Đọc bản đồ từ file
def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        #map_data = file.readlines()
        # đọc kích thước map, thời gian giao hàng và dung tích bình nguyên liệu
        n, m, t, f = map(int, file.readline().strip().split())
        # đọc map
        map_matrix = [list(file.readline().strip().split()) for _ in range(n)]
    return map_matrix, n, m, t, f

def readInput(filepath):
    map = []
    f = open(filepath)
    n, m = f.readline().split()
    try:
        n = int(n)
        m = int(m)
        for i in range (0, n):
            line = f.readline()
            newRow = line.split()
            map.append(newRow)
    except:
        print('The number of row or column is invalid')
    return n, m, map

# Tim diem bat dau va diem ket thuc
def find_start_goal(map_matrix):
    start = None
    goal = None
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[0])):
            if map_matrix[row][col] == 'S':
                start = (col, row)
            elif map_matrix[row][col] == 'G':
                goal = (col, row)
    return start, goal

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up
def BFS(map, start, goal):
    frontier = [start]
    exploredSet = []
    while (len(frontier) > 0):
        currentPos = frontier.pop(0)
        exploredSet.append(currentPos)

        print(currentPos)
        for d in directions:
            newPos = tuple([a+b for a, b in zip(currentPos, d)])
            print('newPos', newPos)
            if newPos == goal:
                print('Goal')
                return 1, frontier, exploredSet
            if 0 <= newPos[0] < len(map[0]) and 0 <= newPos[1] < len(map) and map[newPos] != '-1' and newPos not in exploredSet and newPos not in frontier:
                print('append frontier')
                frontier.append(newPos)
    return exploredSet

# Thuật toán Dijkstra
def dijkstra(map_matrix, start, goal):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = PriorityQueue()
        queue.put((0, start))
        distances = {start: 0}
        previous = {start: None}

        while not queue.empty():
            current_distance, current_cell = queue.get()
            if current_cell == goal:
                break
            for direction in directions:
                neighbor = (current_cell[0] + direction[0], current_cell[1] + direction[1])
                if (0 <= neighbor[0] < len(map_matrix) and 0 <= neighbor[1] < len(map_matrix[0]) and
                        map_matrix[neighbor[1]][neighbor[0]] in ('0', 'G')):
                    distance = current_distance + 1
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current_cell
                        queue.put((distance, neighbor))

        path = []
        cell = goal
        while cell:
            path.append(cell)
            cell = previous[cell]
        path.reverse()
        return path

class PathFinderApp:
    #khoi tao map
    def __init__(self, root, map_matrix, n, m):
        self.root = root
        self.map_matrix = map_matrix
        '''
        map_width = len(self.map_matrix[0])
        map_height = len(self.map_matrix)
        '''
        self.canvas = tk.Canvas(root, width = m * 60, height = n * 60)
        self.canvas.pack()
        self.draw_map(n, m)

    #Ve va to mau cac o trong map
    def draw_map(self, n, m):
        self.canvas.delete("all")
        for row in range(n):
            for col in range(m):
                if self.map_matrix[row][col].startswith('S'):
                    color = "lightgreen"
                elif self.map_matrix[row][col].startswith('G'):
                    color = "lightcoral"
                elif self.map_matrix[row][col].isdigit() and int(self.map_matrix[row][col]) > 0:
                    color = "lightblue"
                elif self.map_matrix[row][col] == '-1':
                    color = "slategray"
                elif self.map_matrix[row][col] == '0':
                    color = "white"
                self.canvas.create_rectangle(
                    col * 60,
                    row * 60,
                    (col + 1) * 60,
                    (row + 1) * 60,
                    fill = color,
                    outline = "black"
                )
                # Ghi chu S va G vao o bat dau va o ket thuc
                if self.map_matrix[row][col].startswith('S') or self.map_matrix[row][col].startswith('G') or (self.map_matrix[row][col].isdigit() and int(self.map_matrix[row][col]) > 0):
                    self.canvas.create_text(col * 60 + 60 / 2, row * 60 + 60 / 2, text = self.map_matrix[row][col], fill = "black", font = ("Helvetica", 16, "bold"))
    
    #Ve duong di tim duoc
    def draw_path(self, path):
        '''
        for (row, col) in path:
            self.canvas.create_rectangle(
                col * self.square_size,
                row * self.square_size,
                (col + 1) * self.square_size,
                (row + 1) * self.square_size,
                fill="blue",
                outline="black"
            )
        '''
        for i in range(len(path) - 1):
            col1, row1 = path[i]
            col2, row2 = path[i + 1]
            self.canvas.create_line(
                col1 * 60 + 60 / 2, row1 * 60 + 60 / 2,
                col2 * 60 + 60 / 2, row2 * 60 + 60 / 2,
                fill= "red", width = 2
            )

def level1_bfs():
    #map_matrix, n, m, t, f = read_map_from_file('input1_level1.txt')  # Đọc bản đồ từ file
    n, m, map_matrix = readInput('input1_level1.txt')
    start, goal = find_start_goal(map_matrix)
    path = dijkstra(map_matrix, start, goal)  # Tìm đường đi ngắn nhất
    #path = BFS(map_matrix, start, goal)
    root = tk.Tk() #tao cua so Tkinter
    #app = PathFinderApp(root, map_matrix, n, m, t, f)
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(path)
    
    root.mainloop()

def main():
    create_screen()
    '''
    map_matrix, n, m, t, f = read_map_from_file('map.txt')  # Đọc bản đồ từ file
    #viet ham tim diem bat dau va ket thuc
    
    start, goal = find_start_goal(map_matrix)
    path = dijkstra(map_matrix, start, goal)  # Tìm đường đi ngắn nhất

    root = tk.Tk() #tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m, t, f)
    app.draw_path(path)
    
    root.mainloop()
    '''

if __name__ == "__main__":
    main()
