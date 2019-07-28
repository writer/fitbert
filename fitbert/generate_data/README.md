# Fill-in-the-blanks dataset (test data for FitBERT)

<em> "FitBert ((F)ill (i)n (t)he blanks, (BERT)) is a library for using [BERT](https://arxiv.org/abs/1810.04805) to fill in the blank(s) in a section of text from a list of options. "</em>

Every solution needs a test set. This subrepo is meant to generate fill-in-the-blanks questions out of any (reasonable) plain text.


## Datasets

Plan text (used to generate fill-in-the-blank tasks) comes from:

[Kaggle: Global News Dataset](//drawception.com/player/546330/nodo-bird/)

You can use other datasets in `.csv` format, but remember to rename text column to `text`.

## Usage

`python3 main.py ./path/to/plain/text.csv ./path/to/output/path.json -m [max_count] -t [gap_type] -s [mask_string]`

where:
- `max_count`: max num of generated datapoints
- `gap_type`: verb, noun, all
- `mask_string`: string marking gaps in sentences, default `***mask***`

## Output

### Verb gap example

```javascript
{
	"question": "There is this weird sort of fervour that surrounds the MacBook Air that i ***mask*** .", 
	"options": 
			[
				{"answer": "never fully understands", "is_correct": false}, 
				{"answer": "have never fully understood", "is_correct": true}, 
				{"answer": "was never fully understanding", "is_correct": false}
			],
	"type": "verb"
}
```


### Noun gap example

```javascript
{
	"question":"There is ***mask*** of fervour that surrounds the MacBook Air that i have never fully understood .", 
	"options": 
			[
				{"answer": "this weird sorting", "is_correct": false}, 
				{"answer": "this weird sort", "is_correct": true}
			], 
	"type": "noun"
}
```

More examples: `world_news_in_month_test.json`.
