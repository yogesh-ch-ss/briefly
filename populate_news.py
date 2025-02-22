import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'briefly.settings')

import django
django.setup()

from briefly_app.models import Category, NewsArticle, SavedNews, UserCategory, ViewedNews

# Sample data for News Articles.
news_data = [
    # Business
    {
        'category_name': 'Business',
        'title': 'Stock Market Update',
        'content': 'The stock market saw a major dip today as companies report quarterly earnings...',
        'source': 'Business Insider'
    },
    {
        'category_name': 'Business',
        'title': 'Entrepreneurship Tips',
        'content': 'Learn how to start your own business with these essential entrepreneurship tips...',
        'source': 'Forbes'
    },
    
    # Entertainment
    {
        'category_name': 'Entertainment',
        'title': 'Movie Release This Week',
        'content': 'The latest blockbuster movie hits theaters this weekend. Here’s what you need to know...',
        'source': 'Variety'
    },
    {
        'category_name': 'Entertainment',
        'title': 'Celebrity News',
        'content': 'Famous actor announces new film project. Fans are excited for the upcoming release...',
        'source': 'Hollywood Reporter'
    },
    
    # General
    {
        'category_name': 'General',
        'title': 'Global News Update',
        'content': 'In today\’s world news, there are important updates regarding climate change and geopolitics...',
        'source': 'BBC News'
    },
    {
        'category_name': 'General',
        'title': 'Breaking News',
        'content': 'A major incident has occurred, and the authorities are working to control the situation...',
        'source': 'Reuters'
    },
    
    # Health
    {
        'category_name': 'Health',
        'title': 'Mental Health Awareness',
        'content': 'In observance of Mental Health Awareness Month, we focus on the importance of self-care...',
        'source': 'Psychology Today'
    },
    {
        'category_name': 'Health',
        'title': 'Nutrition Tips',
        'content': 'Eating healthy doesn’t have to be hard. Here are some easy nutrition tips for everyday life...',
        'source': 'WebMD'
    },
    
    # Science
    {
        'category_name': 'Science',
        'title': 'Space Exploration Update',
        'content': 'NASA is preparing for a new mission to Mars, aimed at discovering signs of life...',
        'source': 'NASA News'
    },
    {
        'category_name': 'Science',
        'title': 'New Particle Discovered',
        'content': 'Scientists have discovered a new subatomic particle that could change our understanding of physics...',
        'source': 'Science Journal'
    },
    
    # Sports
    {
        'category_name': 'Sports',
        'title': 'Football Championship Finals',
        'content': 'The final match of the football championship is set to take place this weekend, with teams vying for the title...',
        'source': 'ESPN'
    },
    {
        'category_name': 'Sports',
        'title': 'Olympics 2024 Preparations',
        'content': 'Athletes from around the world are gearing up for the upcoming Olympics in Paris...',
        'source': 'Sports Illustrated'
    },
    
    # Technology
    {
        'category_name': 'Technology',
        'title': 'New Smartphone Release',
        'content': 'The latest smartphone model promises groundbreaking features that will change the tech landscape...',
        'source': 'TechCrunch'
    },
    {
        'category_name': 'Technology',
        'title': 'AI in Healthcare',
        'content': 'AI is transforming healthcare with new tools that improve patient care and diagnosis...',
        'source': 'Wired'
    }
]


def clear_existing_data():
    # Delete existing data in relevant models
    Category.objects.all().delete()
    NewsArticle.objects.all().delete()
    UserCategory.objects.all().delete()
    ViewedNews.objects.all().delete()
    SavedNews.objects.all().delete()


    

def populate():
    print("Starting population script...")

    # Populate Categories
    categories = {}
    for entry in news_data:
        category_name = entry['category_name']
        # Check if the category already exists
        category, created = Category.objects.get_or_create(CategoryName=category_name)
        categories[category_name] = category
        if created:
            print(f"Created new category: {category_name}")
        else:
            print(f"Category already exists: {category_name}")

    # Populate News Articles
    for entry in news_data:
        category = categories[entry['category_name']]
        title = entry['title']
        content = entry['content']
        source = entry['source']
        news_article, created = NewsArticle.objects.get_or_create(
            CategoryID=category,
            Title=title,
            Content=content,
            Source=source
        )
        if created:
            print(f"Created new news article: {title}")
        else:
            print(f"News article already exists: {title}")


# Start execution here!
if __name__ == '__main__':
    print('Deleting old data...')
    clear_existing_data()
    
    print('Starting population script...')
    populate()
