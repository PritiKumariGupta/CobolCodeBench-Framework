import os
import json
from datasets import load_dataset
def load_dataset_from_hf(dataset_name, split="default"):
    """
    Load a dataset from Hugging Face Datasets library.
    :param dataset_name: Name of the dataset to load.
    :param split: Split of the dataset to load (default is "train").
    :return: Loaded dataset.
    """
    try:
        dataset = load_dataset(dataset_name, split=split)
        return dataset
    except Exception as e:
        print(f"Error loading dataset {dataset_name}: {e}")
        return None
    
def process_dataset_to_instruction_completion_sets(dataset_name, output_dir=None):
    """
    Process the dataset from Hugging Face and create instruction and completion sets.
    
    Args:
        dataset_name: Name of the dataset on Hugging Face
        output_dir: Directory to save the output files (default is 'data' folder)
    
    Returns:
        Tuple containing paths to the generated instruction and completion set files
    """
    # Set default output directory if not provided
    if output_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, "data")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output file paths
    instruction_set_path = os.path.join(output_dir, "Instruction_Set.json")
    completion_set_path = os.path.join(output_dir, "Completion_Set.json")
    
    # Load dataset from Hugging Face
    print(f"Loading dataset: {dataset_name}")
    instruction_dataset = load_dataset_from_hf(dataset_name, split='instruct')
    
    if instruction_dataset is None:
        print("Failed to load Instruction dataset")
        return None, None
    
    print(f"Instruction Dataset loaded with {len(instruction_dataset)} examples")
    
    # Process dataset into instruction and completion sets
    instruction_set = []
    
    for item in instruction_dataset:
        # Common fields for both sets
        program_name = item.get("program_name", "")
        cobol_eval = item.get("instruct_prompt", "")
        expected_program = item.get("canonical_solution", "")
        input_files = item.get("input_file_names", "") # String with comma-separated filename strings Eg: input.txt,error.txt or inputs.txt

        output_files = item.get("output_file_names", "") # String with comma-separated filename strings
        inputs = item.get("inputs", "") # JSON-serialized string
        outputs = item.get("outputs", "") # JSON-serialized string
        
        # Convert file names to lists or strings if no comma-seperated values
        if "," in input_files:
            input_files = [file.strip() for file in input_files.split(",")]
        if "," in output_files:
            output_files = [file.strip() for file in output_files.split(",")]

            
        # Convert JSON-serialized strings to dictionaries
        if inputs:
            try:
                inputs = json.loads(inputs)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for inputs in {program_name}")
                inputs = {}
        if outputs:
            try:
                outputs = json.loads(outputs)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for outputs in {program_name}")
                outputs = {}
                
        # Ensure all fields are strings
        program_name = str(program_name)
        cobol_eval = str(cobol_eval)
        expected_program = str(expected_program)
        
        # Create entries for instruction sets
        instruction_entry = {
            "Program_name": program_name,
            "Cobol_Eval": cobol_eval,
            "Expected_Program": expected_program,
            "input_file_names": input_files,
            "output_file_names": output_files,
            "inputs": inputs,
            "outputs": outputs,
        }
        instruction_set.append(instruction_entry)

        
    # Save to JSON files
    with open(instruction_set_path, 'w') as f:
        json.dump(instruction_set, f, indent=4)
    
    print(f"Created instruction set at: {instruction_set_path}")
    
    completion_dataset = load_dataset_from_hf(dataset_name, split="complete")
    if completion_dataset is None:
        print("Failed to load Completion dataset")
        return None, None
    print(f"Completion Dataset loaded with {len(completion_dataset)} examples")

    completion_set = []

    for item in completion_dataset:
        # Common fields for both sets
        program_name = item.get("program_name", "")
        cobol_eval = item.get("complete_prompt", "")
        expected_program = item.get("canonical_solution", "")
        input_files = item.get("input_file_names", "")
        output_files = item.get("output_file_names", "")
        inputs = item.get("inputs", "")
        outputs = item.get("outputs", "")
        
        
        # Convert file names to lists or strings if no comma-seperated values
        if "," in input_files:
            input_files = [file.strip() for file in input_files.split(",")]
        if "," in output_files:
            output_files = [file.strip() for file in output_files.split(",")]
            
        # Convert JSON-serialized strings to dictionaries
        if inputs:
            try:
                inputs = json.loads(inputs)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for inputs in {program_name}")
                inputs = {}
        if outputs:
            try:
                outputs = json.loads(outputs)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for outputs in {program_name}")
                outputs = {}
                
        # Ensure all fields are strings
        program_name = str(program_name)
        cobol_eval = str(cobol_eval)
        expected_program = str(expected_program)
        
        # Create entries for completion sets
        completion_entry = {
            "Program_name": program_name,
            "Cobol_Eval": cobol_eval,
            "Expected_Program": expected_program,
            "inputs": inputs,
            "outputs": outputs,
            "input_files": input_files,
            "output_files": output_files
        }
        
        completion_set.append(completion_entry)
    
    # Save to JSON files
    
    with open(completion_set_path, 'w') as f:
        json.dump(completion_set, f, indent=4)
    
    print(f"Created completion set at: {completion_set_path}")
    
    return instruction_set_path, completion_set_path

def main():
    """
    Main function to run the data processor
    """
    completion_data = "Completion_Set.json"
    instruction_data = "Instruction_Set.json"
    # Check if the data folder has json files
    if os.path.exists(completion_data) and os.path.exists(instruction_data):
        print("Data folder already exists. Skipping dataset processing.")
        return
    else:
        print("Data folder does not exist. Processing dataset.")
        dataset_name = "harshini-kumar/CobolCodeBench"
        instruction_path, completion_path = process_dataset_to_instruction_completion_sets(dataset_name)
        
        if instruction_path and completion_path:
            print("Successfully created instruction and completion sets")
        else:
            print("Failed to create instruction and completion sets")

if __name__ == "__main__":
    main()