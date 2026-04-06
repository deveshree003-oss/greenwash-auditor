from crewai import Agent, Task, Crew

# Define Agents
csr_agent = Agent(
    role="CSR Analyst",
    goal="Extract sustainability claims",
    backstory="Expert in ESG reports"
)

finance_agent = Agent(
    role="Financial Analyst",
    goal="Analyze financial filings",
    backstory="Expert in capex and investments"
)

reasoning_agent = Agent(
    role="ESG Auditor",
    goal="Find contradictions",
    backstory="Detects greenwashing"
)


def run_crew(csr_text, finance_text):

    task1 = Task(
        description=f"Extract ESG claims from: {csr_text[:2000]}",
        agent=csr_agent
    )

    task2 = Task(
        description=f"Analyze financial data: {finance_text[:2000]}",
        agent=finance_agent
    )

    task3 = Task(
        description="Compare both and find contradictions",
        agent=reasoning_agent
    )

    crew = Crew(
        agents=[csr_agent, finance_agent, reasoning_agent],
        tasks=[task1, task2, task3],
        verbose=True  # 🔥 IMPORTANT (gives logs)
    )

    result = crew.kickoff()
    return result