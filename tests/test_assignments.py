from uuid import uuid4
import pytest
from app.course_service_impl import CourseServiceImpl
from classes.assignment import Assignment
from classes.course import Course

def test_create_assignment_invalid():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_id = course_service.create_course("Intro to Computer Science")
        Assignment("A1", None, uuid4())
        course_service.create_assignment(None, "A1")
        course_service.create_assignment(course_id, "")

def test_create_assignment():
    course_service = CourseServiceImpl()
    course_id = course_service.create_course("Intro to Computer Science")
    course = course_service.get_course_by_id(course_id)
    course_service.create_assignment(course_id, "A1")
    assert len(course.assignments) == 1
    course_service.create_assignment(course_id, "A2")
    assert len(course.assignments) == 2
    for assignment in course.assignments.values():
        assert isinstance(assignment, Assignment)

def test_get_assignment_avg_non_existant_course():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    aid = course_service.create_assignment(cid, "A1")
    assert -1 == course_service.get_assignment_grade_avg(uuid4(), aid)

def test_get_assignemnt_avg_non_existant_assignment():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    assert -1 == course_service.get_assignment_grade_avg(cid, uuid4())