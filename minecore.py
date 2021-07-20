import random

class Mine:
    def __init__(self, size, ratio, shape='rectangle'):
        ratio = ratio if (0 < ratio <= 1) else random.randint(1, 100)/100
        self.size = size
        self.remain = self.size[0] * self.size[1]
        if shape == 'rectangle':
            self.checklist = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        elif shape == 'triangle':
            self.checklist = [[-1, -1], [-1, 0], [0, -1], [0, 1], [1, 0], [1, 1]]
        self.ground = []; self.showground = [[-1 for j in range(size[1])] for i in range(size[0])]
        self.nominelist = []; self.minelist = []
        self.minenum = round(ratio * size[0]*size[1])
        self.diff = round((ratio*10)**2)
        self.stepscount = 0
        self.steps = 0
        self.win = 'draw'
    def setground(self):
        minenumb = self.minenum
        savenum = self.size[0] * self.size[1] - self.minenum
        for i in range(self.size[0]):
            self.ground.append([])
            for j in range(self.size[1]):
                self.ground[i].extend(random.choices([0, 9], weights=[savenum, minenumb]))
                if self.ground[i][j] == 0:
                    self.nominelist.append([i, j])
                    savenum -= 1
                else:
                    self.minelist.append([i, j])
                    minenumb -= 1
    def numsetting(self):
        for nomine in self.nominelist:
            count = 0
            for [i, j] in self.checklist:
                if ((nomine[0]+i < 0) or (nomine[0]+i >= self.size[0])) or ((nomine[1]+j < 0) or (nomine[1]+j >= self.size[1])):
                    continue
                if self.ground[nomine[0]+i][nomine[1]+j] == 9:
                    count += 1
            self.ground[nomine[0]][nomine[1]] = count
    
    def flag(self, i, j):
        flags = 0
        if self.showground[i][j] == -1:
            self.showground[i][j] = -2
        elif self.showground[i][j] == -2:
            self.showground[i][j] = -1
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (self.showground[i][j] == -2) and (self.ground[i][j] == 9):
                    flags += 1
                    if (flags == len(self.minelist)):
                        self.win == 'win'
        if (flags == len(self.minelist)):
            self.win == 'win'
    def click0(self, i, j):
        blank = [[i, j]]
        to_open = []
        count = 0
        while len(blank) > count:
            count = len(blank)
            for index in blank:
                i, j = index[0], index[1]
                for [m, n] in self.checklist:
                    if ((i+m < 0) or (i+m >= self.size[0])) or ((j+n < 0) or (j+n >= self.size[1])):
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