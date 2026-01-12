from langchain_classic.agents import AgentExecutor, create_react_agent


def research_agent(llm, search, research_prompt):
    researcher_agent = create_react_agent(llm, [search], research_prompt)
    return AgentExecutor(
        agent=researcher_agent, 
        tools=[search], 
        verbose=False, 
        handle_parsing_errors=True
    )


def reviewer_agent(llm, review_prompt):
    reviewer_agent = create_react_agent(llm=llm, prompt=review_prompt, tools=[])
    return AgentExecutor(
        agent=reviewer_agent, 
        tools=[], 
        verbose=False, 
        handle_parsing_errors=True
    )
