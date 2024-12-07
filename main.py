from pydotenvs import load_env
import os
import hashlib
import sys
load_env()


def ignore_dir(file_path: str) -> bool:
    for _dir in IGNORE_DIRS:
        if _dir in file_path:
            return True
    return False


def get_file_path() -> None:
    for root, dirs, files in os.walk(git_path, topdown=True):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.basename(full_path) in IGNORE_FILES:
                continue
            if ignore_dir(full_path):
                continue
            FILES.append(full_path)


def write_txt(txt_data: str, file_name: str, md5_hash: str) -> None:
    full_path = os.path.join(save_directory, file_name + f'_{md5_hash}.txt')
    with open(full_path, mode='w') as data:
        data.write(txt_data)
    print(f'TXT written to: {full_path}')


def main() -> None:
    # Get files from git repo
    get_file_path()
    # Verify if files were found
    if len(FILES) == 0:
        print(f"No files found in git directory: {os.environ.get('GIT_PROJECT_DIRECTORY')}")
        sys.exit(1)
    print(f'File count: {len(FILES)}')
    # Build TXT
    print('Creating TXT...')
    for index, file in enumerate(FILES):
        print(f'File #{index+1}: {file}')
        # If line is empty, skip it
        if os.environ.get('SKIP_EMPTY_FILES').upper() == 'TRUE' and os.path.getsize(file) == 0:
            print('FILE IS EMPTY. SKIPPING.')
            continue
        with open(file, mode='r', encoding='utf-8') as git_file:
            file_content = git_file.read()  # Read file content once
            md5_hash = hashlib.md5(file_content.encode('utf-8')).hexdigest()  # Use the content for hashing
            file_name = os.path.basename(file)
            write_txt(txt_data=file_content, file_name=file_name, md5_hash=md5_hash)  # Reuse the content



if __name__ == '__main__':
    FILES = []
    IGNORE_FILES = os.environ.get('IGNORE_FILES').split(',')
    IGNORE_DIRS = os.environ.get('IGNORE_DIRS').split(',')
    PROJECT_NAME = os.path.basename(os.environ.get("GIT_PROJECT_DIRECTORY"))

    git_path = os.environ.get('GIT_PROJECT_DIRECTORY')
    if not os.path.isdir(git_path):
        raise FileNotFoundError('GIT_PROJECT_DIRECTORY not found or not a directory.')
    save_directory = os.environ.get('SAVE_DIRECTORY')
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory, exist_ok=True)
    main()
    print(f'Training data can be found in {save_directory}/ directory.')
