# The ACME corpus: what is in it, and what each file is for

Every lab in this course runs on this one document set. It is small on purpose: you can read all
of it in a few minutes, so when a retrieval scores 0.27 you can go and check whether that is
right. A course that demos on ten thousand documents is asking you to trust it.

Seven files, 571 words. Count it yourself:

```
python -c "from rag.corpus import load_documents; d=load_documents(); print(len(d), sum(len(x.text.split()) for x in d))"
```

| file | doc_id | words | what it is | what it is FOR in this course |
|---|---|---:|---|---|
| `filings/q2_2023_excerpt.md` | `filing_q2_2023` | 159 | a Form 10-Q excerpt | the 3% revenue line. The preface is padded on purpose so a naive fixed-size cut strands the heading away from the number. |
| `runbooks/error_catalog.md` | `error_catalog` | 94 | the platform error catalog | **where TS-999 lives.** The rare-token case a meaning search misses and a keyword search catches. |
| `policies/privacy.md` | `privacy` | 86 | a privacy policy | the PII and redaction case. |
| `policies/access_control.md` | `access_control` | 77 | an access policy | the permissions and refusal case: some answers exist and still must not be returned. |
| `tables/q2_kpis.md` (+ `.pdf`) | `q2_kpis` | 68 | a KPI table, in both markdown and PDF | the table case. A text splitter smashes a table; the PDF is there so the damage is real and not simulated. |
| `faq/support.md` | `faq` | 57 | a support FAQ | the paraphrase case: the question and the answer share no words. |
| `figures/caption.txt` | `figure_seats` | 30 | a figure caption | the multimodal case: when a caption is not enough and the page has to be read as an image. |
| | | **571** | 7 documents | |

## Which file answers which question

| question | file |
|---|---|
| How much did ACME make last quarter? | `filings/q2_2023_excerpt.md` |
| What does error code TS-999 mean? | `runbooks/error_catalog.md` |
| Can I share my login with a contractor? | `policies/access_control.md` |
| How many paid seats were there in Q2? | `tables/q2_kpis.md` |

## The companion files

- `eval/questions.jsonl` — the same questions every lab, each with the gold span it must retrieve.
  This is what makes "did it get better" a measurement instead of an impression.
- `rag/` — the one package. The code you keep.
- `labs/` — the short parts you run per lecture.
- `basics/` — the first small programs, including the ones that run with no API key.

## Why fictional

ACME is invented, and the numbers in it are invented, so that nothing in this course depends on a
real company's filings staying online or staying the same. Every number you see printed in a lab
traces back to one of these seven files, and you can open any of them and check.
