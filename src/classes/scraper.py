# 28.07.25 John
# Wikipedia scraper for TextCatergorizer

import wikipediaapi
import sqlite3

from src.util import util

class Wiki_Scraper:
    def __init__(self):
        self._wiki_api = wikipediaapi.Wikipedia(
            language='en',
            user_agent='PBT project by John Yoo and Foster Rae, Github repo: https://github.com/ExtraBlackBerry/PBT-FactCheckerApp'
            )
        self._data_result = {}
        self._visited_pages = set()
        self._visited_categories = set()

    def category_scraper_multi(self, category_list, depth=0, max_depth=99):              #scrapes multiple categories
        for cat in category_list:
            _result = self._category_scraper(cat, depth, max_depth)
            if _result["error_code"] == 0:
                continue
            else:
                util.print_error(_result)
                return

    def _category_scraper(self, category_name, depth=0, max_depth=99):                  #scrapes single
        
        if not category_name:
            return util.error_code(102, "Catergory name is empty")

        category =  self._wiki_api.page(category_name)

        if not category.exists() or not category.categorymembers:
            return util.error_code(100, f"Category {category} doesn't exist.")
        
        self._visited_categories.add(category_name)

        print("Visisted Categories: ", self._visited_categories)                        #make this into GUI 
        
        if category in self._visited_categories:
            return util.error_code(101, f"Category {category} already visited.")

        for title, member in category.categorymembers.items():
            if title in self._visited_pages:
                continue

            if member.ns == wikipediaapi.Namespace.MAIN:                                #this means it is an article
                self._visited_pages.add(title)
                _categories = list(member.categories.keys())
                self._data_result[title] = _categories
            
            elif member.ns == wikipediaapi.Namespace.CATEGORY and depth < max_depth:    #this means its a category
                _result = self._category_scraper(title, depth +1, max_depth)
                if _result["error_code"] == 0:
                    continue
                    # self._data_result.update(_result["message"])
                elif _result["error_code"] == 101:
                    continue
                else:
                    util.print_error(_result)
                    continue

        return util.result("Success")
    
    def reset_data(self):
        self._data_result = {}

    def reset_visited_data(self):
        self._visited_pages = set()
        self._visited_categories = set()

    def _save_data(self, sqlite_db):
        _result = sqlite_db.save_sqlite(self._data_result)
        if _result["error_code"] == 0:
            pass
        else:
            util.print_error(_result)



 
