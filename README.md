# wordcloud

A small command-line tool that reads a folder of text files, counts word frequencies across all of them in parallel, and writes a tag-cloud report where every word gets a size class (Huge, Big, Normal, Small) based on how often it appears.

It is written in plain Python with no third-party dependencies and can run either directly or inside a Docker container.

## How it works

1. **Collect input** — every `.txt` file in `InputFiles/` is picked up. At least five files are required; otherwise the run fails with a clear error.
2. **Count in parallel** — each file is processed by its own worker in a `ThreadPoolExecutor`. A worker reads the file, extracts words with a Unicode-aware regular expression (`[A-Za-zÀ-ÖØ-öø-ÿ]+`, so Portuguese accents are kept), lowercases them and returns a word count.
3. **Merge and filter** — the per-file counts are summed into one total, and words that appear only once are dropped as noise.
4. **Size each word** — the size class is relative to the most frequent word:

   | Size   | Rule                                   |
   |--------|----------------------------------------|
   | Huge   | the most frequent word                 |
   | Big    | more than 60% of the top frequency     |
   | Normal | more than 30% of the top frequency     |
   | Small  | everything else                        |

5. **Write the report** — words are sorted by frequency (descending), then alphabetically, and written to `OutputFile/wordcloud.txt`.

## Example output

`OutputFile/wordcloud.txt` is tab-separated: `word`, `frequency`, `size`.

```
a           39   Huge
de          35   Big
e           28   Big
and         23   Normal
to          16   Normal
data        15   Normal
segurança   10   Small
security     9   Small
```

## Running it

### With Python

Requires Python 3.8 or later. From the project root:

```bash
python src/wordcloud.py
```

### With Docker

```bash
docker compose up --build   # first run, or after changing the code or Dockerfile
docker compose up           # after changing only the files in InputFiles/
docker compose down         # stop and remove the container
```

`InputFiles/` and `OutputFile/` are mounted as volumes, so you can swap the input texts and read the report without rebuilding the image.

## Error handling

Every helper wraps its failure in a `RuntimeError` with a descriptive message. If anything goes wrong — missing folder, unreadable file, fewer than five inputs — the message is written to `OutputFile/errors.txt` instead of crashing with a stack trace. The file is overwritten on each run.

## Project structure

```
wordcloud/
├── InputFiles/               # input .txt files (sample texts included)
├── OutputFile/               # generated report and error log
├── src/
│   ├── wordcloud.py          # entry point: orchestration and parallel processing
│   └── auxiliary_functions.py  # reading, tokenising, counting, sizing, writing
├── Dockerfile
└── docker-compose.yml
```

## Possible improvements

- Remove stop words (`a`, `de`, `and`, `to`…) so the cloud highlights meaningful terms.
- Switch to a `ProcessPoolExecutor` for large inputs, since word counting is CPU-bound and threads are limited by the GIL.
- Add unit tests for the counting and sizing functions.
