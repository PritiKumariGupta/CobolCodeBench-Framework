class HuggingfaceAPIInferenceGenerator(LLMGenerator):
    """
    Completes WORKING-STORAGE then PROCEDURE DIVISION with Hugging Face's API.
    """

    def __init__(self, model: Model, prompt_type):
        super().__init__(model, prompt_type)
        self.hf_model = model

    def solve(self, eval, sample_id=0):
        logger.info(f"Generating {eval['Program_name']}")
        sol = huggingface_api_inference(eval["Cobol_Eval"], self.hf_model)
        if self.prompt_type == "Complete":
            program = self.construct(eval["Cobol_Eval"], sol)
        else:
            program = extract_code_block(sol)
        logger.info(program)
        return program

    def construct(self, prompt: str, sol: str):
        prog = f"{prompt}\n{sol}"
        return swap_sections(prog)