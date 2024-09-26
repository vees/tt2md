import json
import os
from datetime import datetime
import re

# Load configuration from the config file
def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Load the tweets.js file (assuming it's a valid JSON file with "window.YTD.tweets.part0")
def load_tweets(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Remove the JavaScript part and parse the JSON
        content = f.read().replace("window.YTD.tweets.part0 = ", "")
        tweets = json.loads(content)
    return tweets

# Function to wrap URLs starting with http in backticks
def wrap_urls_in_backticks(text):
    # Regular expression to match URLs starting with http
    url_pattern = re.compile(r'(http\S+)')
    
    # Replace URLs with the same URLs wrapped in backticks
    wrapped_text = re.sub(url_pattern, r'`\1`', text)
    
    return wrapped_text

# Function to wrap words containing { or } in backticks
def wrap_brace_words_in_backticks(text):
    # Regular expression to match words containing { or }
    brace_pattern = re.compile(r'(\S*[\{\}]\S*)')
    
    # Replace words containing { or } with backticks around them
    wrapped_text = re.sub(brace_pattern, r'`\1`', text)
    
    return wrapped_text

# Combined function to wrap both URLs and brace-containing words
def clean_tweet_text(text):
    text = wrap_urls_in_backticks(text)
    text = wrap_brace_words_in_backticks(text)
    return text

# Convert tweet data into a chronological structure organized by year and month
def organize_tweets_by_date(tweets):
    organized_tweets = {}

    for tweet_data in tweets:
        tweet = tweet_data['tweet']
        tweet_text = clean_tweet_text(tweet['full_text'])  # Clean text for URLs and brace-containing words
        created_at = tweet['created_at']
        tweet_date = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')

        year = tweet_date.year
        month = tweet_date.strftime('%B')

        # Organize by year and month
        if year not in organized_tweets:
            organized_tweets[year] = {}
        if month not in organized_tweets[year]:
            organized_tweets[year][month] = []

        # Capture the tweet text and interesting metadata
        organized_tweets[year][month].append({
            'date': tweet_date,
            'text': tweet_text,
            'favorites': tweet['favorite_count'],
            'retweets': tweet['retweet_count']
        })

    return organized_tweets

# Create markdown files for each year and write tweets by month using Variant 1
def write_markdown_files(organized_tweets, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Define the order of months
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    for year, months in organized_tweets.items():
        file_name = f'{year}.md'
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'# Tweets from {year}\n\n')

            # Sort months based on the predefined month order
            for month in month_order:
                if month in months:
                    # Sort tweets by date within each month in ascending order
                    sorted_tweets = sorted(months[month], key=lambda x: x['date'])

                    f.write(f'## {month}\n\n')

                    for tweet in sorted_tweets:
                        tweet_text = tweet['text']
                        date = tweet['date'].strftime('%Y-%m-%d %H:%M:%S')
                        favorites = tweet['favorites']
                        retweets = tweet['retweets']

                        # Variant 1: Minimalist Format
                        f.write(f'**{date}**\n')
                        f.write(f'> {tweet_text}\n')
                        f.write(f'- **Favorites**: {favorites}, **Retweets**: {retweets}\n\n')
                        f.write('---\n\n')

    print(f'Markdown files created in: {output_dir}')

# Main function to run the transformation
def main():
    # Load configuration from the config file
    config = load_config('config.json')
    tweets_js_path = config['tweets_js_path']
    output_dir = config['output_dir']

    # Load tweets and process
    tweets = load_tweets(tweets_js_path)
    organized_tweets = organize_tweets_by_date(tweets)
    write_markdown_files(organized_tweets, output_dir)

# Run the script
if __name__ == "__main__":
    main()
