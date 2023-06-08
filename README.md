# git2txt

Convert all files in git repository to .txt files. This is useful for training LLMs on your codebase.

## How to Use

1. Create new .env file by copying example.env
```shell
cp example.env .env
```
2. Add necessary fields. The default fields are good to start with.
```bash
GIT_PROJECT_DIRECTORY=/path/to/git/repo
IGNORE_FILES=.env,package-lock.json
IGNORE_DIRS=.git,.vscode,node_modules
SAVE_DIRECTORY=training_data
SKIP_EMPTY_FILES=true
```
3. Install dependencies. Using a virtual environment is recommended.
```shell
python -m pip install -r requirements.txt
```
4. Run program
```shell
python main.py
```
5. You'll see your data files in the ```training_data/``` directory. This will be different if you changed the path via ```SAVE_DIRECTORY``` in ```.env``` file.


## Notes
- This program requires Python version 3.6 or later. It uses the f-string formatting technique introduced in Python 3.6.