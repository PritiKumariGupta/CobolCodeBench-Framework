import os
import concurrent.futures
from typing import Union, Dict, Tuple, List
from loguru import logger
from bert_score import BERTScorer
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel

class ScoreEvaluator:
    """
    Evaluate generated code against expected responses using multiple metrics.
    """

    def __init__(self):
        # Lazy initialization of BERT scorer
        self.bert_scorer = None
        self.bert_scores = []

    def bert_score(self, expected_response: str, generated_response: str):
        """
        Calculate BERT score between ground truth and generated response.

        Args:
            expected_response (str): The expected code or response.
            generated_response (str): The generated code or response to evaluate.

        Returns:
            float: The BERT score.
        """
        # Lazy initialization of BERT scorer
        if self.bert_scorer is None:
            self.bert_scorer = BERTScorer(lang="en", rescale_with_baseline=True)

        if expected_response:
            bert_score = self.bert_scorer.score(
                [generated_response], [expected_response]
            )
            return bert_score[0].item()
        else:
            return np.nan

    def evaluate(self, golden_set: List[Dict], instruction_set: pd.DataFrame, model_name: str) -> pd.DataFrame:
        """
        Evaluate generated code against expected responses using multiple metrics.

        Args:
            golden_set: List of dictionaries containing query and expected responses
            instruction_set: DataFrame with program details and responses

        Returns:
            pd.DataFrame: Evaluation results with scores
        """
        self.bert_scores.clear()

        # Validate inputs
        if not golden_set or len(golden_set) == 0:
            logger.error("Empty golden set provided")
            return pd.DataFrame()
        if instruction_set.empty:
            logger.error("Empty instruction set provided")
            return pd.DataFrame()

        for index, row in instruction_set.iterrows():
            program_name = row.get('Program_name', f"Row {index}")
            logger.info(f"Processing {program_name}")

            query = str(row.get('Cobol_Eval', ''))
            generated_response = str(row.get('Generated_program', ''))
            expected_response = str(row.get('Expected_Program', ''))

            if not query or not generated_response or not expected_response:
                logger.warning(f"Missing data in row {index} for program {program_name}")
                self.bert_scores.append(0.0)
                continue

            b_score = self.bert_score(expected_response, generated_response)
            logger.info(f"{program_name} - BERT Score: {b_score:.2f}")
            self.bert_scores.append(b_score)

        # Create results DataFrame
        evaluation_result = pd.DataFrame({
            'Program_name': instruction_set.get('Program_name', instruction_set.index),
            'Cobol_Eval': instruction_set.get('Cobol_Eval', ''),
            'Generated_program': instruction_set.get('Generated_program', ''),
            'Expected_program': instruction_set.get('Expected_Program', ''),
            'Bert_score': self.bert_scores
        })

        return evaluation_result