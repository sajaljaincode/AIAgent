#!/usr/bin/env python3
"""
Multi-Agent AI System with Shared Memory
A simple demonstration of two AI agents (AgentA and AgentB) communicating through shared memory.
"""

import os
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Message:
    """Represents a message in shared memory"""
    agent_name: str
    content: str
    timestamp: str
    message_type: str = "response"  # "response" or "system"

class SharedMemory:
    """
    Simple shared memory implementation using a dictionary.
    All agents can read from and write to this shared context.
    """
    
    def __init__(self):
        self.memory: Dict[str, Any] = {
            "messages": [],  # List of all messages
            "conversation_history": [],  # Formatted conversation history
            "agent_states": {},  # Individual agent states
            "metadata": {
                "conversation_started": datetime.now().isoformat(),
                "total_messages": 0
            }
        }
    
    def add_message(self, agent_name: str, content: str, message_type: str = "response"):
        """Add a message to shared memory"""
        message = Message(
            agent_name=agent_name,
            content=content,
            timestamp=datetime.now().isoformat(),
            message_type=message_type
        )
        
        self.memory["messages"].append(asdict(message))
        self.memory["conversation_history"].append(f"[{agent_name}]: {content}")
        self.memory["metadata"]["total_messages"] += 1
        
        print(f"📝 {agent_name} added to shared memory: {content[:100]}...")
    
    def get_conversation_history(self) -> str:
        """Get formatted conversation history for context"""
        return "\n".join(self.memory["conversation_history"])
    
    def get_messages_by_agent(self, agent_name: str) -> List[Dict]:
        """Get all messages from a specific agent"""
        return [msg for msg in self.memory["messages"] if msg["agent_name"] == agent_name]
    
    def get_latest_messages(self, count: int = 5) -> List[Dict]:
        """Get the latest N messages"""
        return self.memory["messages"][-count:]
    
    def update_agent_state(self, agent_name: str, state: Dict):
        """Update an agent's state in shared memory"""
        self.memory["agent_states"][agent_name] = state
    
    def get_agent_state(self, agent_name: str) -> Dict:
        """Get an agent's state from shared memory"""
        return self.memory["agent_states"].get(agent_name, {})
    
    def print_memory_status(self):
        """Print current memory status for debugging"""
        print("\n" + "="*60)
        print("📊 SHARED MEMORY STATUS")
        print("="*60)
        print(f"Total messages: {self.memory['metadata']['total_messages']}")
        print(f"Active agents: {list(self.memory['agent_states'].keys())}")
        print(f"Conversation started: {self.memory['metadata']['conversation_started']}")
        print("Recent conversation:")
        for msg in self.memory["conversation_history"][-3:]:
            print(f"  {msg}")
        print("="*60 + "\n")

class BaseAgent:
    """Base class for AI agents with shared memory access"""
    
    def __init__(self, name: str, role: str, personality: str, shared_memory: SharedMemory):
        self.name = name
        self.role = role
        self.personality = personality
        self.shared_memory = shared_memory
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.shared_memory.update_agent_state(self.name, {
            "role": self.role,
            "personality": self.personality,
            "messages_sent": 0,
            "last_active": datetime.now().isoformat()
        })
        
        print(f"🤖 {self.name} initialized with role: {self.role}")
    
    def generate_response(self, prompt: str, use_shared_context: bool = True) -> str:
        """Generate a response using OpenAI API with optional shared context"""
        
        system_prompt = f"""You are {self.name}, an AI agent with the role of {self.role}.
        Personality: {self.personality}
        
        You are part of a multi-agent system and can access shared memory to see what other agents have said.
        Be conversational and reference previous messages when relevant.
        Keep responses concise but engaging (2-3 sentences max).
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if use_shared_context:
            conversation_history = self.shared_memory.get_conversation_history()
            if conversation_history:
                context_prompt = f"Previous conversation:\n{conversation_history}\n\nNow respond to: {prompt}"
                messages.append({"role": "user", "content": context_prompt})
            else:
                messages.append({"role": "user", "content": prompt})
        else:
            messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content.strip()
            
            self.shared_memory.add_message(self.name, response_content)
            
            state = self.shared_memory.get_agent_state(self.name)
            state["messages_sent"] += 1
            state["last_active"] = datetime.now().isoformat()
            self.shared_memory.update_agent_state(self.name, state)
            
            return response_content
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"❌ {self.name}: {error_msg}")
            return error_msg

class AgentA(BaseAgent):
    """AgentA - The Curious Questioner"""
    
    def __init__(self, shared_memory: SharedMemory):
        super().__init__(
            name="AgentA",
            role="Curious Questioner", 
            personality="You are curious, ask thoughtful questions, and love to explore new topics. You're enthusiastic and encouraging.",
            shared_memory=shared_memory
        )

class AgentB(BaseAgent):
    """AgentB - The Knowledgeable Responder"""
    
    def __init__(self, shared_memory: SharedMemory):
        super().__init__(
            name="AgentB", 
            role="Knowledgeable Responder",
            personality="You are knowledgeable, helpful, and provide detailed explanations. You're patient and enjoy sharing information.",
            shared_memory=shared_memory
        )

def run_conversation_demo():
    """
    Main driver function that demonstrates the multi-agent system with shared memory.
    Shows AgentA and AgentB having a conversation through shared memory.
    """
    
    print("🚀 Starting Multi-Agent System with Shared Memory Demo")
    print("="*70)
    
    shared_memory = SharedMemory()
    
    agent_a = AgentA(shared_memory)
    agent_b = AgentB(shared_memory)
    
    topics = [
        "What do you think about the future of artificial intelligence?",
        "How do you think AI will change education in the next 10 years?",
        "What's the most exciting technology trend you've heard about recently?"
    ]
    
    print(f"\n💬 Starting conversation between {agent_a.name} and {agent_b.name}")
    print("-" * 50)
    
    try:
        current_topic = topics[0]
        print(f"\n🎯 Topic: {current_topic}")
        
        print(f"\n🗣️ {agent_a.name} is thinking...")
        response_a = agent_a.generate_response(current_topic, use_shared_context=False)
        print(f"💭 {agent_a.name}: {response_a}")
        
        print(f"\n🗣️ {agent_b.name} is thinking...")
        response_b = agent_b.generate_response(
            "Please respond to what AgentA just said and continue the conversation.", 
            use_shared_context=True
        )
        print(f"💭 {agent_b.name}: {response_b}")
        
        for round_num in range(2, 5):
            print(f"\n--- Round {round_num} ---")
            
            print(f"\n🗣️ {agent_a.name} is thinking...")
            response_a = agent_a.generate_response(
                "Continue the conversation based on what was just said.",
                use_shared_context=True
            )
            print(f"💭 {agent_a.name}: {response_a}")
            
            print(f"\n🗣️ {agent_b.name} is thinking...")
            response_b = agent_b.generate_response(
                "Continue the conversation based on what was just said.",
                use_shared_context=True
            )
            print(f"💭 {agent_b.name}: {response_b}")
            
            if round_num % 2 == 0:
                shared_memory.print_memory_status()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Conversation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during conversation: {str(e)}")
        print("Make sure you have set up your OpenAI API key in the .env file")
    
    print("\n🏁 Final Results:")
    shared_memory.print_memory_status()
    
    print("📋 Complete Conversation History:")
    print("-" * 40)
    for i, msg in enumerate(shared_memory.memory["messages"], 1):
        print(f"{i}. [{msg['agent_name']}] {msg['content']}")
    
    print(f"\n✅ Demo completed! Total messages exchanged: {shared_memory.memory['metadata']['total_messages']}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        print("Example: OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    run_conversation_demo()
