# 28.07.25 John
# sqlite db class

if __debug__:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import tkinter as tk
import time
import threading

from src.classes import scraper, sqlite
from src.util import util

class Scraper_App:
    def __init__(self):

        self._scraper = scraper.Wiki_Scraper()                                                      #init scraper
        self._sql_db = sqlite.SqliteDB()                                                            #init sqlite

        self.root = tk.Tk()
        self.root.title("Wikipedia Scraper")
        self.root.geometry("400x200")

        self._category = tk.Label(self.root, text="Enter Category:")
        self._category.pack(pady=5)

        self._entry = tk.Entry(self.root, width=40)
        self._entry.pack(pady=5)

        self._scrape_button = tk.Button(self.root, text="Scrape", command=self._scrape_thread)
        self._scrape_button.pack(pady=10)

        self._save_button = tk.Button(self.root, text="Save", command=self._save)
        self._save_button.pack(pady=10)

        self.root.mainloop()

    def _scrape_thread(self):
        self._scrape_button.config(text="Working...")
        self._scrape_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._scrape)
        thread.start()

    def _scrape_done(self):
        self._scrape_button.config(state=tk.ACTIVE)
        self._scrape_button.config(text="Scrape")

    def _scrape(self):
        _input = "Category:" + self._entry.get()
        _result = self._scraper._category_scraper(_input,0, 1)

        if _result["error_code"] == 0:
            print("success")
        else:
            util.print_error(_result)
        self.root.after(0, self._scrape_done)

    def _save(self):
        
        self._scraper._save_data(self._sql_db)

if __name__ == "__main__":
    Scraper_App()