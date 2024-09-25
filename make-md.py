import json
import os
from datetime import datetime

# Load the tweets.js file (assuming it's a valid JSON file with "window.YTD.tweet.part0")
def load_tweets(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Remove the JavaScript part and parse the JSON
        content = f.read().replace("window.YTD.tweets.part0 = ", "")
        tweets = json.loads(content)
    return tweets

# Convert tweet data into a chronological structure organized by year and month
def organize_tweets_by_date(tweets):
    organized_tweets = {}

    for tweet_data in tweets:
        tweet = tweet_data['tweet']
        tweet_text = tweet['full_text']
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
            'date': tweet_date.strftime('%Y-%m-%d %H:%M:%S'),
            'text': tweet_text,
            'favorites': tweet['favorite_count'],
            'retweets': tweet['retweet_count'],
            'source': tweet['source']
        })

    return organized_tweets

# Create markdown files for each year and write tweets by month
def write_markdown_files(organized_tweets, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for year, months in organized_tweets.items():
        file_name = f'{year}.md'
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'# Tweets from {year}\n\n')

            for month, tweets in months.items():
                f.write(f'## {month}\n\n')

                for tweet in tweets:
                    tweet_text = tweet['text']
                    date = tweet['date']
                    favorites = tweet['favorites']
                    retweets = tweet['retweets']
                    source = tweet['source']

                    f.write(f'- **Date**: {date}\n')
                    f.write(f'  **Source**: {source}\n')
                    f.write(f'  **Favorites**: {favorites}, **Retweets**: {retweets}\n')
                    f.write(f'  **Tweet**: {tweet_text}\n\n')

    print(f'Markdown files created in: {output_dir}')

# Main function to run the transformation
def main(tweets_js_path, output_dir):
    tweets = load_tweets(tweets_js_path)
    organized_tweets = organize_tweets_by_date(tweets)
    write_markdown_files(organized_tweets, output_dir)

# Specify the path to the tweets.js file and the output directory
tweets_js_path = './tweets.js'  # Update this path to your tweets.js location
output_dir = 'tweets_markdown_output'

# Run the script
main(tweets_js_path, output_dir)

