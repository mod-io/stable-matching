from collections import deque

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
    
def gale_shapley(n, hospital, student):

    if n == 0:
        return []

    student_rank = [dict() for _ in range(n)]

    for student_id in range(1, n + 1):
        for rank, hospital_id in enumerate(student[student_id - 1]):
            student_rank[student_id - 1][hospital_id] = rank

    student_match = [0] * n
    next_proposal = [0] * n
    free_hospital = deque(range(1, n + 1))

    while free_hospital:

        hospital_id = free_hospital.popleft()
        hospital_index = hospital_id - 1

        if next_proposal[hospital_index] >= n:
            continue

        student_id = hospital[hospital_index][next_proposal[hospital_index]]
        next_proposal[hospital_index] += 1

        student_index = student_id - 1
        current_hospital = student_match[student_index]

        if current_hospital == 0:
            student_match[student_index] = hospital_id

        else:
            if student_rank[student_index][hospital_id] < student_rank[student_index][current_hospital]:
                student_match[student_index] = hospital_id
                free_hospital.append(current_hospital)
            else:
                free_hospital.append(hospital_id)

    hospital_match = [0] * n

    for student_id in range(1, n + 1):
        hospital_id = student_match[student_id - 1]
        if hospital_id != 0:
            hospital_match[hospital_id - 1] = student_id

    return hospital_match
