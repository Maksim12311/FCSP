from information import *
from study import *

def display_menu():
    print("\n=== Student Management System ===")
    print("1. Add Student")
    print("2. Change Student Information")
    print("3. Delete Student")
    print("4. Search Students")
    print("5. Display All Students")
    print("6. Add Course")
    print("7. Enroll Student in Course")
    print("8. List Student's Courses")
    print("9. View Course Students")
    print("10. Exit")
    print("==============================")

def main():
    system = StudentManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ")

        try:
            if choice == "1":
                name = input("Enter student's first name: ")
                surname = input("Enter student's last name: ")
                dob = input("Enter date of birth (DD-MM-YYYY): ")
                area = input("Enter area of study: ")
                citizenship = input("Enter citizenship: ")
                
                is_valid, message = validate_student_data(name, surname, dob, area, citizenship)
                if is_valid:
                    student = Student(name, surname, dob, citizenship, area, "")
                    system.students.append(student)
                    print(f"Student {student.full_name} added successfully!")
                else:
                    print(f"Error: {message}")

            elif choice == "2":
                code = input("Enter course code: ")
                name = input("Enter course name: ")
                credits = int(input("Enter number of credits: "))
                area = input("Enter area of study: ")
                
                course = Course(code, name, credits, area)
                system.courses.append(course)
                print(f"Course {name} ({code}) added successfully!")

            elif choice == "3":
                name = input("Enter professor's first name: ")
                surname = input("Enter professor's last name: ")
                dob = input("Enter date of birth (DD-MM-YYYY): ")
                citizenship = input("Enter citizenship: ")
                department = input("Enter department: ")
                specialization = input("Enter specialization: ")
                
                professor = Professor(name, surname, dob, citizenship, department, specialization)
                system.professors.append(professor)
                print(f"Professor {professor.full_name} added successfully!")

            elif choice == "4":
                student_name = input("Enter student's full name: ")
                course_code = input("Enter course code: ")
                
                student = next((s for s in system.students if s.full_name == student_name), None)
                course = next((c for c in system.courses if c.code == course_code), None)
                
                if student and course:
                    course.enrolled_students.add(student)
                    print(f"Student {student_name} enrolled in course {course_code}")
                else:
                    print("Student or course not found!")

            elif choice == "5":
                student_name = input("Enter student's full name: ")
                course_code = input("Enter course code: ")
                grade_value = float(input("Enter grade value: "))
                grade_weight = float(input("Enter grade weight: "))
                grade_date = input("Enter grade date (DD-MM-YYYY): ")
                
                student = next((s for s in system.students if s.full_name == student_name), None)
                if student:
                    grade = Grade(grade_value, grade_weight, grade_date)
                    student.add_grade(course_code, grade)
                    print("Grade added successfully!")
                else:
                    print("Student not found!")

            elif choice == "6":
                query = input("Enter search query: ")
                search_by = input("Search by (name/area): ")
                results = search_students(system.students, query, search_by)
                
                if results:
                    print("\nSearch Results:")
                    for student in results:
                        print(f"- {student.full_name} (GPA: {student.gpa:.2f})")
                else:
                    print("No results found!")

            elif choice == "7":
                sort_by = input("Sort by (gpa/name): ")
                if sort_by == "gpa":
                    sorted_students = sort_students_by_gpa(system.students)
                else:
                    sorted_students = sort_students_by_name(system.students)
                
                print("\nSorted Students:")
                for student in sorted_students:
                    print(f"- {student.full_name} (GPA: {student.gpa:.2f})")

            elif choice == "8":
                performance = analyze_performance(system.students)
                print("\nPerformance Analysis:")
                print(f"Sort Time: {performance['sort_time']:.4f} seconds")
                print(f"Search Time: {performance['search_time']:.4f} seconds")
                print(f"Total Time: {performance['total_time']:.4f} seconds")
                print(f"Average GPA: {performance['average_gpa']:.2f}")

            elif choice == "9":
                if export_to_csv(system.students):
                    print("Data exported successfully!")
                else:
                    print("Error exporting data!")

            elif choice == "10":
                system.save_data()
                print("Thank you for using the Student Management System!")
                break

            else:
                print("Invalid choice! Please try again.")

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()