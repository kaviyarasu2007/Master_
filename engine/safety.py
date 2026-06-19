import re
import shlex

class SecurityController:
    def __init__(self):
        # Explicit blocklist targeting destructive system anomalies
        self.blocked_patterns = [
            r"rm\s+-rf", 
            r"mkfs", 
            r"dd\s+if=", 
            r"shutdown", 
            r"reboot",
            r"wget\s+",
            r"curl\s+",
            r">:.*?:\s*&.*?;"
        ]
        # Only allow safe informational utilities locally by default
        self.allowed_utilities = ["ls", "pwd", "echo", "whoami", "cat", "grep", "git"]

    def validate_command(self, raw_command: str) -> dict:
        cleaned = raw_command.strip()
        
        # Pattern checking
        for pattern in self.blocked_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return {
                    "status": "BLOCKED",
                    "reason": f"CRITICAL SECURITY BLOCK: Destructive pattern detected."
                }
        
        try:
            tokens = shlex.split(cleaned)
            if not tokens:
                return {"status": "INVALID", "reason": "Empty command string."}
            
            base_utility = tokens[0]
            if base_utility not in self.allowed_utilities:
                return {
                    "status": "SIMULATED",
                    "command": cleaned,
                    "reason": f"Utility '{base_utility}' run restricted to dry-run emulation."
                }
                
            return {
                "status": "AUTHORIZED",
                "command": cleaned,
                "utility": base_utility
            }
        except Exception as e:
            return {"status": "INVALID", "reason": f"Syntax violation: {str(e)}"}
