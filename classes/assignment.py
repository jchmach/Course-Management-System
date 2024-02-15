class Assignment:
    def __init__(self, name, id, course_id) -> None:
        if not name or not id or not course_id:
            raise Exception
        self.id = id
        self.course = course_id
        self.name = name
        self.grades = {}