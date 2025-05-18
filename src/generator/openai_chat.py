from loguru import logger
from src.utils import extract_code_block,Model
from . import ChatModelsGenerator, LLMGenerator
class OpenAIChat(LLMGenerator):
    def __init__(self, model: Model, prompt_type):
        self.model_name = model.name
        self.prompt_type = prompt_type
        super().__init__(model, prompt_type)

    def construct(self, prompt: str, sol: str):
        if sol.strip().startswith("WORKING-STORAGE SECTION."):
            sol = sol.replace("WORKING-STORAGE SECTION.", "")
        prog = f"{prompt}\n{sol}"
        return prog

    def solve(self, eval, sample_id=0):
        prompt = eval["Cobol_Eval"]
        logger.info(f"Generating {eval['Program_name']}")
        cht = ChatModelsGenerator()
        sol = cht.chat(prompt, model=self.model_name)
        if self.prompt_type == "Complete":
            sol = extract_code_block(sol)
            program = self.construct(prompt, sol)
        else:
            program = extract_code_block(sol)
        return program