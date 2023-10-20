import praw
import json
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("user_agent")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=user_agent,
)

subreddit = reddit.subreddit("nycrail")

top_posts = subreddit.top(limit=10)
all_data = []

for post in top_posts:
    post_data = {
        "title": post.title,
        "text": post.selftext,
        "id": post.id,
        "author": str(post.author),  # converting Redditor object to string
        "url": post.url,
        "score": post.score,
        "comment_count": post.num_comments,
        "created": post.created_utc,
        "comments": [],
        "upvote_ratio": post.upvote_ratio,
        "crossposts": post.num_crossposts,
    }

    post_comments = post.comments
    for comment in post_comments[:2]:
        comment_data = {"body": comment.body, "author": str(comment.author)}
        # Adding the comment dictionary to the 'comments' list of the post
        post_data["comments"].append(comment_data)

    all_data.append(post_data)

json_allData = json.dumps(all_data)

with open("reddit_data.json", "w", encoding="utf-8") as jsonfile:
    jsonfile.write(json_allData)

with open("submission_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Using the keys from 'post_data' dictionary as the fieldnames for the CSV.
    fieldnames = list(post_data.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Writing each post's data as a row in the CSV.
    for post in all_data:
        writer.writerow(post)

print("Done")
