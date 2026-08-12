from pydotenvs import load_env
import os
import hashlib
import sys
from reportlab.pdfgen import canvas


load_env(env_path=r'.\example.env')

def is_text_file(file_path):
    text_file_extensions = ['.txt', '.md', '.go', '.py', '.java', '.html', '.css', '.js', '.mod', '.sum']  # Add more as needed
    return any(file_path.lower().endswith(ext) for ext in text_file_extensions)

def combine_txt_files_and_create_pdf(source_directory, output_file, pdf_output, separator='**'):
    separator_line = separator * 40 + '\n'
    
    # Initialize a list to store combined text
    combined_text = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_directory):
            for filename in files:
                if filename.endswith('.txt'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        combined_text.append(separator_line)
                        combined_text.append(f"{filename.center(len(separator_line))}\n")
                        combined_text.append(separator_line)
                        combined_text.append(content + '\n')
                        combined_text.append(separator_line)
                        
                        # Write to the TXT file
                        outfile.writelines([separator_line, f"{filename.center(len(separator_line))}\n", separator_line, content + '\n', separator_line])

    # Write to the PDF file
    c = canvas.Canvas(pdf_output)
    text = c.beginText(40, 800)  # Starting position
    for line in combined_text:
        # Split the combined text into lines
        for subline in line.split('\n'):
            text.textLine(subline.strip())
            if text.getY() < 40:  # Move to a new page if there's no space
                c.drawText(text)
                c.showPage()
                text = c.beginText(40, 800)
    c.drawText(text)
    c.save()

    print(f'All text files have been combined into {output_file} and {pdf_output}')

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
    with open(full_path, mode='w', encoding='utf-8') as data:
        data.write(txt_data)
    print(f'TXT written to: {full_path}\n')


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

        #if file is not a text file, skip it
        if not is_text_file(file):
            print(f'Skipping: [{os.path.basename(file)}] a (probably) non-text file.\n')
            continue

        # If file is empty, skip it
        if os.environ.get('SKIP_EMPTY_FILES').upper() == 'TRUE' and os.path.getsize(file) == 0:
            print('FILE IS EMPTY. SKIPPING.\n')
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

    # My Code
    source_dir = os.environ.get('SOURCE_DIR')  # Change this to your source directory
    output_file = os.environ.get('OUTPUT_FILE')  # The final combined text file
    pdf_output = os.environ.get('PDF_OUTPUT')  # The final PDF file
    combine_txt_files_and_create_pdf(source_dir, output_file, pdf_output)
