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
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ")

        if choice == "1":
            name = input("Enter student's first name: ")
            surname = input("Enter student's last name: ")
            dob = input("Enter date of birth (DD-MM-YYYY): ")
            area = input("Enter area of study: ")
            citizenship = input("Enter citizenship: ")
            add_student(name, surname, dob, area, citizenship)

        elif choice == "2":
            name = input("Enter student's current first name: ")
            new_data = input("Enter new data (format: name,surname,dob,area,citizenship): ")
            change_information(name, new_data)

        elif choice == "3":
            name = input("Enter student's first name to delete: ")
            delete_student(name)

        elif choice == "4":
            term = input("Enter search term: ")
            search_by = input("Search by (name/area_of_study): ")
            results = search_students(term, search_by)
            if results:
                print("\nSearch Results:")
                for result in results:
                    print(result)
            else:
                print("No matching records found.")

        elif choice == "5":
            display_all_students()

        elif choice == "6":
            code = input("Enter course code: ")
            name = input("Enter course name: ")
            credits = input("Enter number of credits: ")
            area = input("Enter area of study: ")
            add_course(code, name, credits, area)

        elif choice == "7":
            student = input("Enter student's full name: ")
            course = input("Enter course code: ")
            enroll_student_in_course(student, course)

        elif choice == "8":
            student = input("Enter student's full name: ")
            list_student_courses(student)

        elif choice == "9":
            course = input("Enter course code: ")
            get_course_students(course)

        elif choice == "10":
            print("Thank you for using the Student Management System!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()