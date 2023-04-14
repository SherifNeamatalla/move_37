from langchain.agents import Tool
from langchain.python import PythonREPL
from langchain.utilities import BashProcess

python_repl = PythonREPL()
bash = BashProcess()
code_tools = [
    Tool(
        name="Run Python",
        func=python_repl.run,
        description="Run python code"
    ),
    Tool(
        name="Run Bash",
        func=bash.run,
        description="Run bash code"
    )
]
