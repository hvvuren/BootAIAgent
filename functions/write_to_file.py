import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites contents of a specified file with new given content",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to file to be written to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content with which file is to be overridden",
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        valid_file_path = os.path.commonpath([abs_work_dir, abs_file_path]) == abs_work_dir
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
