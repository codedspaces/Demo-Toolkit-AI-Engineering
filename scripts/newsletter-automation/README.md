# 📰 Newsletter Automation Scripts

This directory contains scripts for automating various aspects of newsletter creation and management for AI engineering content.

## 🚀 Quick Start

### Prerequisites
```bash
pip install openai feedparser python-dotenv requests beautifulsoup4
```

### Environment Setup
Create a `.env` file in your project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
NEWSLETTER_API_KEY=your_newsletter_platform_api_key
SOCIAL_MEDIA_TOKENS=your_social_media_api_tokens
```

## 📝 Scripts Overview

### 1. Content Generator (`content_generator.py`)
Automatically generates newsletter content by aggregating AI/ML news and creating summaries.

**Features:**
- Scrapes RSS feeds from top AI/ML sources
- Generates engaging summaries using GPT-4
- Creates tool recommendations
- Outputs HTML or Markdown format

**Usage:**
```bash
python content_generator.py --topic "AI Engineering" --format "html" --output "newsletter.html"
```

**Options:**
- `--topic`: Newsletter topic (default: "AI Engineering")
- `--format`: Output format (html/markdown)
- `--output`: Output file path
- `--days`: Days back to fetch news (default: 7)

### 2. Social Media Publisher (`social_media_publisher.py`)
Automatically posts newsletter content to social media platforms.

**Features:**
- Twitter/X integration
- LinkedIn posting
- Custom message formatting
- Hashtag optimization

**Usage:**
```bash
python social_media_publisher.py --content "newsletter.html" --platforms "twitter,linkedin"
```

### 3. Subscriber Analytics (`subscriber_analytics.py`)
Analyzes newsletter performance and subscriber engagement.

**Features:**
- Open rate tracking
- Click-through analysis
- Subscriber growth metrics
- Engagement reports

**Usage:**
```bash
python subscriber_analytics.py --period "weekly" --export "csv"
```

### 4. Email Scheduler (`email_scheduler.py`)
Schedules and sends newsletters to subscribers.

**Features:**
- Batch email sending
- Personalization
- A/B testing support
- Delivery tracking

**Usage:**
```bash
python email_scheduler.py --template "newsletter.html" --schedule "2024-01-15 09:00"
```

## 🔧 Configuration

### News Sources
Edit the `feeds` dictionary in `content_generator.py` to customize news sources:

```python
self.feeds = {
    'arxiv_ai': 'http://export.arxiv.org/rss/cs.AI',
    'your_source': 'https://your-source.com/feed',
    # Add more sources
}
```

### Newsletter Templates
Customize the HTML and Markdown templates in the `NewsletterFormatter` class.

### API Integration
The scripts support various newsletter platforms:
- Substack
- ConvertKit
- Mailchimp
- Custom SMTP

## 📊 Workflow Examples

### Weekly Newsletter Generation
```bash
# Generate content
python content_generator.py --days 7 --output weekly_newsletter.html

# Post to social media
python social_media_publisher.py --content weekly_newsletter.html

# Send to subscribers
python email_scheduler.py --template weekly_newsletter.html

# Analyze performance
python subscriber_analytics.py --period weekly
```

### Custom Content Pipeline
```bash
# Generate specialized content
python content_generator.py --topic "LLM Engineering" --format markdown

# Custom social media campaign
python social_media_publisher.py --content custom_post.md --hashtags "#LLM #AI"
```

## 🔍 Monitoring & Analytics

### Performance Metrics
- Open rates
- Click-through rates
- Subscriber growth
- Social media engagement
- Content performance

### Automated Reports
Set up automated reports to track:
- Weekly subscriber statistics
- Content engagement metrics
- Social media reach
- Revenue attribution

## 🛠️ Advanced Features

### AI-Powered Personalization
- Subscriber interest analysis
- Dynamic content generation
- Optimal send time prediction
- Subject line optimization

### Integration Capabilities
- CRM integration
- Analytics platforms
- Social media management tools
- Email marketing platforms

## 🚨 Error Handling

The scripts include comprehensive error handling for:
- API rate limits
- Network connectivity issues
- Content parsing errors
- Authentication failures

## 📈 Scaling Considerations

### Performance Optimization
- Async processing for large subscriber lists
- Content caching
- API rate limiting
- Batch processing

### Infrastructure
- Cloud deployment options
- Database integration
- Queue management
- Monitoring and alerting

## 🔐 Security

### Best Practices
- Environment variable management
- API key rotation
- Secure data transmission
- Subscriber data protection

### Compliance
- GDPR compliance features
- CAN-SPAM compliance
- Data retention policies
- Unsubscribe handling

## 🤝 Contributing

To contribute to the newsletter automation scripts:

1. Test your changes with sample data
2. Update documentation
3. Follow security best practices
4. Add error handling
5. Include example usage

## 📚 Additional Resources

- [Newsletter Growth Strategies](../../learning-resources/newsletter-growth/)
- [Content Creation Best Practices](../../templates/newsletter/)
- [API Documentation](./docs/api-reference.md)
- [Troubleshooting Guide](./docs/troubleshooting.md)