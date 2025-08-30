# Snippets test content

# -8<- [start:local-content]

## Test including local content

This content is being included from the local file. It includes `inline code` and a code block.

```python
def main():
    pass
```

# -8<- [end:local-content]

This sentence should *not* be included.

# -8<- [start:remote-content]

## Test including remote content

This content is being included remotely via URL. It contains a Markdown list:

* List item 0
* List item 1
* List item 2

# -8<- [end:remote-content]
