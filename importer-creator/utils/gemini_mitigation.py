import sys
import time


def invoke_with_retry(agent, input_data, max_retries=3, delay=1):
    """
    Invoke an agent with retry logic to mitigate Gemini 2.5 Pro empty response issues.
    
    Args:
        agent: The agent to invoke
        input_data: Input data for the agent (string or dict)
        max_retries: Maximum number of retries (default 3)
        delay: Delay between retries in seconds (default 1)
    
    Returns:
        Agent response with validated output
        
    Raises:
        SystemExit: If all retries fail to produce a valid response
    """
    
    for attempt in range(max_retries):
        try:
            print(f"Invoking agent (attempt {attempt + 1}/{max_retries})...")
            response = agent.invoke(input_data)
            
            # Get the output from response
            if hasattr(response, 'get'):
                response_output = response.get("output")
            else:
                response_output = response
            
            # Validate response is not empty (Gemini 2.5 Pro mitigation)
            if response_output and str(response_output).strip():
                print("✓ Valid response received")
                return response
            else:
                print(f"⚠ WARNING: Empty response from agent on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
        
        except Exception as e:
            print(f"⚠ WARNING: Exception on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                raise
    
    print("❌ ERROR: All retry attempts failed to produce a valid response")
    print("This is likely due to Gemini 2.5 Pro returning empty responses.")
    print("Consider checking your API key or model configuration.")
    sys.exit(1)


def validate_response_content(response, min_length=10):
    """
    Validate that a response contains meaningful content.
    
    Args:
        response: The response to validate
        min_length: Minimum length for valid content (default 10)
    
    Returns:
        bool: True if response is valid, False otherwise
    """
    if not response:
        return False
    
    response_str = str(response).strip()
    if len(response_str) < min_length:
        return False
    
    # Check for common empty/error patterns
    empty_patterns = ["", "null", "none", "{}", "[]"]
    if response_str.lower() in empty_patterns:
        return False
    
    return True 