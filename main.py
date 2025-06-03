from information import *
import time
import pandas as pd
from typing import List, Dict, Optional

class StudentManagementSystem:
    def __init__(self):
        self.students: List[Student] = []
        self.professors: List[Professor] = []
        self.courses: List[Course] = []
        self._load_data()

    def _load_data(self) -> None:
        """Load data from CSV files"""
        try:
            # Load students
            with open("students.txt", "r") as f:
                for line in f:
                    name, surname, dob, area, citizenship = line.strip().split(",")
                    student = Student(name, surname, dob, citizenship, area, "")
                    self.students.append(student)

            # Load courses
            with open("courses.txt", "r") as f:
                for line in f:
                    code, name, credits, area = line.strip().split(",")
                    course = Course(code, name, int(credits), area)
                    self.courses.append(course)
        except FileNotFoundError:
            print("No existing data found. Starting with empty system.")

    def save_data(self) -> None:
        """Save data to CSV files"""
        # Save students
        with open("students.txt", "w") as f:
            for student in self.students:
                f.write(f"{student.first_name},{student.last_name},{student.dob},"
                       f"{student.area_of_study},{student.citizenship}\n")

        # Save courses
        with open("courses.txt", "w") as f:
            for course in self.courses:
                f.write(f"{course.code},{course.name},{course.credits},{course.area}\n")

    def add_student(self, student: Student) -> bool:
        """Add a new student to the system"""
        try:
            self.students.append(student)
            return True
        except Exception as e:
            print(f"Error adding student: {str(e)}")
            return False

    def add_course(self, course: Course) -> bool:
        """Add a new course to the system"""
        try:
            self.courses.append(course)
            return True
        except Exception as e:
            print(f"Error adding course: {str(e)}")
            return False

    def add_professor(self, professor: Professor) -> bool:
        """Add a new professor to the system"""
        try:
            self.professors.append(professor)
            return True
        except Exception as e:
            print(f"Error adding professor: {str(e)}")
            return False

    def enroll_student(self, student_name: str, course_code: str) -> bool:
        """Enroll a student in a course"""
        student = next((s for s in self.students if s.full_name == student_name), None)
        course = next((c for c in self.courses if c.code == course_code), None)
        
        if student and course:
            course.enrolled_students.add(student)
            return True
        return False

    def add_grade(self, student_name: str, course_code: str, grade: Grade) -> bool:
        """Add a grade for a student in a course"""
        student = next((s for s in self.students if s.full_name == student_name), None)
        if student:
            student.add_grade(course_code, grade)
            return True
        return False

    def get_student(self, name: str) -> Optional[Student]:
        """Get a student by name"""
        return next((s for s in self.students if s.full_name == name), None)

    def get_course(self, code: str) -> Optional[Course]:
        """Get a course by code"""
        return next((c for c in self.courses if c.code == code), None)

    def get_professor(self, name: str) -> Optional[Professor]:
        """Get a professor by name"""
        return next((p for p in self.professors if p.full_name == name), None)

    def export_to_csv(self, filename: str = "student_export.csv") -> bool:
        """Export student data to CSV"""
        try:
            data = []
            for student in self.students:
                data.append({
                    'First Name': student.first_name,
                    'Last Name': student.last_name,
                    'Date of Birth': student.dob,
                    'Area of Study': student.area_of_study,
                    'Citizenship': student.citizenship,
                    'GPA': student.gpa,
                    'Is Active': student.is_active
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"Successfully exported {len(self.students)} students to {filename}")
            return True
            
        except Exception as e:
            print(f"Error during export: {str(e)}")
            return False

    def analyze_performance(self) -> Dict[str, float]:
        """Analyze system performance"""
        start_time = time.time()
        
        # Measure sorting performance
        sort_start = time.time()
        sorted_students = sorted(self.students, key=lambda x: x.gpa)
        sort_time = time.time() - sort_start

        # Measure search performance
        search_start = time.time()
        _ = [s for s in self.students if s.gpa >= 3.0]
        search_time = time.time() - search_start

        # Calculate average GPA
        gpas = [student.gpa for student in self.students]
        avg_gpa = sum(gpas) / len(gpas) if gpas else 0.0

        total_time = time.time() - start_time

        return {
            'sort_time': sort_time,
            'search_time': search_time,
            'total_time': total_time,
            'average_gpa': avg_gpa
        }

    def generate_truth_table(self, operation: str) -> None:
        """Generate and display a truth table for logical operations"""
        print(f"\nTruth Table for {operation.upper()}")
        print("-" * 40)
        
        if operation.lower() == "and":
            print("p\tq\tp AND q")
            print("-" * 40)
            for p in [True, False]:
                for q in [True, False]:
                    print(f"{p}\t{q}\t{p and q}")
                    
        elif operation.lower() == "or":
            print("p\tq\tp OR q")
            print("-" * 40)
            for p in [True, False]:
                for q in [True, False]:
                    print(f"{p}\t{q}\t{p or q}")
                    
        elif operation.lower() == "not":
            print("p\tNOT p")
            print("-" * 20)
            for p in [True, False]:
                print(f"{p}\t{not p}")
                
        elif operation.lower() == "nand":
            print("p\tq\tp NAND q")
            print("-" * 40)
            for p in [True, False]:
                for q in [True, False]:
                    print(f"{p}\t{q}\t{not (p and q)}")
                    
        elif operation.lower() == "nor":
            print("p\tq\tp NOR q")
            print("-" * 40)
            for p in [True, False]:
                for q in [True, False]:
                    print(f"{p}\t{q}\t{not (p or q)}")
                    
        elif operation.lower() == "xor":
            print("p\tq\tp XOR q")
            print("-" * 40)
            for p in [True, False]:
                for q in [True, False]:
                    print(f"{p}\t{q}\t{p != q}")
        else:
            print("Invalid operation! Available operations: AND, OR, NOT, NAND, NOR, XOR")

def display_menu():
    print("\n=== Student Management System ===")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Add Professor")
    print("4. Enroll Student in Course")
    print("5. Show All Students")
    print("6. Add Grade")
    print("7. Search Students")
    print("8. Sort Students")
    print("9. Analyze Performance")
    print("10. Export to CSV")
    print("11. Generate Truth Table")
    print("12. Exit")
    print("==============================")

def main():
    system = StudentManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-12): ")

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
                    if system.add_student(student):
                        print(f"Student {student.full_name} added successfully!")
                else:
                    print(f"Error: {message}")

            elif choice == "2":
                code = input("Enter course code: ")
                name = input("Enter course name: ")
                credits = int(input("Enter number of credits: "))
                area = input("Enter area of study: ")
                
                course = Course(code, name, credits, area)
                if system.add_course(course):
                    print(f"Course {name} ({code}) added successfully!")

            elif choice == "3":
                name = input("Enter professor's first name: ")
                surname = input("Enter professor's last name: ")
                dob = input("Enter date of birth (DD-MM-YYYY): ")
                citizenship = input("Enter citizenship: ")
                department = input("Enter department: ")
                specialization = input("Enter specialization: ")
                
                professor = Professor(name, surname, dob, citizenship, department, specialization)
                if system.add_professor(professor):
                    print(f"Professor {professor.full_name} added successfully!")

            elif choice == "4":
                student_name = input("Enter student's full name: ")
                course_code = input("Enter course code: ")
                
                if system.enroll_student(student_name, course_code):
                    print(f"Student {student_name} enrolled in course {course_code}")
                else:
                    print("Student or course not found!")

            elif choice == "5":
                print("\nList of All Students:")
                if system.students:
                    for student in system.students:
                        print(f"- {student.full_name} (GPA: {student.gpa:.2f})")
                else:
                    print("No students in the system.")

            elif choice == "6":
                print("\nAvailable Students:")
                for student in system.students:
                    print(f"- {student.full_name}")
                print("\nAvailable Courses:")
                for course in system.courses:
                    print(f"- {course.name} ({course.code})")
                print("\n")
                
                student_name = input("Enter student's full name: ")
                course_code = input("Enter course code: ")
                grade_value = float(input("Enter grade value: "))
                grade_weight = float(input("Enter grade weight: "))
                grade_date = input("Enter grade date (DD-MM-YYYY): ")
                
                grade = Grade(grade_value, grade_weight, grade_date)
                if system.add_grade(student_name, course_code, grade):
                    print("Grade added successfully!")
                else:
                    print("Student not found!")

            elif choice == "7":
                query = input("Enter search query: ")
                search_by = input("Search by (name/area): ")
                results = search_students(system.students, query, search_by)
                
                if results:
                    print("\nSearch Results:")
                    for student in results:
                        print(f"- {student.full_name} (GPA: {student.gpa:.2f})")
                else:
                    print("No results found!")

            elif choice == "8":
                sort_by = input("Sort by (gpa/name): ")
                if sort_by == "gpa":
                    sorted_students = sort_students_by_gpa(system.students)
                else:
                    sorted_students = sort_students_by_name(system.students)
                
                print("\nSorted Students:")
                for student in sorted_students:
                    print(f"- {student.full_name} (GPA: {student.gpa:.2f})")

            elif choice == "9":
                performance = system.analyze_performance()
                print("\nPerformance Analysis:")
                print(f"Sort Time: {performance['sort_time']:.4f} seconds")
                print(f"Search Time: {performance['search_time']:.4f} seconds")
                print(f"Total Time: {performance['total_time']:.4f} seconds")
                print(f"Average GPA: {performance['average_gpa']:.2f}")

            elif choice == "10":
                if system.export_to_csv():
                    print("Data exported successfully!")
                else:
                    print("Error exporting data!")

            elif choice == "11":
                print("\nAvailable operations:")
                print("1. AND")
                print("2. OR")
                print("3. NOT")
                print("4. NAND")
                print("5. NOR")
                print("6. XOR")
                operation = input("Enter operation name: ").lower()
                system.generate_truth_table(operation)

            elif choice == "12":
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