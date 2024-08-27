from Agent import *
from UI import *

def main():
    inputFilepath = open_file_dialog()

    # create output file path based on input file path
    slash_index = inputFilepath.rindex('/')
    outputFilepath = inputFilepath[:slash_index] + inputFilepath[slash_index:].replace('map', 'result')

    i = Interface(inputFilepath, outputFilepath)
    a = Agent(i) 

    a.explore_world()

    app = WumpusWorldApp(inputFilepath, outputFilepath)
    app.run()

if __name__ == "__main__":
    # Run the main function
    main()