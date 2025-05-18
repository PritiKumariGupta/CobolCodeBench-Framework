# COBOL Code Generator

This project is designed to generate COBOL code using various language models. It leverages state-of-the-art AI models to assist in code generation tasks, making it easier for developers to create COBOL programs efficiently.

## Project Structure

```
cobol-code-generator
├── src
│   ├── generator
│   │   ├── __init__.py
│   │   ├── llm_generator.py
│   │   ├── openai_chat.py
│   │   ├── huggingface_instruct.py
│   │   ├── huggingface_complete.py
│   │   └── huggingface_api.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── code_extractor.py
│   │   ├── file_utils.py
│   │   └── command_utils.py
│   ├── evaluator
│   │   ├── __init__.py
│   │   |── compile_execute.py
|   |   |── evaluate.py
|   |   └── score_evaluator.py
│   ├── data
│   │   ├── __init__.py
│   │   └── data_loader.py
│   └── __init__.py
├── data
│   ├── Instruction_Set.json
│   └── Completion_Set.json
├── config
│   └── model_config.py
├── main.py
├── requirements.txt
└── README.md
```

## Features

- **Model Integration**: Supports multiple models for code generation including OpenAI and Hugging Face.
- **Evaluation**: Provides tools to evaluate the generated code against expected outputs.
- **Data Handling**: Includes utilities for loading and processing instruction and completion sets from JSON files.
- **Command Execution**: Utilities for executing shell commands related to COBOL code compilation.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the code generator, execute the following command:

```
python main.py
```

Make sure to configure the model settings in `config/model_config.py` as needed.

# Generation only
```
python main.py --model gpt-4o --mode Instruct --method openai --generation-only
```

# Run evaluation after generation is complete
```
python evaluate.py
```

# Or run specific evaluation types
```
python evaluate.py --bert-score
python evaluate.py --compile-execute
```

# Or specify a different model/mode than the last run
```
python evaluate.py --model claude-sonnet --mode Complete
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

