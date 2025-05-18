from loguru import logger
from . import LLMGenerator
from src.utils import extract_code_block, Model
from transformers import AutoTokenizer, AutoModelForCausalLM

def huggingface_api_inference(prompt, model, tokenizer, max_length=8000, eos_token=None):
    """
    Generate text using a Hugging Face API inferencing with instruction-based prompting.
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

class HuggingfaceAPIInferenceGenerator(LLMGenerator):
    """
    Completes WORKING-STORAGE then PROCEDURE DIVISION with Hugging Face's API.
    """

    def __init__(self, model: Model, prompt_type):
        super().__init__(model, prompt_type)
        self.hf_model = model
        self.hf_tokenizer = model.tokenizer
        self.prompt_type = prompt_type
        if model.tokenizer:
            self.hf_model.tokenizer = AutoTokenizer.from_pretrained(model.tokenizer)
        else:
            self.hf_model.tokenizer = AutoTokenizer.from_pretrained(model.name)

    def solve(self, eval, sample_id=0):
        logger.info(f"Generating {eval['Program_name']}")
        sol = huggingface_api_inference(eval["Cobol_Eval"], self.hf_model, self.hf_tokenizer, 8000, eos_token=self.hf_tokenizer.eos_token)
        if self.prompt_type == "Complete":
            program = self.construct(eval["Cobol_Eval"], sol)
        else:
            program = extract_code_block(sol)
        logger.info(program)
        return program

    def construct(self, prompt: str, sol: str):
        prog = f"{prompt}\n{sol}"
        return prog