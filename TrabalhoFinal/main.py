from gui import SoccerApp
from searcher import Searcher


if __name__ == "__main__":
    searcher = Searcher()
    app = SoccerApp(searcher)
    app.mainloop()

