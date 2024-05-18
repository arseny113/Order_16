import os
import shutil

directory = 'src/tg_accounts'

files = os.listdir(directory)

file_groups = {}

for file in files:
    file_name = os.path.splitext(file)[0]
    if file_name in file_groups:
        file_groups[file_name].append(file)
    else:
        file_groups[file_name] = [file]

for file_name, grouped_files in file_groups.items():
    folder_path = os.path.join(directory, file_name)
    os.makedirs(folder_path, exist_ok=True)
    for file in grouped_files:
        src_path = os.path.join(directory, file)
        dst_path = os.path.join(folder_path, file)
        shutil.move(src_path, dst_path)

print("Файлы успешно сгруппированы по папкам.")
