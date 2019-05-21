# watailtinypng
`wagtailtinypng` optimizes the original uploaded image and removes old renditions so they can be re-created using a smaller file source. 

> .jpeg, .jpg and .png images are supported

**Note:** Currently this only support locally served files.

![](images/preview.gif)

## Installation 
1. `pip install wagtailtinypng`
2. Add `wagtail_tinypng` to your `INSTALLED_APPS` like so: 
    ```
    INSTALLED_APPS = [
        ...
        'wagtail_tinypng',
    ]
    ```
3. Add your `TINIFY_API_KEY` to your `base.py` file (or add `TINIFY_API_KEY = "{your_key_here}"` to `dev.py` or `production.py` to separate environments). If you need an API key, head on over to [https://tinypng.com/developers](https://tinypng.com/developers) to get your free API key.
4. **For existing websites only**: You'll want to run a management command to sync your existing images with this package. For that, run `./manage.py sync_tinypng_images`. You will see how many new table relationships were created vs. existing. This command is safe to run on new installations _and_ you can run this command multiple times, no harm done.

## Enable the list view 
This package comes with a simple List View of all your images. To enable it, make sure you have `wagtail.contrib.modeladmin` in your `INSTALLED_APPS` like so:

```
INSTALLED_APPS = [
    ...
    'wagtail.contrib.modeladmin',
]
```

## Settings 
You can add a maximum image width or height when compressing an image. Let's say you've uploaded a large 5000px * 5000px image, you can set a `TINIFY_MAX_WIDTH` or `TINIFY_MAX_HEIGHT`. If neither setting is set, no image resizing will happen.

```
TINIFY_MAX_WIDTH = 2000
# Or
TINIFY_MAX_HEIGHT = 1000
```

If you set both, the `TINIFY_MAX_WIDTH` will take precedence. 

**Note**: You images will be cropped to fit the width and height. This will attempt to keep the same aspect ratio, and simply shrink the images dimensions to the maximum width or height. 
 
![](images/list-view.gif)
