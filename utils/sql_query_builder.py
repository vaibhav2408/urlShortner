class SQLQueryBuilder:
    """
    This class build the SQL Query and returns it
    """

    def __init__(self, table_name):
        self.table_name = table_name

    def build_create_table_query(self):
        return 'CREATE TABLE {table_name}(SHORT_URL TEXT NOT NULL PRIMARY KEY, ORIGINAL_URL TEXT NOT NULL);'.format(
            table_name=self.table_name)

    def build_select_query(self):
        query = 'SELECT ORIGINAL_URL FROM {table_name} WHERE SHORT_URL=?'.format(table_name=self.table_name)
        return query

    def build_insert_query(self):
        query = 'INSERT INTO {table_name} (SHORT_URL, ORIGINAL_URL) VALUES (?, ?)'.format(table_name=self.table_name)
        return query

    def build_delete_table_query(self):
        return 'DROP TABLE {table_name};'.format(table_name=self.table_name)

    def build_select_all_query(self):
        return 'SELECT * FROM {table_name}'.format(table_name=self.table_name)
