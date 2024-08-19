from Agent import *
from UI import *

def main():
    file_path = open_file_dialog()
    i = Interface(file_path, 'result1.txt')
    a = Agent(i) 

    a.explore_world()

    app = WumpusWorldApp(file_path, "result1.txt")
    app.run()

if __name__ == "__main__":
    # Run the main function
    main()
