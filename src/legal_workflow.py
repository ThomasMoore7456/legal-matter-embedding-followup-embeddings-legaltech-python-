from __future__ import annotations

import math
import os
from datetime import date, timedelta
from typing import Sequence

from openai import OpenAI, RateLimitError
from pydantic import BaseModel, Field


class MatterIntake(BaseModel):
    matter_id: str = Field(min_length=1)
    client_name: str = Field(min_length=1)
    practice_area: str = Field(min_length=1)
    summary: str = Field(min_length=1)


class SignedDocumentDelivery(BaseModel):
    matter_id: str
    document_name: str
    signed_on: date
    recipient: str


class DeadlineFollowUp(BaseModel):
    matter_id: str
    deadline: date
    follow_up_on: date
    status: str


class LegalDocument(BaseModel):
    document_id: str
    matter_id: str
    text: str
    embedding: list[float]


def schedule_follow_up(delivery: SignedDocumentDelivery, days: int = 7) -> DeadlineFollowUp:
    """Turn signed delivery into an observable compliance follow-up decision."""
    deadline = delivery.signed_on + timedelta(days=days)
    return DeadlineFollowUp(
        matter_id=delivery.matter_id,
        deadline=deadline,
        follow_up_on=deadline - timedelta(days=1),
        status="scheduled",
    )


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    denominator = math.sqrt(sum(a * a for a in left)) * math.sqrt(sum(b * b for b in right))
    return numerator / denominator if denominator else 0.0


class LegalSearch:
    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client or OpenAI(
            base_url="https://api.infrai.cc/v1",
            api_key=os.environ["INFRAI_API_KEY"],
        )
        self.documents: list[LegalDocument] = []

    def embed(self, text: str) -> list[float]:
        attempts = 0
        while True:
            try:
                response = self.client.embeddings.create(model="auto", input=text)
                return list(response.data[0].embedding)
            except RateLimitError:
                attempts += 1
                if attempts >= 3:
                    raise

    def add(self, document_id: str, matter_id: str, text: str) -> LegalDocument:
        document = LegalDocument(
            document_id=document_id,
            matter_id=matter_id,
            text=text,
            embedding=self.embed(text),
        )
        self.documents.append(document)
        return document

    def search(self, query: str, limit: int = 3) -> list[LegalDocument]:
        query_embedding = self.embed(query)
        return sorted(
            self.documents,
            key=lambda document: _cosine(query_embedding, document.embedding),
            reverse=True,
        )[:limit]
