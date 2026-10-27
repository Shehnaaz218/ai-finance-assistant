import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Download once (safe if already installed)
try:
    nltk.download('punkt')
except:
    pass


# -----------------------------
# LLM FOR JUDGING
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)


# -----------------------------
# BLEU SCORE
# -----------------------------
def compute_bleu(reference, prediction):
    try:
        reference_tokens = [reference.split()]
        prediction_tokens = prediction.split()

        return sentence_bleu(reference_tokens, prediction_tokens)

    except Exception:
        return 0


# -----------------------------
# ROUGE SCORE
# -----------------------------
def compute_rouge(reference, prediction):
    try:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, prediction)

        return scores["rougeL"].fmeasure

    except Exception:
        return 0


# -----------------------------
# LLM JUDGE
# -----------------------------
def llm_judge(query, response):
    try:
        prompt = f"""
        You are an evaluator.

        Check if the response correctly answers the query.

        Query: {query}
        Response: {response}

        Answer only:
        - Correct
        - Partially Correct
        - Incorrect
        """

        result = llm.invoke(prompt)

        return result.content.strip()

    except Exception:
        return "Evaluation Failed"


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def evaluate_response(query, response):

    if not response or response.strip() == "":
        return {
            "BLEU Score": 0,
            "ROUGE Score": 0,
            "LLM Judge": "No Response"
        }

    # ✅ GUARDRAIL FIX
    if "⚠️ Please ask finance-related questions only." in response:
        return {
            "BLEU Score": 0,
            "ROUGE Score": 0,
            "LLM Judge": "Correct (Guardrail Applied)"
        }

    reference = query

    bleu = compute_bleu(reference, response)
    rouge = compute_rouge(reference, response)
    judge = llm_judge(query, response)

    return {
        "BLEU Score": round(bleu, 3),
        "ROUGE Score": round(rouge, 3),
        "LLM Judge": judge
    }