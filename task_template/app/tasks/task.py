import os

# define the Task
from task_examples import poetry, tangram, mindmap

if os.environ.get("TASK_NAME") == "tangram":
    task = tangram.Tangram()
elif os.environ.get("TASK_NAME") == "mindmap":
    task = mindmap.Mindmap()
else:
    task = mindmap.Mindmap()
