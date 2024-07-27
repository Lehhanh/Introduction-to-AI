import tkinter as tk
from helper import*
from level_1 import*
from level_2 import*
from level_3 import*
from Node import*
from tkinter import filedialog
from PIL import ImageTk, Image

window_width = 1000 
window_height = 600
global entered_text # filename
#Hàm tạo cửa sổ
def create_root(string):
    root = tk.Tk()
    root.title(string)
    return root

#Các nút level
def level4():
    print("Hello")


class PathFinderApp:
    #khoi tao map
    def __init__(self, root, map_matrix, n, m):
        self.root = root
        self.map_matrix = map_matrix
        self.canvas = tk.Canvas(root, width = 600, height = 600)
        self.canvas.pack()
        self.square_size = min(600 // len(map_matrix), 600 // len(map_matrix[0])) #kich thuoc o vuong
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
                elif self.map_matrix[row][col].startswith('F'):
                    color = "lemonchiffon"
                elif self.map_matrix[row][col].isdigit() and int(self.map_matrix[row][col]) > 0:
                    color = "lightblue"
                elif self.map_matrix[row][col] == '-1':
                    color = "slategray"
                elif self.map_matrix[row][col] == '0':
                    color = "white"
                self.canvas.create_rectangle(
                    col * self.square_size,
                    row * self.square_size,
                    (col + 1) * self.square_size,
                    (row + 1) * self.square_size,
                    fill = color,
                    outline = "black"
                )
                # Ghi chu S va G vao o bat dau va o ket thuc
                if self.map_matrix[row][col].startswith('S') or self.map_matrix[row][col].startswith('G') or self.map_matrix[row][col].startswith('F') or (self.map_matrix[row][col].isdigit() and int(self.map_matrix[row][col]) > 0):
                    self.canvas.create_text(col * self.square_size + self.square_size / 2, row * self.square_size + self.square_size / 2, text = self.map_matrix[row][col], fill = "black", font = ("Helvetica", 16, "bold"))
    
    #Ve duong di tim duoc
    def draw_path(self, path):
        for i in range(len(path) - 1):
            row1, col1 = path[i]
            row2, col2 = path[i + 1]
            self.canvas.create_line(
                col1 * self.square_size + self.square_size / 2, row1 * self.square_size + self.square_size / 2,
                col2 * self.square_size + self.square_size / 2, row2 * self.square_size + self.square_size / 2,
                fill= "red", width = 2
            )



def create_screen():
    #Tạo cửa sổ
    root = create_root("Searching")

    #Căn giữa màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    # Đọc hình ảnh và chuyển đổi thành đối tượng Image của Pillow
    background_image = Image.open("background.jpg")
    # Điều chỉnh kích thước hình ảnh phù hợp với cửa sổ tkinter
    background_image = background_image.resize((window_width, window_height), Image.NEAREST)
    # Chuyển đổi hình ảnh thành đối tượng ImageTk của tkinter để có thể sử dụng như làm nền
    background_image_tk = ImageTk.PhotoImage(background_image)

    # Tạo widget Label để hiển thị hình ảnh làm nền
    background_label = tk.Label(root, image=background_image_tk)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Nhãn tiêu đề
    title_label = tk.Label(root, text="Welcome to My Game", font=("Arial", 24, "bold italic"), fg="Black")
    title_label.grid(row=0, column=0, columnspan=2, padx=window_width/3, pady=window_height/4)
    title_label.config(bg=root.cget('bg'),  # Đặt màu nền của Label giống với màu nền của cửa sổ
             highlightthickness=0)  # Loại bỏ đường viền xung quanh Label

    # Nút bắt đầu trò chơi
    start_button = tk.Button(root, text="Start", width=15, height=5, command= lambda: start_game(start_button, title_label, root), bg="Orange", fg="Black")
    start_button.grid(row=1, column=0, columnspan=2, padx=window_width/3, pady=10)

    # Chạy vòng lặp chính của tkinter để hiển thị cửa sổ
    root.mainloop()

def start_game(start_button, title_label, root):
    #Dừng các nút ban đầu
    start_button.grid_forget()
    title_label.grid_forget()

    #Các nút xuất hiện trong giao diện Level
    start_label = tk.Label(root, text="Select Level", font=("Arial", 24, "bold italic"), fg="Black")
    start_label.config(bg=root.cget('bg'),  # Đặt màu nền của Label giống với màu nền của cửa sổ
             highlightthickness=0)  # Loại bỏ đường viền xung quanh Label
    start_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/7)

    #các nút level
    level1_button = tk.Button(root, text="Level1", width=10, height=3, command= lambda: algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root), bg="Orange", fg="Black")
    level1_button.grid(row=1, column=0, padx=(window_width/2.5 + 50), pady=5)

    level2_button = tk.Button(root, text="Level2", width=10, height=3, command=level2, bg="Orange", fg="Black")
    level2_button.grid(row=2, column=0, padx=(window_width/2.5 + 50), pady=5)

    level3_button = tk.Button(root, text="Level3", width=10, height=3, command=level3, bg="Orange", fg="Black")
    level3_button.grid(row=3, column=0, padx=(window_width/2.5 + 50), pady=5)

    level4_button = tk.Button(root, text="Level4", width=10, height=3, command=level4, bg="Orange", fg="Black")
    level4_button.grid(row=4, column=0, padx=(window_width/2.5 + 50), pady=5)


def algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root):
    #Dừng các nút
    start_label.grid_forget()
    level1_button.grid_forget()
    level2_button.grid_forget()
    level3_button.grid_forget()
    level4_button.grid_forget()
    
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    # Đọc bản đồ từ file
    n, m, map_matrix = readInput(file_path, 1)
    pathList = pathFinding_level1(map_matrix)
    
    start1_label = tk.Label(root, text="Select algorithm", font=("Arial", 24, "bold italic"), fg="Black")
    start1_label.config(bg=root.cget('bg'),  # Đặt màu nền của Label giống với màu nền của cửa sổ
            highlightthickness=0)  # Loại bỏ đường viền xung quanh Label
    start1_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/8)

    BFS_button = tk.Button(root, text="BFS", width=8, height=3, command=lambda: level1_bfs(n, m, map_matrix, pathList), bg="Orange", fg="Black")
    BFS_button.grid(row=1, column=0, padx=(window_width/2.5 + 50), pady=5)

    DFS_button = tk.Button(root, text="DFS", width=8, height=3, command=lambda: level1_dfs(n, m, map_matrix, pathList), bg="Orange", fg="Black")
    DFS_button.grid(row=2, column=0, padx=(window_width/2.5 + 50), pady=5)

    UCS_button = tk.Button(root, text="UCS", width=8, height=3, command=lambda: level1_ucs(n, m, map_matrix, pathList), bg="Orange", fg="Black")
    UCS_button.grid(row=3, column=0, padx=(window_width/2.5 + 50), pady=5)

    Astar_button = tk.Button(root, text="A*", width=8, height=3, command=lambda: level1_astar(n, m, map_matrix, pathList), bg="Orange", fg="Black")
    Astar_button.grid(row=4, column=0, padx=(window_width/2.5 + 50), pady=5)

    GBFS_button = tk.Button(root, text="GBFS", width=8, height=3, command=lambda: level1_gbfs(n, m, map_matrix, pathList), bg="Orange", fg="Black")
    GBFS_button.grid(row=5, column=0, padx=(window_width/2.5 + 50), pady=5)   
    
    return_button = tk.Button(root, text="Return", width=8, height=3, command=lambda: return_start(start1_label, BFS_button, UCS_button, Astar_button, GBFS_button, return_button, root), bg="Orange", fg="Black")
    return_button.grid(row=6, column=0, padx=(window_width/2.5 + 50), pady=5)   

def level1_bfs(n, m, map_matrix, pathList):
    root = create_root("BFS") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(pathList[0])
        
    root.mainloop()
    
def level1_dfs(n, m, map_matrix, pathList):
    root = create_root("BFS") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(pathList[1])
        
    root.mainloop()
    
def level1_ucs(n, m, map_matrix, pathList):
    root = create_root("BFS") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(pathList[2])
        
    root.mainloop()
    
def level1_astar(n, m, map_matrix, pathList):
    root = create_root("BFS") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(pathList[3])
        
    root.mainloop()
    
def level1_gbfs(n, m, map_matrix, pathList):
    root = create_root("BFS") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(pathList[4])
        
    root.mainloop()

def level2():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    # Đọc bản đồ từ file
    n, m, map_matrix, t = readInput(file_path, 2)
    path = pathFinding_level2(map_matrix, t)
    root = create_root("Level 2") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(path)
        
    root.mainloop()

def level3():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    # Đọc bản đồ từ file
    n, m, map_matrix, t, f = readInput(file_path, 3)
    path = pathFinding_level3(map_matrix, t, f)
    root = create_root("Level 3") #Ham tao cua so Tkinter
    app = PathFinderApp(root, map_matrix, n, m)
    app.draw_path(path)
        
    root.mainloop()


def return_start(start1_label, BFS_button, UCS_button, Astar_button, GBFS_button, return_button, root):
    start1_label.grid_forget()
    BFS_button.grid_forget()
    UCS_button.grid_forget()
    Astar_button.grid_forget()
    GBFS_button.grid_forget()
    return_button.grid_forget()
    #Các nút xuất hiện trong giao diện Level
    start_label = tk.Label(root, text="Select Level", font=("Arial", 24, "bold italic"), fg="Black")
    start_label.config(bg=root.cget('bg'),  # Đặt màu nền của Label giống với màu nền của cửa sổ
             highlightthickness=0)  # Loại bỏ đường viền xung quanh Label
    start_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/7)

    #các nút level
    level1_button = tk.Button(root, text="Level1", width=10, height=3, command= lambda: algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root), bg="Orange", fg="Black")
    level1_button.grid(row=1, column=0, padx=(window_width/2.5 + 50), pady=5)

    level2_button = tk.Button(root, text="Level2", width=10, height=3, command= lambda: level2(), bg="Orange", fg="Black")
    level2_button.grid(row=2, column=0, padx=(window_width/2.5 + 50), pady=5)

    level3_button = tk.Button(root, text="Level3", width=10, height=3, command= lambda: level3(), bg="Orange", fg="Black")
    level3_button.grid(row=3, column=0, padx=(window_width/2.5 + 50), pady=5)

    level4_button = tk.Button(root, text="Level4", width=10, height=3, command=level4, bg="Orange", fg="Black")
    level4_button.grid(row=4, column=0, padx=(window_width/2.5 + 50), pady=5)
