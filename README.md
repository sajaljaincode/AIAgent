# AIAgent - Multi-Agent AI System Demo

A simple Python demonstration of multiple AI agents working together using OpenAI's API.

## Overview

This project demonstrates a multi-agent AI system where different AI agents collaborate to complete tasks:

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

3. Run the demo:
```bash
python multi_agent_system.py
```

## Usage

The system will present you with example requests or allow you to enter a custom request. Each agent will process the request in sequence:

1. Research Agent gathers information
2. Writer Agent creates content
3. Reviewer Agent provides feedback
4. Coordinator Agent summarizes the results

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## Example Output

The system will show the output from each agent as they work together to complete your request, demonstrating how multiple AI agents can collaborate effectively.
