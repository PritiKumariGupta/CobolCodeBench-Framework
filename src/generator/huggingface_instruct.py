from loguru import logger
from . import LLMGenerator
from src.utils import extract_code_block, Model

def hf_instruct(prompt, model, tokenizer, max_length=8000, eos_token=None):
    """
    Generate text using a Hugging Face model with instruction-based prompting.
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
class HuggingfaceInstruct(LLMGenerator):
    """
    Completes WORKING-STORAGE then PROCEDURE DIVISION with local Huggingface model
    """

    def __init__(self, model: Model, prompt_type):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
        super().__init__(model, prompt_type)
        self.hf_model = AutoModelForCausalLM.from_pretrained(model.name, device_map="auto", torch_dtype=torch.bfloat16)
        if model.tokenizer:
            self.hf_tokenizer = AutoTokenizer.from_pretrained(model.tokenizer)
        else:
            self.hf_tokenizer = AutoTokenizer.from_pretrained(model.name)

    def solve(self, eval, sample_id=0):
        logger.info(f"generating {eval['Program_name']}")
        sol = hf_instruct(eval["Cobol_Eval"], self.hf_model, self.hf_tokenizer, 8000, eos_token=self.hf_tokenizer.eos_token)
        logger.info(sol)
        program = extract_code_block(sol)
        return program