from app.course_service import CourseService
from classes.assignment import Assignment
from classes.course import Course
from typing import List
from uuid import uuid4
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
    except:
      print(f"Course with name {course_name} could not be created. Please make sure course name is valid. I.e. Non-empty")
      raise Exception

  def delete_course(self, course_id):
    if course_id not in self.courses:
      print(f"404: Course with id {course_id} could not be found")
      return
    self.courses.pop(course_id)

  def create_assignment(self, course_id, assignment_name):
      # Create assignment id
      try:
        assgn_id = uuid4()
        assignment = Assignment(assignment_name, assgn_id, course_id)
        self.courses[course_id].assignments[assgn_id] = assignment
      except:
        print(f"Assignment with the following paramaters could not be made: name={assignment_name}, and course={course_id}")
        
  def enroll_student(self, course_id, student_id):
      return super().enroll_student(course_id, student_id)
  
  def dropout_student(self, course_id, student_id):
      return super().dropout_student(course_id, student_id)

  def submit_assignment(self, course_id, student_id, assignment_id, grade: int):
      return super().submit_assignment(course_id, student_id, assignment_id, grade)

  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
      return super().get_assignment_grade_avg(course_id, assignment_id)

  def get_student_grade_avg(self, course_id, student_id) -> int:
      return super().get_student_grade_avg(course_id, student_id)

  def get_top_five_students(self, course_id) -> List[int]:
      return super().get_top_five_students(course_id)

  