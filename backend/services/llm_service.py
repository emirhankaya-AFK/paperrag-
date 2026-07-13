import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import google.generativeai as genai
from ..config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.prompts = self._load_prompts()
        self.mock_mode = not self.api_key
        
        if not self.mock_mode:
            genai.configure(api_key=self.api_key)
            
    def _load_prompts(self) -> Dict[str, str]:
        prompt_path = Path(__file__).parent.parent / "config" / "prompts.yaml"
        if prompt_path.exists():
            with open(prompt_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def generate_text(self, prompt_name: str, variables: Dict[str, Any], fallback_text: str = "") -> str:
        """
        Generates text using the specified prompt template and variables.
        """
        prompt_template = self.prompts.get(prompt_name, "")
        if not prompt_template:
            # Fallback if prompt template is missing
            prompt_template = "{text}"
            if "text" not in variables:
                variables["text"] = str(variables)
                
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return self._mock_response(prompt_name, variables)
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(formatted_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}. Falling back to mock/template.")
            return self._mock_response(prompt_name, variables)

    def generate_json(self, prompt_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured JSON using Gemini API.
        """
        prompt_template = self.prompts.get(prompt_name, "")
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(
                formatted_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            # Parse response
            return json.loads(response.text.strip())
        except Exception as e:
            print(f"Gemini JSON API Error: {e}. Falling back to mock.")
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates embeddings using Gemini API (or mock dimensions).
        """
        if self.mock_mode or not self.api_key:
            # 1536 dim mock vector
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding API Error: {e}. Falling back to mock vector.")
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]

    def _mock_response(self, prompt_name: str, variables: Dict[str, Any], json_format: bool = False) -> str:
        """
        Provides mock responses for local testing without API keys.
        """
        if json_format:
            if prompt_name == "extraction":
                return json.dumps({
                    "title": variables.get("title", "Attention Is All You Need"),
                    "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
                    "key_contributions": [
                        "Propose the Transformer, a new simple network architecture based solely on attention mechanisms.",
                        "Show that Transformers generalise well to other tasks like English constituency parsing.",
                        "Achieve state-of-the-art results on translation tasks while being significantly faster to train."
                    ],
                    "methodology": "The paper replaces recurrent layers with multi-head self-attention. It uses positional encodings to preserve sequence order and stacked encoder-decoder layers.",
                    "main_results": [
                        "Achieved 28.4 BLEU on WMT 2014 English-to-German translation task.",
                        "Achieved 41.8 BLEU on WMT 2014 English-to-French translation task.",
                        "Reduced training time to a fraction of traditional sequence-to-sequence models."
                    ],
                    "limitations": [
                        "High memory consumption due to the quadratic complexity of self-attention with sequence length.",
                        "Lack of recurrent inductive bias makes it hard to generalize to sequences much longer than seen in training."
                    ]
                })
            return "{}"
            
        else:
            if prompt_name == "summary":
                return f"""### Executive Summary
This paper introduces the Transformer model, removing recurrent/convolutional layers and relying entirely on multi-head attention.

### Problem
Recurrent networks are sequential, limiting parallelization during training and making long-term dependencies hard to learn.

### Approach
Use self-attention mechanisms to compute representations of input and output without sequence-aligned RNNs or convolutions.

### Results
The model achieves state-of-the-art results on translation benchmarks while training in much less time.

### Impact
It serves as the base architecture for modern LLMs including GPT, BERT, and Gemini.
"""
            elif prompt_name == "qa":
                q = variables.get("question", "").lower()
                if "sample size" in q or "dataset" in q:
                    return "The model was trained on the WMT 2014 English-to-German dataset containing 4.5 million sentence pairs."
                elif "limit" in q:
                    return "The limitations include quadratic memory cost with sequence length and lack of sequence-order induction bias without positional encodings."
                return f"Based on the provided excerpts, the paper discusses this topic. (Mock Answer to: '{variables.get('question')}')"
                
            elif prompt_name == "synthesis":
                return f"""# Literature Review: {variables.get('topic', 'Overview')}
Processed {variables.get('count', 3)} research documents.

## Key Findings & Consensus
The reviewed literature shows a general consensus on adopting self-attention models over recurrent architectures for sequence modeling. Performance gains are consistently observed.

## Disagreements & Variations
There are varying viewpoints on how to optimize attention mechanisms, with some authors using sparse attention patterns while others rely on linear approximations.

## Open Questions & Future Directions
1. Scaling efficiency for extremely long contexts.
2. Low-resource domain adaptation.
"""
            return f"Mock response for prompt: {prompt_name}"
