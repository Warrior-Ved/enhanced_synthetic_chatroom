import json
import time
import requests
from datetime import datetime
import sys

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
JSON_FILE = "data.json"
DELAY_SECONDS = 1  # Time to wait between each action


def parse_date(date_str):
    """Parses 'DD-MM-YYYY HH:MM:SS' to ISO 8601 string."""
    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
        return dt.isoformat()
    except ValueError as e:
        print(f"❌ Error parsing date '{date_str}': {e}")
        return None


def seed_database():
    print(f"🚀 Starting to seed data from {JSON_FILE}...")
    print(f"⏱️  Delay set to {DELAY_SECONDS} seconds between actions.\n")

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File {JSON_FILE} not found!")
        sys.exit(1)

    for i, entry in enumerate(data, 1):
        # 1. Create the Post
        # We prepend the author to the content for display purposes
        formatted_content = f"{entry['author']} says:\n\n{entry['content']}"
        post_payload = {
            "content": formatted_content,
            "channel_id": entry['channel'].lower(),
            "scheduled_at": parse_date(entry['timestamp']),
            "image_url": None
        }

        print(f"[{i}/{len(data)}] Posting to #{entry['channel']}...")
        try:
            res = requests.post(f"{API_URL}/posts/", json=post_payload)
            res.raise_for_status()
            post_db_id = res.json()['id']
            print(f"   ✅ Post created (DB ID: {post_db_id})")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Failed to create post: {e}")
            continue

        time.sleep(DELAY_SECONDS)

        # ✅ KEY CHANGE: This dictionary will map the JSON's comment_id to the REAL database ID.
        comment_id_map = {}

        # 2. Process Comments with Correct Nesting
        # Sort by comment_id to ensure parents are created before their replies
        comments_in_order = sorted(entry.get('comments', []), key=lambda c: c['comment_id'])

        for comment in comments_in_order:
            json_comment_id = comment['comment_id']
            parent_json_id = comment.get('parent_comment_id')
            formatted_comment = f"{comment['handler_id']}: {comment['comment']}"

            # Determine the real database ID of the parent comment
            parent_db_id = None
            if parent_json_id is not None:
                parent_db_id = comment_id_map.get(parent_json_id)
                if parent_db_id is None:
                    print(
                        f"      ⚠️  Could not find parent comment with JSON ID {parent_json_id}. Posting as a top-level comment.")

            comment_payload = {
                "text": formatted_comment,
                "parent_id": parent_db_id
            }

            try:
                c_res = requests.post(f"{API_URL}/comments/{post_db_id}", json=comment_payload)
                c_res.raise_for_status()
                created_comment = c_res.json()

                # ✅ KEY CHANGE: Store the newly created comment's REAL ID in our map
                new_db_id = created_comment.get('id')
                comment_id_map[json_comment_id] = new_db_id

                if parent_db_id:
                    print(
                        f"      ➡️  Reply added by {comment['handler_id']} (replying to comment with DB ID {parent_db_id})")
                else:
                    print(f"      💬 Comment added by {comment['handler_id']} (as PARENT, DB ID: {new_db_id})")

            except requests.exceptions.RequestException as e:
                print(f"      ❌ Failed to add comment/reply: {e}")

            time.sleep(DELAY_SECONDS)

        print(f"   ✨ Finished processing post {i}\n")

    print("🎉 Data seeding complete!")


if __name__ == "__main__":
    seed_database()