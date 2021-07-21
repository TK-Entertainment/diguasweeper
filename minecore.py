import random

class Mine:
    def __init__(self, **options):
        ratio = options.get('ratio') if (0 < options.get('ratio') <= 1) else random.randint(1, 100)/100
        self.shape = options.get('shape')
        self.size = options.get('size')
        self.ground = []
        if self.shape == 'rectangle':
            self.remain = self.size[0] * self.size[1]
            self.showground = [[-1 for j in range(self.size[1])] for i in range(self.size[0])]
            self.checklist = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
            self.minenum = round(ratio * self.size[0]*self.size[1])
        elif self.shape == 'triangle':
            self.remain = self.size[0] * (self.size[0]+1) / 2
            self.showground = [[-1 for j in range(i+1)] for i in range(self.size[0])]
            self.checklist = [[-1, -1], [-1, 0], [0, -1], [0, 1], [1, 0], [1, 1]]
            self.minenum = round(ratio * self.size[0]*(self.size[0]+1)/2)
        self.nominelist = []; self.minelist = []
        self.diff = round((ratio*10)**2)
        self.stepscount = 0
        self.steps = 0
        self.win = 'draw'
    def setground(self):
        minenumb = self.minenum
        savenum = self.remain - self.minenum
        for i in range(self.size[0]):
            self.ground.append([])
            for j in range(self.size[1] if self.shape == 'rectangle' else i+1):
                self.ground[i].extend(random.choices([0, 9], weights=[savenum, minenumb]))
                if self.ground[i][j] == 0:
                    self.nominelist.append([i, j])
                    savenum -= 1
                else:
                    self.minelist.append([i, j])
                    minenumb -= 1
    def numsetting(self):
        for [i, j] in self.nominelist:
            count = 0
            for [m ,n] in self.checklist:
                if (i+m < 0) or (i+m >= self.size[0]):
                    continue
                elif self.shape == 'rectangle' and ((j+n < 0) or (j+n >= self.size[1])):
                    continue
                elif self.shape == 'triangle' and ((j+n < 0) or (j+n > i+m)):
                    continue
                if self.ground[i+m][j+n] == 9:
                    count += 1
            self.ground[i][j] = count
    
    def flag(self, i, j):
        flags = 0
        if self.showground[i][j] == -1:
            self.showground[i][j] = -2
        elif self.showground[i][j] == -2:
            self.showground[i][j] = -1
        for i in range(self.size[0]):
            for j in range(self.size[1] if self.shape == 'rectangle' else i+1):
                if (self.showground[i][j] == -2) and (self.ground[i][j] == 9):
                    flags += 1
                    if (flags == len(self.minelist)):
                        self.win == 'win'
        if (flags == len(self.minelist)):
            self.win == 'win'
    def click0(self, i, j):
        blank = [[i, j]]
        to_open = [[i, j]]
        self.showground[i][j] = self.ground[i][j]
        count = 0
        while len(blank) > count:
            count = len(blank)
            for [i, j] in blank:
                for [m, n] in self.checklist:
                    if (i+m < 0) or (i+m >= self.size[0]):
                        continue
                    elif self.shape == 'rectangle' and ((j+n < 0) or (j+n >= self.size[1])):
                        continue
                    elif self.shape == 'triangle' and ((j+n < 0) or (j+n > i+m)):
                        continue
                    if ([i+m, j+n] not in to_open) and (self.showground[i+m][j+n] == -1):
                        self.showground[i+m][j+n] = self.ground[i+m][j+n]
                        to_open.append([i+m, j+n])
                        if (self.ground[i+m][j+n] == 0):
                            blank.append([i+m, j+n])
        self.remain -= len(to_open)
        if self.remain <= len(self.minelist):
            self.win = 'win'
            for mine in self.minelist:
                self.showground[mine[0]][mine[1]] = 9
            return to_open+self.minelist+[[i, j]]
        return to_open
    def click(self, i, j):
        if self.ground[i][j] == 0:
            return self.click0(i, j)
        else:
            self.showground[i][j] = self.ground[i][j]
            if self.ground[i][j] == 9:
                self.win = 'lose'
                for mine in self.minelist:
                    self.showground[mine[0]][mine[1]] = 9
                return self.minelist
            else:
                self.remain = self.remain - 1
                if self.remain <= len(self.minelist):
                    self.win = 'win'
                    for mine in self.minelist:
                        self.showground[mine[0]][mine[1]] = 9
                    return self.minelist+[[i, j]]
                else:
                    return [[i, j]]