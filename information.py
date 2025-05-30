from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import csv
import time
import statistics
import pandas as pd

@dataclass
class Grade:
    value: float
    weight: float
    date: str

class Person(ABC):
    def __init__(self, first_name: str, last_name: str, dob: str, citizenship: str):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.citizenship = citizenship
        self._id: Optional[int] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def get_role(self) -> str:
        pass

class Student(Person):
    def __init__(self, first_name: str, last_name: str, dob: str, citizenship: str, 
                 area_of_study: str, enrollment_date: str):
        super().__init__(first_name, last_name, dob, citizenship)
        self.area_of_study = area_of_study
        self.enrollment_date = enrollment_date
        self.courses: Dict[str, List[Grade]] = {}
        self.gpa: float = 0.0
        self.is_active: bool = True

    def get_role(self) -> str:
        return "Student"

    def add_grade(self, course_code: str, grade: Grade) -> None:
        if course_code not in self.courses:
            self.courses[course_code] = []
        self.courses[course_code].append(grade)
        self._update_gpa()

    def _update_gpa(self) -> None:
        if not self.courses:
            self.gpa = 0.0
            return

        total_weighted_grade = 0
        total_weight = 0

        for grades in self.courses.values():
            for grade in grades:
                total_weighted_grade += grade.value * grade.weight
                total_weight += grade.weight

        self.gpa = total_weighted_grade / total_weight if total_weight > 0 else 0.0

class Professor(Person):
    def __init__(self, first_name: str, last_name: str, dob: str, citizenship: str,
                 department: str, specialization: str):
        super().__init__(first_name, last_name, dob, citizenship)
        self.department = department
        self.specialization = specialization
        self.courses_taught: Set[str] = set()
        self.is_tenured: bool = False

    def get_role(self) -> str:
        return "Professor"

class Course:
    def __init__(self, code: str, name: str, credits: int, area: str):
        self.code = code
        self.name = name
        self.credits = credits
        self.area = area
        self.prerequisites: Set[str] = set()
        self.professor: Optional[Professor] = None
        self.enrolled_students: Set[Student] = set()

    def add_prerequisite(self, course_code: str) -> None:
        self.prerequisites.add(course_code)

    def assign_professor(self, professor: Professor) -> None:
        self.professor = professor
        professor.courses_taught.add(self.code)

def validate_student_data(name: str, surname: str, date_of_birth: str, 
                         area_of_study: str, citizenship: str) -> tuple[bool, str]:
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

def sort_students_by_gpa(students: List[Student]) -> List[Student]:
    """Sort students by GPA using quicksort (recursive)"""
    if len(students) <= 1:
        return students
    pivot = students[len(students) // 2]
    left = [s for s in students if s.gpa < pivot.gpa]
    middle = [s for s in students if s.gpa == pivot.gpa]
    right = [s for s in students if s.gpa > pivot.gpa]
    return sort_students_by_gpa(left) + middle + sort_students_by_gpa(right)

def sort_students_by_name(students: List[Student]) -> List[Student]:
    """Sort students by name using bubble sort (iterative)"""
    n = len(students)
    for i in range(n):
        for j in range(0, n - i - 1):
            if students[j].full_name > students[j + 1].full_name:
                students[j], students[j + 1] = students[j + 1], students[j]
    return students

def search_students(students: List[Student], query: str, search_by: str = 'name') -> List[Student]:
    """Search students using binary search (iterative)"""
    sorted_students = sort_students_by_name(students)
    left, right = 0, len(sorted_students) - 1
    results = []

    while left <= right:
        mid = (left + right) // 2
        current = sorted_students[mid]

        if search_by == 'name':
            value = current.full_name.lower()
        elif search_by == 'area':
            value = current.area_of_study.lower()
        else:
            raise ValueError("Invalid search criteria")

        if query.lower() in value:
            results.append(current)
            # Check adjacent elements for more matches
            i = mid - 1
            while i >= 0 and query.lower() in sorted_students[i].full_name.lower():
                results.append(sorted_students[i])
                i -= 1
            i = mid + 1
            while i < len(sorted_students) and query.lower() in sorted_students[i].full_name.lower():
                results.append(sorted_students[i])
                i += 1
            break
        elif value < query.lower():
            left = mid + 1
        else:
            right = mid - 1

    return results

def evaluate_student_performance(student: Student) -> Dict[str, float]:
    """Evaluate student performance using truth table logic"""
    performance = {
        'academic_standing': 0.0,
        'course_load': 0.0,
        'attendance': 0.0
    }

    # Truth table evaluation for academic standing
    gpa_condition = student.gpa >= 3.0
    active_condition = student.is_active
    performance['academic_standing'] = 1.0 if (gpa_condition and active_condition) else 0.0

    # Truth table evaluation for course load
    course_count = len(student.courses)
    performance['course_load'] = 1.0 if (course_count >= 3 and course_count <= 6) else 0.0

    # Truth table evaluation for attendance
    has_grades = any(len(grades) > 0 for grades in student.courses.values())
    performance['attendance'] = 1.0 if has_grades else 0.0

    return performance

def analyze_performance(students: List[Student]) -> Dict[str, float]:
    """Analyze system performance"""
    start_time = time.time()
    
    # Measure sorting performance
    sort_start = time.time()
    sort_students_by_gpa(students)
    sort_time = time.time() - sort_start

    # Measure search performance
    search_start = time.time()
    search_students(students, "")
    search_time = time.time() - search_start

    # Calculate average GPA
    gpas = [student.gpa for student in students]
    avg_gpa = statistics.mean(gpas) if gpas else 0.0

    total_time = time.time() - start_time

    return {
        'sort_time': sort_time,
        'search_time': search_time,
        'total_time': total_time,
        'average_gpa': avg_gpa
    }

def export_to_csv(students: List[Student], filename: str = "student_export.csv") -> bool:
    """Export student data to CSV using pandas"""
    try:
        data = []
        for student in students:
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
        print(f"Successfully exported {len(students)} students to {filename}")
        return True
        
    except Exception as e:
        print(f"Error during export: {str(e)}")
        return False

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
