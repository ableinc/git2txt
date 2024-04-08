# git2txt

Converts all the files of a git repository into .txt files. It also generates a single .txt & .pdf file containing the whole code base. This is useful for training LLMs on your codebase.

## How to Use

1. Create new .env file by copying example.env

```shell
cp example.env .env
```

2. Add necessary fields. The default fields are good to start with.

```bash
GIT_PROJECT_DIRECTORY=/path/to/git/repo (ex. C:\Users\MyUserName\Codebases\GitHub\my-project-name)
IGNORE_FILES=.env,package-lock.json
IGNORE_DIRS=.git,.vscode,node_modules
SAVE_DIRECTORY=training_data
SKIP_EMPTY_FILES=true

SOURCE_DIR=training_data
OUTPUT_FILE=your_code_base.txt
PDF_OUTPUT=your_code_base.pdf
```

3. Install dependencies. Using a virtual environment is recommended.

```shell
python -m pip install -r requirements.txt
```

4. In the "is_text_file" function, you MUST add the extensions of the file you want to be converted.

5. Run program

```shell
python main.py
```

6. You'll see your data files in the `training_data/` directory. This will be different if you changed the path via `SAVE_DIRECTORY` in `.env` file.

## Notes

- This program requires Python version 3.6 or later. It uses the f-string formatting technique introduced in Python 3.6.
