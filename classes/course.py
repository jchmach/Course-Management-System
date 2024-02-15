class Course:
    def __init__(self, id: int, name: str) -> None:
        if id == None or id < 0 or not name:
            raise Exception
        self.id = id
        self.name = name
        self.assignments = {}
        self.students = set()