# Personal Financial AI Agent Assistant

> **🚧 Proof of Concept** - A stateful multi-agent AI system for personalized financial advice using LangGraph, LangChain, and MCP tools.

## Overview

A **multi-agent AI system** that combines specialized financial agents to deliver personalized financial advice. Each agent focuses on a specific domain and collaborates through a cyclical LangGraph orchestration layer, allowing for iterative research and quality review.

### 🤖 AI Agents

| Agent                    | Role              | Status            | Capabilities                                                         |
| ------------------------ | ----------------- | ----------------- | -------------------------------------------------------------------- |
| 💼 Investment Agent      | Specialist        | ✅ Active         | Portfolio recommendations, market analysis                           |
| 🔍 Review Agent          | Quality Control   | ✅ Active         | Validates outputs, provides feedback, ensures consistency            |
| 🎯 Supervisor Agent      | Orchestrator      | 🔄 In Development | Routes queries, manages workflow, coordinates agents                 |
| 🤖 Generalist Agent      | General Assistant | 📋 Planned        | Handles general queries unrelated to finance, conversational support |
| 📊 Tax Specialist Agent  | Specialist        | 🔄 In Development | Tax optimization, deduction strategies                               |
| ⚠️ Risk Assessment Agent | Specialist        | 📋 Planned        | Risk evaluation, mitigation strategies                               |
| 💰 Budget Planner Agent  | Specialist        | 📋 Planned        | Expense tracking, budget optimization                                |

**Technology:** LangGraph • LangChain • Model Context Protocol (MCP) • Python 3.11+

**Agent Flow (Powered by LangGraph `StateGraph`):**

1. 🎯 **User Query** is passed into the initial state.
2. 💼 **Investment Agent (Researcher)** performs analysis using Search tools and generates a report.
3. 🔍 **Review Agent** validates the output.
4. **Conditional Router:**
   - If Reviewer replies with `PASS` ➡️ Return final response to User.
   - If Reviewer replies with `FAIL` ➡️ Loop back to the Researcher with feedback for refinement (up to 3 iterations).

### 🔌 MCP Servers Integration

The system will leverage multiple MCP servers to extend functionality:

- **Web Search Server**

  - Real-time market data and financial news retrieval
  - General web search for non-financial queries (Generalist Agent)
  - _Current_: Using LangChain Google Search Wrapper
  - _Planned_: Migration to dedicated MCP Search server

- **File Data Server** _(planned)_

  - Excel/CSV file processing for user-provided portfolio data
  - Historical transaction analysis

- **Database Server** _(planned)_
  - Persistent storage for user preferences and transaction history
  - Portfolio tracking across sessions

### 💻 User Interface

- **Current:** Streamlit-based chat UI with real-time agent interaction ✅
- **Next Phase:** Migration to React/Next.js for production-ready web application _(planned)_

## 🏗️ Architecture

### Current (v1.5 - LangGraph State Orchestration)

The system currently uses a cyclic graph architecture to ensure high-quality outputs.

**Flow:**

1. User submits financial query via Streamlit chat interface.
2. The `StateGraph` initializes the state dictionary.
3. **Research Node** fetches real-time data and drafts a plan.
4. **Review Node** audits the plan.
5. If the plan fails the audit, it is routed back to the Research Node with constructive feedback.
6. Final verified response returned to user in chat UI.

### Planned (v2.0 - Supervisor Routing + MCP)

**Enhanced Multi-Agent System:**

- 🎯 **Supervisor/Orchestrator** - Routes queries, manages workflow
- 🤖 **Generalist Agent** - General conversational queries
- 💼 **Specialist Agents** - Investment, Tax, Risk, Budget
- 🔍 **Review Agent** - Quality control & feedback

## 🚀 Quick Start

### Prerequisites

- **uv** - Python package and project manager
- Python 3.11+
- `.env` file containing your `GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `GOOGLE_CSE_ID`

### Installation

```bash
# Install uv
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run streamlit.py
```
