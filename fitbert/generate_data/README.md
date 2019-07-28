# FitBERT - fill in the blank dataset (test data)

## Datasets

[Kaggle: Global News Dataset](//drawception.com/player/546330/nodo-bird/)

## Usage

`python3 main.py ./path/to/plain/text.csv ./output/path.json -m [max_count] -t [gap_type] -s [mask_string]`

where:
- max_count: max num of generated datapoints
- gap_type: verb, noun, all
- mask_string: string marking gaps in sentences, default `***mask***`

## Output

### Verb gap

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


### Noun gap

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