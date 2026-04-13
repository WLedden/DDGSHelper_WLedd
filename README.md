# DDGSHelper
### (Dux Distributed Global Search) Helper

This is a small package for a helper function for improving the reliability of the ddgs images() search function.

## collect_images()
```python
def collect_images(
    query: str,
    region: str = "uk-en",
    target: int = 100,
    cache_file: str = "seen_urls.json"
) -> list[any]:
'''
Args:
    query: images search query.
    region: any ddgs.images() region.
    target: number of unique images to collect.
    cache_file: location of saved image urls.

Returns:
    List of unique image urls.
'''
```


