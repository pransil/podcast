# AI Podcast Generator
**** Note - this project was mostly about testing the cursor.ai programming tool to see what it is capable of doing for me. Currently the real news feeds are not working so it is all 'example' (ie fake) news summaries.
*****

An AI-powered podcast generator that creates engaging political discussions between two hosts with different perspectives. The system uses Google's Gemini AI model to generate natural-sounding conversations about current events and political topics.

## Features

- Generates podcast transcripts with two hosts (Alex and Sara)
- Integrates with news APIs to get current topics
- Uses Google's Gemini AI for natural conversation generation
- Structured podcast format with introduction, news summary, main topic, and closing segments
- Fallback to sample news when external APIs are unavailable

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-podcast-generator.git
cd ai-podcast-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
```

## Usage

1. Start the server:
```bash
uvicorn src.api.main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

3. Generate a podcast by making a POST request to `/generate-podcast` with:
```json
{
    "topic": "Your Topic",
    "duration_minutes": 15
}
```

## API Endpoints

- `POST /generate-podcast`: Generate a new podcast transcript
- `GET /health`: Check API health status

## Project Structure

```
src/
├── api/
│   └── main.py           # FastAPI application
├── news/
│   └── aggregator.py     # News aggregation logic
└── utils/
    └── config.py         # Configuration and constants
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 