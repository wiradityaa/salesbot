"""Evaluation pipeline untuk menilai kualitas SalesBot."""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.intent_classifier import classify_intent
from agents.tool_router import route
from agents.response_generator import generate_response

EVAL_DIR = Path(__file__).parent
REPORT_DIR = EVAL_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

# Load test questions
TEST_QUESTIONS_FILE = EVAL_DIR / "test_questions.json"


def load_test_questions() -> dict:
    """Load test questions dari file."""
    with open(TEST_QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_intent_accuracy(predicted_intent: str, expected_intent: str) -> bool:
    """Check apakah predicted intent sesuai expected intent."""
    return predicted_intent.lower() == expected_intent.lower()


def evaluate_answer_relevance(answer: str, expected_keywords: List[str]) -> float:
    """
    Score berapa banyak expected keywords yang muncul di answer (0-1).
    """
    if not expected_keywords:
        return 1.0

    found_keywords = sum(1 for kw in expected_keywords if kw.lower() in answer.lower())
    relevance_score = found_keywords / len(expected_keywords)

    return min(1.0, relevance_score)


def evaluate_answer_quality(answer: str) -> Dict[str, float]:
    """Score berbagai aspek kualitas jawaban."""
    scores = {
        "language_quality": 1.0 if len(answer) > 20 else 0.5,  # Ada jawaban dengan minimum length
        "completeness": 1.0 if len(answer) > 100 else 0.7 if len(answer) > 50 else 0.3,
        "clarity": 1.0 if "\n" in answer or "●" in answer or "-" in answer else 0.8
    }
    return scores


def run_evaluation(
    test_category: Optional[str] = None,
    verbose: bool = False
) -> Dict:
    """
    Jalankan evaluation pada test questions.

    Args:
        test_category: Filter category tertentu (e.g., "product_analysis")
        verbose: Print detail setiap test case

    Returns:
        Dict dengan hasil evaluation dan metrics
    """
    test_data = load_test_questions()
    results = {
        "timestamp": datetime.now().isoformat(),
        "test_runs": [],
        "summary": {}
    }

    total_questions = 0
    total_latency = 0
    intent_accuracy_count = 0
    relevance_scores = []
    quality_scores = {"language_quality": [], "completeness": [], "clarity": []}

    # Iterate setiap category
    for category, questions in test_data.items():
        if category == "metadata":
            continue

        if test_category and category != test_category:
            continue

        if verbose:
            print(f"\n{'='*60}")
            print(f"Category: {category.upper()}")
            print(f"{'='*60}")

        for question_data in questions:
            question_id = question_data["id"]
            question = question_data["question"]
            expected_intent = question_data["intent"]
            expected_keywords = question_data.get("expected_keywords", [])

            if verbose:
                print(f"\n[{question_id}] {question}")

            # Measure latency
            start_time = time.time()

            try:
                # Run SalesBot pipeline
                intent_result = classify_intent(question)
                predicted_intent = intent_result.get("intent", "unknown")

                route_result = route(intent_result.get("data", {}))
                answer = generate_response(question, route_result, intent_result.get("data", {}))

                latency = time.time() - start_time

                # Evaluate
                intent_match = evaluate_intent_accuracy(predicted_intent, expected_intent)
                relevance_score = evaluate_answer_relevance(answer, expected_keywords)
                quality_scores_detail = evaluate_answer_quality(answer)

                # Collect metrics
                total_questions += 1
                total_latency += latency
                if intent_match:
                    intent_accuracy_count += 1
                relevance_scores.append(relevance_score)
                for key, val in quality_scores_detail.items():
                    quality_scores[key].append(val)

                test_result = {
                    "question_id": question_id,
                    "question": question,
                    "category": category,
                    "predicted_intent": predicted_intent,
                    "expected_intent": expected_intent,
                    "intent_correct": intent_match,
                    "answer": answer[:200] + "..." if len(answer) > 200 else answer,
                    "relevance_score": round(relevance_score, 2),
                    "quality_scores": {k: round(v, 2) for k, v in quality_scores_detail.items()},
                    "latency_ms": round(latency * 1000, 2),
                    "status": "success"
                }

                if verbose:
                    print(f"  Intent: {predicted_intent} {'✓' if intent_match else '✗'}")
                    print(f"  Relevance: {relevance_score:.2f}")
                    print(f"  Latency: {latency*1000:.0f}ms")

            except Exception as e:
                test_result = {
                    "question_id": question_id,
                    "question": question,
                    "category": category,
                    "status": "error",
                    "error": str(e),
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }

                total_questions += 1
                total_latency += (time.time() - start_time)

                if verbose:
                    print(f"  ✗ Error: {str(e)[:100]}")

            results["test_runs"].append(test_result)

    # Calculate summary metrics
    if total_questions > 0:
        results["summary"] = {
            "total_questions": total_questions,
            "successful_runs": len([r for r in results["test_runs"] if r["status"] == "success"]),
            "failed_runs": len([r for r in results["test_runs"] if r["status"] == "error"]),
            "intent_accuracy": round(intent_accuracy_count / total_questions, 3),
            "avg_relevance_score": round(sum(relevance_scores) / len(relevance_scores), 3) if relevance_scores else 0,
            "avg_language_quality": round(sum(quality_scores["language_quality"]) / len(quality_scores["language_quality"]), 3) if quality_scores["language_quality"] else 0,
            "avg_completeness": round(sum(quality_scores["completeness"]) / len(quality_scores["completeness"]), 3) if quality_scores["completeness"] else 0,
            "avg_clarity": round(sum(quality_scores["clarity"]) / len(quality_scores["clarity"]), 3) if quality_scores["clarity"] else 0,
            "avg_latency_ms": round(total_latency * 1000 / total_questions, 2)
        }

    return results


def save_evaluation_report(results: Dict, filename: Optional[str] = None) -> str:
    """Save evaluation results ke JSON file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"eval_report_{timestamp}.json"

    filepath = REPORT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return str(filepath)


def print_summary(results: Dict) -> None:
    """Print summary metrics dalam format yang readable."""
    summary = results.get("summary", {})

    if not summary:
        print("No evaluation results to display.")
        return

    print("\n" + "="*70)
    print("SALESBOT EVALUATION REPORT")
    print("="*70)
    print(f"Timestamp: {results.get('timestamp', 'N/A')}")
    print(f"\nTotal Questions Tested: {summary.get('total_questions', 0)}")
    print(f"Successful Runs: {summary.get('successful_runs', 0)}")
    print(f"Failed Runs: {summary.get('failed_runs', 0)}")

    print("\n" + "-"*70)
    print("QUALITY METRICS")
    print("-"*70)
    print(f"Intent Accuracy: {summary.get('intent_accuracy', 0):.1%}")
    print(f"Avg Relevance Score: {summary.get('avg_relevance_score', 0):.2f}/1.0")
    print(f"Avg Language Quality: {summary.get('avg_language_quality', 0):.2f}/1.0")
    print(f"Avg Completeness: {summary.get('avg_completeness', 0):.2f}/1.0")
    print(f"Avg Clarity: {summary.get('avg_clarity', 0):.2f}/1.0")

    print("\n" + "-"*70)
    print("PERFORMANCE METRICS")
    print("-"*70)
    print(f"Avg Latency: {summary.get('avg_latency_ms', 0):.0f}ms")

    print("\n" + "="*70 + "\n")


def get_evaluation_history() -> List[Dict]:
    """Get list semua evaluation reports yang tersimpan."""
    if not REPORT_DIR.exists():
        return []

    reports = []
    for filepath in sorted(REPORT_DIR.glob("eval_report_*.json"), reverse=True):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                reports.append({
                    "filename": filepath.name,
                    "timestamp": data.get("timestamp"),
                    "total_questions": data.get("summary", {}).get("total_questions", 0),
                    "intent_accuracy": data.get("summary", {}).get("intent_accuracy", 0)
                })
        except Exception:
            pass

    return reports


if __name__ == "__main__":
    # Run full evaluation
    print("Starting SalesBot evaluation...")
    print("This may take a few minutes...\n")

    results = run_evaluation(verbose=True)

    # Print summary
    print_summary(results)

    # Save report
    report_path = save_evaluation_report(results)
    print(f"Report saved to: {report_path}")

    # Show evaluation history
    print("\nRecent Evaluation Reports:")
    for i, report in enumerate(get_evaluation_history()[:5], 1):
        print(f"  {i}. {report['filename']} - Intent Accuracy: {report['intent_accuracy']:.1%}")
