import json
import re

def format_text_to_schema(text_response: str, analysis_type:str) -> str:
    """
    Format the text response to match the required JSON schema structure.
    Extracts analysis, psychosocial indicators, and summary.
    """

    def extract_value(text: str, labels: list[str]) -> str | None:
        """Extract value by matching one of the given labels in the text."""
        for line in text.splitlines():
            for label in labels:
                if label.lower() in line.lower():
                    return line.split(":", 1)[1].strip()
        return None

    def extract_resume(text: str) -> str | None:
        """Extract the résumé section, handling formatting variations."""
        # Match everything after "En résumé" until the end
        match = re.search(r"En résumé.*?:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            value = re.sub(r"\*\*", "", value)  # remove markdown bold markers
            return value
        return None

    try:
        result = {
            "type": "object",
            "analysis_type": analysis_type,
            "analysis": "",
            "psychosocial_status": {
                "stress_level": "modéré",
                "burnout_risk": "modéré",
                "motivation_engagement": "modéré",
                "adaptability": "modéré",
                "social_integration_tendency": "modéré"
            },
            "summary": ""
        }

        lines = text_response.splitlines()
        for i, line in enumerate(lines):
            if any(key in line.lower() for key in ["niveau de stress", "risque de burnout", "en résumé"]):
                result["analysis"] = "\n".join(lines[:i]).strip()
                break
        else:
            result["analysis"] = text_response.strip()

        mapping = {
            "stress_level": ["Niveau de stress"],
            "burnout_risk": ["Risque de burnout"],
            "motivation_engagement": ["État de motivation", "Motivation"],
            "adaptability": ["Adaptabilité"],
            "social_integration_tendency": [
                "Capacité de régulation émotionnelle",
                "Tendance à l'intégration sociale"
            ]
        }

        for key, labels in mapping.items():
            value = extract_value(text_response, labels)
            if value and value.lower() in ["faible", "modéré", "élevé"]:
                result["psychosocial_status"][key] = value.lower()

        # Résumé
        result["summary"] = extract_resume(text_response) or \
                           "Résumé non disponible dans le format attendu."

        return json.dumps(result, indent=4, ensure_ascii=False)

    except Exception:
        return json.dumps({
            "type": "object",
            "analysis": text_response,
            "psychosocial_status": {
                "stress_level": "modéré",
                "burnout_risk": "modéré",
                "motivation_engagement": "modéré",
                "adaptability": "modéré",
                "social_integration_tendency": "modéré"
            },
            "summary": "Erreur lors du formatage de la réponse."
        }, indent=4, ensure_ascii=False)