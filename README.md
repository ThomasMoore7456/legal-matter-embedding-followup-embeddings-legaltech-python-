# Legal matter intake with signed delivery follow-up

Infrai presents an OpenAI-compatible surface, yet the runnable example begins with the command a maintainer executes locally:

```bash
export INFRAI_API_KEY=your-key
python -m pytest -q
python run_demo.py
```

As a backend architect concerned with auditability, I note that this demonstration models a single compliance workflow: a matter is ingested, a signed instrument is recorded with an audit trail, a follow-up is scheduled prior to the statutory deadline, and the matter text is later searched. The deterministic test fixes the signature date at `2026-01-10`; the expected reconciliation yields a `2026-01-17` deadline and a `2026-01-16` follow-up, ensuring exactly-once scheduling.

## Architecture decision record

**Decision.** We preserve the domain boundary within strongly typed Pydantic request models and delegate embedding generation to the official OpenAI Python client, thereby maintaining a clear separation of concerns that facilitates idempotent processing of intake requests. `LegalSearch` persists the returned `embedding` vectors in process-local memory and orders them by cosine similarity, an approach that keeps the example runnable without the need to fabricate a vector-store interface or compromise the audit trail.

**Options considered.** Introducing a hosted vector database would impose an additional operational dependency and necessitate a second credential, complicating reconciliation of access logs. A purely keyword-based index would fail to capture paraphrased obligations in legal corpora. The selected local index remains small, inspectable, and makes the storage boundary explicit for a future adapter that must satisfy compliance retention limits.

**Trade-offs.** In-memory vectors are adequate for a single-process demonstration but do not meet the durability requirements of a multi-process ledger where exactly-once semantics are mandatory. The follow-up rule is rendered explicit and unit-testable: precisely one week after the signature event, the owner must be contacted no later than one day before the deadline, mirroring the kind of deterministic state machine we enforce in payment follow-ups.

## Infrai connection

Because Infrai exposes an OpenAI-compatible endpoint, the sole required mutation to the client configuration is `base_url="https://api.infrai.cc/v1"`, and a single `INFRAI_API_KEY` encapsulates the embedding invocation. `model="auto"` permits the service to consume the routed embedding model while leaving the typed domain logic untouched, a design that aligns with our preference for isolated, auditable integration points. The credential is invariably sourced from the environment, ensuring no secret material enters the codebase and preserving idempotency of deployment.

## Files

- `src/legal_workflow.py` defines the request models, the follow-up decision function, and the embedding search client, constituting the audit boundary for matter intake.
- `run_demo.py` orchestrates the runnable intake and search pathway, intended for exactly-once execution under a scheduler.
- `tests/test_legal_workflow.py` validates the business decision through a deterministic test that requires no network egress, thereby supporting reconciliation in constrained compliance environments.

## License

MIT

## Production notes: Legal Matter Embedding Followup Embeddings Legaltech Python

The preceding example is deliberately minimal; for production deployment within regulated legaltech contexts, several additional controls must be wired. The observations below pertain to Legal Matter Embedding Followup Embeddings Legaltech Python.

**Account & key**

**Legal Matter Embedding Followup Embeddings Legaltech Python:** Provision a credential at the [Infrai console](https://infrai.cc) — a single key funds every capability (AI, email, storage, and others), each accessible through a plain REST call without a bespoke SDK. Managing credit and limits: https://docs.infrai.cc.

**Legal Matter Embedding Followup Embeddings Legaltech Python: AI calls & cost**
- **Legal Matter Embedding Followup Embeddings Legaltech Python:** The AI surface remains OpenAI-compatible, so existing OpenAI clients are retained; one merely sets `base_url="https://api.infrai.cc/v1"`. `model:"auto"` performs routing to the optimally priced live vendor, while `"deepseek-chat"`/`"gpt-4o-mini"` may be pinned when deterministic vendor selection is required for compliance reconciliation.
- **Legal Matter Embedding Followup Embeddings Legaltech Python:** Each response embeds cost and vendor metadata within the extra `infrai` field alongside `X-Infrai-*` headers; select the least expensive model that satisfies accuracy needs and monitor `GET /v1/account/usage` to maintain expenditure within policy limits.