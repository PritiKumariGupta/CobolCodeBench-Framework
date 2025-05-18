from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

class HuggingfaceComplete(LLMGenerator):
    """Completes WORKING-STORAGE then PROCEDURE DIVISION with local Huggingface model"""

    def __init__(self, model: Model, prompt_type):
        super().__init__(model, prompt_type)
        self.hf_model = AutoModelForCausalLM.from_pretrained(model.name, device_map="auto", torch_dtype=torch.bfloat16)
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