from uuid import uuid4
import pytest
from app.course_service_impl import CourseServiceImpl
from classes.assignment import Assignment
from classes.course import Course
from classes.student import Student


def test_enroll_student_non_existant_student():
    course_service = CourseServiceImpl()
    course_id = course_service.create_course("Intro to Computer Science")
    student_id = 1
    course_service.enroll_student(course_id, student_id)
    assert len(course_service.students) == 1
    course = course_service.get_course_by_id(course_id)
    assert student_id in course.students
    assert student_id in course_service.students


def test_enroll_student():
    course_service = CourseServiceImpl()
    student_id = 1
    student = Student(student_id)
    course_service.students[student_id] = student
    course_id = course_service.create_course("Intro to Computer Science")
    course_service.enroll_student(course_id, student_id)
    assert len(course_service.students) == 1
    course = course_service.get_course_by_id(course_id)
    assert student_id in course.students


def test_enroll_student_non_existant_course():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_service.enroll_student(uuid4(), 1)


def test_dropout_non_existant_student():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_id = course_service.create_course("Intro to Computer Science")
        course_service.dropout_student(course_id, 1)


def test_dropout_non_existant_course():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_service.students[1] = Student(1)
        course_service.dropout_student(uuid4(), 1)


def test_dropout_student_not_enrolled():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_id = course_service.create_course("Intro to Computer Science")
        course_service.students[1] = Student(1)
        course_service.dropout_student(course_id, 1)


def test_dropout_student():
    course_service = CourseServiceImpl()
    course_id = course_service.create_course("Intro to Computer Science")
    course_service.enroll_student(course_id, 1)
    course_service.dropout_student(course_id, 1)
    assert len(course_service.students) == 1
    assert len(course_service.get_course_by_id(course_id).students) == 0


def test_dropout_student_multiple_courses():
    course_service = CourseServiceImpl()
    cid1 = course_service.create_course("Intro to Computer Science")
    cid2 = course_service.create_course("Intro to Calculus")
    course_service.enroll_student(cid1, 1)
    course_service.enroll_student(cid2, 1)
    assert len(course_service.students) == 1
    assert 1 in course_service.get_course_by_id(cid1).students
    assert 1 in course_service.get_course_by_id(cid2).students


def test_submit_assignment_non_existant_student():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        cid1 = course_service.create_course("Intro to Computer Science")
        aid = course_service.create_assignment(cid1, "A1")
        course_service.submit_assignment(cid1, 1, aid, 100)


def test_submit_assignment_non_existant_course():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_service.students[1] = Student(1)
        cid1 = course_service.create_course("Intro to Computer Science")
        aid = course_service.create_assignment(cid1, "A1")
        course_service.submit_assignment(uuid4(), 1, aid, 100)


def test_submit_assignment_not_enrolled_student():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        course_service.students[1] = Student(1)
        cid1 = course_service.create_course("Intro to Computer Science")
        aid = course_service.create_assignment(cid1, "A1")
        course_service.submit_assignment(cid1, 1, aid, 100)


def test_submit_assignment_non_existant_assignment():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        cid1 = course_service.create_course("Intro to Computer Science")
        _ = course_service.create_assignment(cid1, "A1")
        course_service.enroll_student(cid1, 1)
        course_service.submit_assignment(cid1, 1, uuid4(), 100)


def test_submit_assignment_grade_out_of_bounds_lower():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        cid1 = course_service.create_course("Intro to Computer Science")
        aid = course_service.create_assignment(cid1, "A1")
        course_service.enroll_student(cid1, 1)
        course_service.submit_assignment(cid1, 1, aid, -1)


def test_submit_assignment_grade_out_of_bounds_upper():
    with pytest.raises(Exception):
        course_service = CourseServiceImpl()
        cid1 = course_service.create_course("Intro to Computer Science")
        aid = course_service.create_assignment(cid1, "A1")
        course_service.enroll_student(cid1, 1)
        course_service.submit_assignment(cid1, 1, aid, 101)


def test_submit_assignment():
    course_service = CourseServiceImpl()
    cid1 = course_service.create_course("Intro to Computer Science")
    aid = course_service.create_assignment(cid1, "A1")
    course_service.enroll_student(cid1, 1)
    course_service.submit_assignment(cid1, 1, aid, 40)
    assert aid in course_service.students[1].submitted_assgns
    assert 1 in course_service.get_course_by_id(cid1).assignments[aid].grades
    assert course_service.get_course_by_id(
        cid1).assignments[aid].grades[1] == 40
    # Check for assignment resubmission
    course_service.submit_assignment(cid1, 1, aid, 100)
    assert aid in course_service.students[1].submitted_assgns
    assert 1 in course_service.get_course_by_id(cid1).assignments[aid].grades
    assert course_service.get_course_by_id(
        cid1).assignments[aid].grades[1] == 100


def test_get_assignment_avg():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    aid = course_service.create_assignment(cid, "A1")
    assert 0 == course_service.get_assignment_grade_avg(cid, aid)
    course_service.enroll_student(cid, 1)
    course_service.submit_assignment(cid, 1, aid, 90)
    assert 90 == course_service.get_assignment_grade_avg(cid, aid)
    course_service.enroll_student(cid, 2)
    course_service.submit_assignment(cid, 2, aid, 70)
    assert 80 == course_service.get_assignment_grade_avg(cid, aid)
    cid2 = course_service.create_course("Intro to Calculus")
    aid2 = course_service.create_assignment(cid, "A2")
    course_service.submit_assignment(cid, 1, aid2, 90)
    course_service.submit_assignment(cid, 2, aid2, 90)
    assert 90 == course_service.get_assignment_grade_avg(cid, aid2)
    aid3 = course_service.create_assignment(cid2, "A1")
    course_service.enroll_student(cid2, 1)
    course_service.enroll_student(cid2, 2)
    # Test for multiple courses and flooring
    course_service.submit_assignment(cid2, 1, aid3, 87)
    course_service.submit_assignment(cid2, 2, aid3, 82)
    assert 84 == course_service.get_assignment_grade_avg(cid2, aid3)


def test_get_student_avg_non_existant_student():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    assert -1 == course_service.get_student_grade_avg(cid, 1)


def test_get_student_avg_non_existant_course():
    course_service = CourseServiceImpl()
    course_service.students[1] = Student(1)
    assert -1 == course_service.get_student_grade_avg(uuid4(), 1)


def test_get_student_avg():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    course_service.enroll_student(cid, 1)
    # Test for a course with no assignments
    assert 0 == course_service.get_student_grade_avg(cid, 1)
    # Test for a course with assignments but no submissions
    aid1 = course_service.create_assignment(cid, "A1")
    assert 0 == course_service.get_student_grade_avg(cid, 1)
    # Test for a course with only some assignments submitted
    aid2 = course_service.create_assignment(cid, "A2")
    course_service.submit_assignment(cid, 1, aid1, 87)
    assert 43 == course_service.get_student_grade_avg(cid, 1)
    course_service.submit_assignment(cid, 1, aid2, 90)
    assert 88 == course_service.get_student_grade_avg(cid, 1)
    # Add multiple students and courses and test to make sure the values are still correct
    course_service.enroll_student(cid, 2)
    course_service.submit_assignment(cid, 2, aid1, 1)
    assert 88 == course_service.get_student_grade_avg(cid, 1)
    cid2 = course_service.create_course("Intro to Calculus")
    course_service.enroll_student(cid2, 1)
    aid3 = course_service.create_assignment(cid2, "A1")
    course_service.submit_assignment(cid2, 1, aid3, 1)
    assert 88 == course_service.get_student_grade_avg(cid, 1)


def test_get_top_five_non_existant_course():
    course_service = CourseServiceImpl()
    assert course_service.get_top_five_students(uuid4()) == []


def test_get_top_five():
    course_service = CourseServiceImpl()
    cid = course_service.create_course("Intro to Computer Science")
    # Test for a course with no students enrolled
    assert [] == course_service.get_top_five_students(cid)
    aid1 = course_service.create_assignment(cid, "A1")
    aid2 = course_service.create_assignment(cid, "A2")
    course_service.enroll_student(cid, 1)
    course_service.enroll_student(cid, 2)
    course_service.enroll_student(cid, 3)
    course_service.submit_assignment(cid, 1, aid1, 90)
    course_service.submit_assignment(cid, 2, aid1, 50)
    course_service.submit_assignment(cid, 3, aid1, 100)
    course_service.submit_assignment(cid, 1, aid2, 87)
    course_service.submit_assignment(cid, 2, aid2, 46)
    course_service.submit_assignment(cid, 3, aid2, 98)
    # Test for less than 5 students enrolled
    assert course_service.get_top_five_students(cid) == [3, 1, 2]
    course_service.enroll_student(cid, 4)
    course_service.enroll_student(cid, 5)
    course_service.enroll_student(cid, 6)
    course_service.submit_assignment(cid, 4, aid1, 90)
    course_service.submit_assignment(cid, 5, aid1, 50)
    course_service.submit_assignment(cid, 6, aid1, 100)
    course_service.submit_assignment(cid, 4, aid2, 87)
    course_service.submit_assignment(cid, 5, aid2, 46)
    course_service.submit_assignment(cid, 6, aid2, 98)
    # Test for more than 5 students enrolled
    assert course_service.get_top_five_students(cid) == [3, 6, 1, 4, 2]


def test_dropout_student_with_assignments():
    course_service = CourseServiceImpl()
    # Create a few courses, and add assignments, then make sure the grades are dropped
    # when a student drops out
    cid1 = course_service.create_course("Intro to Computer Science")
    cid2 = course_service.create_course("Intro to Calculus")
    course_service.enroll_student(cid1, 1)
    course_service.enroll_student(cid2, 1)
    aid1 = course_service.create_assignment(cid1, "A1")
    aid2 = course_service.create_assignment(cid1, "A2")
    aid3 = course_service.create_assignment(cid2, "A1")
    course_service.submit_assignment(cid1, 1, aid1, 100)
    course_service.submit_assignment(cid1, 1, aid2, 100)
    course_service.submit_assignment(cid2, 1, aid3, 100)
    course_service.dropout_student(cid1, 1)
    assignments = course_service.get_course_by_id(cid1).assignments
    assert 1 not in course_service.get_course_by_id(cid1).students
    assert aid1 not in course_service.students[1].submitted_assgns
    assert aid2 not in course_service.students[1].submitted_assgns
    for assignment in assignments.values():
        assert 1 not in assignment.grades
    course_service.dropout_student(cid2, 1)
    assignments = course_service.get_course_by_id(cid2).assignments
    assert 1 not in course_service.get_course_by_id(cid2).students
    assert len(list(assignments.values())[0].grades) == 0
    assert len(course_service.students[1].submitted_assgns) == 0


def test_delete_course_with_assignments():
    course_service = CourseServiceImpl()
    # Create a course, create a few assignments then submit them. Make sure that the assignments are properly removed
    # when a course is deleted
    cid = course_service.create_course("Intro to Computer Science")
    course_service.enroll_student(cid, 1)
    course_service.enroll_student(cid, 2)
    aid1 = course_service.create_assignment(cid, "A1")
    aid2 = course_service.create_assignment(cid, "A2")
    course_service.submit_assignment(cid, 1, aid1, 100)
    course_service.submit_assignment(cid, 2, aid1, 40)
    course_service.submit_assignment(cid, 1, aid2, 90)
    course_service.delete_course(cid)
    assert aid1 not in course_service.students[1].submitted_assgns
    assert aid1 not in course_service.students[2].submitted_assgns
    assert aid2 not in course_service.students[1].submitted_assgns
