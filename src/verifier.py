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
