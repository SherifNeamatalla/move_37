from src.tools.single_function_agents.zapier import zapier_agent

query = "List me all the events in the next 2 days"
zapier_agent.run({
    "query": query,
})
