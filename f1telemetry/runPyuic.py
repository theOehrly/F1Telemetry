import os

print('Processing files...')

directories = ['.']

while directories:
    # print(directories)
    current_dir = directories[0]
    dircontent = os.listdir(current_dir)
    for item in dircontent:
        path = current_dir + '/' + item
        try:
            name, ending = item.split('.')
        except ValueError:
            if os.path.isdir(path):
                directories.append(path)
            continue

        if os.path.isfile(path) and ending == 'ui':
            print(path)
            os.system('python -m PyQt5.uic.pyuic {} -o {}.py -x'.format(path, current_dir + '/' + name))

    directories.remove(current_dir)
