# Configuration settings for the models used in the project

class ModelConfig:
    def __init__(self, model_name: str, tokenizer_name: str, method:str, mode:str, samples_per_task: int):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.samples_per_task = samples_per_task
        self.method = method
        self.mode = mode

    def display_config(self):
        print(f"Model Name: {self.model_name}")
        print(f"Tokenizer Name: {self.tokenizer_name}")
        print(f"Samples Per Task: {self.samples_per_task}")
        print(f"Method: {self.method}")
        print(f"Mode: {self.mode}")

# Example configuration
default_config = ModelConfig(
    model_name="gpt-35-turbo", 
    tokenizer_name="gpt-35-turbo", 
    method="chat-api",
    mode="Instruct",
    samples_per_task=1)