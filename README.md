# python-kobo-to-notion

Credit to @juliariec for the great work of [export-kobo-to-notion](https://github.com/juliariec/export-kobo-to-notion)

## Description

This project is helping the users transfer their kobo highlights to their notion.

## Installation

1. Clone the repository or download the executable
```bash
    git clone https://github.com/kueiyu/python-kobo-to-notion.git
    cd python-kobo-to-notion
    pip install -r requirements.txt
```

Version 1.0 download [link](https://github.com/kueiyu/python-kobo-to-notion/blob/b23b7fa6288790301a03cff662fd3755ead0a0ed/kobo_notes_to_notion.exe)

2. Create a `.env` file with the following content:
(You could checkout the details in the `.env.example`)
```
NOTION_TOKEN=your_notion_integration_token
DATABASE_ID=your_notion_database_id
```
To save `.env` in Windows, use `note` and save as `.env` as All files type.

3. Copy your KoboReader.sqlite and put all of them in the folder python-kobo-to-notion

4. Make sure your Notion Page is combine with your Notion Database, and also provide the `Text:Title` and `Checkbox:Highlights`

5. Run the python script by `python main`
