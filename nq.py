'''N Queens problem'''

from functools import reduce
from itertools import chain


# queenPuzzle :: Int -> Int -> [[Int]]
def queenPuzzle(nRows, nCols):
    '''All board patterns of this dimension
       in which no two Queens share a row,
       column, or diagonal.
    '''

    def go(nRows):
        def cr_safe_board(a, xys):
            def next_safe_board(b, iCol):
                good_board = b + [xys + [iCol]] if (
                    safe(lessRows, iCol, xys)
                ) else b
                return good_board
            partA = a + reduce(
                next_safe_board,
                enumFromTo(1, nCols),
                []
            )
            return partA

        lessRows = nRows - 1
        return reduce(
            cr_safe_board,
            go(lessRows),
            []
        ) if nRows > 0 else [[]]

    return go(nRows)


# safe :: Int -> Int -> [Int] -> Bool
def safe(iRow, iCol, pattern):
    '''True if no two queens in the pattern
       share a row, column or diagonal.
    '''
    def collapse(sc, sr):
        return (iCol == sc) or (
            sc + sr == (iCol + iRow)
        ) or (sc - sr == (iCol - iRow))
    res = not any(map(collapse, pattern, range(0, iRow)))
    return res


# TEST ----------------------------------------------------
# main :: IO ()
def main():
    '''Number of solutions for boards of various sizes'''

    n = 5
    xs = queenPuzzle(n, n)

    print(
        str(len(xs)) + ' solutions for a {n} * {n} board:\n'.format(n=n)
    )
    print(showBoards(1)(xs))

    # print(
    #     fTable(
    #         '\n\n' + main.__doc__ + ':\n'
    #     )(str)(lambda n: str(n).rjust(3, ' '))(
    #         lambda n: len(queenPuzzle(n, n))
    #     )(enumFromTo(1)(10))
    # )


# GENERIC -------------------------------------------------

# enumFromTo :: (Int, Int) -> [Int]
def enumFromTo(m, n):
    '''Integer enumeration from m to n.'''
    return list(range(m, 1 + n))


# chunksOf :: Int -> [a] -> [[a]]
def chunksOf(n):
    '''A series of lists of length n, subdividing the
       contents of xs. Where the length of xs is not evenly
       divible, the final list will be shorter than n.
    '''
    def serial(xs):
        def nextChunk(a, i):
            return a + [xs[i:n + i]]

        return reduce(
            nextChunk,
            range(0, len(xs), n), []
        ) if 0 < n else []

    return serial


# intercalate :: [a] -> [[a]] -> [a]
# intercalate :: String -> [String] -> String
def intercalate(x):
    '''The concatenation of xs
       interspersed with copies of x.
    '''
    def concatenation(xs):
        return x.join(xs) if isinstance(x, str) else list(
            chain.from_iterable(
                reduce(lambda a, v: a + [x, v], xs[1:], [xs[0]])
            )
        ) if xs else []
    return concatenation


# FORMATTING ----------------------------------------------

# showBoards :: Int -> [[Int]] -> String
def showBoards(nCols):
    '''String representation, with N columns
       of a set of board patterns.
    '''
    def showBlock(b):
        return '\n'.join(map(intercalate('  '), zip(*b)))

    def displayByNBlocks(bs):
        return '\n\n'.join(map(
            showBlock,
            chunksOf(nCols)(
                list(map(showBoard, bs))
            )
        ))
    return displayByNBlocks


# showBoard :: [Int] -> String
def showBoard(xs):
    '''String representation of a Queens board.'''
    lng = len(xs)

    def showLine(n):
        return (' . ' * (n - 1)) + ' ♛ ' + (' . ' * (lng - n))
    return list(map(showLine, xs))


# fTable :: String -> (a -> String) ->
#                     (b -> String) -> (a -> b) -> [a] -> String
def fTable(s):
    '''Heading -> x display function -> fx display function ->
                     f -> xs -> tabular string.
    '''
    def go(xShow, fxShow, f, xs):
        ys = [xShow(x) for x in xs]
        w = max(map(len, ys))
        return s + '\n' + '\n'.join(map(
            lambda x, y: y.rjust(w, ' ') + ' -> ' + fxShow(f(x)),
            xs, ys
        ))
    return lambda xShow: lambda fxShow: lambda f: lambda xs: go(
        xShow, fxShow, f, xs
    )


# MAIN ---
if __name__ == '__main__':
    main()
