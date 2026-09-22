from datetime import date

from src.legal_workflow import LegalSearch, MatterIntake, SignedDocumentDelivery, schedule_follow_up


def main() -> None:
    matter = MatterIntake(
        matter_id="MAT-1042",
        client_name="Northstar Payments",
        practice_area="data protection",
        summary="Review processor addendum and signature evidence.",
    )
    delivery = SignedDocumentDelivery(
        matter_id=matter.matter_id,
        document_name="processor-addendum.pdf",
        signed_on=date(2026, 9, 1),
        recipient="compliance@northstar.example",
    )
    print(schedule_follow_up(delivery).model_dump(mode="json"))

    search = LegalSearch()
    search.add("DOC-1", matter.matter_id, "The processor must notify the controller within 48 hours.")
    search.add("DOC-2", matter.matter_id, "Signed copies are retained with the matter audit record.")
    for document in search.search("notification deadline for a processor incident"):
        print(document.document_id, document.text)


if __name__ == "__main__":
    main()
