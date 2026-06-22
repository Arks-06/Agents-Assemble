from app.agents.researcher import build_research_agent


agent = build_research_agent()

print("Agent initialized. Sending task...")


response = agent.run("Explain the core concept of Retrieval-Augmented Generation (RAG).")

print("\n--- AGENT OUTPUT ---")
print(f"Type: {type(response.content)}")
print(f"Data: {response.content.model_dump_json(indent=2)}")