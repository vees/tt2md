# Twitter Takeout to Markdown Transformer

This Python script processes a Twitter Takeout file (`tweets.js`) and converts the tweets into individual Markdown files, organized by year and month. The script also extracts media files (e.g., images) from the `tweets_media` directory, and can optionally prefix the media URLs with a specified base URL for external hosting.

## Features

- Converts tweets into a series of Markdown files, with one file per year.
- Organizes tweets by month and sorts them in ascending order by timestamp.
- Embeds media (e.g., images) from the `tweets_media` directory in the Markdown output.
- Optionally allows prefixing the media URLs with a full URL for external hosting.
- Handles special characters and ensures proper Markdown formatting.
- Properly formats images to sit on their own lines in Markdown.

## Requirements

- Python 3.x

## Setup

1. Clone the repository or download the script.

2. Install Python if you don't have it installed. You can download it from [python.org](https://www.python.org/downloads/).

3. Install the required Python libraries (if necessary). The script primarily uses standard libraries, but ensure you have `json` and `os` available.

## Configuration

Before running the script, you need to set up the configuration file `config.json`.

### `config.json` Example:

```json
{
    "tweets_js_path": "path/to/tweets.js",
    "output_dir": "tweets_markdown_output",
    "media_dir": "tweets_media",
    "image_url_prefix": "https://example.com/tweets_media"
}
```

- `tweets_js_path`: Path to your `tweets.js` file from the Twitter Takeout.
- `output_dir`: Directory where the Markdown files will be created.
- `media_dir`: Directory where media files (e.g., images) are stored, extracted from the Twitter Takeout.
- `image_url_prefix`: (Optional) Base URL to prefix the image filenames if they are hosted externally (e.g., `https://example.com/tweets_media`). If not provided, the script will use local paths from `media_dir`.

## How to Run

1. **Prepare the Files**:
   - Extract your Twitter Takeout and locate the `tweets.js` file and `tweets_media` directory.
   - Place the paths of these files in the `config.json` file as shown in the example above.

2. **Run the Script**:

   Open a terminal or command prompt and run the script:

   ```bash
   python3 twitter_takeout_to_markdown.py
   ```

3. **Check the Output**:
   - The script will generate Markdown files organized by year in the directory specified by `output_dir`.
   - Each file (e.g., `2021.md`) will contain tweets organized by month, with embedded images (if available) and proper Markdown formatting.

## Example Markdown Output

Here’s a sample of what the generated Markdown might look like:

```markdown
# Tweets from 2021

## January

**2021-01-01 12:34:56**
> Happy New Year everyone! `https://t.co/example`
- **Favorites**: 10, **Retweets**: 5

![Tweet Image](https://example.com/tweets_media/1586060195976732673-FgLP8R8XgAc8yMk.png)

---

**2021-01-15 09:22:10**
> First big meeting of the year! `http://example.com`
- **Favorites**: 15, **Retweets**: 7

![Tweet Image](https://example.com/tweets_media/1586060195976732673-FgLP8R8XgAc8yMk.png)

---
```

## Customization

You can customize the script by modifying the following:
- **Image Handling**: Modify the logic that handles image paths in the `extract_local_image_filenames()` function.
- **Markdown Formatting**: Adjust how tweet text, timestamps, and images are formatted in the Markdown output.

## License

This script is free to use and modify.

## Contact

Feel free to reach out if you have any questions or run into issues with the script!

