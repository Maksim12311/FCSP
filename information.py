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



def search_students(search_term, search_by):
    results = []
    with open("students.txt", "r") as f:
        students = f.readlines()

    for student in students:
        name, surname, date_of_birth, area_of_study, citizenship = student.strip().split(",")
        
        if search_by == "name" and search_term.lower() in name.lower():
            results.append(student.strip())

        elif search_by == "area_of_study" and search_term.lower() in area_of_study.lower():
            results.append(student.strip())

    return results



def display_all_students():
    """Display all students in a formatted way"""
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()
            
        if not students:
            print("No students found in the system.")
            return
            
        print("\nAll Students:")
        print("-" * 80)
        for student in students:
            name, surname, dob, study, citizenship = student.strip().split(",")
            print(f"Name: {name} {surname}")
            print(f"Date of Birth: {dob}")
            print(f"Area of Study: {study}")
            print(f"Citizenship: {citizenship}")
            print("-" * 80)
    except FileNotFoundError:
        print("Student database not found.")



def count_students_by_area():
    """Count how many students are in each area of study"""
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()
        
        area_counts = {}
        for student in students:
            _, _, _, area, _ = student.strip().split(",")
            area_counts[area] = area_counts.get(area, 0) + 1
        
        print("\nStudents per Area of Study:")
        print("-" * 30)
        for area, count in area_counts.items():
            print(f"{area}: {count} students")
    except FileNotFoundError:
        print("Student database not found.")