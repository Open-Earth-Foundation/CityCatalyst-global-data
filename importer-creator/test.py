from utils.agent_creation import create_agent_with_rag_and_csv_filter

# Create the agent
agent = create_agent_with_rag_and_csv_filter(verbose=True)

# Define a test query
test_query = """
Please find the emission factors where actor_name is world and 'gpc_refno' is 'I.1.1' and the gas is CO2 adn the unit is 'kg/m3'
Use the FilterData tool to retrieve this information.
"""

# Run the agent on the test query
response = agent.invoke(test_query)

# Print the agent's response
print("\nAgent's Response:")
print(response)
