class LevelInfo():
    def __init__(self, name, grid, attr, high_scores = [],
                 colors = ['green','brown'], lavaspeed = 0, snow = None,
                 complete_color = 'black', wrap = False):
        self.grid = grid
        self.attr = attr
        self.high_scores = list(high_scores)
        self.colors = colors
        self.lavaspeed = lavaspeed
        self.snow = snow
        self.complete_color = complete_color
        self.wrap = wrap
        
    def __str__(self):
        return name + ":\n"+str(self.grid)+"\n"+str(self.attr)