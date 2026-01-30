def read_file(filename):

    if filename is None:
        lines = sys.stdin.read().strip().splitlines()
    else:
        lines = open(filename, "r").read().strip().splitlines()

    if not lines:
        return 0, [], [] 

    n = int(lines[0].strip())
	
    if n == 0:
        return 0, [], []

    if len(lines) != 1 + 2*n:
        print("Error: expected 1 + 2n lines")

    hospital = [list(map(int, lines[1+i].split())) for i in range(n)]
    student = [list(map(int, lines[1+n+i].split())) for i in range(n)]

    for row in hosp + stud:
        if len(row) != n:
            print("Error: each line must have n numbers")

    return n, hospital, student