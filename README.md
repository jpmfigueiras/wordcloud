# Word Cloud (Tag Cloud) - Execution

## Requirements
- Python 3

## Folder structure
- `InputFiles/` place the `.txt` files here (minimum 5).
- `OutputFile/` receives the output.
- `Script/` contains the code (`word_cloud.py` and `generic_functions.py`).

## How to run
From the project root in a terminal:

```bash
python3 Script/word_cloud.py
```

## Output
- `OutputFile/word_cloud.txt` with lines in the format:
  `word<TAB>frequency<TAB>size`
- If a `RuntimeError` occurs, it creates:
  `OutputFile/errors.txt`
- The output file is overwritten on each run (not appended).

## Notes
- The regex used to split words is in `Script/word_cloud.py`:
  `[A-Za-zÀ-ÖØ-öø-ÿ]+`
- Words that appear only once are removed.

## Docker
Build the image:
```bash
docker build -t word-cloud .
```

Run with volumes (reads `InputFiles/` and writes to `OutputFile/` on the host):
```bash
docker run \
  -v "$PWD/InputFiles:/app/InputFiles" \
  -v "$PWD/OutputFile:/app/OutputFile" \
  word-cloud
```
