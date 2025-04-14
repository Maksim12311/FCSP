def add_student(name, surname, date_of_birth, area_of_study, citizenship):
    with open("students.txt", "a") as f:
        f.write(f"{name},{surname},{date_of_birth},{area_of_study},{citizenship}\n")



def change_information(name, new_data):
    with open("students.txt", "r") as f:
        students = f.readlines()

    with open("students.txt", "w") as f:
        for student in students:
            if student.startswith(name):
                f.write(new_data + "\n")
            else:
                f.write(student)



def delete_student(name):
    with open("students.txt", "r") as f:
        students = f.readlines()

    with open("students.txt", "w") as f:
        for student in students:
            if not student.startswith(name):
                f.write(student)
