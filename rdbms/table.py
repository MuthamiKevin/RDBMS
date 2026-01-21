class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []

    def _cast(self, value):
        if value is None:
            return None

        value = str(value).strip()

        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]

        if value.isdigit():
            return int(value)

        try:
            return float(value)
        except ValueError:
            return value

    def insert(self, row: dict):
        self.rows.append(row)
        return row

    def select(self, condition=None):
        if not condition:
            return self.rows

        col, val = condition
        val = self._cast(val)

        return [r for r in self.rows if r.get(col) == val]

    def update(self, condition, updates: dict):
        col, val = condition
        val = self._cast(val)

        count = 0
        for row in self.rows:
            if row.get(col) == val:
                row.update(updates)
                count += 1
        return count

    def delete(self, condition):
        col, val = condition
        val = self._cast(val)

        before = len(self.rows)
        self.rows = [r for r in self.rows if r.get(col) != val]
        return before - len(self.rows)
