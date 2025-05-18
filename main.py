import os
import json
import argparse
from loguru import logger
import pandas as pd
from src.generator.openai_chat import OpenAIChat
from src.generator.huggingface_instruct import HuggingfaceInstruct
from src.generator.huggingface_complete import HuggingfaceComplete
from src.generator.huggingface_api import HuggingfaceAPIInferenceGenerator
from src.utils.file_utils import json_to_csv, zip_and_download_folder
from src.generator import Model

def setup_logger():
    """Configure logger settings"""
    # Make sure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    logger.remove()
    logger.add(
        "logs/generation_{time}.log",
        rotation="100 MB",
        level="INFO",
        format="{time} {level} {message}"
    )
    logger.add(lambda msg: print(msg), level="INFO")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="COBOL Code Generation using LLMs")
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-35-turbo",
        choices=["gpt-35-turbo", "gpt-4o", "claude-sonnet", "claude-opus", "gemini-pro", "Llama-3.1-8B-instruct"],
        help="Model to use for generation"
    )
    parser.add_argument(
        "--mode", 
        type=str, 
        default="Complete",
        choices=["Complete", "Instruct"],
        help="Generation mode: Complete or Instruct"
    )
    parser.add_argument(
        "--method", 
        type=str, 
        default="openai",
        choices=["openai", "hf-instruct", "hf-complete", "hf-api"],
        help="Method for code generation"
    )
    parser.add_argument(
        "--samples", 
        type=int, 
        default=1,
        help="Number of samples per task"
    )
    parser.add_argument(
        "--generation-only", 
        action="store_true",
        help="Only run generation, skip evaluation"
    )
    parser.add_argument(
        "--export", 
        action="store_true",
        help="Export results as zip file"
    )
    return parser.parse_args()

def export_results(model_name):
    """Export results as a zip file"""
    try:
        model_path = model_name
        zip_filename = f"model_predictions_{model_name}.zip"
        zip_and_download_folder(f"preds/{model_path}", zip_filename)
        logger.info(f"Results exported to {zip_filename}")
        return True
    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        return False

def main():
    setup_logger()
    args = parse_arguments()
    
    # Configure model
    model = Model(
        name=args.model, 
        tokenizer=args.model, 
        samples_per_task=args.samples
    )
    
    logger.info(f"Starting code generation with {args.model} model in {args.mode} mode")
    
    # Choose the model type for code generation
    if args.method == "openai":
        runner = OpenAIChat(model, args.mode)
    elif args.method == "hf-instruct":
        runner = HuggingfaceInstruct(model, args.mode)
    elif args.method == "hf-complete":
        runner = HuggingfaceComplete(model, args.mode)
    elif args.method == "hf-api":
        runner = HuggingfaceAPIInferenceGenerator(model, args.mode)
    else:
        logger.error(f"Unknown method: {args.method}")
        return
    
    # Run code generation
    success = runner.eval()
    
    if success:
        logger.success(f"Code generation completed for {args.model}")
        
        # Run evaluation if not in generation-only mode
        if not args.generation_only:
            logger.info("Running evaluation script...")
            # Save model info to file for evaluation script
            eval_config = {
                "model_name": args.model,
                "mode": args.mode
            }
            os.makedirs("config", exist_ok=True)
            with open("config/last_run.json", "w") as f:
                json.dump(eval_config, f)
                
            # Here we could import and run evaluation, but keeping it separate is better
            # Just inform the user about the next step
            logger.info("Generation complete. Run 'python evaluate.py' to evaluate the results.")
        else:
            logger.info("Generation-only mode - skipping evaluation")
        
        # Export results if requested
        if args.export:
            logger.info("Exporting results...")
            export_success = export_results(args.model)
            if export_success:
                logger.success("Results exported successfully")
    else:
        logger.error("Code generation failed")

if __name__ == "__main__":
    main()