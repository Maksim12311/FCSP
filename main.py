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
                    self.students.append(Student(name, surname, dob, citizenship, area, ""))

            # Load courses
            with open("courses.txt", "r") as f:
                for line in f:
                    code, name, credits, area = line.strip().split(",")
                    self.courses.append(Course(code, name, int(credits), area))
        except FileNotFoundError:
            print("System: No existing data found. Starting fresh.")

    def save_data(self) -> None:
        """Save data to CSV files"""
        # Save students
        with open("students.txt", "w") as f:
            for s in self.students:
                f.write(f"{s.first_name},{s.last_name},{s.dob},{s.area_of_study},{s.citizenship}\n")

        # Save courses
        with open("courses.txt", "w") as f:
            for c in self.courses:
                f.write(f"{c.code},{c.name},{c.credits},{c.area}\n")

    def add_student(self, student: Student) -> bool:
        """Add a new student to the system"""
        try:
            self.students.append(student)
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def add_course(self, course: Course) -> bool:
        """Add a new course to the system"""
        try:
            self.courses.append(course)
            return True
        except Exception as e:
            print(f"Error adding course: {e}")
            return False

    def add_professor(self, professor: Professor) -> bool:
        """Add a new professor to the system"""
        try:
            self.professors.append(professor)
            return True
        except Exception as e:
            print(f"Error adding professor: {e}")
            return False

    def enroll_student(self, student_name: str, course_code: str) -> bool:
        """Enroll a student in a course"""
        student = next((s for s in self.students if s.full_name == student_name), None)
        course = next((c for c in self.courses if c.code == course_code), None)
        
        if not student:
            print(f"Error: Student '{student_name}' not found")
            return False
        if not course:
            print(f"Error: Course '{course_code}' not found")
            return False
            
        course.enrolled_students.add(student)
        return True

    def add_grade(self, student_name: str, course_code: str, grade: Grade) -> bool:
        """Add a grade for a student in a course"""
        student = self.get_student(student_name)
        if not student:
            print(f"Error: Student '{student_name}' not found")
            return False
            
        course = self.get_course(course_code)
        if not course:
            print(f"Error: Course '{course_code}' not found")
            return False
            
        if student not in course.enrolled_students:
            print(f"Error: Student {student_name} is not enrolled in course {course_code}")
            return False
            
        student.add_grade(course_code, grade)
        print(f"Success: Added grade for {student_name} in {course_code}")
        return True

    def get_student(self, name: str) -> Optional[Student]:
        """Get a student by name"""
        for student in self.students:
            if student.full_name.lower() == name.lower():
                return student
        return None

    def get_course(self, code: str) -> Optional[Course]:
        """Get a course by code"""
        for course in self.courses:
            if course.code.lower() == code.lower():
                return course
        return None

    def get_professor(self, name: str) -> Optional[Professor]:
        """Get a professor by name"""
        return next((p for p in self.professors if p.full_name == name), None)

    def export_to_csv(self, filename: str = "export.csv") -> bool:
        """Export student data to CSV"""
        try:
            data = [{
                'First': s.first_name,
                'Last': s.last_name,
                'DOB': s.dob,
                'Area': s.area_of_study,
                'Citizen': s.citizenship,
                'GPA': s.gpa,
                'Active': s.is_active
            } for s in self.students]
            
            pd.DataFrame(data).to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def analyze_performance(self) -> Dict[str, float]:
        """Analyze system performance"""
        start = time.time()
        
        # Measure sorting performance
        sort_time = time.time() - start
        sorted(self.students, key=lambda x: x.gpa)

        # Measure search performance
        search_time = time.time() - start
        [s for s in self.students if s.gpa >= 3.0]

        # Calculate average GPA
        gpas = [s.gpa for s in self.students]
        avg_gpa = sum(gpas) / len(gpas) if gpas else 0.0

        return {
            'sort': sort_time,
            'search': search_time,
            'total': time.time() - start,
            'gpa': avg_gpa
        }

    def generate_truth_table(self, op: str) -> None:
        """Generate and display a truth table for course registration status"""
        print("\nTruth Table: Course Registration Status")
        print("-" * 50)
        print("Student Active\tCourse Available\tPrerequisites Met\tCan Register")
        print("-" * 50)
        
        # Define all possible combinations
        conditions = [
            (True, True, True),    # Active student, available course, prerequisites met
            (True, True, False),   # Active student, available course, no prerequisites
            (True, False, True),   # Active student, unavailable course, prerequisites met
            (True, False, False),  # Active student, unavailable course, no prerequisites
            (False, True, True),   # Inactive student, available course, prerequisites met
            (False, True, False),  # Inactive student, available course, no prerequisites
            (False, False, True),  # Inactive student, unavailable course, prerequisites met
            (False, False, False)  # Inactive student, unavailable course, no prerequisites
        ]
        
        # Evaluate each combination
        for student_active, course_available, prereqs_met in conditions:
            # Can register if student is active AND course is available AND prerequisites are met
            can_register = student_active and course_available and prereqs_met
            print(f"{student_active}\t\t{course_available}\t\t{prereqs_met}\t\t{can_register}")

def display_menu():
    print("\n=== Menu ===")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Add Professor")
    print("4. Enroll")
    print("5. List Students")
    print("6. Add Grade")
    print("7. Search")
    print("8. Sort")
    print("9. Performance")
    print("10. Export")
    print("11. Truth Table")
    print("12. Exit")

def main():
    system = StudentManagementSystem()
    
    while True:
        display_menu()
        choice = input("Choice (1-12): ")

        try:
            if choice == "1":
                name = input("First name: ")
                surname = input("Last name: ")
                dob = input("DOB (DD-MM-YYYY): ")
                area = input("Area: ")
                citizenship = input("Citizenship: ")
                
                if validate_student_data(name, surname, dob, area, citizenship)[0]:
                    student = Student(name, surname, dob, citizenship, area, "")
                    if system.add_student(student):
                        print(f"Success: Added student {student.full_name}")
                else:
                    print("Error: Invalid student data")

            elif choice == "2":
                code = input("Code: ")
                name = input("Name: ")
                try:
                    credits = int(input("Credits: "))
                    if credits <= 0:
                        raise ValueError
                except ValueError:
                    print("Error: Credits must be a positive number")
                    continue
                    
                area = input("Area: ")
                course = Course(code, name, credits, area)
                if system.add_course(course):
                    print(f"Success: Added course {name} ({code})")

            elif choice == "3":
                name = input("First name: ")
                surname = input("Last name: ")
                dob = input("DOB: ")
                citizenship = input("Citizenship: ")
                dept = input("Department: ")
                spec = input("Specialization: ")
                
                prof = Professor(name, surname, dob, citizenship, dept, spec)
                if system.add_professor(prof):
                    print(f"Success: Added professor {prof.full_name}")

            elif choice == "4":
                student = input("Student name: ")
                course = input("Course code: ")
                if system.enroll_student(student, course):
                    print(f"Success: Enrolled {student} in {course}")

            elif choice == "5":
                if system.students:
                    for s in system.students:
                        print(f"{s.full_name} (GPA: {s.gpa:.2f})")
                else:
                    print("Info: No students in system")

            elif choice == "6":
                student_name = input("Enter student name: ")
                course_code = input("Enter course code: ")
                try:
                    grade_value = float(input("Enter grade (0-100): "))
                    if not (0 <= grade_value <= 100):
                        print("Error: Grade must be between 0 and 100")
                        continue
                    weight = float(input("Enter weight (0-1): "))
                    if not (0 < weight <= 1):
                        print("Error: Weight must be between 0 and 1")
                        continue
                    date = input("Enter date (DD-MM-YYYY): ")
                    
                    grade = Grade(grade_value, weight, date)
                    system.add_grade(student_name, course_code, grade)
                except ValueError:
                    print("Error: Invalid grade or weight format")

            elif choice == "7":
                query = input("Enter student name to search: ")
                if not query:
                    print("Error: Search query cannot be empty")
                    continue
                    
                student = system.get_student(query)
                if student:
                    print(f"\nFound student: {student.full_name}")
                    print(f"Area of study: {student.area_of_study}")
                    print(f"GPA: {student.gpa:.2f}")
                    print(f"Active: {'Yes' if student.is_active else 'No'}")
                    if student.courses:
                        print("\nEnrolled courses:")
                        for course_code, grades in student.courses.items():
                            print(f"- {course_code}: {len(grades)} grades")
                else:
                    print(f"No student found with name: {query}")

            elif choice == "8":
                by = input("Sort by (gpa/name): ")
                if by not in ["gpa", "name"]:
                    print("Error: Sort by must be 'gpa' or 'name'")
                    continue
                    
                students = sort_students_by_gpa(system.students) if by == "gpa" else sort_students_by_name(system.students)
                for s in students:
                    print(f"{s.full_name} (GPA: {s.gpa:.2f})")

            elif choice == "9":
                perf = system.analyze_performance()
                print(f"Sort: {perf['sort']:.4f}s")
                print(f"Search: {perf['search']:.4f}s")
                print(f"Total: {perf['total']:.4f}s")
                print(f"GPA: {perf['gpa']:.2f}")

            elif choice == "10":
                if system.export_to_csv():
                    print("Success: Data exported")
                else:
                    print("Error: Export failed")

            elif choice == "11":
                system.generate_truth_table("")

            elif choice == "12":
                system.save_data()
                print("System: Goodbye!")
                break

            else:
                print("Error: Invalid menu choice")

        except ValueError as e:
            print(f"Error: Invalid input - {e}")
        except Exception as e:
            print(f"System Error: {e}")
            print("Please try again or contact support")

if __name__ == "__main__":
    main()