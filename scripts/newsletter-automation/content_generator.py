#!/usr/bin/env python3
"""
AI Engineering Newsletter Content Generator

This script automatically generates newsletter content by:
1. Scraping AI/ML news from various sources
2. Analyzing trending topics on social media
3. Generating summaries using LLMs
4. Creating formatted newsletter content

Usage:
    python content_generator.py --topic "ai-engineering" --format "html"
"""

import os
import sys
import argparse
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import openai
from dotenv import load_dotenv
import feedparser
from dataclasses import dataclass
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class NewsItem:
    """Data class for news items"""
    title: str
    description: str
    url: str
    source: str
    published_date: datetime
    category: str = "general"

class NewsAggregator:
    """Aggregates news from various AI/ML sources"""
    
    def __init__(self):
        self.feeds = {
            'arxiv_ai': 'http://export.arxiv.org/rss/cs.AI',
            'arxiv_ml': 'http://export.arxiv.org/rss/cs.LG', 
            'towards_data_science': 'https://towardsdatascience.com/feed',
            'ai_news': 'https://artificialintelligence-news.com/feed/',
            'machine_learning_mastery': 'https://machinelearningmastery.com/feed/'
        }
    
    def fetch_feed_content(self, feed_url: str, source_name: str) -> List[NewsItem]:
        """Fetch and parse RSS feed content"""
        try:
            feed = feedparser.parse(feed_url)
            items = []
            
            for entry in feed.entries[:10]:  # Limit to 10 items per source
                pub_date = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                
                item = NewsItem(
                    title=entry.title,
                    description=getattr(entry, 'description', ''),
                    url=entry.link,
                    source=source_name,
                    published_date=pub_date
                )
                items.append(item)
            
            logger.info(f"Fetched {len(items)} items from {source_name}")
            return items
            
        except Exception as e:
            logger.error(f"Error fetching {source_name}: {str(e)}")
            return []
    
    def get_latest_news(self, days_back: int = 7) -> List[NewsItem]:
        """Get latest news from all sources"""
        all_news = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for source_name, feed_url in self.feeds.items():
            news_items = self.fetch_feed_content(feed_url, source_name)
            # Filter by date
            recent_items = [item for item in news_items if item.published_date >= cutoff_date]
            all_news.extend(recent_items)
        
        # Sort by publication date (newest first)
        all_news.sort(key=lambda x: x.published_date, reverse=True)
        return all_news

class ContentGenerator:
    """Generates newsletter content using AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
    def summarize_news(self, news_items: List[NewsItem], max_items: int = 20) -> str:
        """Generate a summary of news items"""
        if not news_items:
            return "No recent news found."
        
        # Prepare content for summarization
        news_content = "\n\n".join([
            f"**{item.title}**\n{item.description[:200]}...\nSource: {item.source}"
            for item in news_items[:max_items]
        ])
        
        prompt = f"""
        As an AI Engineering newsletter editor, create a comprehensive weekly summary of the following AI/ML news.
        
        Structure the summary with:
        1. Key Highlights (3-4 most important stories)
        2. Technical Developments
        3. Industry News
        4. Research Updates
        
        Keep it engaging and informative for AI engineers and practitioners.
        
        News Content:
        {news_content}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Error generating content summary."
    
    def generate_newsletter_intro(self, topic: str = "AI Engineering") -> str:
        """Generate an engaging newsletter introduction"""
        prompt = f"""
        Write an engaging introduction for this week's {topic} newsletter. 
        Make it conversational, welcoming, and highlight what readers can expect.
        Keep it under 100 words.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating intro: {str(e)}")
            return f"Welcome to this week's {topic} newsletter!"
    
    def suggest_tools_and_resources(self) -> str:
        """Generate tool recommendations"""
        prompt = """
        Suggest 3-5 trending AI engineering tools or resources that would be valuable 
        for AI engineers this week. Include a brief description of each and why it's noteworthy.
        Format as a bulleted list.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating tool suggestions: {str(e)}")
            return "• Check out the latest updates in the AI engineering ecosystem"

class NewsletterFormatter:
    """Formats newsletter content in various formats"""
    
    @staticmethod
    def format_html(title: str, intro: str, summary: str, tools: str, date: str) -> str:
        """Format newsletter as HTML"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border-left: 4px solid #667eea; background: #f8f9ff; }}
        .footer {{ text-align: center; color: #666; border-top: 1px solid #eee; padding-top: 20px; margin-top: 40px; }}
        h1 {{ margin: 0; font-size: 2.5em; }}
        h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .date {{ font-style: italic; opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 {title}</h1>
        <p class="date">{date}</p>
    </div>
    
    <div class="section">
        <h2>👋 Welcome</h2>
        <p>{intro}</p>
    </div>
    
    <div class="section">
        <h2>📰 This Week in AI</h2>
        <div>{summary}</div>
    </div>
    
    <div class="section">
        <h2>🛠️ Tools & Resources</h2>
        <div>{tools}</div>
    </div>
    
    <div class="footer">
        <p>Thank you for reading! Share this newsletter with fellow AI engineers.</p>
        <p><a href="#">Unsubscribe</a> | <a href="#">Archive</a> | <a href="#">Website</a></p>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def format_markdown(title: str, intro: str, summary: str, tools: str, date: str) -> str:
        """Format newsletter as Markdown"""
        return f"""# 🤖 {title}

*{date}*

## 👋 Welcome

{intro}

## 📰 This Week in AI

{summary}

## 🛠️ Tools & Resources

{tools}

---

Thank you for reading! Share this newsletter with fellow AI engineers.

[Unsubscribe](#) | [Archive](#) | [Website](#)
"""

def main():
    """Main function to generate newsletter content"""
    parser = argparse.ArgumentParser(description='Generate AI Engineering Newsletter Content')
    parser.add_argument('--topic', default='AI Engineering', help='Newsletter topic')
    parser.add_argument('--format', choices=['html', 'markdown'], default='html', help='Output format')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--days', type=int, default=7, help='Days back to fetch news')
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY environment variable is required")
        sys.exit(1)
    
    try:
        # Initialize components
        aggregator = NewsAggregator()
        generator = ContentGenerator()
        
        # Generate content
        logger.info("Fetching latest news...")
        news_items = aggregator.get_latest_news(days_back=args.days)
        
        logger.info("Generating newsletter content...")
        intro = generator.generate_newsletter_intro(args.topic)
        summary = generator.summarize_news(news_items)
        tools = generator.suggest_tools_and_resources()
        
        # Format output
        current_date = datetime.now().strftime("%B %d, %Y")
        title = f"{args.topic} Weekly Newsletter"
        
        if args.format == 'html':
            content = NewsletterFormatter.format_html(title, intro, summary, tools, current_date)
        else:
            content = NewsletterFormatter.format_markdown(title, intro, summary, tools, current_date)
        
        # Output content
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Newsletter saved to {args.output}")
        else:
            print(content)
        
        logger.info("Newsletter generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error generating newsletter: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()