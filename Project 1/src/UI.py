import tkinter as tk
from queue import PriorityQueue
from helper import*
from level_1 import*
from Node import*
from tkinter import messagebox
from tkinter import filedialog
import os
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

# Tim diem bat dau va diem ket thuc
def find_start_goal(map_matrix):
    start = None
    goal = None
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[0])):
            if map_matrix[row][col] == 'S':
                start = (row, col)
            elif map_matrix[row][col] == 'G':
                goal = (row, col)
    return start, goal

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
            row1, col1 = path[i]
            row2, col2 = path[i + 1]
            self.canvas.create_line(
                col1 * 60 + 60 / 2, row1 * 60 + 60 / 2,
                col2 * 60 + 60 / 2, row2 * 60 + 60 / 2,
                fill= "red", width = 2
            )


    def level1_bfs():
        algorithm =  "bfs"
        get_algorithm(algorithm)
    
    def level1_dfs():
        algorithm =  "dfs"
        get_algorithm(algorithm)
    
    def level1_ucs():
        algorithm =  "ucs"
        get_algorithm(algorithm)
    
    def level1_astar():
        algorithm =  "astar"
        get_algorithm(algorithm)
    
    def level1_gbfs():
        algorithm =  "gbfs"
        get_algorithm(algorithm)
    
    def get_algorithm(algorithm):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        # Đọc bản đồ từ file
        n, m, map_matrix = readInput(file_path)
        #Tim diem bat dau va diem dich
        start, goal = find_start_goal(map_matrix)
        if algorithm == "bfs":
            _, _, exploredSet = BFS(map_matrix, start, goal)
            root = create_root("BFS") #Ham tao cua so Tkinter
        elif algorithm == "dfs":
            _, _, exploredSet = DFS(map_matrix, start, goal)
            root = create_root("DFS")
        elif algorithm == "ucs":
            _, _, exploredSet = UCS(map_matrix, start, goal)
            root = create_root("UCS")
        elif algorithm == "astar":
            _, _, exploredSet = Astar(map_matrix, start, goal)
            root = create_root("A*")
        elif algorithm == "gbfs":
            _, _, exploredSet = GBFS(map_matrix, start, goal)
            root = create_root("GBFS")
        #Tim duong di
        path = reconstructPath(exploredSet, start, goal, False)
        #root = tk.Tk() #tao cua so Tkinter
        #app = PathFinderApp(root, map_matrix, n, m, t, f)
        app = PathFinderApp(root, map_matrix, n, m)
        app.draw_path(path)
        
        root.mainloop()

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

    '''
def check_file(level, entry):
    #Kiểm tra có trong danh sách file không
    entered_text = entry.get()

    file_exists = False
    for filename in os.listdir():
        if entered_text in filename:
            file_exists = True
            break
    
    if file_exists:
        messagebox.showinfo("Text Found", f"The text '{entered_text}' is found in file names. Please go to algorithm.")
        level.grid(row=3, column=0, padx=window_width/4, pady=7)
    else:
        messagebox.showinfo("Text Not Found", f"The text '{entered_text}' is not found in file names. Please try again.")
        entry.delete(0, tk.END)  # Xóa nội dung nhập vào Entry để người dùng nhập lại
        entry.focus_set()  # Đặt con trỏ tại Entry để người dùng có thể nhập lại
    '''

def check_text_level1(start_label, level1_button, level2_button, level3_button, level4_button, root):
    #Dừng các nút
    start_label.grid_forget()
    level1_button.grid_forget()
    level2_button.grid_forget()
    level3_button.grid_forget()
    level4_button.grid_forget()

    #Nhãn để thông báo
    #label = tk.Label(root, text="Enter file name text", font=("Arial", 20, "bold italic"), fg="Black")
    #label.grid(row=0, column=0, padx=window_width/2.6, pady = 8)

    # Tạo một Entry để nhập văn bản
    #entry = tk.Entry(root, width=30)
    #entry.grid(row=1, column=0, padx=window_width/4, pady= 7)

    #check = tk.Button(root, text="Save", width=10, height=3, command= lambda: check_file(level, entry), bg="Orange", fg="Black")
    #check.grid(row=2, column=0, padx=window_width/4, pady=7)

    #level = tk.Button(root, text="Algorithm", width=10, height=3, command= lambda: algorithm(level, label, entry, check, root), bg="Orange", fg="Black")
    ##level.grid(row=3, column=0, padx=window_width/4, pady=7)
    #level.grid_forget()

def algorithm(start_label, level1_button, level2_button, level3_button, level4_button, root):
    #Dừng các nút
    start_label.grid_forget()
    level1_button.grid_forget()
    level2_button.grid_forget()
    level3_button.grid_forget()
    level4_button.grid_forget()

    start1_label = tk.Label(root, text="Select algorithm", font=("Arial", 24, "bold italic"), fg="Black")
    start1_label.config(bg=root.cget('bg'),  # Đặt màu nền của Label giống với màu nền của cửa sổ
            highlightthickness=0)  # Loại bỏ đường viền xung quanh Label
    start1_label.grid(row=0, column=0, columnspan=2, padx=window_width/2.5, pady=window_height/8)

    BFS_button = tk.Button(root, text="BFS", width=8, height=3, command=lambda: level1_bfs(), bg="Orange", fg="Black")
    BFS_button.grid(row=1, column=0, padx=(window_width/2.5 + 50), pady=5)

    DFS_button = tk.Button(root, text="DFS", width=8, height=3, command=lambda: level1_dfs(), bg="Orange", fg="Black")
    DFS_button.grid(row=2, column=0, padx=(window_width/2.5 + 50), pady=5)

    UCS_button = tk.Button(root, text="UCS", width=8, height=3, command=lambda: level1_ucs(), bg="Orange", fg="Black")
    UCS_button.grid(row=3, column=0, padx=(window_width/2.5 + 50), pady=5)

    Astar_button = tk.Button(root, text="A*", width=8, height=3, command=lambda: level1_astar(), bg="Orange", fg="Black")
    Astar_button.grid(row=4, column=0, padx=(window_width/2.5 + 50), pady=5)

    GBFS_button = tk.Button(root, text="GBFS", width=8, height=3, command=lambda: level1_gbfs(), bg="Orange", fg="Black")
    GBFS_button.grid(row=5, column=0, padx=(window_width/2.5 + 50), pady=5)   
    
    return_button = tk.Button(root, text="Return", width=8, height=3, command=lambda: return_start(start1_label, BFS_button, UCS_button, Astar_button, GBFS_button, return_button, root), bg="Orange", fg="Black")
    return_button.grid(row=6, column=0, padx=(window_width/2.5 + 50), pady=5)   

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

    level2_button = tk.Button(root, text="Level2", width=10, height=3, command=level2, bg="Orange", fg="Black")
    level2_button.grid(row=2, column=0, padx=(window_width/2.5 + 50), pady=5)

    level3_button = tk.Button(root, text="Level3", width=10, height=3, command=level3, bg="Orange", fg="Black")
    level3_button.grid(row=3, column=0, padx=(window_width/2.5 + 50), pady=5)

    level4_button = tk.Button(root, text="Level4", width=10, height=3, command=level4, bg="Orange", fg="Black")
    level4_button.grid(row=4, column=0, padx=(window_width/2.5 + 50), pady=5)
# Đọc bản đồ từ file
'''
def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        #map_data = file.readlines()
        # đọc kích thước map, thời gian giao hàng và dung tích bình nguyên liệu
        n, m, t, f = map(int, file.readline().strip().split())
        # đọc map
        map_matrix = [list(file.readline().strip().split()) for _ in range(n)]
    return map_matrix, n, m, t, f

'''
    
