def rowComplete(grid, rowNo):
    for y in range(0, 16):
        if(grid[rowNo][y] == -1):
            return False
    return True

def colComplete(grid, colNo):
    for x in range(0, 16):
        if(grid[x][colNo] == -1):
            return False
    return True

def regComplete(grid, regx, regy):
    for x in range(4*regx, 4*regx + 4):
        for y in range(4*regy, 4*regy + 4):
            if(grid[x][y] == -1):
                return False
    return True

def testCompleteness(grid, incomplete):
    count = 0
    while(count < len(incomplete['row'])):
        if(rowComplete(grid, incomplete['row'][count])):
          incomplete['row'].pop(count)
        else:
            count += 1
    count = 0
    while(count < len(incomplete['col'])):
        if(colComplete(grid, incomplete['col'][count])):
          incomplete['col'].pop(count)
        else:
            count += 1
    count = 0
    while(count < len(incomplete['reg'])):
        if(regComplete(grid, incomplete['reg'][count][0], incomplete['reg'][count][1])):
          incomplete['reg'].pop(count)
        else:
            count += 1
            
def populateIncomplete():
    incomplete = {
        'row' : [],
        'col' : [],
        'reg' : []
        }
    for x in range(0, 16):
        incomplete['row'].append(x)
        incomplete['col'].append(x)
        incomplete['reg'].append((x % 4, x // 4))
    return incomplete
        
def isComplete(grid, incomplete):
    testCompleteness(grid, incomplete)
    if(len(incomplete['row']) == 0 and
           len(incomplete['col']) == 0 and
           len(incomplete['reg']) == 0):
        return True
    else:
        return False

def isDoable(grid, posGrid):
    for x in range(0, 16):
        for y in range(0, 16):
            if(grid[x][y] == -1 and len(posGrid[x][y]) == 0):
                return False
    return True

def rowConsistant(grid, rowNo):
    valCount = []
    for x in range (0 ,16):
        valCount.append(0)
    for y in range(0, 16):
        if(grid[rowNo][y] != -1):
            valCount[grid[rowNo][y]] += 1
            if(valCount[grid[rowNo][y]] > 1):
                return False
    return True
    

def colConsistant(grid, colNo):
    valCount = []
    for x in range (0 ,16):
        valCount.append(0)
    for x in range(0, 16):
        if(grid[x][colNo] != -1):
            valCount[grid[x][colNo]] += 1
            if(valCount[grid[x][colNo]] > 1):
                return False
    return True

def regConsistant(grid, regx, regy):
    valCount = []
    for x in range (0 ,16):
        valCount.append(0)
    for x in range(4*regx, 4*regx + 4):
        for y in range(4*regy, 4*regy + 4):
            if(grid[x][y] != -1):
                valCount[grid[x][y]] += 1
                if(valCount[grid[x][y]] > 1):
                    return False
    return True
    

def isConsistant(grid):
    for x in range(0, 16):
        if(not(rowConsistant(grid, x) and colConsistant(grid, x) and regConsistant(grid, x % 4, x // 4))):
            return False
    return True

def getRegionNo(x):
    if(x > 11):
        return 3
    elif(x > 7):
        return 2
    elif(x > 3):
        return 1
    else:
        return 0
    
def printGrid(grid):
    for r in grid:
        print(r)
        
def getInitialGrid():
    grid = []
    for x in range(0,16):
        grid.append([])
        for y in range(0,16):
            grid[x].append(-1)
    return grid

def getInitialposGrid():
    grid = []
    for x in range(0,16):
        grid.append([])
        for y in range(0,16):
            grid[x].append([])
    fillposGrid(grid)
    return grid

def removePos(posList, value):
    if(posList.count(value)>0):
        posList.remove(value)
        return True
    return False

def fillposGrid(posGrid):
    for x in range(0,16):
        for y in range (0,16):
            for z in range(0,16):
                posGrid[x][y].append(z)

def fixAfterWrite(x, y, posGrid, value):
    posGrid[x][y].clear()
    for z in range(0,16):
        removePos(posGrid[x][z], value)
        removePos(posGrid[z][y], value)
    xreg = getRegionNo(x)*4
    yreg = getRegionNo(y)*4
    for x1 in range(0,4):
        for y1 in range(0,4):
            removePos(posGrid[xreg + x1][yreg + y1], value)

def write(x, y, value, grid, posGrid):
    grid[x][y] = value
    fixAfterWrite(x, y, posGrid, value)

def FirstStep(grid, posGrid, incomplete):
    if(not(isConsistant(grid))):
        return False
    elif(not(isDoable(grid, posGrid))):
        return False
    elif(isComplete(grid, incomplete)):
        return True
    else:
        return nakedSingle(grid, posGrid, incomplete)

def nakedSingle(grid, posGrid, incomplete):
    x = 0
    same = True
    while(x < 16 and same):
        y = 0
        while(y < 16 and same):
            if(len(posGrid[x][y]) == 1):
                val = posGrid[x][y][0]
                write(x, y, val, grid, posGrid)
                print("naked single", x, y, val)
                same = False
            y += 1
        x += 1
    if(same):
        return rowExclusive(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    
def rowExclusive(grid, posGrid, incomplete):
    
    same = True
    rowMax = len(incomplete['row'])
    val = 0
    while(val < 16 and same):
        rowCount = 0
        while(rowCount < rowMax and same):
            rowNo = incomplete['row'][rowCount]
            valCount = 0
            for x in range(0,16):
                if(posGrid[rowNo][x].count(val) > 0):
                    valCount += 1
            if(valCount == 1):
                for x in range(0,16):
                    if(posGrid[rowNo][x].count(val) > 0):
                        write(rowNo, x, val, grid, posGrid)
                        print("row exclusive", rowNo, x, val)
                        same = False
                        break
            rowCount += 1
        val += 1
    if(same):
        return colExclusive(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colExclusive(grid, posGrid, incomplete):
    val = 0
    colMax = len(incomplete['col'])
    same = True
    while(val < 16 and same):
        colCount = 0
        while(colCount < colMax and same):
            colNo = incomplete['col'][colCount]
            valCount = 0
            for x in range(0,16):
                if(posGrid[x][colNo].count(val) > 0):
                    valCount += 1
            if(valCount == 1):
                for x in range(0,16):
                    if(posGrid[x][colNo].count(val) > 0):
                        write(x, colNo, val, grid, posGrid)
                        print("col exclusive", x, colNo, val)
                        same = False
                        break
            colCount += 1
        val += 1
    if(same):
        return regExclusive(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regExclusive(grid, posGrid, incomplete):
    val = 0;
    regMax = len(incomplete['reg'])
    same = True
    while(val < 16 and same):
        regCount = 0;
        while(regCount < regMax and same):
            xreg = incomplete['reg'][regCount][0] * 4
            yreg = incomplete['reg'][regCount][1] * 4
            valCount = 0
            for x in range(0,4):
                for y in range(0,4):
                    if(posGrid[xreg+x][yreg+y].count(val) > 0):
                        valCount += 1
            if(valCount == 1):
                for x in range(0,4):
                    for y in range(0,4):
                        if(posGrid[xreg+x][yreg+y].count(val) > 0):
                            write(xreg+x,yreg+y,val,grid,posGrid)
                            print("reg exclusive", xreg+x, yreg+y, val)
                            same = False
                            break
            regCount += 1
        val += 1
    if(same):
        return rowPair(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowPair(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            rowCount = 0
            while(rowCount < rowMax and same):
                rowNo = incomplete['row'][rowCount]
                canditList = []
                for y in range(0, 16):
                    cell = posGrid[rowNo][y]
                    if((len(cell) > 0) and (cell.count(val1) + cell.count(val2) == len(cell))):
                        canditList.append(y)
                if(len(canditList) == 2):
                    for y in range(0, 16):
                        if(y != canditList[0] and y != canditList[1]):
                            if(removePos(posGrid[rowNo][y], val1)):
                                if(same):
                                    same = False
                                    print("Row Pair", rowNo, val1, val2)
                            if(removePos(posGrid[rowNo][y], val2)):
                                if(same):
                                    same = False
                                    print("Row Pair", rowNo, val1, val2)
                rowCount += 1
            val2 += 1
        val1 += 1
    if(same):
        return colPair(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colPair(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            colCount = 0
            while(colCount < 16 and same):
                colNo = incomplete['col'][colCount]
                canditList = []
                for x in range(0, 16):
                    cell = posGrid[x][colNo]
                    if((len(cell) > 0) and (cell.count(val1) + cell.count(val2) == len(cell))):
                        canditList.append(x)
                if(len(canditList) == 2):
                    for x in range(0, 16):
                        if(x != canditList[0] and x != canditList[1]):
                            if(removePos(posGrid[x][colNo], val1)):
                                if(same):
                                    same = False
                                    print("Col Pair", colNo, val1, val2)
                            if(removePos(posGrid[x][colNo], val2)):
                                if(same):
                                    same = False
                                    print("Col Pair", colNo, val1, val2)
                colCount += 1
            val2 += 1
        val1 += 1
    if(same):
        return regPair(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regPair(grid, posGrid, incomplete):
    val1 = 0
    regMax = len(incomplete['reg'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            regCount = 0
            while(regCount < regMax and same):
                xreg = incomplete['reg'][regCount][0] * 4
                yreg = incomplete['reg'][regCount][1] * 4
                canditList = []
                for x in range(0, 4):
                    for y in range(0, 4):
                        cell = posGrid[xreg + x][yreg + y]
                        if(len(cell)>0 and cell.count(val1) + cell.count(val2) == len(cell)):
                            canditList
                if(len(canditList) == 2):
                    for x in range(0,4):
                        for y in range(0, 4):
                            if(not((x == canditList[0][0] and y == canditList[0][1]) or (x == canditList[1][0] and y == canditList[1][1]))):
                                if(removePos(posGrid[x + xreg][y + yreg], val1)):
                                    if(same):
                                        same = False
                                        print("Reg Pair", xreg, yreg, val1, val2)
                                if(removePos(posGrid[x + xreg][y + yreg], val2)):
                                    if(same):
                                        same = False
                                        print("Reg Pair", xreg, yreg, val1, val2)
                regCount += 1
            val2 += 1
        val1 += 1
    if(same):
        return rowTripple(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowTripple(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                rowCount = 0
                while(rowCount < rowMax and same):
                    rowNo = incomplete['row'][rowCount]
                    canditList = []
                    for y in range(0, 16):
                        cell = posGrid[rowNo][y]
                        if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) == len(cell)):
                            canditList.append(y)
                    if(len(canditList) == 3):
                        for y in range(0, 16):
                            if(y != canditList[0] and y != canditList[1] and y != canditList[2]):
                                zlen = len(posGrid[rowNo][y])
                                removePos(posGrid[rowNo][y], val1)
                                removePos(posGrid[rowNo][y], val2)
                                removePos(posGrid[rowNo][y], val3)
                                if(len(posGrid[rowNo][y]) < zlen):
                                    if(same):
                                        same = False
                                        print("Row Tripple", rowNo, val1, val2, val3)
                    rowCount += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return colTripple(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
        
def colTripple(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                colCount = 0
                while(colCount < colMax and same):
                    colNo = incomplete['col'][colCount]
                    canditList = []
                    for x in range(0, 16):
                        cell = posGrid[x][colNo]
                        if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) == len(cell)):
                            canditList.append(x)
                    if(len(canditList) == 3):
                        for x in range(0, 16):
                            if(x != canditList[0] and x != canditList[1] and x != canditList[2]):
                                zlen = len(posGrid[x][colNo])
                                removePos(posGrid[x][colNo], val1)
                                removePos(posGrid[x][colNo], val2)
                                removePos(posGrid[x][colNo], val3)
                                if(len(posGrid[x][colNo]) < zlen):
                                    if(same):
                                        same = False
                                        print("Col Tripple", colNo, val1, val2, val3) 
                    colCount += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return regTripple(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regTripple(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                regCount = 0
                while(regCount < regMax and same):
                    xreg = incomplete['reg'][regCount][0] * 4
                    yreg = incomplete['reg'][regCount][1] * 4
                    canditList = []
                    for x in range(0, 4):
                        for y in range(0, 4):
                            cell = posGrid[xreg + x][yreg + y]
                            if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) == len(cell)):
                                canditList.append((x,y))
                    if(len(canditList) == 3):
                        for x in range(0,4):
                            for y in range(0, 4):
                                if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                       (x == canditList[1][0] and y == canditList[1][1]) or
                                       (x==canditList[2][0] and y == canditList[2][1]))):
                                    zlen = len(posGrid[x + xreg][y + yreg])
                                    removePos(posGrid[x + xreg][y + yreg], val1)
                                    removePos(posGrid[x + xreg][y + yreg], val2)
                                    removePos(posGrid[x + xreg][y + yreg], val3)
                                    if(zlen < len(posGrid[x + xreg][y + yreg])):
                                        if(same):
                                            same = False
                                            print("Reg Tripple", xreg, yreg, val1, val2, val3)
                    regCount += 1
                val3 += 1
            val2 += 1
        val1 += 1
        
    if(same):
        return doubleRowExclusion(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def doubleRowExclusion(grid, posGrid, incomplete):
    same = True
    val1 = 0
    while(val1 < 0 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            rowNo = 0
            while(rowNo < 16 and same):
                valCount = 0
                for y in range (0, 16):
                    if(possiblities[rowNo][y].count(val1) > 0 or possiblities[rowNo][y].count(val2) > 0):
                        valCount += 1
                if(valCount == 2):
                    for y in range(0,16):
                        if(possiblities[rowNo][y].count(val1) > 0 and possiblities[rowNo][y].count(val2) > 0):
                            if(len(possiblities[rowNo][y])>2):
                                same = False
                                print("double row exclusion", rowNo, val1, val2)
                                possiblities[rowNo][y].clear()
                                possiblities[rowNo][y].append(val1)
                                possiblities[rowNo][y].append(val2)
                rowNo += 1
            val2 += 1
        val1 += 1

    if(same):
        return doubleColExclusion(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def doubleColExclusion(grid, posGrid, incomplete):
    same = True
    val1 = 0
    while(val1 < 0 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            colNo = 0
            while(colNo < 16 and same):
                valCount = 0
                for x in range (0, 16):
                    if(possiblities[x][colNo].count(val1) > 0 or possiblities[x][colNo].count(val2) > 0):
                        valCount += 1
                if(valCount == 2):
                    for x in range(0,16):
                        if(possiblities[x][colNo].count(val1) > 0 and possiblities[x][colNo].count(val2) > 0):
                            if(len(possiblities[x][colNo])>2):
                                same = False
                                print("double col exclusion", colNo, val1, val2)
                                possiblities[x][colNo].clear()
                                possiblities[x][colNo].append(val1)
                                possiblities[x][colNo].append(val2)

                colNo += 1
            val2 += 1
        val1 += 1

    if(same):
        return doubleRegExclusion(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def doubleRegExclusion(grid, posGrid, incomplete):
    same = True
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            xreg = 0
            while(xreg < 16 and same):
                yreg = 0
                while(yreg < 16 and same):
                    valCount = 0
                    for x in range(0, 4):
                        for y in range(0, 4):
                            if(posGrid[xreg + x][yreg + y].count(val1) > 0 or posGrid[xreg + x][yreg + y].count(val2) > 0):
                                valCount += 1
                    if(valCount == 2):
                        for x in range(0,4):
                            for y in range(0,4):
                                if(posGrid[xreg + x][yreg + y].count(val1) > 0 and posGrid[xreg + x][yreg + y].count(val2) > 0):
                                    if(len(posGrid[xreg + x][yreg + y]) > 2):
                                        same = False
                                        print("double reg exclusion", xreg, yreg, val1, val2)
                                        posGrid[x + xreg][y + yreg].clear()
                                        posGrid[x + xreg][y + yreg].append(val1)
                                        posGrid[x + xreg][y + yreg].append(val2)
                    yreg += 4
                xreg += 4
            val2 += 1
        val1 += 1
    if(same):
        return xWingVer(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    
def xWingVer(grid, posGrid, incomplete):
    same = True
    val = 0
    while (val < 16 and same):
        locList = []
        for x in range(0, 16):
            locList.append([])
            for y in range(0, 16):
                if(posGrid[x][y].count(val)>0):
                    locList[x].append(y)
        for x1 in range(0, 16):
            if(len(locList[x1]) == 2):
                pos1 = locList[x1][0]
                pos2 = locList[x1][1]
                for x2 in range(x1 + 1, 16):
                    if(len(locList[x2]) == 2 and pos1 == locList[x2][0] and pos2 == locList[x2][1]):
                        for x3 in range(0, 16):
                            if(x3 != x1 and x3 != x2):
                                if(posGrid[x3][pos1].count(val)>0 or posGrid[x3][pos2].count(val)>0):
                                    removePos(posGrid[x3][pos1], val)
                                    removePos(posGrid[x3][pos2], val)
                                    if(same):
                                        same = False
                                        print("X-Wing Ver", x1, pos1, x2, pos2)
        val += 1
        
    if(same):
        return xWingHor(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def xWingHor(grid, posGrid, incomplete):
    same = True
    val = 0
    while (val < 16 and same):
        locList = []
        for y in range(0, 16):
            locList.append([])
            for x in range(0, 16):
                if(posGrid[x][y].count(val)>0):
                    locList[y].append(x)
        for y1 in range(0, 16):
            if(len(locList[y1]) == 2):
                pos1 = locList[y1][0]
                pos2 = locList[y1][1]
                for y2 in range(y1 + 1, 16):
                    if(len(locList[y2]) == 2 and pos1 == locList[y2][0] and pos2 == locList[y2][1]):
                        for y3 in range(0, 16):
                            if(y3 != y1 and y3 != y2):
                                if(posGrid[pos1][y3].count(val)>0 or posGrid[pos2][y3].count(val)>0):
                                    removePos(posGrid[pos1][y3], val)
                                    removePos(posGrid[pos2][y3], val)
                                    if(same):
                                        same = False
                                        print("X-Wing Hor", pos1, y1, pos2, y2)
        val += 1
        
    if(same):
        return rowQuad(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowQuad(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    rowCount = 0
                    while(rowCount < rowMax and same):
                        rowNo = incomplete['row'][rowCount]
                        canditList = []
                        for y in range(0, 16):
                            cell = posGrid[rowNo][y]
                            if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) == len(cell)):
                                canditList.append(y)
                        if(len(canditList) == 4):
                            for y in range(0, 16):
                                if(y != canditList[0] and y != canditList[1] and y != canditList[2] and y != canditList[3]):
                                    zlen = len(posGrid[rowNo][y])
                                    removePos(posGrid[rowNo][y], val1)
                                    removePos(posGrid[rowNo][y], val2)
                                    removePos(posGrid[rowNo][y], val3)
                                    removePos(posGrid[rowNo][y], val4)
                                    if(len(posGrid[rowNo][y]) < zlen):
                                        if(same):
                                            same = False
                                            print("Row Quad", rowNo, val1, val2, val3, val4)
                        rowCount += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
        
    if(same):
        return colQuad(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colQuad(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    colCount = 0
                    while(colCount < colMax and same):
                        colNo = incomplete['col'][colCount]
                        canditList = []
                        for x in range(0, 16):
                            cell = posGrid[x][colNo]
                            if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) == len(cell)):
                                canditList.append(x)
                        if(len(canditList) == 4):
                            for x in range(0, 16):
                                if(x != canditList[0] and x != canditList[1] and x != canditList[2] and x != canditList[3]):
                                    zlen = len(posGrid[x][colNo])
                                    removePos(posGrid[x][colNo], val1)
                                    removePos(posGrid[x][colNo], val2)
                                    removePos(posGrid[x][colNo], val3)
                                    removePos(posGrid[x][colNo], val4)
                                    if(len(posGrid[x][colNo]) < zlen):
                                        if(same):
                                            same = False
                                            print("Col Quad", colNo, val1, val2, val3, val4) 
                        colCount += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
        
    if(same):
        return regQuad(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regQuad(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    regCount = 0
                    while(regCount < regMax and same):
                        xreg = incomplete['reg'][regCount][0] * 4
                        yreg = incomplete['reg'][regCount][1] * 4
                        canditList = []
                        for x in range(0, 4):
                            for y in range(0, 4):
                                cell = posGrid[xreg + x][yreg + y]
                                if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) == len(cell)):
                                    canditList.append((x,y))
                        if(len(canditList) == 4):
                            for x in range(0,4):
                                for y in range(0, 4):
                                    if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                           (x == canditList[1][0] and y == canditList[1][1]) or
                                           (x == canditList[2][0] and y == canditList[2][1]) or
                                           (x == canditList[3][0] and y == canditList[3][1]))):
                                        zlen = len(posGrid[x + xreg][y + yreg])
                                        removePos(posGrid[x + xreg][y + yreg], val1)
                                        removePos(posGrid[x + xreg][y + yreg], val2)
                                        removePos(posGrid[x + xreg][y + yreg], val3)
                                        removePos(posGrid[x + xreg][y + yreg], val4)
                                        if(zlen < len(posGrid[x + xreg][y + yreg])):
                                            if(same):
                                                same = False
                                                print("Reg Quad", xreg, yreg, val1, val2, val3, val4)
                        regCount += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
    
    if(same):
        return swordfishVert(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def swordfishVert(grid, posGrid, incomplete):
    same = True
    val = 0
    while (val < 16 and same):
        locList = []
        for x in range(0, 16):
            locList.append([])
            for y in range(0, 16):
                if(posGrid[x][y].count(val)>0):
                    locList[x].append(y)
        for x1 in range(0, 16):
            if(len(locList[x1]) == 2):
                pos1 = locList[x1][0]
                pos2 = locList[x1][1]
                for x2 in range(x1 + 1, 16):
                    if(len(locList[x2]) == 2):
                        pos3 = -1
                        if((pos1 == locList[x2][0] and pos2 != locList[x2][1]) or (pos2 == locList[x2][0] and pos1 != locList[x2][1])):
                            pos3 = locList[x2][1]
                        elif((pos1 != locList[x2][0] and pos2 == locList[x2][1]) or (pos2 != locList[x2][0] and pos1 == locList[x2][1])):
                            pos3 = locList[x2][0]
                        if(pos3 != -1):
                            for x3 in range (x2 + 1, 16):
                                if(len(locList[x3]) == 2 and (pos1 == locList[x3][0] or pos2 == locList[x3][0] or pos3 == locList[x3][0]) and (pos1 == locList[x3][1] or pos2 == locList[x3][1] or pos3 == locList[x3][1])):
                                    for x4 in range(0, 16):
                                        if(x4 != x1 and x4 != x2 and x4 != x3):
                                            if(posGrid[x4][pos1].count(val)>0 or posGrid[x4][pos2].count(val)>0 or posGrid[x4][pos3].count(val)>0):
                                                removePos(posGrid[x4][pos1], val)
                                                removePos(posGrid[x4][pos2], val)
                                                removePos(posGrid[x4][pos3], val)
                                            if(same):
                                                same = False
                                                print("Swordfish Ver", x1, pos1, x2, pos2, x3, pos3)
        val += 1
    
    if(same):
        return swordfishHor(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    

def swordfishHor(grid, posGrid, incomplete):
    same = True
    val = 0
    while (val < 16 and same):
        locList = []
        for y in range(0, 16):
            locList.append([])
            for x in range(0, 16):
                if(posGrid[x][y].count(val)>0):
                    locList[y].append(x)
        for y1 in range(0, 16):
            if(len(locList[y1]) == 2):
                pos1 = locList[y1][0]
                pos2 = locList[y1][1]
                for y2 in range(y1 + 1, 16):
                    if(len(locList[y2]) == 2):
                        pos3 = -1
                        if((pos1 == locList[y2][0] and pos2 != locList[y2][1]) or (pos2 == locList[y2][0] and pos1 != locList[y2][1])):
                            pos3 = locList[y2][1]
                        elif((pos1 != locList[y2][0] and pos2 == locList[y2][1]) or (pos2 != locList[y2][0] and pos1 == locList[y2][1])):
                            pos3 = locList[y2][0]
                        if(pos3 != -1):
                            for y3 in range (y2 + 1, 16):
                                if(len(locList[y3]) == 2 and (pos1 == locList[y3][0] or pos2 == locList[y3][0] or pos3 == locList[y3][0]) and (pos1 == locList[y3][1] or pos2 == locList[y3][1] or pos3 == locList[y3][1])):
                                    for y4 in range(0, 16):
                                        if(y4 != y1 and y4 != y2 and y4 != y3):
                                            if(posGrid[pos1][y4].count(val)>0 or posGrid[pos2][y4].count(val)>0 or posGrid[pos3][y4].count(val)>0):
                                                removePos(posGrid[pos1][y4], val)
                                                removePos(posGrid[pos2][y4], val)
                                                removePos(posGrid[pos3][y4], val)
                                            if(same):
                                                same = False
                                                print("Swordfish Hor", y1, pos1, y2, pos2, y3, pos3)
        val += 1
    
    if(same):
        return geniusExclusive11(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def geniusExclusive11(grid, posGrid, incomplete):
    same = True
    region1coor = []
    region2coor = []
    for x in range(0, 3):
        for y in range(0, 3):
            region1coor.append((x, y))
            region1coor.append((x + 13, y))
            region1coor.append((x, y + 13))
            region1coor.append((x + 13, y + 13))
    
    for x in range(3, 12):
        region2coor.append((x, 3))
        region2coor.append((12, x))
        region2coor.append((x + 1, 12))
        region2coor.append((3, x + 1))

    regionVal = []
    for x in range(0, 16):
        regionVal.append(0)
    for x in range(0,36):
        if(grid[region1coor[x][0]][region1coor[x][1]] != -1):
            regionVal[grid[region1coor[x][0]][region1coor[x][1]]] += 1
        if(grid[region2coor[x][0]][region2coor[x][1]] != -1):
            regionVal[grid[region2coor[x][0]][region2coor[x][1]]] -= 1

    for x in range(0, 16):
        if(regionVal[x] > 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                   regionCount += 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick1", x)
                for y in range(0,36):
                    if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                       write(region2coor[y][0], region2coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
                           
        elif(regionVal[x] < 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                   regionCount -= 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick1", x)
                for y in range(0,36):
                    if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                       write(region1coor[y][0], region1coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
    
    if(same):
        return geniusExclusive12(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def geniusExclusive12(grid, posGrid, incomplete):
    same = True
    region1coor = []
    region2coor = []

    region1coor.append((4 ,4))
    region1coor.append((4 ,11))
    region1coor.append((11 ,4))
    region1coor.append((11 ,11))
    for x in range(0, 4):
        region1coor.append((x, 4))
        region1coor.append((4, x))
        region1coor.append((x + 12, 4))
        region1coor.append((11, x))

        region1coor.append((x, 11))
        region1coor.append((4, x + 12))
        region1coor.append((x + 12, 11))
        region1coor.append((11, x + 12))
        
    
    for x in range(5, 11):
        for y in range(5, 11):
            region2coor.append((x, y))

    regionVal = []
    for x in range(0, 16):
        regionVal.append(0)
    for x in range(0,36):
        if(grid[region1coor[x][0]][region1coor[x][1]] != -1):
            regionVal[grid[region1coor[x][0]][region1coor[x][1]]] += 1
        if(grid[region2coor[x][0]][region2coor[x][1]] != -1):
            regionVal[grid[region2coor[x][0]][region2coor[x][1]]] -= 1

    for x in range(0, 16):
        if(regionVal[x] > 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                   regionCount += 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick3", x)
                for y in range(0,36):
                    if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                       write(region2coor[y][0], region2coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
                           
        elif(regionVal[x] < 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                   regionCount -= 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick3", x)
                for y in range(0,36):
                    if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                       write(region1coor[y][0], region1coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
    
    if(same):
        return geniusExclusive21(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def geniusExclusive21(grid, posGrid, incomplete):
    same = True
    region1coor = []
    region2coor = []
    for x in range(1, 4):
        for y in range(1, 4):
            region1coor.append((x, y))
            region1coor.append((x + 11, y))
            region1coor.append((x, y + 11))
            region1coor.append((x + 11, y + 11))
    region2coor.append((0, 0))
    region2coor.append((0, 15))
    region2coor.append((15, 0))
    region2coor.append((15, 15))
    for x in range(4, 12):
        region2coor.append((x, 0))
        region2coor.append((0, x))
        region2coor.append((x, 15))
        region2coor.append((15, x))

    regionVal = []
    for x in range(0, 16):
        regionVal.append(0)
    for x in range(0,36):
        if(grid[region1coor[x][0]][region1coor[x][1]] != -1):
            regionVal[grid[region1coor[x][0]][region1coor[x][1]]] += 1
        if(grid[region2coor[x][0]][region2coor[x][1]] != -1):
            regionVal[grid[region2coor[x][0]][region2coor[x][1]]] -= 1

    for x in range(0, 16):
        if(regionVal[x] > 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                   regionCount += 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick2", x)
                for y in range(0,36):
                    if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                       write(region2coor[y][0], region2coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
                           
        elif(regionVal[x] < 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                   regionCount -= 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick2", x)
                for y in range(0,36):
                    if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                       write(region1coor[y][0], region1coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
    
    if(same):
        return geniusExclusive22(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def geniusExclusive22(grid, posGrid, incomplete):
    same = True
    region1coor = []
    region2coor = []

    region1coor.append((7 ,7))
    region1coor.append((7 ,8))
    region1coor.append((8 ,7))
    region1coor.append((8 ,8))
    for x in range(0, 4):
        region1coor.append((x, 7))
        region1coor.append((7, x))
        region1coor.append((x + 12, 7))
        region1coor.append((8, x))

        region1coor.append((x, 8))
        region1coor.append((7, x + 12))
        region1coor.append((x + 12, 8))
        region1coor.append((8, x + 12))
        
    
    for x in range(5, 11):
        for y in range(5, 11):
            region2coor.append((x, y))

    regionVal = []
    for x in range(0, 16):
        regionVal.append(0)
    for x in range(0,36):
        if(grid[region1coor[x][0]][region1coor[x][1]] != -1):
            regionVal[grid[region1coor[x][0]][region1coor[x][1]]] += 1
        if(grid[region2coor[x][0]][region2coor[x][1]] != -1):
            regionVal[grid[region2coor[x][0]][region2coor[x][1]]] -= 1

    for x in range(0, 16):
        if(regionVal[x] > 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                   regionCount += 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick3", x)
                for y in range(0,36):
                    if(posGrid[region2coor[y][0]][region2coor[y][1]].count(x) > 0):
                       write(region2coor[y][0], region2coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
                           
        elif(regionVal[x] < 0):
            regionCount = 0
            for y in range(0,36):
                if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                   regionCount -= 1
            if(regionCount == regionVal[x]):
                print("PhistomaphelTrick3", x)
                for y in range(0,36):
                    if(posGrid[region1coor[y][0]][region1coor[y][1]].count(x) > 0):
                       write(region1coor[y][0], region1coor[y][1], x, grid, posGrid)
                       if(same):
                           same = False
    
    if(same):
        return rowPenta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowPenta(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        rowCount = 0
                        while(rowCount < rowMax and same):
                            rowNo = incomplete['row'][rowCount]
                            canditList = []
                            for y in range(0, 16):
                                cell = posGrid[rowNo][y]
                                if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) == len(cell)):
                                    canditList.append(y)
                            if(len(canditList) == 5):
                                for y in range(0, 16):
                                    if(y != canditList[0] and y != canditList[1] and y != canditList[2] and y != canditList[3] and y != canditList[4]):
                                        zlen = len(posGrid[rowNo][y])
                                        removePos(posGrid[rowNo][y], val1)
                                        removePos(posGrid[rowNo][y], val2)
                                        removePos(posGrid[rowNo][y], val3)
                                        removePos(posGrid[rowNo][y], val4)
                                        removePos(posGrid[rowNo][y], val5)
                                        if(len(posGrid[rowNo][y]) < zlen):
                                            if(same):
                                                same = False
                                                print("Row Penta", rowNo, val1, val2, val3, val4, val5)
                            rowCount += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
    
    if(same):
        return colPenta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colPenta(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        colCount = 0
                        while(colCount < colMax and same):
                            colNo = incomplete['col'][colCount]
                            canditList = []
                            for x in range(0, 16):
                                cell = posGrid[x][colNo]
                                if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) == len(cell)):
                                    canditList.append(x)
                            if(len(canditList) == 5):
                                for x in range(0, 16):
                                    if(x != canditList[0] and x != canditList[1] and x != canditList[2] and x != canditList[3] and x != canditList[4]):
                                        zlen = len(posGrid[x][colNo])
                                        removePos(posGrid[x][colNo], val1)
                                        removePos(posGrid[x][colNo], val2)
                                        removePos(posGrid[x][colNo], val3)
                                        removePos(posGrid[x][colNo], val4)
                                        removePos(posGrid[x][colNo], val5)
                                        if(len(posGrid[x][colNo]) < zlen):
                                            if(same):
                                                same = False
                                                print("Col Penta", colNo, val1, val2, val3, val4, val5) 
                            colCount += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
    
    if(same):
        return regPenta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regPenta(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        regCount = 0
                        while(regCount < regMax and same):
                            xreg = incomplete['reg'][regCount][0] * 4
                            yreg = incomplete['reg'][regCount][1] * 4
                            canditList = []
                            for x in range(0, 4):
                                for y in range(0, 4):
                                    cell = posGrid[xreg + x][yreg + y]
                                    if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) == len(cell)):
                                        canditList.append((x,y))
                            if(len(canditList) == 5):
                                for x in range(0,4):
                                    for y in range(0, 4):
                                        if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                               (x == canditList[1][0] and y == canditList[1][1]) or
                                               (x == canditList[2][0] and y == canditList[2][1]) or
                                               (x == canditList[3][0] and y == canditList[3][1]) or
                                               (x == canditList[4][0] and y == canditList[4][1]))):
                                            zlen = len(posGrid[x + xreg][y + yreg])
                                            removePos(posGrid[x + xreg][y + yreg], val1)
                                            removePos(posGrid[x + xreg][y + yreg], val2)
                                            removePos(posGrid[x + xreg][y + yreg], val3)
                                            removePos(posGrid[x + xreg][y + yreg], val4)
                                            removePos(posGrid[x + xreg][y + yreg], val5)
                                            if(zlen < len(posGrid[x + xreg][y + yreg])):
                                                if(same):
                                                    same = False
                                                    print("Reg Penta", xreg, yreg, val1, val2, val3, val4, val5)
                            regCount += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1
    if(same):
        return rowHexa(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowHexa(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            rowCount = 0
                            while(rowCount < rowMax and same):
                                rowNo = incomplete['row'][rowCount]
                                canditList = []
                                for y in range(0, 16):
                                    cell = posGrid[rowNo][y]
                                    if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) == len(cell)):
                                        canditList.append(y)
                                if(len(canditList) == 6):
                                    for y in range(0, 16):
                                        if(y != canditList[0] and y != canditList[1] and y != canditList[2] and y != canditList[3] and y != canditList[4] and y != canditList[5]):
                                            zlen = len(posGrid[rowNo][y])
                                            removePos(posGrid[rowNo][y], val1)
                                            removePos(posGrid[rowNo][y], val2)
                                            removePos(posGrid[rowNo][y], val3)
                                            removePos(posGrid[rowNo][y], val4)
                                            removePos(posGrid[rowNo][y], val5)
                                            removePos(posGrid[rowNo][y], val6)
                                            if(len(posGrid[rowNo][y]) < zlen):
                                                if(same):
                                                    same = False
                                                    print("Row Hexa", rowNo, val1, val2, val3, val4, val5, val6)
                                rowCount += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return colHexa(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    
def colHexa(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            colCount = 0
                            while(colCount < colMax and same):
                                colNo = incomplete['col'][colCount]
                                canditList = []
                                for x in range(0, 16):
                                    cell = posGrid[x][colNo]
                                    if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) == len(cell)):
                                        canditList.append(x)
                                if(len(canditList) == 6):
                                    for x in range(0, 16):
                                        if(x != canditList[0] and x != canditList[1] and x != canditList[2] and x != canditList[3] and x != canditList[4] and x != canditList[5]):
                                            zlen = len(posGrid[x][colNo])
                                            removePos(posGrid[x][colNo], val1)
                                            removePos(posGrid[x][colNo], val2)
                                            removePos(posGrid[x][colNo], val3)
                                            removePos(posGrid[x][colNo], val4)
                                            removePos(posGrid[x][colNo], val5)
                                            removePos(posGrid[x][colNo], val6)
                                            if(len(posGrid[x][colNo]) < zlen):
                                                if(same):
                                                    same = False
                                                    print("Col Hexa", colNo, val1, val2, val3, val4, val5, val6) 
                                colCount += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return regHexa(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    
def regHexa(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            regCount = 0
                            while(regCount < regMax and same):
                                xreg = incomplete['reg'][regCount][0] * 4
                                yreg = incomplete['reg'][regCount][1] * 4
                                canditList = []
                                for x in range(0, 4):
                                    for y in range(0, 4):
                                        cell = posGrid[xreg + x][yreg + y]
                                        if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) == len(cell)):
                                            canditList.append((x,y))
                                if(len(canditList) == 6):
                                    for x in range(0,4):
                                        for y in range(0, 4):
                                            if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                                   (x == canditList[1][0] and y == canditList[1][1]) or
                                                   (x == canditList[2][0] and y == canditList[2][1]) or
                                                   (x == canditList[3][0] and y == canditList[3][1]) or
                                                   (x == canditList[4][0] and y == canditList[4][1]) or
                                                   (x == canditList[5][0] and y == canditList[5][1]))):
                                                zlen = len(posGrid[x + xreg][y + yreg])
                                                removePos(posGrid[x + xreg][y + yreg], val1)
                                                removePos(posGrid[x + xreg][y + yreg], val2)
                                                removePos(posGrid[x + xreg][y + yreg], val3)
                                                removePos(posGrid[x + xreg][y + yreg], val4)
                                                removePos(posGrid[x + xreg][y + yreg], val5)
                                                removePos(posGrid[x + xreg][y + yreg], val6)
                                                if(zlen < len(posGrid[x + xreg][y + yreg])):
                                                    if(same):
                                                        same = False
                                                        print("Reg Hexa", xreg, yreg, val1, val2, val3, val4, val5, val6)
                                regCount += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return rowSepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)
    
def rowSepta(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                rowCount = 0
                                while(rowCount < rowMax and same):
                                    rowNo = incomplete['row'][rowCount]
                                    canditList = []
                                    for y in range(0, 16):
                                        cell = posGrid[rowNo][y]
                                        if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) == len(cell)):
                                            canditList.append(y)
                                    if(len(canditList) == 7):
                                        for y in range(0, 16):
                                            if(y != canditList[0] and y != canditList[1] and y != canditList[2] and y != canditList[3] and y != canditList[4] and y != canditList[5] and y != canditList[6]):
                                                zlen = len(posGrid[rowNo][y])
                                                removePos(posGrid[rowNo][y], val1)
                                                removePos(posGrid[rowNo][y], val2)
                                                removePos(posGrid[rowNo][y], val3)
                                                removePos(posGrid[rowNo][y], val4)
                                                removePos(posGrid[rowNo][y], val5)
                                                removePos(posGrid[rowNo][y], val6)
                                                removePos(posGrid[rowNo][y], val7)
                                                if(len(posGrid[rowNo][y]) < zlen):
                                                    if(same):
                                                        same = False
                                                        print("Row Septa", rowNo, val1, val2, val3, val4, val5, val6, val7)
                                    rowCount += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return colSepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colSepta(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                colCount = 0
                                while(colCount < colMax and same):
                                    colNo = incomplete['col'][colCount]
                                    canditList = []
                                    for x in range(0, 16):
                                        cell = posGrid[x][colNo]
                                        if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) == len(cell)):
                                            canditList.append(x)
                                    if(len(canditList) == 7):
                                        for x in range(0, 16):
                                            if(x != canditList[0] and x != canditList[1] and x != canditList[2] and x != canditList[3] and x != canditList[4] and x != canditList[5] and x != canditList[6]):
                                                zlen = len(posGrid[x][colNo])
                                                removePos(posGrid[x][colNo], val1)
                                                removePos(posGrid[x][colNo], val2)
                                                removePos(posGrid[x][colNo], val3)
                                                removePos(posGrid[x][colNo], val4)
                                                removePos(posGrid[x][colNo], val5)
                                                removePos(posGrid[x][colNo], val6)
                                                removePos(posGrid[x][colNo], val7)
                                                if(len(posGrid[x][colNo]) < zlen):
                                                    if(same):
                                                        same = False
                                                        print("Col Septa", colNo, val1, val2, val3, val4, val5, val6, val7) 
                                    colCount += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return regSepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regSepta(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                regCount = 0
                                while(regCount < regMax and same):
                                    xreg = incomplete['reg'][regCount][0] * 4
                                    yreg = incomplete['reg'][regCount][1] * 4
                                    canditList = []
                                    for x in range(0, 4):
                                        for y in range(0, 4):
                                            cell = posGrid[xreg + x][yreg + y]
                                            if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) == len(cell)):
                                                canditList.append((x,y))
                                    if(len(canditList) == 7):
                                        for x in range(0,4):
                                            for y in range(0, 4):
                                                if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                                       (x == canditList[1][0] and y == canditList[1][1]) or
                                                       (x == canditList[2][0] and y == canditList[2][1]) or
                                                       (x == canditList[3][0] and y == canditList[3][1]) or
                                                       (x == canditList[4][0] and y == canditList[4][1]) or
                                                       (x == canditList[5][0] and y == canditList[5][1]) or
                                                       (x == canditList[6][0] and y == canditList[6][1]))):
                                                    zlen = len(posGrid[x + xreg][y + yreg])
                                                    removePos(posGrid[x + xreg][y + yreg], val1)
                                                    removePos(posGrid[x + xreg][y + yreg], val2)
                                                    removePos(posGrid[x + xreg][y + yreg], val3)
                                                    removePos(posGrid[x + xreg][y + yreg], val4)
                                                    removePos(posGrid[x + xreg][y + yreg], val5)
                                                    removePos(posGrid[x + xreg][y + yreg], val6)
                                                    removePos(posGrid[x + xreg][y + yreg], val7)
                                                    if(zlen < len(posGrid[x + xreg][y + yreg])):
                                                        if(same):
                                                            same = False
                                                            print("Reg Septa", xreg, yreg, val1, val2, val3, val4, val5, val6, val7)
                                    regCount += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return rowHepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def rowHepta(grid, posGrid, incomplete):
    val1 = 0
    rowMax = len(incomplete['row'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                val8 = val7 + 1
                                while(val8 < 16 and same):
                                    rowCount = 0
                                    while(rowCount < rowMax and same):
                                        rowNo = incomplete['row'][rowCount]
                                        canditList = []
                                        for y in range(0, 16):
                                            cell = posGrid[rowNo][y]
                                            if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) + cell.count(val8) == len(cell)):
                                                canditList.append(y)
                                        if(len(canditList) == 8):
                                            for y in range(0, 16):
                                                if(y != canditList[0] and y != canditList[1] and y != canditList[2] and y != canditList[3] and y != canditList[4] and y != canditList[5] and y != canditList[6] and y != canditList[7]):
                                                    zlen = len(posGrid[rowNo][y])
                                                    removePos(posGrid[rowNo][y], val1)
                                                    removePos(posGrid[rowNo][y], val2)
                                                    removePos(posGrid[rowNo][y], val3)
                                                    removePos(posGrid[rowNo][y], val4)
                                                    removePos(posGrid[rowNo][y], val5)
                                                    removePos(posGrid[rowNo][y], val6)
                                                    removePos(posGrid[rowNo][y], val7)
                                                    removePos(posGrid[rowNo][y], val8)
                                                    if(len(posGrid[rowNo][y]) < zlen):
                                                        if(same):
                                                            same = False
                                                            print("Row Hepta", rowNo, val1, val2, val3, val4, val5, val6, val7, val8)
                                        rowCount += 1
                                    val8 += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return colHepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def colHepta(grid, posGrid, incomplete):
    val1 = 0
    colMax = len(incomplete['col'])
    same = True
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                val8 = val7 + 1
                                while(val8 < 16 and same):
                                    colCount = 0
                                    while(colCount < colMax and same):
                                        colNo = incomplete['col'][colCount]
                                        canditList = []
                                        for x in range(0, 16):
                                            cell = posGrid[x][colNo]
                                            if(len(cell) > 0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) + cell.count(val8) == len(cell)):
                                                canditList.append(x)
                                        if(len(canditList) == 8):
                                            for x in range(0, 16):
                                                if(x != canditList[0] and x != canditList[1] and x != canditList[2] and x != canditList[3] and x != canditList[4] and x != canditList[5] and x != canditList[6] and x != canditList[7]):
                                                    zlen = len(posGrid[x][colNo])
                                                    removePos(posGrid[x][colNo], val1)
                                                    removePos(posGrid[x][colNo], val2)
                                                    removePos(posGrid[x][colNo], val3)
                                                    removePos(posGrid[x][colNo], val4)
                                                    removePos(posGrid[x][colNo], val5)
                                                    removePos(posGrid[x][colNo], val6)
                                                    removePos(posGrid[x][colNo], val7)
                                                    removePos(posGrid[x][colNo], val8)
                                                    if(len(posGrid[x][colNo]) < zlen):
                                                        if(same):
                                                            same = False
                                                            print("Col Hepta", colNo, val1, val2, val3, val4, val5, val6, val7, val8) 
                                        colCount += 1
                                    val8 += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return regHepta(grid, posGrid, incomplete)
    else:
        return FirstStep(grid, posGrid, incomplete)

def regHepta(grid, posGrid, incomplete):
    same = True
    regMax = len(incomplete['reg'])
    val1 = 0
    while(val1 < 16 and same):
        val2 = val1 + 1
        while(val2 < 16 and same):
            val3 = val2 + 1
            while(val3 < 16 and same):
                val4 = val3 + 1
                while(val4 < 16 and same):
                    val5 = val4 + 1
                    while(val5 < 16 and same):
                        val6 = val5 + 1
                        while(val6 < 16 and same):
                            val7 = val6 + 1
                            while(val7 < 16 and same):
                                val8 = val7 + 1
                                while(val8 < 16 and same):
                                    regCount = 0
                                    while(regCount < regMax and same):
                                        xreg = incomplete['reg'][regCount][0] * 4
                                        yreg = incomplete['reg'][regCount][1] * 4
                                        canditList = []
                                        for x in range(0, 4):
                                            for y in range(0, 4):
                                                cell = posGrid[xreg + x][yreg + y]
                                                if(len(cell)>0 and cell.count(val1) + cell.count(val2) + cell.count(val3) + cell.count(val4) + cell.count(val5) + cell.count(val6) + cell.count(val7) + cell.count(val8) == len(cell)):
                                                    canditList.append((x,y))
                                        if(len(canditList) == 8):
                                            for x in range(0,4):
                                                for y in range(0, 4):
                                                    if(not((x == canditList[0][0] and y == canditList[0][1]) or
                                                           (x == canditList[1][0] and y == canditList[1][1]) or
                                                           (x == canditList[2][0] and y == canditList[2][1]) or
                                                           (x == canditList[3][0] and y == canditList[3][1]) or
                                                           (x == canditList[4][0] and y == canditList[4][1]) or
                                                           (x == canditList[5][0] and y == canditList[5][1]) or
                                                           (x == canditList[6][0] and y == canditList[6][1]) or
                                                           (x == canditList[7][0] and y == canditList[7][1]))):
                                                        zlen = len(posGrid[x + xreg][y + yreg])
                                                        removePos(posGrid[x + xreg][y + yreg], val1)
                                                        removePos(posGrid[x + xreg][y + yreg], val2)
                                                        removePos(posGrid[x + xreg][y + yreg], val3)
                                                        removePos(posGrid[x + xreg][y + yreg], val4)
                                                        removePos(posGrid[x + xreg][y + yreg], val5)
                                                        removePos(posGrid[x + xreg][y + yreg], val6)
                                                        removePos(posGrid[x + xreg][y + yreg], val7)
                                                        removePos(posGrid[x + xreg][y + yreg], val8)
                                                        if(zlen < len(posGrid[x + xreg][y + yreg])):
                                                            if(same):
                                                                same = False
                                                                print("Reg Hepta", xreg, yreg, val1, val2, val3, val4, val5, val6, val7, val8)
                                        regCount += 1
                                    val8 += 1
                                val7 += 1
                            val6 += 1
                        val5 += 1
                    val4 += 1
                val3 += 1
            val2 += 1
        val1 += 1

    if(same):
        return False
    else:
        return FirstStep(grid, posGrid, incomplete)


def Initialize(puzzle):
    grid = getInitialGrid()
    posGrid = getInitialposGrid()
    incomplete = populateIncomplete()
    for i in range(0, len(puzzle)):
        write(puzzle[i][0], puzzle[i][1], puzzle[i][2], grid, posGrid)
    if(FirstStep(grid, posGrid, incomplete)):
        printGrid(grid)
    else:
        print("Failed")
        printGrid(grid)
        printGrid(posGrid)

def strToNum(s):
    if(s == "1"):
        return 1
    elif(s == "2"):
        return 2
    elif(s == "3"):
        return 3
    elif(s == "4"):
        return 4
    elif(s == "5"):
        return 5
    elif(s == "6"):
        return 6
    elif(s == "7"):
        return 7
    elif(s == "8"):
        return 8
    elif(s == "9"):
        return 9
    elif(s == "A"):
        return 10
    elif(s == "B"):
        return 11
    elif(s == "C"):
        return 12
    elif(s == "D"):
        return 13
    elif(s == "E"):
        return 14
    elif(s == "F"):
        return 15
    elif(s == "G"):
        return 0
    else:
        return -1

def stringGrid(s):
    puzzle = []
    for x in range(0, 16):
        for y in range(0, 16):
            val = strToNum(s[x*16 + y])
            if (val >= 0):
                puzzle.append((x, y, val))
    return puzzle

