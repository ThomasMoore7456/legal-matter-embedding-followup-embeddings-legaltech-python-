from datetime import date

from src.legal_workflow import SignedDocumentDelivery, schedule_follow_up


def test_signed_delivery_sets_a_pre_deadline_follow_up() -> None:
    delivery = SignedDocumentDelivery(
        matter_id="MAT-7",
        document_name="msa.pdf",
        signed_on=date(2026, 1, 10),
        recipient="legal@example.com",
    )

    decision = schedule_follow_up(delivery)

    assert decision.deadline == date(2026, 1, 17)
    assert decision.follow_up_on == date(2026, 1, 16)
    assert decision.status == "scheduled"
