from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
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

def sort_students_by_gpa(students: List[Student]) -> List[Student]:
    if not students:
        return []
    return sorted(students, key=lambda x: x.gpa, reverse=True)

def sort_students_by_name(students: List[Student]) -> List[Student]:
    if not students:
        return []
    return sorted(students, key=lambda x: x.full_name)
