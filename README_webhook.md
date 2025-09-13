# LinkedIn Profile Search Webhook API

A Flask-based webhook server that receives search queries from n8n and returns LinkedIn profile search results.

## Features

- **Webhook Endpoint**: Receives POST requests from n8n with search parameters
- **LinkedIn Scraping**: Uses undetected Chrome driver to bypass Google's bot detection
- **JSON Response**: Returns structured data perfect for n8n workflows
- **Error Handling**: Comprehensive error handling and logging
- **Health Check**: Built-in health monitoring endpoint

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the webhook server:
```bash
python webhook_server.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /webhook/linkedin-search
Main webhook endpoint for LinkedIn profile searches.

**Request Body:**
```json
{
  "search_query": "(CEO OR COO OR \"Managing Director\") \"APM - Australian Property Management\" site:linkedin.com/in",
  "company_name": "APM - Australian Property Management",
  "job_titles": ["CEO", "COO", "Managing Director", "Sales Director"]
}
```

**Response:**
```json
{
  "success": true,
  "query": "(CEO OR COO OR \"Managing Director\") \"APM - Australian Property Management\" site:linkedin.com/in",
  "results_count": 5,
  "profiles": [
    {
      "url": "https://www.linkedin.com/in/john-doe-ceo/",
      "meta_title": "John Doe - CEO at APM - Australian Property Management",
      "description": "Experienced CEO with 10+ years in property management...",
      "additional_info": "Melbourne, Victoria, Australia · CEO · APM Group",
      "headings": ["John Doe - CEO at APM - Australian Property Management"]
    }
  ],
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /
API documentation endpoint.

## n8n Integration

### 1. HTTP Request Node Configuration

**Method:** POST  
**URL:** `http://localhost:5000/webhook/linkedin-search`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "company_name": "{{ $json.company_name }}",
  "job_titles": ["CEO", "COO", "Managing Director", "Sales Director", "Marketing Director", "Founder", "Co-Founder", "Partner", "Managing Partner"]
}
```

### 2. Alternative: Custom Search Query

```json
{
  "search_query": "{{ $json.custom_search_query }}"
}
```

### 3. Response Processing in n8n

The webhook returns a structured JSON response that you can easily process in n8n:

- `success`: Boolean indicating if the search was successful
- `query`: The actual search query used
- `results_count`: Number of profiles found
- `profiles`: Array of profile objects with:
  - `url`: LinkedIn profile URL
  - `meta_title`: Profile title/name
  - `description`: Profile description
  - `additional_info`: Additional profile information
  - `headings`: Array of headings found

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Missing required parameters
- **500 Internal Server Error**: Search failed (usually due to bot detection)
- **JSON Error**: Invalid JSON in request body

## Logging

The server includes detailed logging for debugging:
- Search queries received
- Browser setup and navigation
- LinkedIn profiles found
- Errors and warnings

## Security Notes

- The server runs in headless mode for better performance
- Uses undetected Chrome driver to avoid bot detection
- Includes comprehensive anti-fingerprinting measures
- Randomizes user agents and browser behavior

## Troubleshooting

### Common Issues

1. **"Failed to setup browser"**
   - Ensure Chrome is installed on your system
   - Check that undetected-chromedriver is properly installed

2. **"Failed to perform search - possible bot detection"**
   - Google is blocking the search
   - Try running at different times
   - The server will automatically retry with different parameters

3. **"No LinkedIn profiles found"**
   - The search query might be too specific
   - Try broader search terms
   - Check if the company name is correct

### Debug Mode

To enable debug logging, modify the logging level in `webhook_server.py`:

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## Example n8n Workflow

1. **Trigger Node**: Manual trigger or webhook
2. **HTTP Request Node**: Send search request to the webhook
3. **Code Node**: Process the response data
4. **Email Node**: Send results via email
5. **Google Sheets Node**: Save results to spreadsheet

## Production Deployment

For production use:

1. Use a production WSGI server like Gunicorn
2. Set up proper logging
3. Add authentication if needed
4. Use environment variables for configuration
5. Set up monitoring and health checks

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 webhook_server:app
```
