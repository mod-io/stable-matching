import sys
import time
import random
from collections import deque
import matplotlib.pyplot as mplib
import verifier

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
        return 0, [], []

    hospital = [list(map(int, lines[1+i].split())) for i in range(n)]
    student = [list(map(int, lines[1+n+i].split())) for i in range(n)]

    for row in hospital + student:
        if len(row) != n:
            print("Error: each line must have n numbers")
            return 0, [], [] 

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

def write_matching(hospital_match, output_filename):

    if output_filename is None:
        output_file = sys.stdout

    else:
        output_file = open(output_filename, "w")

    for hospital_id, student_id in enumerate(hospital_match, start=1):
        output_file.write(f"{hospital_id} {student_id}\n")

    if output_filename is not None:
        output_file.close()

def random_matching(n, rng):

    ids = list(range(1, n + 1))
    rng.shuffle(ids)
    hospital = [rng.sample(ids, n) for _ in range(n)]
    student  = [rng.sample(ids, n) for _ in range(n)]

    return hospital, student

def benchmark(max_n=512, seed=67):

    rng = random.Random(seed)
    ns = []
    match_times = []
    verify_times = []
    n = 1

    while n <= max_n:

        hospital, student = random_matching(n, rng)

        start_time = time.perf_counter()
        hospital_match = gale_shapley(n, hospital, student)
        end_time = time.perf_counter()

        pairs = [(hospital_id, hospital_match[hospital_id - 1]) for hospital_id in range(1, n + 1)]

        verify_start = time.perf_counter()
        ok, message = verifier.verify(n, hospital, student, pairs)
        verify_end = time.perf_counter()

        if not ok:
            print("Error: verifier rejected matching")
            return

        ns.append(n)
        match_times.append(end_time - start_time)
        verify_times.append(verify_end - verify_start)

        n *= 2

    mplib.figure()
    mplib.plot(ns, match_times, marker="o")
    mplib.xlabel("n")
    mplib.ylabel("seconds")
    mplib.title("Matcher runtime")
    mplib.grid(True)
    mplib.savefig("matcher_runtime.png", dpi=200)

    mplib.figure()
    mplib.plot(ns, verify_times, marker="o")
    mplib.xlabel("n")
    mplib.ylabel("seconds")
    mplib.title("Verifier runtime")
    mplib.grid(True)
    mplib.savefig("verifier_runtime.png", dpi=200)

    print("Saved: matcher_runtime.png, verifier_runtime.png")


def main():

    if len(sys.argv) >= 2 and sys.argv[1] == "--bench":

        max_n = 512

        if len(sys.argv) >= 3:
            max_n = int(sys.argv[2])

        benchmark(max_n=max_n)
        return

    input_filename  = sys.argv[1] if len(sys.argv) >= 2 else None
    output_filename = sys.argv[2] if len(sys.argv) >= 3 else None

    n, hospital, student = read_file(input_filename)
    hospital_match = gale_shapley(n, hospital, student)
    write_matching(hospital_match, output_filename)


if __name__ == "__main__":
    main()


