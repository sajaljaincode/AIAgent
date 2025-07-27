import openai
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_response(self, user_input: str, context: str = "") -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context: {context}"})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            role="Researcher",
            system_prompt="You are a research agent. Your job is to gather information, analyze data, and provide comprehensive research on topics. Be thorough and factual in your responses."
        )

class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Writer Agent", 
            role="Content Writer",
            system_prompt="You are a creative writer agent. Your job is to take research and information and turn it into engaging, well-structured content. Focus on clarity, flow, and readability."
        )

class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Reviewer Agent",
            role="Quality Reviewer", 
            system_prompt="You are a quality reviewer agent. Your job is to review content for accuracy, clarity, grammar, and overall quality. Provide constructive feedback and suggestions for improvement."
        )

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Coordinator Agent",
            role="Project Coordinator",
            system_prompt="You are a coordinator agent. Your job is to manage the workflow between different agents, summarize their outputs, and ensure the final result meets the user's requirements."
        )
