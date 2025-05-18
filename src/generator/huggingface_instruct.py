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