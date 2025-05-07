import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from ..presenters.personalities import ALEX, SARA, get_presenter_prompt
from ..news.aggregator import NewsAggregator

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded")

# Get API key and validate
google_api_key = os.getenv("GOOGLE_API_KEY")
logger.debug(f"GOOGLE_API_KEY present: {'Yes' if google_api_key else 'No'}")
if not google_api_key:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please create a .env file with your Google API key. "
        "You can get one from https://makersuite.google.com/app/apikey"
    )

# Configure Google's Generative AI
try:
    genai.configure(api_key=google_api_key)
    # List available models to verify access
    models = genai.list_models()
    available_models = [model.name for model in models]
    logger.debug(f"Available models: {available_models}")
    
    if 'models/gemini-1.5-pro' not in available_models:
        raise ValueError("Gemini Pro model not available. Please check your API key and access.")
        
    logger.debug("Successfully configured Google AI")
except Exception as e:
    logger.error(f"Error configuring Google AI: {str(e)}")
    raise

app = FastAPI(title="AI Podcast System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PodcastRequest(BaseModel):
    topic: str
    duration_minutes: int = 15

class PodcastResponse(BaseModel):
    title: str
    transcript: str
    topics: List[Dict[str, Any]]

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Podcast System"}

@app.post("/generate-podcast", response_model=PodcastResponse)
async def generate_podcast(request: PodcastRequest):
    try:
        # Initialize news aggregator
        news_aggregator = NewsAggregator()
        
        # Get news summaries
        news_items = await news_aggregator.get_news_summaries()
        
        # Generate discussion topics
        topics = news_aggregator.generate_discussion_topics(news_items)
        
        # Initialize the model with the correct name
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate podcast transcript
        transcript = await generate_transcript(model, topics, request.duration_minutes)
        
        return PodcastResponse(
            title=f"AI Podcast: {request.topic}",
            transcript=transcript,
            topics=topics
        )
    except Exception as e:
        logger.error(f"Error generating podcast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_transcript(model: Any, topics: List[Dict[str, Any]], duration_minutes: int) -> str:
    """Generate a podcast transcript using the AI model."""
    
    # Get current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Ensure we have exactly 4 topics for the news summary segment
    news_topics = topics[:4]
    
    # Create the conversation context
    context = f"""Generate a {duration_minutes}-minute podcast discussion between two hosts: {ALEX.name} and {SARA.name}.

The podcast should follow this structure:

1. Introduction (2-3 minutes):
   - Start with a warm greeting and mention today's date: {current_date}
   - Briefly mention that they'll be discussing significant political and economic news from the past week
   - Introduce the special topic for this week's show
   - Keep the introduction engaging and natural

2. News Summary Segment (8-10 minutes):
   For each of these 4 topics (spend about 2 minutes per topic):
   {chr(10).join(f'- {topic["title"]}: {topic["summary"]}' for topic in news_topics)}

   For each topic, follow this pattern:
   a) First presenter gives a non-partisan summary of the news
   b) First presenter asks the other presenter for their perspective
   c) Second presenter responds with their perspective, consistent with their political view
   d) Second presenter asks a follow-up question
   e) First presenter responds with their perspective
   f) Brief back-and-forth discussion (30-45 seconds)
   g) Smooth transition to next topic

3. Main Topic Discussion (5-7 minutes):
   Focus on a current issue where both conservatives and liberals agree America can do better.
   Follow this structure:
   a) First presenter introduces the topic and explains why it's important for America's future
   b) First presenter asks the other presenter for their thoughts and ideas for improvement
   c) Second presenter shares their perspective and specific suggestions
   d) Back-and-forth discussion incorporating:
      - Recent news relevant to the topic
      - Data and statistics when available
      - Specific examples of what's working or not working
      - Concrete ideas for improvement
   e) If the issue can be explained with data visualization:
      - Describe what the graph/chart would show
      - Explain the key trends and patterns
      - Discuss what the data means for America's future
      - Use the visualization to support specific improvement suggestions

4. Closing Segment (3-4 minutes):
   Each presenter finds common ground with the other's political goals:
   a) {ALEX.name} (liberal) should:
      - Choose a current conservative policy goal or initiative
      - Find genuine positive aspects in it
      - Explain how it could work and be beneficial from a liberal perspective
      - Suggest how it could be implemented in a way that aligns with liberal values
   
   b) {SARA.name} (conservative) should:
      - Choose a current liberal policy goal or initiative
      - Find genuine positive aspects in it
      - Explain how it could work and be beneficial from a conservative perspective
      - Suggest how it could be implemented in a way that aligns with conservative values
   
   c) End with a brief, positive reflection on finding common ground

Remember:
- Keep the tone engaging, conversational, and fun
- Both hosts should be polite and open-minded
- Look for opportunities to find common ground
- Show genuine curiosity about different perspectives
- Use their favorite quotes when relevant
- Reference their trusted sources when appropriate
- Maintain a good pace - about 2 minutes per news topic
- Ensure smooth transitions between topics
- Focus on constructive solutions and improvements
- Use data and examples to support points
- Keep the discussion forward-looking and solution-oriented
- In the closing segment, be genuine and specific about finding common ground
- End on a positive, hopeful note about America's future
"""

    try:
        # Generate the transcript - note that generate_content is not async
        response = model.generate_content(
            context,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        
        if not response or not response.text:
            raise ValueError("No response generated from the model")
            
        return response.text
    except Exception as e:
        logger.error(f"Error generating transcript: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate podcast transcript: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 