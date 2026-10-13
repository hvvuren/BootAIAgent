from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")
test1 = get_file_content("calculator", "main.py")
print(test1)
test2 = get_file_content("calculator", "pkg/calculator.py")
print(test2)
test3 = get_file_content("calculator", "/bin/cat")
print(test3)
test4 = get_file_content("calculator", "pkg/does_not_exist.py")
print(test4)
