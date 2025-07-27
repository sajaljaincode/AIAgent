from agents import ResearchAgent, WriterAgent, ReviewerAgent, CoordinatorAgent
from typing import Dict
import time

class MultiAgentSystem:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.reviewer_agent = ReviewerAgent()
        self.coordinator_agent = CoordinatorAgent()
        
    def process_request(self, user_request: str) -> Dict[str, str]:
        print(f"🚀 Starting multi-agent processing for: '{user_request}'\n")
        
        print("📚 Research Agent is working...")
        research_result = self.research_agent.generate_response(
            f"Research the following topic and provide key information: {user_request}"
        )
        print(f"✅ Research completed: {research_result[:100]}...\n")
        
        print("✍️ Writer Agent is working...")
        writer_result = self.writer_agent.generate_response(
            f"Based on this research, write engaging content about: {user_request}",
            context=research_result
        )
        print(f"✅ Content created: {writer_result[:100]}...\n")
        
        print("🔍 Reviewer Agent is working...")
        review_result = self.reviewer_agent.generate_response(
            "Review this content for quality, accuracy, and improvements:",
            context=writer_result
        )
        print(f"✅ Review completed: {review_result[:100]}...\n")
        
        print("🎯 Coordinator Agent is finalizing...")
        final_result = self.coordinator_agent.generate_response(
            f"Coordinate and summarize the work done by all agents for the request: {user_request}",
            context=f"Research: {research_result}\n\nContent: {writer_result}\n\nReview: {review_result}"
        )
        print(f"✅ Final coordination completed\n")
        
        return {
            "original_request": user_request,
            "research": research_result,
            "content": writer_result, 
            "review": review_result,
            "final_summary": final_result
        }
    
    def display_results(self, results: Dict[str, str]):
        print("=" * 80)
        print("🎉 MULTI-AGENT SYSTEM RESULTS")
        print("=" * 80)
        
        print(f"\n📝 Original Request:")
        print(f"{results['original_request']}\n")
        
        print(f"📚 Research Agent Output:")
        print(f"{results['research']}\n")
        
        print(f"✍️ Writer Agent Output:")
        print(f"{results['content']}\n")
        
        print(f"🔍 Reviewer Agent Output:")
        print(f"{results['review']}\n")
        
        print(f"🎯 Coordinator Agent Final Summary:")
        print(f"{results['final_summary']}\n")
        
        print("=" * 80)

def main():
    print("🤖 Multi-Agent AI System Demo")
    print("=" * 50)
    
    system = MultiAgentSystem()
    
    example_requests = [
        "Explain the benefits of renewable energy",
        "Write about the future of artificial intelligence",
        "Describe the importance of cybersecurity in modern businesses"
    ]
    
    print("Choose a demo request or enter your own:")
    for i, request in enumerate(example_requests, 1):
        print(f"{i}. {request}")
    print("4. Enter custom request")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice in ['1', '2', '3']:
            user_request = example_requests[int(choice) - 1]
        elif choice == '4':
            user_request = input("Enter your custom request: ").strip()
        else:
            print("Invalid choice. Using default request.")
            user_request = example_requests[0]
        
        results = system.process_request(user_request)
        
        system.display_results(results)
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("Make sure you have set up your OpenAI API key in the .env file")

if __name__ == "__main__":
    main()
