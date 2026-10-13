from array import array
import os, subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a designated python file",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to file to be run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command line arguments",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        valid_file_path = os.path.commonpath([abs_work_dir, abs_file_path]) == abs_work_dir
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args is not None:
            command.extend(args)
        output = subprocess.run(command, cwd=abs_work_dir, capture_output=True, text=True, timeout=30)
        readout = []
        if output.returncode != 0:
            readout.append(f"Process exited with code {output.returncode}")
        if not output.stdout and not output.stderr:
            readout.append("No output produced")
        if output.stdout:
            readout.append(f"STDOUT:\n"+ output.stdout)
        if output.stderr:
            readout.append(f"STDERR:\n"+ output.stderr)
        return "\n".join(readout)
    except Exception as e:
        return f"Error: executing Python file: {e}"
