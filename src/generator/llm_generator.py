import json
class LLMGenerator:
    def __init__(self, model, prompt_type):
        self.model = model
        self.prompt_type = prompt_type
        self.output_path = None
        self.solutions_path = None
        self.errors_path = None
        self.samples = []

    def eval(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def solve(self, eval, sample_id=0):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def save_samples(self):
        if self.output_path:
            with open(f"{self.output_path}/samples.jsonl", "w+") as f:
                for sample in self.samples:
                    f.write(json.dumps(sample) + "\n")