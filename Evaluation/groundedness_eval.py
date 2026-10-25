import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

# Define the 25 benchmark questions (Mixed In-Scope and Out-of-Scope)
benchmark_questions = [
    {"q": "What are the safety requirements and guidelines for placing traffic signs on highways?", "type": "in_scope"},
    {"q": "How do I bake a sourdough bread at home?", "type": "out_of_scope"},
    {"q": "What is the required distance of a traffic sign from the road edge?", "type": "in_scope"},
    {"q": "Explain the theory of quantum entanglement.", "type": "out_of_scope"},
    {"q": "What are the rules for night work and adequate lighting during road maintenance?", "type": "in_scope"},
    {"q": "What is the best way to invest in the stock market?", "type": "out_of_scope"},
    {"q": "What materials are allowed for pavement markings?", "type": "in_scope"},
    {"q": "Who won the Formula 1 world championship in 2023?", "type": "out_of_scope"},
    {"q": "What is the minimum safety distance for road workers near traffic?", "type": "in_scope"},
    {"q": "What are the best tourist attractions in Tokyo?", "type": "out_of_scope"},
    {"q": "How should distressed pavement be handled and repaired?", "type": "in_scope"},
    {"q": "What is the traditional recipe for chocolate chip cookies?", "type": "out_of_scope"},
    {"q": "What are the guidelines for temporary traffic arrangements during construction?", "type": "in_scope"},
    {"q": "How do quantum computers process information differently from classical computers?", "type": "out_of_scope"},
    {"q": "What is the Code of Practice for Road Signs?", "type": "in_scope"},
    {"q": "How to make a sourdough starter from scratch?", "type": "out_of_scope"},
    {"q": "What is the Pavement Condition Index (PCI) and how is it used?", "type": "in_scope"},
    {"q": "How to tune a Formula 1 engine for maximum performance?", "type": "out_of_scope"},
    {"q": "What are the specific requirements for barricades in work zones?", "type": "in_scope"},
    {"q": "What are the main differences between value investing and day trading?", "type": "out_of_scope"},
    {"q": "What is the required width for diverting traffic during road maintenance?", "type": "in_scope"},
    {"q": "What is the capital city of Japan and its population?", "type": "out_of_scope"},
    {"q": "How is the Mean Profile Depth (MPD) of asphalt measured?", "type": "in_scope"},
    {"q": "What are the key ingredients for making fluffy pancakes?", "type": "out_of_scope"},
    {"q": "What are the regulations for bicycle lanes and pedestrian crossings?", "type": "in_scope"}
]

def run_groundedness_evaluation(generate_answer_fn, kpi_threshold=0.90):
    results = []
    passed_count = 0
    for item in benchmark_questions:
        q = item["q"]
        q_type = item["type"]
        answer = generate_answer_fn(q)
        passed = False
        reason = ""
        if q_type == "out_of_scope":
            if "I don't know" in answer:
                passed = True
                reason = "Passed Guardrail (Blocked)"
            else:
                passed = False
                reason = "Failed (Hallucinated or Answered)"
        else:
            if "I don't know" in answer:
                passed = False
                reason = "Failed (No Context Found)"
            elif "[Source" in answer:
                passed = True
                reason = "Success (Grounded & Cited)"
            else:
                passed = False
                reason = "Failed (No Citation / Hallucination)"
        if passed:
            passed_count += 1
        results.append({
            "Question": q,
            "Type": q_type,
            "Passed": "✅" if passed else "❌",
            "Reason": reason,
            "Preview": answer[:60].replace("\n", " ") + "..."
        })
    accuracy = (passed_count / len(benchmark_questions)) * 100
    return results, accuracy