def execute_user_code(code):
    # Simple simulation of code execution
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return {"output": "Code executed successfully."}
    except Exception as e:
        return {"error": str(e)}
