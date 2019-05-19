# watail-tinypng
`wagtail-tinypng` optimizes the original uploaded image and removes old renditions so they can be re-created using a smaller file source. 

**Note:** Currently this only support locally served files.

![](images/preview.gif)

## Installation 
1. `pip install wagtail-tinypng`
2. Add `wagtail_tinypng` to your `INSTALLED_APPS` like so: 
    ```
    INSTALLED_APPS = [
        ...
        'wagtail_tinypng',
    ]
    ```
3. Add your `TINIFY_API_KEY` to your `base.py` file (or add `TINIFY_API_KEY = "{your_key_here}"` to `dev.py` or `production.py` to separate environments). If you need an API key, head on over to [https://tinypng.com/developers](https://tinypng.com/developers) to get your free API key.

## Enable the list view 
This package comes with a simple List View of all your images. To enable it, make sure you have `wagtail.contrib.modeladmin` in your `INSTALLED_APPS` like so:

```
INSTALLED_APPS = [
    ...
    'wagtail.contrib.modeladmin',
]
```

![](images/list-view.gif)
