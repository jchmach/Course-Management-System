import pytest
from app.course_service_impl import CourseServiceImpl
from classes.course import Course

def test_get_courses_empty():
    assert [] == CourseServiceImpl().get_courses()

def test_get_courses():
    course_service = CourseServiceImpl()
    course1 = Course(0, "Intro to Computer Science")
    course_service.courses[0] = course1
    assert course_service.get_courses() == [course1]
    course2 = Course(1, "Intro to Calculus 1")
    course_service.courses[1] = course2
    assert course_service.get_courses() == [course1, course2]


def test_create_course_invalid_id():
    with pytest.raises(Exception):
        Course(None, "Intro to Computer Science")

def test_create_course_invalid_name():
    with pytest.raises(Exception):
        Course(0, "")
    with pytest.raises(Exception):
        CourseServiceImpl().create_course("")

def test_create_course_single():
    course_service = CourseServiceImpl()
    course_service.create_course("Intro to Computer Science")
    assert course_service.courses[0].id == 0
    assert course_service.courses[0].name == "Intro to Computer Science"

def test_create_course_multi():
    course_service = CourseServiceImpl()
    course_service.create_course("Intro to Computer Science")
    course_service.create_course("Intro to Calculus 1")
    assert course_service.courses[0].id == 0
    assert course_service.courses[0].name == "Intro to Computer Science"
    assert course_service.courses[1].id == 1
    assert course_service.courses[1].name == "Intro to Calculus 1"

def test_get_course_id_empty():
    course_service = CourseServiceImpl()
    assert None == course_service.get_course_by_id(0)

def test_get_course_id_not_found():
    course_service = CourseServiceImpl()
    course_service.courses[0] = "Intro to Computer Science"
    assert None == course_service.get_course_by_id(1)

def test_get_course_id():
    course_service = CourseServiceImpl()
    course1 = Course(0, "Intro to Computer Science")
    course_service.courses[0] = course1
    assert course_service.get_course_by_id(0) == course1
    course2 = Course(1, "Intro to Calculus 1")
    course_service.courses[1] = course2
    assert course_service.get_course_by_id(1) == course2 


def test_delete_course_empty():
    course_service = CourseServiceImpl()
    course_service.delete_course(0)
    assert len(course_service.courses) == 0

def test_delete_course_not_found():
    course_service = CourseServiceImpl()
    course1 = Course(0, "Intro to Computer Science")
    course_service.courses[0] = course1
    course2 = Course(1, "Intro to Calculus 1")
    course_service.courses[1] = course2
    course_service.delete_course(2)
    assert len(course_service.courses) == 2

def test_delete_course():
    course_service = CourseServiceImpl()
    course1 = Course(0, "Intro to Computer Science")
    course_service.courses[0] = course1
    course2 = Course(1, "Intro to Calculus 1")
    course_service.courses[1] = course2
    course_service.delete_course(0)
    assert len(course_service.courses) == 1
    assert course_service.courses[1] == course2
    course_service.delete_course(1)
    assert len(course_service.courses) == 0