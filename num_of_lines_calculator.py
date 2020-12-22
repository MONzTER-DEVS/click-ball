import os

files = ['main.py',
         'level_editor.py'
         ]

directories = ['imports', 'imports/extra_screens']

num_of_lines = 0
for i in range(0, len(files)):
    with open(files[i], 'r') as f:
        for n in f:
            num_of_lines += 1
for i in range(0, len(directories)):
    for file in os.listdir('./' + directories[i]):
        if file != "extra_screens" and file != '__pycache__':
            with open(directories[i] + "/" + file, 'r') as f:
                for n in f:
                    num_of_lines += 1
print('Number of lines coded till now in the game are:', num_of_lines)
