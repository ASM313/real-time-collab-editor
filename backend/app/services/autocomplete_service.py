from typing import List


class AutocompleteService:
    """Service for providing autocomplete suggestions."""
    
    # Mock database of completions for different languages
    PYTHON_SUGGESTIONS = {
        "def": ["def function_name():", "def __init__(self):"],
        "class": ["class ClassName:", "class ClassName(BaseClass):"],
        "import": ["import module", "from module import"],
        "for": ["for item in iterable:", "for i in range():"],
        "if": ["if condition:", "if not condition:"],
        "print": ["print()", "print(f'')"],
        "try": ["try:", "try-except"],
        "with": ["with open() as file:", "with statement:"],
        "list": ["list()", "[item for item in list]"],
        "dict": ["dict()", "{key: value}"],
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
