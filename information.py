def add_student(name, surname, date_of_birth, area_of_study, citizenship):
    """Add a new student to the system"""
    is_valid, message = validate_student_data(name, surname, date_of_birth, area_of_study, citizenship)
    if not is_valid:
        print(f"Error: {message}")
        return False
        
    with open("students.txt", "a") as f:
        f.write(f"{name},{surname},{date_of_birth},{area_of_study},{citizenship}\n")
    print(f"Student {name} {surname} has been added successfully.")
    return True



def change_information(name, new_data):
    """Update existing student information"""
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()

        student_found = False
        with open("students.txt", "w") as f:
            for student in students:
                if student.startswith(name):
                    f.write(new_data + "\n")
                    student_found = True
                else:
                    f.write(student)
        
        if student_found:
            print("Student information updated successfully.")
        else:
            print("Student not found.")
            
    except FileNotFoundError:
        print("Student database not found.")



def delete_student(name):
    """Delete a student from the system"""
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()

        student_found = False
        with open("students.txt", "w") as f:
            for student in students:
                if not student.startswith(name):
                    f.write(student)
                else:
                    student_found = True
        
        if student_found:
            print(f"Student {name} has been deleted successfully.")
        else:
            print("Student not found.")
            
    except FileNotFoundError:
        print("Student database not found.")



def search_students(search_term, search_by):
    """Search for students by name or area of study"""
    results = []
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()

        for student in students:
            name, surname, date_of_birth, area_of_study, citizenship = student.strip().split(",")
            
            if search_by == "name" and search_term.lower() in name.lower():
                results.append(student.strip())
            elif search_by == "area_of_study" and search_term.lower() in area_of_study.lower():
                results.append(student.strip())

        return results
    except FileNotFoundError:
        print("Student database not found.")
        return []



def display_all_students():
    """Display all students in the system"""
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



def validate_student_data(name, surname, date_of_birth, area_of_study, citizenship):
    """Validate student data before adding to the system"""
    if not all([name, surname, date_of_birth, area_of_study, citizenship]):
        return False, "All fields are required"
    
    if not (name.isalpha() and surname.isalpha()):
        return False, "Name and surname should contain only letters"
    
    try:
        day, month, year = date_of_birth.split("-")
        if not (len(day) == 2 and len(month) == 2 and len(year) == 4):
            raise ValueError
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            raise ValueError
    except ValueError:
        return False, "Date should be in DD-MM-YYYY format"
    
    return True, "Data is valid"



def export_to_csv(filename="student_export.csv"):
    """Export all student data to a CSV file"""
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()
        
        if not students:
            print("No students to export.")
            return False
            
        with open(filename, "w") as csv_file:
            # Write header
            csv_file.write("First Name,Last Name,Date of Birth,Area of Study,Citizenship\n")
            # Write student data
            for student in students:
                csv_file.write(student)
        
        print(f"Successfully exported {len(students)} students to {filename}")
        return True
        
    except FileNotFoundError:
        print("Student database not found.")
        return False
    except Exception as e:
        print(f"Error during export: {str(e)}")
        return False
