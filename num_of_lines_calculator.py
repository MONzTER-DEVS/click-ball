import os


def calc_lines(path):
    lines = 0
    with open(path, 'rt') as f:
        for n in f:
            lines += 1
    return lines


def process_dir(directory):
    num_of_lines = 0
    files = os.listdir(directory)

    for file in files:
        file_path = f"{directory}/{file}"
        if file == "__pycache__" or file.endswith(".pyc"):
            pass

        elif os.path.isdir(file_path):
            num_of_lines += process_dir(file_path)

        else:
            num_of_lines += calc_lines(file_path)
    return num_of_lines

files = ['main.py', 'level_editor.py']

directories = ['imports', 'assets/levels']

num_of_lines = 0

for file in files:
    num_of_lines += calc_lines(file)

for dir in directories:
    num_of_lines += process_dir(dir)

print('Number of lines coded till now in the game are:', num_of_lines)
