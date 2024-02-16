class Student:
    def __init__(self, id) -> None:
        if not id:
            raise Exception
        self.id = id
        self.submitted_assgns = set()