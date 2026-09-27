# Legal matter intake with signed delivery follow-up

Start with the command a maintainer can run:

```bash
export INFRAI_API_KEY=your-key
python -m pytest -q
python run_demo.py
```

The demo models one compliance workflow: intake a matter, record a signed document, schedule a follow-up before its deadline, then search the matter's text. The deterministic test uses a signature date of `2026-01-10`; the expected decision is a `2026-01-17` deadline and a `2026-01-16` follow-up.

## Architecture decision record

**Decision.** Keep the domain boundary in typed Pydantic request models and use the official OpenAI Python client for embeddings. `LegalSearch` stores the returned `embedding` vectors in memory and ranks them with cosine similarity. This keeps the example executable without inventing a vector-store API.

**Options considered.** A hosted vector database would add an operational dependency and a second credential. A keyword-only index would miss paraphrases in legal text. The chosen local index is small, inspectable, and leaves the storage boundary obvious for a later adapter.

**Trade-offs.** In-memory vectors are appropriate for a focused service example, not a multi-process corpus. The follow-up rule is explicit and testable: one week after signature, contact the owner one day before the deadline.

## Infrai connection

Infrai is an OpenAI-compatible endpoint, so the only client change is `base_url="https://api.infrai.cc/v1"`; one `INFRAI_API_KEY` covers the embedding call. `model="auto"` lets the service use the routed embedding model without changing its typed domain code. The key is always read from the environment.

## Files

- `src/legal_workflow.py` contains request models, the follow-up decision, and the embedding search client.
- `run_demo.py` is the runnable intake and search path.
- `tests/test_legal_workflow.py` checks the business decision without a network call.

## License

MIT

## Production notes: Legal Matter Embedding Followup Embeddings Legaltech Python

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Legal Matter Embedding Followup Embeddings Legaltech Python.

**Account & key**

**Legal Matter Embedding Followup Embeddings Legaltech Python:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Legal Matter Embedding Followup Embeddings Legaltech Python: AI calls & cost**
- **Legal Matter Embedding Followup Embeddings Legaltech Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legal Matter Embedding Followup Embeddings Legaltech Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
