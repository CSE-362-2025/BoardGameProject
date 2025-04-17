"""
Author: Andrew
Created: 2025/02/29
Last Edited: 2025/03/02
Class to generate ai summary
"""

from transformers import AutoTokenizer
from transformers import pipeline
import torch
import os

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

torch.cuda.empty_cache()

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
access_token = "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"

pipeline = pipeline(
    "text-generation",
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,  # Use FP16 to reduce memory usage
    device_map="cuda",  
    max_new_tokens=256
)

def llm(query):

    output = pipeline(query)

    output = output[0]['generated_text']

    summary = output.split("START")[2]
    summary = summary.split("END")[0]

    return summary