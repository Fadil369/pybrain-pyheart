"""Tests for analytics engine."""

from pybrain.core.analytics import AnalyticsEngine


def test_brainsait_patient_recommendations_include_language_and_region():
    """Test BrainSAIT-specific care coordination recommendations."""
    engine = AnalyticsEngine()

    patient_data = {
        "region": "SA",
        "patient": {
            "id": "patient-1",
            "conditions": ["Diabetes", "Hypertension"],
            "communication": [
                {
                    "language": {
                        "coding": [{"code": "ar"}]
                    }
                }
            ],
        },
        "observations": [],
    }

    insights = engine.analyze_patient_trends(patient_data)

    assert "Provide Arabic-first outreach and education materials" in insights["recommendations"]
    assert "Enroll patient in diabetes care coordination pathway" in insights["recommendations"]
    assert "Align follow-up plan with BrainSAIT regional care escalation protocol" in insights["recommendations"]


def test_population_metrics_include_language_distribution():
    """Test population analytics capture BrainSAIT language and regional context."""
    engine = AnalyticsEngine()

    population = [
        {
            "region": "SA",
            "patient": {
                "id": "1",
                "birthDate": "1960-01-01",
                "gender": "female",
                "conditions": [{"display": "Diabetes"}],
                "communication": [
                    {
                        "language": {
                            "coding": [{"code": "ar"}]
                        }
                    }
                ],
            },
            "observations": [],
        }
    ]

    metrics = engine.calculate_population_metrics(population)

    assert metrics["language_distribution"]["ar"] == 1
    assert metrics["region_distribution"]["SA"] == 1
    assert any("Arabic outreach" in recommendation for recommendation in metrics["recommendations"])
