# RoadGuard

AI-assisted road-damage detection and municipal triage.

**Team:** Benny Saliroses, Ovad Biton, Or Arbeli, Shai Sadeh.

## Problem and intended use

RoadGuard helps review road-hazard reports by combining image-based damage detection, report metadata, retrieval of maintenance guidance, and an agent-generated recommendation.

The system supports four actions: urgent inspection, standard queue, request for additional evidence, and human review.

This is a research prototype for human decision support. It does not certify road safety, estimate engineering severity, or authorize autonomous road closures or contractor dispatch.

## Repository structure

- `CHARTER_RoadGuard.md` — project objectives, scope, risks, and evaluation plan.
- `Data/` — dataset preparation, exploratory analysis, and corpus documentation.
- `Models/RoadGuard_Model_Notebook.ipynb` — CV experiments and evaluation workflow.
- `Models/reports/` — model card, recorded results, versions, and class mapping.
- `Models/handoff_contract.json` — exported model integration contract.
- `Models/README_HANDOFF.md` — preprocessing, postprocessing, and integration instructions.
- `Agents/` — agent service, browser application, RAG integration, and software tests.
- `Agents/README.md` — detailed application setup and architecture.

## Data and provenance

The CV experiments use the team's processed archive of Roboflow's **road-damage-10k, version 1**:

https://universe.roboflow.com/xjsj/road-damage-10k/dataset/1

Processed archive:

https://drive.google.com/file/d/1xzHdXoXc4NPibka0KG9GAqq_EfdTUulo/view

The archive is not presented as the complete canonical RDD2022 dataset. See `Models/reports/MODEL_CARD.md` for provenance, archive hash, class mapping, and split limitations.

Damage classes:

| Class | Meaning |
|---|---|
| D00 | Longitudinal crack |
| D10 | Transverse crack |
| D20 | Alligator cracking |
| D40 | Pothole |

The data does not provide pothole depth or engineering severity. Bounding-box area represents image pixels, not physical damage area.

The source listing specifies CC BY 4.0. Dataset attribution and applicable terms for model weights and corpus documents must be documented separately.

## Methodology

The CV work includes:

1. A HOG + SVM crop-classification baseline.
2. A YOLOv5nu detection benchmark.
3. YOLOv8n experiments with learning-rate and color-augmentation variations.
4. Validation-based model and confidence-threshold comparison.
5. Detection evaluation and error analysis.

Crop classification uses annotated object locations and is not directly equivalent to full-image detection.

The prepared data split was retained. Cross-split checks do not rule out neighboring-frame leakage because original sequence identifiers are unavailable. The test set was inspected during development, so its reported results are retrospective.

## Documented exported model

The currently documented export is the `yolov8_n_lr0003_coloraug` experiment.

| Metric | Recorded result |
|---|---:|
| Confidence threshold | 0.01 |
| D40 precision | 4.38% |
| D40 recall | 79.41% |
| Overall mAP@0.5 | 0.3778 |
| Overall mAP@0.5:0.95 | 0.1561 |

These figures describe the exported model recorded in `Models/reports/MODEL_CARD.md`; they are not results for a newly selected operating point.

The original targets were D40 recall ≥ 80% and overall mAP@0.5 ≥ 0.55. Both were missed. The low D40 precision also indicates a substantial false-positive burden.

Following review, the team is reassessing the precision–recall trade-off. The revised working selection criterion is to maximize validation D40 recall subject to D40 precision ≥ 30%. A candidate found during this analysis must not be described as deployed until its evaluation and exported artifacts are updated consistently.

## Model integration

Documented browser-model path:

`Agents/webapp/assets/models/yolov8n-roadguard.onnx`

Check `Models/handoff_contract.json` and `Models/README_HANDOFF.md` before replacing or integrating weights.

- Input: RGB float32, NCHW, 640 × 640, normalized by 255.
- Preserve aspect ratio with letterbox padding.
- Native training class order: D20, D00, D40, D10.
- Exported ONNX class order: D00, D10, D20, D40.
- Confidence filtering and class-aware NMS are applied outside the exported graph.
- No detection does not establish that a road is safe.

The one-row-per-image prediction CSV is a reduced integration artifact. It cannot reproduce full detection mAP or per-class recall.

## Agent and RAG

The application combines visual findings, free-text reports, metadata, and retrieved guidance to recommend a next action.

Operational priority is distinct from engineering severity. Model confidence is not a calibrated probability of road safety.

Detailed architecture and setup:

[Agent README](Agents/README.md)

Project ChromaDB artifact:

https://drive.google.com/drive/folders/1jqhrnFsKQlf3XiQEkGhTrjjDyt1ytx0Y?usp=drive_link

The ChromaDB artifact must be accompanied by corpus provenance, document versions, licensing information, and compatible dependency versions. A database link alone is not a complete reproduction procedure.

## Evaluation plan following review

Software tests and synthetic scenarios are reported separately from evidence of real-world usefulness.

Planned evaluation:

- 50 held-out scenarios based on real images, including at least 20 with free-text reports.
- Independent reference-action labels from two reviewers who do not see system outputs, with disagreements adjudicated.
- Agent versus fixed-rule comparison on the same cases.
- Target ≥ 85% correct actions.
- Target ≥ 90% source-supported explanations among source-requiring cases.
- RAG evaluation using 30 reference questions plus approximately 10 questions without sufficient answers in the corpus.
- Reporting of errors, unsupported claims, unsafe recommendations, processing time, and sample sizes.

These targets and planned evaluations are not claims of achieved performance. Independent local field performance has not been established.

## Run the agent service

From the repository root:

```bash
cd Agents
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install dependencies and configure the service:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, configure the required settings, and follow `Agents/README.md` for the LLM provider, corpus initialization, and browser application.

Start the API:

```bash
uvicorn roadguard_api:app --host 127.0.0.1 --port 8000
```

Recorded CV dependency versions are available in `Models/reports/versions.json` and `Models/reports/requirements.freeze.txt`.

## Run software tests

From `Agents/`:

```bash
pip install -r requirements-dev.txt
pytest -q
```

Passing software tests does not establish detector quality, agent decision accuracy on real cases, or RAG answer quality.

## Limitations and next steps

- Complete and document the revised detector operating-point evaluation.
- Keep model weights, thresholds, class mapping, model card, and application configuration consistent.
- Complete the real-image agent-versus-rules evaluation.
- Evaluate RAG retrieval, answer support, and abstention.
- Document corpus sources, licenses, versions, and reproduction steps.
- Evaluate on independent local images before operational use.

Response-time reductions and contractor-cost savings remain future pilot objectives; they were not measured in this course project.
