# Setting Up Your npoint.io API Endpoint

## Step 1: Create Your JSON Document

1. Go to https://www.npoint.io/
2. Click "New" to create a new JSON document
3. Copy the contents of `blog-posts.json` from this project
4. Paste it into the npoint.io editor
5. Click "Save" to create your endpoint

## Step 2: Get Your API URL

After saving, you'll get a URL like:
```
https://api.npoint.io/YOUR_UNIQUE_ID
```

## Step 3: Update main.py

In [main.py](main.py#L9), replace the `BLOG_API_URL` with your own endpoint:

```python
BLOG_API_URL = "https://api.npoint.io/YOUR_UNIQUE_ID"
```

## JSON Data Format

Your npoint.io document should follow this structure:

```json
[
  {
    "id": 1,
    "title": "Post Title",
    "subtitle": "Post subtitle",
    "body": "Post content goes here...",
    "author": "Author Name",
    "date": "Month DD, YYYY"
  }
]
```

### Required Fields:
- `id` (integer): Unique identifier for each post
- `title` (string): The post title
- `subtitle` (string): Brief description
- `body` (string): Main content
- `author` (string): Author name
- `date` (string): Publication date

## Example

See the sample document here: https://www.npoint.io/docs/674f5423f73deab1e9a7

The API endpoint would be: https://api.npoint.io/674f5423f73deab1e9a7

## Testing Your Endpoint

You can test your endpoint by visiting the URL in your browser:
```
https://api.npoint.io/YOUR_UNIQUE_ID
```

You should see your JSON data displayed.
