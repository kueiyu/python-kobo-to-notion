import os
import sqlite3
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
DB_PATH = 'KoboReader.sqlite'

# Print environment variables for debugging
# print(f"NOTION_TOKEN: {NOTION_TOKEN}")
# print(f"NOTION_DATABASE_ID: {NOTION_DATABASE_ID}")
# print(f"DB_PATH: {DB_PATH}")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# Function to export highlights
def export_highlights():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get list of books
    get_book_list_query = """
    SELECT DISTINCT content.ContentID, content.Title, content.Attribution AS Author
    FROM Bookmark
    INNER JOIN content ON Bookmark.VolumeID = content.ContentID
    ORDER BY content.Title
    """
    cursor.execute(get_book_list_query)
    book_list = cursor.fetchall()

    # Debug: Print retrieved books
    # print(f"Books retrieved from SQLite: {book_list}")

    for book in book_list:
        try:
            # Remove subtitles from book title
            title = book[1].split(":")[0]
            print(f"Processing book: {title}")

            # Check Notion database for the book
            response = notion.databases.query(
                **{
                    "database_id": NOTION_DATABASE_ID,
                    "filter": {
                        "and": [
                            {"property": "Title", "title": {"contains": title}},
                            {"property": "Highlights", "checkbox": {"equals": False}},
                        ]
                    },
                }
            )

            # Debug: Print query results
            # print(f"Query results for {title}: {response['results']}")

            # Use the results to determine status of the book
            valid = False
            if len(response['results']) == 1:
                valid = True
            elif len(response['results']) > 1:
                print(f"{title} matched multiple items.")
            else:
                print(f"{title} was skipped.")

            if valid:
                page_id = response['results'][0]['id']
                blocks = []

                # Retrieves highlights for the book
                get_highlights_query = """
                SELECT Bookmark.Text
                FROM Bookmark
                INNER JOIN content ON Bookmark.VolumeID = content.ContentID
                WHERE content.ContentID = ?
                ORDER BY Bookmark.DateCreated DESC
                """
                cursor.execute(get_highlights_query, (book[0],))
                highlights_list = cursor.fetchall()

                # Start with a block for the heading
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Highlights"}}]
                    }
                })

                # Generate a text block for each highlight
                for highlight in highlights_list:
                    if highlight[0] is not None:
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": highlight[0]}}]
                            }
                        })

                # Debug: Print blocks to be added
                # print(f"Blocks to be added for {title}: {blocks}")

                # Append the blocks to the book page
                notion.blocks.children.append(block_id=page_id, children=blocks)

                # Update the status of the book page
                notion.pages.update(
                    page_id=page_id,
                    properties={"Highlights": {"checkbox": True}}
                )

                print(f"Uploaded highlights for {title}.")
        except Exception as error:
            print(f"Error with {book[1]}: {error}")

    # Close the SQLite connection
    conn.close()

# Run the export highlights function
if __name__ == "__main__":
    export_highlights()
