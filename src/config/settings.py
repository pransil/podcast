from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
API_SETTINGS: Dict[str, Any] = {
    "title": "AI Podcast System",
    "description": "An AI-powered podcast system with two presenters discussing current events",
    "version": "1.0.0",
    "debug": os.getenv("DEBUG", "False").lower() == "true"
}

# News Aggregation Settings
NEWS_SETTINGS: Dict[str, Any] = {
    "max_news_items": 10,
    "min_relevance_score": 0.3,
    "cache_duration_minutes": 30,
    "sources": [
        "The New York Times",
        "The Wall Street Journal",
        "The Economist",
        "The Atlantic",
        "NPR",
        "BBC News",
        "Reuters",
        "Associated Press"
    ]
}

# Twitter Settings
TWITTER_SETTINGS: Dict[str, Any] = {
    "max_tweets": 100,
    "min_engagement": 100,
    "search_terms": [
        "breaking news",
        "just in",
        "developing",
        "update",
        "announcement"
    ]
}

# AI Model Settings
AI_SETTINGS: Dict[str, Any] = {
    "model_name": "gemini-pro",
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
    "safety_settings": {
        "harassment": "block_none",
        "hate_speech": "block_none",
        "sexually_explicit": "block_none",
        "dangerous_content": "block_none"
    }
}

# Podcast Settings
PODCAST_SETTINGS: Dict[str, Any] = {
    "default_duration_minutes": 15,
    "max_duration_minutes": 60,
    "min_duration_minutes": 5,
    "topics_per_episode": 3,
    "max_topic_duration_minutes": 20
} 