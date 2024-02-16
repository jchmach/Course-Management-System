import heapq
from app.course_service import CourseService
from classes.assignment import Assignment
from classes.course import Course
from classes.student import Student
from typing import List
from uuid import uuid4
from math import floor


class CourseServiceImpl(CourseService):
    """
    Please implement the CourseService interface according to the requirements.
    """

    def __init__(self) -> None:
        self.courses = {}
        self.students = {}

    def get_courses(self):
        return list(self.courses.values())

    def get_course_by_id(self, course_id):
        if course_id in self.courses:
            return self.courses[course_id]
        print(f"404: course with id {course_id} could not be found")
        return None

    def create_course(self, course_name):
        # To create a course, we would insert a new course in to the courses maop with a new constructed obj
        try:
            id = uuid4()
            course = Course(id, course_name)
            self.courses[id] = course
            return id
        except:
            print(
                f"Course with name {course_name} could not be created. Please make sure course name is valid. I.e. Non-empty")
            raise Exception

    def delete_course(self, course_id):
        course = self.get_course_by_id(course_id)
        if not course:
            print(f"404: Course with id {course_id} could not be found")
            raise Exception
        students = course.students
        self.courses.pop(course_id)
        # Remove the submitted assignments associated with the deleted course
        for assignment in course.assignments.values():
            id = assignment.id
            for student in students:
                if id in self.students[student].submitted_assgns:
                    self.students[student].submitted_assgns.remove(id)

    def create_assignment(self, course_id, assignment_name):
        # Create assignment id
        try:
            assgn_id = uuid4()
            assignment = Assignment(assignment_name, assgn_id, course_id)
            self.get_course_by_id(course_id).assignments[assgn_id] = assignment
            return assgn_id
        except:
            print(
                f"Assignment with the following paramaters could not be made: name={assignment_name}, and course={course_id}")

    def enroll_student(self, course_id, student_id):
        try:
          # If the student doesn't exist in the system yet, we create them
            if student_id not in self.students:
                student = Student(student_id)
                self.students[student_id] = student
            course = self.get_course_by_id(course_id)
            if not course:
                raise Exception
            course.students.add(student_id)
        except:
            print(
                f"Error was made in trying to enrol student {student_id} in course {course_id}")
            raise Exception

    def dropout_student(self, course_id, student_id):
        if student_id not in self.students:
            print(f"Student with id {student_id} does not exist")
            raise Exception
        # We need to remove the student from the course, but also remove all occurrences regarding the student and the assignments in both Assgn and Student
        # Get the course
        course = self.get_course_by_id(course_id)
        if not course:
            print(f"Course with id {course_id} does not exist")
            raise Exception
        if student_id not in course.students:
            print(
                f"Student with id {student_id} is not enrolled in course {course_id}")
            raise Exception
        # Get all assignments from the course
        assignments = course.assignments
        student = self.students[student_id]
        # Go through each assignment submitted by the desired student
        submitted = student.submitted_assgns.copy()
        for assignment in submitted:
            # If that submitted assignment is part of the course, then we have to delete it and the grade associated with it
            if assignment in assignments:
                assignments[assignment].grades.pop(student_id)
                student.submitted_assgns.remove(assignment)
        # Now remove the student from the course
        course.students.remove(student_id)

    def submit_assignment(self, course_id, student_id, assignment_id, grade: int):
        if student_id not in self.students:
            print(f"Student with id {student_id} does not exist")
            raise Exception
        course = self.get_course_by_id(course_id)
        student = self.students[student_id]
        if not course:
            raise Exception
        if student_id not in course.students:
            print(
                f"Student with id {student_id} is not enrolled in course {course_id}")
            raise Exception
        assignments = course.assignments
        if assignment_id not in assignments:
            print(
                f"Course {course_id} does not have an assignment {assignment_id}")
            raise Exception
        if grade < 0 or grade > 100:
            print(f"Grade of value {grade} is out of bounds.")
            raise Exception
        student.submitted_assgns.add(assignment_id)
        assignment = assignments[assignment_id]
        assignment.grades[student_id] = grade

    def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
        course = self.get_course_by_id(course_id)
        if not course:
            return -1
        assignments = course.assignments
        if assignment_id not in assignments:
            print(
                f"Course {course_id} does not have an assignment {assignment_id}")
            return -1
        grades = assignments[assignment_id].grades
        if not grades:
            return 0
        return floor(sum(grades.values())/len(grades))

    def get_student_grade_avg(self, course_id, student_id) -> int:
        if student_id not in self.students:
            print(f"Student with id {student_id} does not exist")
            return -1
        student = self.students[student_id]
        course = self.get_course_by_id(course_id)
        if not course:
            return -1
        assignments = course.assignments
        mark_sum = 0
        if len(assignments) == 0:
            return 0
        for assignment in assignments:
            if assignment in student.submitted_assgns:
                mark_sum += assignments[assignment].grades[student_id]
        return floor(mark_sum/len(assignments))

    def get_top_five_students(self, course_id) -> List[int]:
        course = self.get_course_by_id(course_id)
        if not course:
            print(f"Course with id {course_id} does not exist")
            return []
        # Create a heap with the grade of all students
        grade_heap = []
        for student in course.students:
            mark = self.get_student_grade_avg(course_id, student)
            heapq.heappush(grade_heap, (mark, student))
        top_five = heapq.nlargest(5, grade_heap, key=lambda x: (x[0], -x[1]))
        return [student[1] for student in top_five]
