from typing import List


class AutocompleteService:
    """Service for providing autocomplete suggestions."""
    
    # Mock database of completions for different languages
    PYTHON_SUGGESTIONS = {
        "def": ["def function_name():", "def __init__(self):", "def method(self, param):"],
        "class": ["class ClassName:", "class ClassName(BaseClass):", "class ClassName(object):"],
        "import": ["import module", "from module import", "from . import local_module"],
        "for": ["for item in iterable:", "for i in range():", "for key, value in dict.items():"],
        "if": ["if condition:", "if not condition:", "if x is None:", "elif condition:"],
        "print": ["print()", "print(f'')", "print(variable, end='\\n')"],
        "try": ["try:", "try-except:", "try-except-finally:"],
        "with": ["with open() as file:", "with statement:", "with lock:"],
        "list": ["list()", "[item for item in list]", "[x for x in range(n)]"],
        "dict": ["dict()", "{key: value}", "{k: v for k, v in items}"],
        "lambda": ["lambda x: x", "lambda x, y: x + y", "sorted(list, key=lambda x: x[0])"],
        "while": ["while condition:", "while True:", "while not done:"],
        "return": ["return value", "return None", "return result"],
        "yield": ["yield value", "yield from iterable"],
        "assert": ["assert condition", "assert value is not None"],
        "pass": ["pass"],
        "break": ["break"],
        "continue": ["continue"],
        "raise": ["raise Exception()", "raise ValueError('message')"],
        "except": ["except Exception:", "except (ValueError, KeyError):", "except Exception as e:"],
        "finally": ["finally:"],
        "else": ["else:"],
        "elif": ["elif condition:"],
        "async": ["async def function():", "async with:", "async for"],
        "await": ["await coroutine()", "await function()"],
        "len": ["len()", "len(list)", "len(string)"],
        "range": ["range(n)", "range(start, end)", "range(start, end, step)"],
        "enumerate": ["enumerate(list)", "for i, item in enumerate(list):"],
        "zip": ["zip(list1, list2)", "for a, b in zip(x, y):"],
        "map": ["map(function, iterable)", "list(map(func, items))"],
        "filter": ["filter(function, iterable)", "list(filter(func, items))"],
        "sorted": ["sorted(list)", "sorted(list, reverse=True)", "sorted(list, key=lambda x: x[0])"],
        "isinstance": ["isinstance(obj, type)", "isinstance(var, (int, float))"],
        "hasattr": ["hasattr(obj, 'attr')", "if hasattr(obj, 'method'):"],
        "getattr": ["getattr(obj, 'attr')", "getattr(obj, 'attr', default)"],
        "setattr": ["setattr(obj, 'attr', value)"],
        "property": ["@property", "def value(self):", "@value.setter"],
        "staticmethod": ["@staticmethod", "def static_method():"],
        "classmethod": ["@classmethod", "def class_method(cls):"],
        "super": ["super().__init__()", "super().method()"],
        "self": ["self", "self.attribute", "self.method()"],
        "None": ["None"],
        "True": ["True"],
        "False": ["False"],
        "and": ["and"],
        "or": ["or"],
        "not": ["not"],
        "in": ["in"],
        "is": ["is", "is not"],
        "str": ["str()", "str.upper()", "str.lower()"],
        "int": ["int()", "int('42')"],
        "float": ["float()", "float('3.14')"],
        "bool": ["bool()", "isinstance(x, bool)"],
        "set": ["set()", "{1, 2, 3}", "set.add()"],
        "tuple": ["tuple()", "(1, 2, 3)", "tuple.count()"],
        "json": ["import json", "json.dumps()", "json.loads()"],
        "os": ["import os", "os.path.join()", "os.listdir()"],
        "sys": ["import sys", "sys.argv", "sys.exit()"],
        "re": ["import re", "re.match()", "re.findall()"],
        "datetime": ["import datetime", "datetime.datetime.now()", "datetime.timedelta()"],
        "time": ["import time", "time.sleep()", "time.time()"],
        "random": ["import random", "random.choice()", "random.shuffle()"],
        "collections": ["from collections import defaultdict", "from collections import Counter"],
    }
    
    JAVASCRIPT_SUGGESTIONS = {
        "function": ["function name() {}", "function* generator() {}"],
        "const": ["const name = ", "const { } = object"],
        "let": ["let name = ", "let [a, b] = array"],
        "async": ["async function() {}", "async () => {}"],
        "await": ["await promise", "await function()"],
        "class": ["class Name {}", "class Name extends Base {}"],
        "import": ["import { } from ''", "import name from ''"],
        "export": ["export const", "export default"],
        "setTimeout": ["setTimeout(() => {}, ms)", "setTimeout(callback, delay)"],
        "fetch": ["fetch(url)", "fetch(url).then(res => res.json())"],
    }
    
    def get_suggestions(self, prefix: str, language: str = "python") -> List[str]:
        """
        Get autocomplete suggestions for a given prefix.
        
        Args:
            prefix: The text prefix to complete
            language: The programming language (python, javascript)
            
        Returns:
            List[str]: List of suggestions
        """
        prefix = prefix.strip().lower()
        
        if not prefix:
            return []
        
        # Select language-specific suggestions
        if language.lower() == "javascript":
            suggestions_db = self.JAVASCRIPT_SUGGESTIONS
        else:
            suggestions_db = self.PYTHON_SUGGESTIONS
        
        # Find matching suggestions
        suggestions = []
        for key, values in suggestions_db.items():
            if key.startswith(prefix):
                suggestions.extend(values)
        
        # Return limited suggestions
        return suggestions[:5]
