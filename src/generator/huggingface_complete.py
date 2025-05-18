from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger
from src.utils import Model
from . import LLMGenerator

def hf_complete(prompt, model, tokenizer, max_length=8000, eos_token=None):
    """
    Generate text using a Hugging Face model with completion-based prompting.
    Args:
        prompt (str): The input prompt for the model.
        model: The Hugging Face model to use for generation.
        tokenizer: The tokenizer for the model.
        max_length (int): Maximum length of the generated text.
        eos_token (str): End-of-sequence token for the model.
    Returns:
        str: The generated text.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=max_length, eos_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
class HuggingfaceComplete(LLMGenerator):
    """Completes WORKING-STORAGE then PROCEDURE DIVISION with local Huggingface model"""

    def __init__(self, model: Model, prompt_type):
        super().__init__(model, prompt_type)
        self.hf_model = AutoModelForCausalLM.from_pretrained(model.name, device_map="auto")
        if model.tokenizer:
            self.hf_tokenizer = AutoTokenizer.from_pretrained(model.tokenizer)
        else:
            self.hf_tokenizer = AutoTokenizer.from_pretrained(model.name)

    def combine_prompt_and_solution(self, prompt, solution):
        """Combine the prompt and solution into a single program."""
        combined_program = f"{prompt}\n{solution}"
        return combined_program

    def solve(self, eval, sample_id=0):
        logger.info(f"generating {eval['Program_name']}")
        sol = hf_complete(eval["Cobol_Eval"], self.hf_model, self.hf_tokenizer, 8000, eos_token=self.model.eos_token)
        logger.info(sol)
        program = self.combine_prompt_and_solution(eval['Cobol_Eval'], sol)
        return program