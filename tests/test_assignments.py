from uuid import uuid4
import pytest
from app.course_service_impl import CourseServiceImpl
from classes.assignment import Assignment
from classes.course import Course

course_service = CourseServiceImpl()
course_service.create_course("Intro to Computer Science")
course = course_service.get_courses()[0]
course_id = course.id

def test_create_assignment_invalid():
    with pytest.raises(Exception):
        Assignment("A1", None, uuid4())
        course_service.create_assignment(None, "A1")
        course_service.create_assignment(course_id, "")

def test_create_assignment():
    course_service.create_assignment(course_id, "A1")
    assert len(course.assignments) == 1
    course_service.create_assignment(course_id, "A2")
    assert len(course.assignments) == 2
    for assignment in course.assignments.values():
        assert isinstance(assignment, Assignment)