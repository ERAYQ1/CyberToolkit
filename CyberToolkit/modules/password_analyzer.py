import re
from PySide6.QtCore import QObject

class PasswordAnalyzer(QObject):
    def __init__(self):
        super().__init__()

    def analyze(self, password):
        """
        Analyzes the password and returns a dictionary with score, strength,
        estimated crack time, and suggestions.
        """
        score = 0
        suggestions = []
        
        # Length check
        length = len(password)
        if length < 8:
            suggestions.append("Increase length to at least 8 characters.")
        elif length >= 12:
            score += 2
        else:
            score += 1
            
        # Character type checks
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            suggestions.append("Add uppercase letters.")
            
        if re.search(r"[a-z]", password):
            score += 1
        else:
            suggestions.append("Add lowercase letters.")
            
        if re.search(r"[0-9]", password):
            score += 1
        else:
            suggestions.append("Add numbers.")
            
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 2
        else:
            suggestions.append("Add special characters (!@#$...).")
            
        # Determine strength
        if score < 3:
            strength = "Weak"
            color = "#ff4444"
        elif score < 5:
            strength = "Medium"
            color = "#ffaa00"
        else:
            strength = "Strong"
            color = "#00cc66"
            
        # Estimate crack time (Rule-based heuristic)
        # Not a scientifically exact measure, but visually representative
        charset_size = 0
        if re.search(r"[a-z]", password): charset_size += 26
        if re.search(r"[A-Z]", password): charset_size += 26
        if re.search(r"[0-9]", password): charset_size += 10
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset_size += 32
        
        if charset_size == 0: charset_size = 1 # fallback
        
        combinations = charset_size ** length
        hashes_per_second = 10**10 # 10 Billion guesses per second (modern GPU)
        seconds = combinations / hashes_per_second
        
        crack_time = self._format_time(seconds)
        
        return {
            "score": score,
            "max_score": 7,
            "strength": strength,
            "color": color,
            "suggestions": suggestions,
            "crack_time": crack_time
        }

    def _format_time(self, seconds):
        if seconds < 1:
            return "Instantly"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds/3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds/86400)} days"
        elif seconds < 3153600000:
            return f"{int(seconds/31536000)} years"
        else:
            return "Centuries"
