from rdbms.table import Table

class Engine:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):
        self.tables[name] = Table(name, columns)

    def insert(self, table, data):
        return self.tables[table].insert(data)

    def select(self, table, condition=None):
        return self.tables[table].select(condition)

    def update(self, table, condition, updates):
        return self.tables[table].update(condition, updates)

    def delete(self, table, condition):
        return self.tables[table].delete(condition)


engine = Engine()
