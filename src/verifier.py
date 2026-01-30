def verify(number_of_pairs, hospital_preferences, student_preferences, matching_pairs):

    """
    matching_pairs = list of (hospital_id, student_id), length n
    Returns (ok, message)
    """

    # ---------- validity ----------
    if number_of_pairs == 0:

        if len(matching_pairs) == 0:
            return True, "VALID STABLE"
        else:
            return False, "INVALID: n=0 but pairs given"

    if len(matching_pairs) != number_of_pairs:
        return False, "INVALID: wrong number of pairs"

    seen_hospitals = set()
    seen_students = set()

    hospital_to_student = {}
    student_to_hospital = {}

    for hospital_id, student_id in matching_pairs:

        if not (1 <= hospital_id <= number_of_pairs) or not (1 <= student_id <= number_of_pairs):
            return False, "INVALID: id out of range"

        if hospital_id in seen_hospitals:
            return False, f"INVALID: hospital {hospital_id} appears twice"

        if student_id in seen_students:
            return False, f"INVALID: student {student_id} appears twice"

        seen_hospitals.add(hospital_id)
        seen_students.add(student_id)

        hospital_to_student[hospital_id] = student_id
        student_to_hospital[student_id] = hospital_id

    # ---------- stability ----------
    hospital_rankings = [dict() for _ in range(number_of_pairs)]

    for hospital_id in range(1, number_of_pairs + 1):
        for rank, student_id in enumerate(hospital_preferences[hospital_id - 1]):
            hospital_rankings[hospital_id - 1][student_id] = rank

    student_rankings = [dict() for _ in range(number_of_pairs)]

    for student_id in range(1, number_of_pairs + 1):
        for rank, hospital_id in enumerate(student_preferences[student_id - 1]):
            student_rankings[student_id - 1][hospital_id] = rank

    for hospital_id in range(1, number_of_pairs + 1):

        current_student = hospital_to_student[hospital_id]
        current_student_rank = hospital_rankings[hospital_id - 1][current_student]

        better_students = hospital_preferences[hospital_id - 1][:current_student_rank]

        for student_id in better_students:

            current_hospital_for_student = student_to_hospital[student_id]

            if student_rankings[student_id - 1][hospital_id] < student_rankings[student_id - 1][current_hospital_for_student]:
                return False, f"UNSTABLE: blocking pair ({hospital_id}, {student_id})"

    return True, "VALID STABLE"


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 3:
        print("Usage: python3 verifier.py instance.in matching.out")
        sys.exit(2)

    instance_filename = sys.argv[1]
    matching_filename = sys.argv[2]

    lines = open(instance_filename).read().strip().splitlines()

    if not lines:
        print("INVALID: empty instance")
        sys.exit(1)

    number_of_pairs = int(lines[0])

    hospital_preferences = [
        list(map(int, lines[1 + i].split()))
        for i in range(number_of_pairs)
    ]

    student_preferences = [
        list(map(int, lines[1 + number_of_pairs + i].split()))
        for i in range(number_of_pairs)
    ]

    matching_lines = open(matching_filename).read().strip().splitlines()

    matching_pairs = []

    for line in matching_lines:
        hospital_id, student_id = map(int, line.split())
        matching_pairs.append((hospital_id, student_id))

    ok, message = verify(number_of_pairs, hospital_preferences, student_preferences, matching_pairs)

    print(message)

    sys.exit(0 if ok else 1)
