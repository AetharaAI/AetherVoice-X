import pytest

from services.asr.app.schemas.requests import ASRTriageRequest
from services.asr.app.services.triage_service import TriageService


@pytest.mark.asyncio
async def test_triage_marks_electrical_hazard_as_emergency():
    service = TriageService()
    result = await service.classify(
        "req_test",
        ASRTriageRequest(
            session_id="sess_test",
            domain="electrical_emergency",
            transcript="My panel is sparking and there is a burning smell.",
        ),
    )
    assert result.classification == "emergency"
    assert result.requires_human_review is True


@pytest.mark.asyncio
async def test_triage_marks_short_input_as_unclear():
    service = TriageService()
    result = await service.classify(
        "req_test",
        ASRTriageRequest(
            session_id="sess_test",
            domain="locksmith_urgent",
            transcript="Need help",
        ),
    )
    assert result.classification == "unclear"
