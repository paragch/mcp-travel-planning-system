# mcp_server.py
import json
import sys
from typing import Any, Dict

class MCPServer:
    def __init__(self):
        self.tools = {}
        self.register_tool("greet", self.greet, {
            "type": "function",
            "function": {
                "name": "greet",
                "description": "Greets a person by their name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the person to greet"
                        }
                    },
                    "required": ["name"]
                }
            }
        })
        
        self.register_tool("calculate", self.calculate, {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Performs basic arithmetic calculations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                        }
                    },
                    "required": ["expression"]
                }
            }
        })
        
        self.register_tool("get_time", self.get_time, {
            "type": "function",
            "function": {
                "name": "get_time",
                "description": "Gets the current date and time.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        })

    def register_tool(self, name: str, func, schema: Dict[str, Any]):
        self.tools[name] = {"func": func, "schema": schema}

    def greet(self, name: str) -> str:
        """Greets a person by their name."""
        return f"Hello, {name}! This is coming from your local MCP server."
    
    def calculate(self, expression: str) -> str:
        """Performs basic arithmetic calculations."""
        try:
            # Simple eval for basic math - in production, use a proper math parser
            result = eval(expression)
            return f"The result of '{expression}' is: {result}"
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
    
    def get_time(self) -> str:
        """Gets the current date and time."""
        import datetime
        now = datetime.datetime.now()
        return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "local-greeter",
                        "version": "1.0.0"
                    }
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [tool["schema"] for tool in self.tools.values()]
                }
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name]["func"](**arguments)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def run(self):
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

if __name__ == "__main__":
    server = MCPServer()
    server.run()
