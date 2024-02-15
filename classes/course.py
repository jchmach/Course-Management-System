class Course:
    def __init__(self, id: int, name: str) -> None:
        if id == None or not name:
            raise Exception
        self.id = id
        self.name = name
        self.assignments = {}
        self.students = set()

    def __eq__(self, __o: object) -> bool:
        return __o.id == self.id