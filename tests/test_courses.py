from uuid import uuid4
import pytest
from app.course_service_impl import CourseServiceImpl
from classes.course import Course

def test_get_courses_empty():
    assert [] == CourseServiceImpl().get_courses()

def test_get_courses():
    course_service = CourseServiceImpl()
    id1 = uuid4()
    course1 = Course(id1, "Intro to Computer Science")
    course_service.courses[0] = course1
    assert course_service.get_courses() == [course1]
    id2 = uuid4()
    course2 = Course(id2, "Intro to Calculus 1")
    course_service.courses[1] = course2
    assert course_service.get_courses() == [course1, course2]


def test_create_course_invalid_id():
    with pytest.raises(Exception):
        Course(None, "Intro to Computer Science")

def test_create_course_invalid_name():
    with pytest.raises(Exception):
        Course(uuid4(), "")
    with pytest.raises(Exception):
        CourseServiceImpl().create_course("")

def test_create_course():
    course_service = CourseServiceImpl()
    id1 = course_service.create_course("Intro to Computer Science")
    assert len(course_service.courses) == 1
    id2 = course_service.create_course("Intro to Calculus 1")
    assert len(course_service.courses) == 2
    assert isinstance(course_service.courses[id1], Course)
    assert isinstance(course_service.courses[id2], Course)
    
def test_get_course_id_empty():
    course_service = CourseServiceImpl()
    assert None == course_service.get_course_by_id(uuid4())

def test_get_course_id_not_found():
    course_service = CourseServiceImpl()
    id = uuid4()
    course_service.courses[id] = Course(id, "Intro to Computer Science")
    assert None == course_service.get_course_by_id(uuid4())

def test_get_course_id():
    course_service = CourseServiceImpl()
    id1 = uuid4()
    course1 = Course(id1, "Intro to Computer Science")
    course_service.courses[id1] = course1
    assert course_service.get_course_by_id(id1) == course1
    id2 = uuid4()
    course2 = Course(id2, "Intro to Calculus 1")
    course_service.courses[id2] = course2
    assert course_service.get_course_by_id(id2) == course2 


def test_delete_course_empty():
    course_service = CourseServiceImpl()
    course_service.delete_course(uuid4())
    assert len(course_service.courses) == 0

def test_delete_course_not_found():
    course_service = CourseServiceImpl()
    id1 = uuid4()
    course1 = Course(id1, "Intro to Computer Science")
    course_service.courses[id1] = course1
    id2 = uuid4()
    course2 = Course(id2, "Intro to Calculus 1")
    course_service.courses[id2] = course2
    course_service.delete_course(uuid4())
    assert len(course_service.courses) == 2

def test_delete_course():
    course_service = CourseServiceImpl()
    id1 = uuid4()
    course1 = Course(id1, "Intro to Computer Science")
    course_service.courses[id1] = course1
    id2 = uuid4()
    course2 = Course(id2, "Intro to Calculus 1")
    course_service.courses[id2] = course2
    course_service.delete_course(id1)
    assert len(course_service.courses) == 1
    assert course_service.courses[id2] == course2
    course_service.delete_course(id2)
    assert len(course_service.courses) == 0

def test_delete_and_add():
    course_service = CourseServiceImpl()
    id1 = course_service.create_course("Intro to Computer Science")
    course_service.create_course("Intro to Calculus 1")
    course_service.delete_course(id1)
    course_service.create_course("Intro to Calculus 2")
    assert len(course_service.courses) == 2