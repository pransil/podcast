import os
import json
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
import tweepy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class NewsAggregator:
    def __init__(self):
        self.twitter_client = self._setup_twitter_client()
        
    def _setup_twitter_client(self) -> tweepy.Client:
        """Initialize Twitter API client."""
        try:
            # Check if all required Twitter credentials are present
            required_credentials = [
                "TWITTER_API_KEY",
                "TWITTER_API_SECRET",
                "TWITTER_ACCESS_TOKEN",
                "TWITTER_ACCESS_SECRET"
            ]
            
            missing_credentials = [
                cred for cred in required_credentials 
                if not os.getenv(cred)
            ]
            
            if missing_credentials:
                logger.warning(
                    f"Missing Twitter credentials: {', '.join(missing_credentials)}. "
                    "Twitter integration will be disabled."
                )
                return None
                
            return tweepy.Client(
                consumer_key=os.getenv("TWITTER_API_KEY"),
                consumer_secret=os.getenv("TWITTER_API_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
            )
        except Exception as e:
            logger.warning(f"Failed to initialize Twitter client: {e}")
            return None

    async def get_news_summaries(self) -> List[Dict[str, Any]]:
        """Fetch and aggregate news from various sources."""
        news_items = []
        
        # Fetch from news APIs
        try:
            news_items.extend(await self._fetch_news_api())
        except Exception as e:
            logger.warning(f"Failed to fetch news from APIs: {e}")
        
        # Fetch from Twitter if client is available
        if self.twitter_client:
            try:
                twitter_news = await self._fetch_twitter_news()
                if twitter_news:
                    news_items.extend(twitter_news)
            except Exception as e:
                logger.warning(f"Failed to fetch Twitter news: {e}")
        
        # If we have no news items, add some sample items
        if not news_items:
            logger.info("No news items available, using sample news")
            news_items = self._get_sample_news()
        
        # Sort by relevance and recency
        news_items.sort(key=lambda x: (x.get('relevance_score', 0), x.get('published_at', datetime.min)), reverse=True)
        
        return news_items[:10]  # Return top 10 most relevant items

    def _get_sample_news(self) -> List[Dict[str, Any]]:
        """Return sample news items when no real news is available."""
        return [
            {
                'title': 'Economic Growth Shows Strong Recovery',
                'summary': 'Recent economic indicators show strong recovery in key sectors, with job growth exceeding expectations.',
                'source': 'Sample News',
                'url': 'https://example.com/news/1',
                'published_at': datetime.now(),
                'relevance_score': 0.9
            },
            {
                'title': 'New Infrastructure Bill Passes Senate',
                'summary': 'Bipartisan infrastructure bill passes with support from both parties, promising major investments in roads, bridges, and broadband.',
                'source': 'Sample News',
                'url': 'https://example.com/news/2',
                'published_at': datetime.now() - timedelta(days=1),
                'relevance_score': 0.85
            },
            {
                'title': 'Climate Change Initiatives Gain Momentum',
                'summary': 'Cities and states across the country are implementing innovative solutions to address climate change challenges.',
                'source': 'Sample News',
                'url': 'https://example.com/news/3',
                'published_at': datetime.now() - timedelta(days=2),
                'relevance_score': 0.8
            },
            {
                'title': 'Education Reform Bill Introduced',
                'summary': 'New education reform bill aims to improve access to quality education and address achievement gaps.',
                'source': 'Sample News',
                'url': 'https://example.com/news/4',
                'published_at': datetime.now() - timedelta(days=3),
                'relevance_score': 0.75
            }
        ]

    async def _fetch_news_api(self) -> List[Dict[str, Any]]:
        """Fetch news from various news APIs."""
        # This is a placeholder - you would implement actual API calls here
        # For now, return sample news
        return self._get_sample_news()

    async def _fetch_twitter_news(self) -> List[Dict[str, Any]]:
        """Fetch relevant news from Twitter."""
        if not self.twitter_client:
            return []
            
        try:
            # Search for trending topics and news
            tweets = self.twitter_client.search_recent_tweets(
                query="news OR breaking OR update",
                max_results=100,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations']
            )
            
            news_items = []
            for tweet in tweets.data or []:
                news_items.append({
                    'title': tweet.text[:100] + '...',
                    'summary': tweet.text,
                    'source': 'Twitter',
                    'url': f"https://twitter.com/user/status/{tweet.id}",
                    'published_at': tweet.created_at,
                    'relevance_score': self._calculate_tweet_relevance(tweet)
                })
            
            return news_items
        except Exception as e:
            logger.warning(f"Error fetching Twitter news: {e}")
            return []

    def _calculate_tweet_relevance(self, tweet: Any) -> float:
        """Calculate relevance score for a tweet based on various factors."""
        # Implement relevance scoring logic here
        # Consider factors like:
        # - Engagement metrics
        # - Account credibility
        # - Topic relevance
        # - Time sensitivity
        return 0.5  # Placeholder score

    def _extract_article_content(self, url: str) -> str:
        """Extract main content from a news article URL."""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()
            
            # Extract main content (this would need to be customized per news source)
            content = soup.find('article') or soup.find('main') or soup.find('body')
            return content.get_text() if content else ""
        except Exception as e:
            logger.warning(f"Error extracting article content: {e}")
            return ""

    def generate_discussion_topics(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate discussion topics from news items."""
        topics = []
        for item in news_items:
            topics.append({
                'title': item['title'],
                'summary': item['summary'],
                'source': item['source'],
                'url': item['url'],
                'discussion_points': [
                    "What are the key implications of this news?",
                    "How might this affect different stakeholders?",
                    "What historical context is relevant here?",
                    "What are potential future developments?"
                ]
            })
        return topics 