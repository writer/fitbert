# FitBERT

![buff bert](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/8dbae12a-4088-4550-a059-36a63be1532c/dauvov6-670a232d-4d64-47e6-a662-4fdc18d003ce.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzhkYmFlMTJhLTQwODgtNDU1MC1hMDU5LTM2YTYzYmUxNTMyY1wvZGF1dm92Ni02NzBhMjMyZC00ZDY0LTQ3ZTYtYTY2Mi00ZmRjMThkMDAzY2UucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.XPgC9GT93k_AWVSwSL7a9TTJNWcdO-LgrlK4dIoXn_8)

FitBERT ((F)ill (i)n (t)he blanks, (BERT)) is a library for using [BERT](https://arxiv.org/abs/1810.04805) to fill in the blank(s) in a section of text from a list of options. Here is the imagined usecase for FitBERT:

1. A service (statistical model or something simpler) suggests replacements/corrections for a segment of text
2. That service is specialized to a domain, and isn't good at the big picture, e.g. grammar
3. That service passes the segment of text, with the words to be replaced identified, and the lsit of suggestions
4. FitBERT _crushes_ all but the best suggestion :muscle:

## Installation

...

## Usage

```python
import fitbert as fb

masked_string = "Why Bert, you're looking ***mask*** today!"
options = ['buff', 'handsome', 'strong']

# in theory you can pass a model_name and tokenizer, but currently only
# bert-large-uncased and BertTokenizer are available
# this takes a while and loads a whole big BERT into memory
fb.load_model()

ranked_options = fb.rank(masked_string, options=options)
# >>> ['handsome', 'strong', 'buff']
# or
filled_in = fb.fitb(masked_string, options=options)
# >>> "Why Bert, you're looking handsome today!"
```

We commonly find ourselves knowing what verb to suggest, but not what conjugation:

```python
import fitbert as fb

masked_string = "Why Bert, you're ***mask*** handsome today!"
options = ['looks']

filled_in = fb.fitb(masked_string, options=options)
# >>> "Why Bert, you're looking handsome today!"

# under the hood, we notice there is only one suggestion and act as if
# fitb was called with delemmatize=True:
filled_in = fb.fitb(masked_string, options=options, delemmatize=True)
```

If you are already using `pytorch_pretrained_bert.BertForMaskedLM`, you can pass pass it in (this is not implemented):

```python
BLM = pytorch_pretrained_bert.BertForMaskedLM.from_pretrained(model_name)

fb.load_model(model=BLM)
```
