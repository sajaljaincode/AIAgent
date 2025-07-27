# AIAgent - Multi-Agent AI System with Shared Memory

A simple Python demonstration of AI agents communicating through shared memory using OpenAI's API.

## Overview

This project demonstrates two different multi-agent AI systems:

### 1. Shared Memory System (shared_memory_agents.py) - **MAIN DEMO**
- **AgentA (Curious Questioner)**: Asks thoughtful questions and explores topics
- **AgentB (Knowledgeable Responder)**: Provides detailed explanations and information
- **Shared Memory**: Both agents read from and write to a common memory structure
- **Real-time Communication**: Agents can see and respond to each other's messages

### 2. Sequential Processing System (multi_agent_system.py)
- **Research Agent**: Gathers information and analyzes data
- **Writer Agent**: Creates engaging content based on research
- **Reviewer Agent**: Reviews content for quality and accuracy
- **Coordinator Agent**: Manages workflow and provides final summaries

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. Run the shared memory demo (recommended):
```bash
python shared_memory_agents.py
```

Or run the sequential processing demo:
```bash
python multi_agent_system.py
```

## Shared Memory System Features

- **Two AI Agents**: AgentA and AgentB with distinct personalities
- **Shared Memory**: Dictionary-based memory system that both agents can access
- **Message History**: Complete conversation history with timestamps
- **Agent States**: Individual agent state tracking
- **Real-time Updates**: Agents can see what others have written
- **Error Handling**: Graceful handling of API errors and interruptions

## Example Usage

The shared memory system will automatically start a conversation between AgentA and AgentB:

```
🚀 Starting Multi-Agent System with Shared Memory Demo
🤖 AgentA initialized with role: Curious Questioner  
🤖 AgentB initialized with role: Knowledgeable Responder

💬 Starting conversation between AgentA and AgentB
🎯 Topic: What do you think about the future of artificial intelligence?

💭 AgentA: I'm really fascinated by AI's potential! What aspects of AI development do you think will have the biggest impact on society in the next decade?

💭 AgentB: Great question! I believe the integration of AI in education and healthcare will be transformative, making personalized learning and early disease detection more accessible than ever before.
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection

## Code Structure

- `shared_memory_agents.py`: Main shared memory demo with AgentA and AgentB
- `multi_agent_system.py`: Sequential processing system demo
- `agents.py`: Base agent classes for the sequential system
- `requirements.txt`: Python dependencies
- `.env.example`: Environment variable template

## Example Output

The shared memory system shows:
- Real-time agent communication
- Shared memory status updates
- Complete conversation history
- Agent state tracking
- Message timestamps and metadata
