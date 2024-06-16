# python-kobo-to-notion

**Credit:** to @juliariec for the incredible work of [export-kobo-to-notion](https://github.com/juliariec/export-kobo-to-notion)

## Description

This project helps users transfer their kobo highlights to their Notion page.

## Installation

1. Clone the repository or download the executable
```bash
    git clone https://github.com/kueiyu/python-kobo-to-notion.git
    cd python-kobo-to-notion
    pip install -r requirements.txt
```


2. Create a `.env` file with the following content:
(You could checkout the details in the `.env.example`)
```
NOTION_TOKEN=your_notion_integration_token
DATABASE_ID=your_notion_database_id
```
Save `.env` in Windows
Use Notepad and save as `.env` as "All files" type selected.

3. Copy the `.kobo/KoboReader.sqlite` to the folder python-kobo-to-notion
```
python-kobo-to-notion/
├── KoboReader.sqlite
├── .env
├── main.py
└── (optional) kono_notes_to_notion.exe
```

4. Make sure your Notion Page is combine with your Notion Database, and creates properties named `Text:Title` and `Checkbox:Highlights`

5. Run the python
- Using Python: run the python script by `python main.py` in your terminal
- Using the executable: Double click the file kono_notes_to_notion.exe (Windows only)
