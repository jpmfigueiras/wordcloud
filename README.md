# Word Cloud (Tag Cloud) - Execution

## Requirements
- Python 3

## Folder structure
- `InputFiles/` place the `.txt` files here (minimum 5).
- `OutputFile/` receives the output.
- `src/` contains the code (`wordcloud.py` and `generic_functions.py`).

## How to run
### Terminal
From the project root in a terminal:

```bash
python3 src/wordcloud.py
```
### Docker
From the project root first run (or after code/Dockerfile changes):
```bash
docker compose up --build
```

If you change only the files in `InputFiles/`:
```bash
docker compose up
```

Stop and remove the container:
```bash
docker compose down
```

## Output
- `OutputFile/wordcloud.txt` with lines in the format:
  `word<TAB>frequency<TAB>size`
- If any error occurs during execution, the error are logged to the output file, it creates:
  `OutputFile/errors.txt`
- The errors file is overwritten on each run (not appended).

## Notes
- The regex used to split words is in `src/wordcloud.py`:
  `[A-Za-zÀ-ÖØ-öø-ÿ]+`
- Words that appear only once are removed.


