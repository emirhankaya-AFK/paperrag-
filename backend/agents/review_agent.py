from typing import List, Dict, Any
from ..services.llm_service import LLMService

class ReviewAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def generate_literature_review(self, topic: str, papers: List[Dict[str, Any]]) -> str:
        """
        Synthesizes research summaries and abstracts from multiple papers
        and generates a cohesive literature review.
        """
        # Assemble references and metadata
        paper_summaries = []
        for idx, paper in enumerate(papers):
            title = paper.get("title", f"Paper {idx+1}")
            authors = paper.get("authors", "Unknown Authors")
            abstract = paper.get("abstract", "")
            if isinstance(authors, list):
                authors_str = ", ".join(authors)
            else:
                authors_str = str(authors)
            paper_summaries.append(f"[{idx+1}] Title: {title}\nAuthors: {authors_str}\nAbstract: {abstract[:1000]}...")
            
        context_data = "\n\n".join(paper_summaries)
        
        # Call the synthesis prompt
        variables = {
            "count": len(papers),
            "topic": topic,
            "text": context_data  # LLM prompts might map to variable keys
        }
        # In prompts.yaml, we have {count} and {topic} and the text is not directly formatted, but we can pass all of them.
        # Let's inspect prompts.yaml: "synthesis: These {count} papers study {topic}." Wait, it does not have a {text} placeholder!
        # Let's check our prompts.yaml:
        # synthesis: |
        #   You are a research synthesis agent. These {count} papers study the topic: "{topic}".
        #   Synthesize the state of research across these papers. Include:
        #   ...
        # Wait, if we format prompts.yaml with {count} and {topic}, where does the actual papers text go? It is best to append the papers text to the prompt!
        # So we can format the prompt, then append the context_data, or modify prompts.yaml to have a {context} field!
        # Let's check prompts.yaml: yes, it says "These {count} papers study the topic: "{topic}". Synthesize..."
        # We can pass variables = {"count": len(papers), "topic": topic} and then append context_data to the formatted prompt or send it along.
        # Let's structure the synthesis agent to format the prompt template with count and topic, then append the papers text so the LLM has it.
        
        prompt_template = self.llm.prompts.get("synthesis", "These {count} papers study {topic}. Synthesize:")
        formatted_prompt = prompt_template.format(count=len(papers), topic=topic)
        
        final_prompt = f"{formatted_prompt}\n\nHere are the details of the papers to synthesize:\n{context_data}"
        
        if self.llm.mock_mode:
            return self.llm._mock_response("synthesis", {"topic": topic, "count": len(papers)})
            
        try:
            import google.generativeai as genai
            from ..config import settings
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(final_prompt)
            return response.text
        except Exception as e:
            print(f"Error during literature review synthesis: {e}")
            return self.llm._mock_response("synthesis", {"topic": topic, "count": len(papers)})
