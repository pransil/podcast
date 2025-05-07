# AI Podcast System Architecture

## System Overview

The AI Podcast System is designed to generate dynamic, engaging podcast discussions between two AI presenters with distinct political perspectives. The system aggregates news from multiple sources, processes it through AI models, and generates natural-sounding conversations that maintain the unique personalities of each presenter.

## Core Components

### 1. Presenter System (`src/presenters/`)

#### PresenterPersonality Class
- Defines the personality traits, background, and characteristics of each AI presenter
- Maintains trusted news sources and favorite quotes for each presenter
- Generates context-aware prompts for the AI model

#### Key Presenters
- **Alex Rivera (Center-left)**
  - Progressive, analytical perspective
  - Focuses on social and economic policy
  - Trusts sources like The New York Times, NPR, and The Atlantic

- **Sam Bennett (Center-right)**
  - Conservative, business-oriented perspective
  - Emphasizes market-based solutions
  - Trusts sources like The Wall Street Journal and The Economist

### 2. News Aggregation System (`src/news/`)

#### NewsAggregator Class
- Fetches and processes news from multiple sources:
  - Traditional news APIs
  - Twitter/X for real-time updates
  - Custom news sources
- Implements relevance scoring and content filtering
- Generates discussion topics from news items

#### Key Features
- Real-time news monitoring
- Content relevance scoring
- Source credibility assessment
- Article content extraction
- Discussion topic generation

### 3. API Layer (`src/api/`)

#### FastAPI Application
- RESTful API endpoints for podcast generation
- Request/response models for data validation
- Error handling and logging
- CORS middleware for cross-origin requests

#### Key Endpoints
- `/generate-podcast`: Main endpoint for podcast generation
- `/health`: System health check
- Additional endpoints for configuration and monitoring

### 4. Configuration System (`src/config/`)

#### Settings Management
- Centralized configuration for all system components
- Environment variable management
- API key configuration
- System-wide parameters

#### Configuration Categories
- API Settings
- News Aggregation Settings
- Twitter Integration Settings
- AI Model Settings
- Podcast Generation Settings

## Data Flow

1. **News Collection**
   ```
   News Sources → NewsAggregator → Processed News Items
   ```

2. **Topic Generation**
   ```
   Processed News Items → Discussion Topics → AI Model Input
   ```

3. **Podcast Generation**
   ```
   AI Model Input → Presenter Prompts → Generated Transcript
   ```

4. **Response Delivery**
   ```
   Generated Transcript → API Response → Client
   ```

## AI Integration

### Google's NotebookLM Integration
- Uses Gemini Pro model for natural language generation
- Custom prompt engineering for each presenter
- Context-aware conversation generation
- Safety and content filtering

### Model Configuration
- Temperature: 0.7 (balanced creativity and coherence)
- Top-p: 0.8 (controlled randomness)
- Max tokens: 2048 (sufficient for detailed discussions)

## Security Considerations

1. **API Key Management**
   - Environment variable storage
   - Secure key rotation
   - Access control

2. **Content Safety**
   - AI model safety settings
   - Content filtering
   - Source verification

3. **Rate Limiting**
   - API request limits
   - Resource usage monitoring
   - Error handling

## Scalability

The system is designed to scale horizontally with:
- Asynchronous processing
- Caching mechanisms
- Modular architecture
- Stateless API design

## Future Enhancements

1. **Content Generation**
   - Multiple AI model support
   - Enhanced personality customization
   - Advanced topic analysis

2. **News Integration**
   - Additional news sources
   - Advanced content filtering
   - Real-time trend analysis

3. **User Features**
   - Custom presenter creation
   - Topic preference settings
   - Discussion style customization

## Development Guidelines

1. **Code Organization**
   - Modular design
   - Clear separation of concerns
   - Consistent naming conventions

2. **Testing**
   - Unit tests for core components
   - Integration tests for API endpoints
   - Mock services for external dependencies

3. **Documentation**
   - Code documentation
   - API documentation
   - Architecture documentation

## Deployment

The system can be deployed using:
- Docker containers
- Cloud platforms (AWS, GCP, Azure)
- Traditional server deployment

## Monitoring and Maintenance

1. **Health Checks**
   - API endpoint monitoring
   - Service status tracking
   - Error rate monitoring

2. **Logging**
   - Request logging
   - Error logging
   - Performance metrics

3. **Updates**
   - Regular dependency updates
   - Security patches
   - Feature enhancements 