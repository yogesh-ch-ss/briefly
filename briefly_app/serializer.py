#Script for fetching news from database
#Maybe just put this in the views.py

import os
import pandas as pd
import json
import django
from views import JSON_FILE_PATH
from models import NewsArticle

if name == '__main__':
  with open(JSON_FILE_PATH, 'news_data.json') as f:
    data = json.load(f)

  df = pd.json_normalize(data['articles'],
                       meta = [['source', 'name'], 'author', 'title', 'description', 'url', 'publishedAt' 'content'])

  df.columns = ['Source', 'Author', 'Title', 'Description', 'URL', 'Date', 'Content']

  print(df)

  for row in df.iterrows:
  
    if not NewsArticle.objects.filter(Title=row['Title']).exists():
      NewsArticle.objects.create(
          Category="General",
          Title=row['Title'],
          Date=row['Date'],  # Ensure your model handles string-to-datetime conversion
          Content=row['Content'] if pd.notna(row['Content']) else "",
          Source=row['Source'],
          Region="us"  # Modify as per requirement
      )