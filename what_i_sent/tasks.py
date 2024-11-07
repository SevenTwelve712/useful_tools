from json import dump, load
from sqlite3 import connect


class Tasks:
    def __init__(self, type_: str, student: str):
        self.tasks = {}
        self.new = []
        self.to_delete = []

        self.curr_id = 1
        self.student = student
        self.type = type_

        con = connect('tasks.db')
        cur = con.cursor()
        cur.execute(f'SELECT id, task FROM {student} WHERE type=?', [type_])
        for elem in cur.fetchall():
            self.tasks[elem[0]] = elem[1]
            self.curr_id += 1
        con.close()

    def append(self, task: str):
        if task in [self.tasks[elem] for elem in self.tasks]:
            raise KeyError('Такое задание уже есть')
        else:
            self.new.append(task)

    def delete(self, task):
        ids = [id_ for id_ in self.tasks if self.tasks[id_] == task]
        if len(ids) > 1:
            raise KeyError('Существуют два или больше одинаковых пути')

        id_ = int(ids[0])
        self.to_delete.append(id_)

    def __str__(self):
        return str(self.tasks)

    def save(self):
        con = connect('tasks.db')
        cur = con.cursor()
        for task in self.new:
            cur.execute(f'INSERT INTO {self.student} (task, type) VALUES (?, ?)', [task, self.type])

        for id_ in self.to_delete:
            cur.execute(f'DELETE FROM {self.student} WHERE id=?', [id_])

        con.commit()
        con.close()

    def __iter__(self):
        return iter([self.tasks[elem] for elem in self.tasks])

    def get_list(self):
        return self.tasks


class Read(Tasks):
    def __init__(self, student: str):
        if student not in ['usolcev', 'verichev']:
            raise KeyError('У меня есть только ученики usolcev и verichev')

        super().__init__('read',  student)

    def append(self, task: str):
        super().append(task)

    def delete(self, task: str):
        super().delete(task)

    def save(self):
        super().save()

    def __str__(self):
        return str(self.tasks)

    def __iter__(self):
        return iter([self.tasks[elem] for elem in self.tasks])


class Crossword(Tasks):
    def __init__(self, student: str):
        if student not in ['usolcev', 'verichev']:
            raise KeyError('У меня есть только ученики usolcev и verichev')

        super().__init__('crossword', student)

    def append(self, task: str):
        super().append(task)

    def delete(self, task: str):
        super().delete(task)

    def save(self):
        super().save()

    def __str__(self):
        return str(self.tasks)

    def __iter__(self):
        return iter([self.tasks[elem] for elem in self.tasks])


def get_task(type_: str, student: str):
    if type_ == 'Crossword':
        return Crossword(student)

    elif type_ == 'Read':
        return Read(student)
