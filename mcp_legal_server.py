import httpx  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from mcp.server.fastmcp import FastMCP  # type: ignore
from ddgs import DDGS  # type: ignore

# Create an MCP server
mcp = FastMCP("Internet Legal Assistant")

# Initialize DuckDuckGo Search
ddgs = DDGS()

@mcp.tool()
def search_indian_law(query: str, max_results: int = 5) -> str:
    """
    Search the internet for legal information, precedents, and procedures.
    Always prefix searches with "Indian law" to ensure accurate regional results.
    
    Args:
        query: The legal search term or question to look up.
        max_results: The maximum number of search results to return (default 5).
    """
    try:
        # Append "Indian law" to implicitly target Indian law context
        search_query = f"{query} Indian law"
        
        # Perform the search
        results = [r for r in ddgs.text(search_query, max_results=max_results)]
        
        if not results:
            return "No relevant legal information found for this query on the internet."
            
        formatted_results = "Here are the top web search results for your query:\n\n"
        for i, res in enumerate(results, 1):
            formatted_results += f"[{i}] {res['title']}\n"
            formatted_results += f"Source: {res['href']}\n"
            formatted_results += f"Summary: {res['body']}\n\n"
            
        return formatted_results
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@mcp.tool()
def read_legal_article(url: str) -> str:
    """
    Fetches and reads the text content of a specific webpage or article URL.
    Use this if a search result looks promising and you need more details from the page to answer.
    
    Args:
        url: The full URL of the webpage to read.
    """
    try:
        # Use httpx to get the page content
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        
        # Parse text using beautifulsoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator='\\n')
        
        # Collapse multiple newlines and spaces
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\\n'.join(chunk for chunk in chunks if chunk)
        
        # Return first 8000 characters to avoid context overflow for the LLM
        return text[:8000] + "\\n...[Content Truncated]..." if len(text) > 8000 else text  # type: ignore
    except Exception as e:
        return f"Error reading the webpage: {str(e)}"

@mcp.prompt()
def legal_assistant_prompt() -> str:
    """
    The main system prompt for the Legal AI Agent.
    """
    return '''You are 'AI Legal Assistant', a highly professional, polite, and helpful legal expert specializing in Indian law (FIRs, Tenant Rights, Bail, Consumer Protection, etc.). 

# BEHAVIOR GUIDELINES:
1. **Casual Conversation:** You may engage in brief, polite small talk, greetings, or farewells (e.g., "Hello! How can I help you?", "Goodbye!"). Answer these naturally WITHOUT using any tools.
2. **Legal Queries:** If the user asks a legal question, ALWAYS use the `search_indian_law` tool first to find accurate, up-to-date information from the internet. If a specific source looks useful, use `read_legal_article` to get the full text. Do not guess or hallucinate laws.
3. **Strict Domain Boundary:** You are strictly a legal assistant. If the user asks you to do something outside the legal domain (e.g., write a poem, write code, give medical advice, talk about sports), you MUST politely refuse.

# REFUSAL TEMPLATE:
If a user asks a non-legal question, reply exactly with: "I apologize, but I am specialized exclusively in legal assistance. I cannot help with that topic. However, I would be happy to help you with tenant rights, filing complaints, or explaining legal procedures in India."'''

if __name__ == "__main__":
    # Start the FastMCP server
    mcp.run()
