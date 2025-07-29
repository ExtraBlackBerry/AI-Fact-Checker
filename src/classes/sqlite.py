# 28.07.25 John
# sqlite db class

import os
import sqlite3
import json

from src.util import util

class SqliteDB:
    def __init__(self, db_path="data/wikipedia_data.db"):
        dir_path = os.path.dirname(db_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        self._conn = sqlite3.connect(db_path)

        self._cursor = self._conn.cursor()

    def __del__(self):
        if hasattr(self, '_conn') and self._conn:
            if self._conn:
                self._conn.close()

    def save_sqlite(self, data_result = None , ner_data_dict = None):                                              #saves data into sqlite.db
            
            if not data_result:
                return util.error_code(200, "Data Result is Empty")

            try:

                self._cursor.execute('''
                    CREATE TABLE IF NOT EXISTS wiki_pages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        categories TEXT,
                        ner TEXT
                    )
                ''')

                for title, categories in data_result.items():
                    try:
                        _categories_json = json.dumps(categories)
                        _ner = ner_data_dict[title]
                        self._cursor.execute('''
                            INSERT OR REPLACE INTO wiki_pages (title, categories, ner)
                            VALUES (?, ?, ?)
                        ''', (title, _categories_json, _ner))
                    except Exception as e:
                         return util.error_code(202, f"Insert failed for '{title}': {e}")

                self._conn.commit()
                return util.result("Save Success")

            except Exception as e:
                return util.error_code(201, f"Database save failed: {e}")

    def load_sqlite(self, data_dict):      
        _query = "SELECT title, categories, ner FROM wiki_pages"                                              
        self._cursor.execute(_query)
        _rows = self._cursor.fetchall()

        for title, categories_json, ner in _rows:
            categories = json.loads(categories_json)                                        #json to list

            data_dict[title] = {
                "categories": categories, 
                "ner": ner
            }