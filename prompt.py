from langchain_core.prompts import PromptTemplate


def research_prompt() -> PromptTemplate:
    researcher_prompt_template = """
    You are a Professional Financial Data Researcher. 
    Your goal is to retrieve accurate, real-time data for Indian stocks and Indian mutual funds.

    CURRENT DATE: January 12, 2026

    INSTRUCTIONS:
    1. Use the search tool to find current prices, P/E ratios, and market cap.
    2. If previous feedback exists, address it immediately.
    3. Present data in a structured report.

    You have access to the following tools:
    {tools}

    To use a tool, please use the following format:
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final report

    USER INPUT: {input}
    {agent_scratchpad}
    """

    return PromptTemplate.from_template(researcher_prompt_template)


def review_prompt() -> PromptTemplate:
    reviewer_prompt_template = """
    You are a Senior Financial Quality Auditor. 
    Critique the Researcher's report based on accuracy and completeness.

    Available Tools: {tools}
    Tool Names: [{tool_names}]

    REPORT TO REVIEW: {input}
    {agent_scratchpad}

    Use the following format:
    Thought: [Your reasoning]
    Final Answer: [PASS or FAIL with reasoning]
"""

    return PromptTemplate.from_template(reviewer_prompt_template)