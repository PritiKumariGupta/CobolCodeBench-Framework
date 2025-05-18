from dataclasses import dataclass

@dataclass
class Model:
    """
    Model configuration for LLMs.
    Attributes:
        name (str): Name of the model.
        temp (float): Temperature for sampling.
        samples_per_task (int): Number of samples per task.
        tokenizer (str): Tokenizer name.
        prefix_token (str): Prefix token for the model.
        suffix_token (str): Suffix token for the model.
        middle_token (str): Middle token for the model.
        eos_token (str): End-of-sequence token for the model.
    """
    name: str
    temp: float = 0.0
    samples_per_task: int = 1
    tokenizer: str = None
    prefix_token: str = None
    suffix_token: str = None
    middle_token: str = None
    eos_token: str = None

@dataclass
class Result:
    """
    Result of the code generation process.
    Attributes:
        returncode (int): Return code from the generation process.
        error (str): Error message if any occurred during generation.
    """
    returncode: int
    error: str = None

