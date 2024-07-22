from helper import *
#from level_1 import *
from UI import *

#map = readInput('..\\input\\input1_level1.txt')
#algorithm = input('Enter algorithm: ')
#pathfindingLevel_1(algorithm, map)

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