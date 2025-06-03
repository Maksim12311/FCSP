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
    def __init__(self, first: str, last: str, dob: str, citizen: str):
        self.first_name = first
        self.last_name = last
        self.dob = dob
        self.citizenship = citizen
        self._id: Optional[int] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def get_role(self) -> str:
        pass

class Student(Person):
    def __init__(self, first: str, last: str, dob: str, citizen: str, 
                 area: str, enroll: str):
        super().__init__(first, last, dob, citizen)
        self.area_of_study = area
        self.enrollment_date = enroll
        self.courses: Dict[str, List[Grade]] = {}
        self.gpa: float = 0.0
        self.is_active: bool = True

    def get_role(self) -> str:
        return "Student"

    def add_grade(self, code: str, grade: Grade) -> None:
        if code not in self.courses:
            self.courses[code] = []
        self.courses[code].append(grade)
        self._update_gpa()

    def _update_gpa(self) -> None:
        if not self.courses:
            self.gpa = 0.0
            return

        total = 0
        weight = 0
        for grades in self.courses.values():
            for g in grades:
                total += g.value * g.weight
                weight += g.weight

        self.gpa = total / weight if weight > 0 else 0.0

class Professor(Person):
    def __init__(self, first: str, last: str, dob: str, citizen: str,
                 dept: str, spec: str):
        super().__init__(first, last, dob, citizen)
        self.department = dept
        self.specialization = spec
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

    def add_prerequisite(self, code: str) -> None:
        self.prerequisites.add(code)

    def assign_professor(self, prof: Professor) -> None:
        self.professor = prof
        prof.courses_taught.add(self.code)

def validate_student_data(name: str, surname: str, dob: str, area: str, citizen: str) -> tuple[bool, str]:
    if not all([name, surname, dob, area, citizen]):
        return False, "All fields are required"
        
    if not (name.isalpha() and surname.isalpha()):
        return False, "Name and surname must contain only letters"
        
    try:
        day, month, year = dob.split("-")
        if not (len(day) == 2 and len(month) == 2 and len(year) == 4):
            return False, "Date must be in DD-MM-YYYY format"
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return False, "Date must contain only numbers"
        if not (1 <= int(day) <= 31 and 1 <= int(month) <= 12):
            return False, "Invalid date values"
    except ValueError:
        return False, "Invalid date format"
        
    return True, ""

def search_students(students: List[Student], query: str, by: str) -> List[Student]:
    if not query:
        return []
        
    if by not in ["name", "area"]:
        raise ValueError("Search type must be 'name' or 'area'")
        
    if by == "name":
        return [s for s in students if query.lower() in s.full_name.lower()]
    else:
        return [s for s in students if query.lower() in s.area_of_study.lower()]

def sort_students_by_gpa(students: List[Student]) -> List[Student]:
    if not students:
        return []
    return sorted(students, key=lambda x: x.gpa, reverse=True)

def sort_students_by_name(students: List[Student]) -> List[Student]:
    if not students:
        return []
    return sorted(students, key=lambda x: x.full_name)

def evaluate_student_performance(student: Student) -> Dict[str, float]:
    if not student:
        raise ValueError("Student object is required")
        
    performance = {
        'academic_standing': 0.0,
        'course_load': 0.0,
        'attendance': 0.0
    }

    # Academic standing evaluation
    gpa_condition = student.gpa >= 3.0
    active_condition = student.is_active
    performance['academic_standing'] = 1.0 if (gpa_condition and active_condition) else 0.0

    # Course load evaluation
    course_count = len(student.courses)
    performance['course_load'] = 1.0 if (course_count >= 3 and course_count <= 6) else 0.0

    # Attendance evaluation
    has_grades = any(len(grades) > 0 for grades in student.courses.values())
    performance['attendance'] = 1.0 if has_grades else 0.0

    return performance

def analyze_performance(students: List[Student]) -> Dict[str, float]:
    if not students:
        return {
            'sort_time': 0.0,
            'search_time': 0.0,
            'total_time': 0.0,
            'average_gpa': 0.0
        }
        
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
    gpas = [s.gpa for s in students]
    avg_gpa = statistics.mean(gpas) if gpas else 0.0

    return {
        'sort_time': sort_time,
        'search_time': search_time,
        'total_time': time.time() - start_time,
        'average_gpa': avg_gpa
    }

def export_to_csv(students: List[Student], filename: str = "export.csv") -> bool:
    if not students:
        print("Warning: No students to export")
        return False
        
    try:
        data = [{
            'First': s.first_name,
            'Last': s.last_name,
            'DOB': s.dob,
            'Area': s.area_of_study,
            'Citizen': s.citizenship,
            'GPA': s.gpa,
            'Active': s.is_active
        } for s in students]
        
        pd.DataFrame(data).to_csv(filename, index=False)
        print(f"Success: Exported {len(students)} students")
        return True
        
    except Exception as e:
        print(f"Error: Export failed - {e}")
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
