# RoadGuard — CV Model Card

## Intended use
Human decision support for municipal road-hazard image triage. Not engineering certification,
depth estimation, physical damage measurement, or autonomous road closure/dispatch.

## Data and provenance
- Repository: https://github.com/shaisadeh/Final-Project-DS.git
- Commit: 05b9d4f4fac4c5fb2c53fb0a6e443bb5412e7bfe
- Processed archive: https://drive.google.com/file/d/1xzHdXoXc4NPibka0KG9GAqq_EfdTUulo/view?usp=sharing
- Archive SHA256: 9551c4a5d43cdd9a100796d58476c7245e635174be57870e10439104c7bab84c
- Upstream project: https://universe.roboflow.com/xjsj/road-damage-10k/dataset/1
- Team-processed archive; do not identify it as canonical RDD2020/RDD2022 without evidence.
- Original YAML names: {0: 'Class_0', 1: 'Class_1', 2: 'Class_2', 3: 'Class_3'}
- Used semantic mapping: {0: 'D20', 1: 'D00', 2: 'D40', 3: 'D10'}
- Mapping status: Original Roboflow YAML supplied by user; repository preprocessing preserves numeric class IDs.
- Source listing: CC BY 4.0. Retain source attribution; verify derivative/weight redistribution rights separately.
- Original source YAML class order: AlligatorCrack, LongitudinalCracks, Potholes, TransverseCrack.

## Protocol
Preserved the prepared split. HOG-SVM uses training-only scaling and validation-only C selection.
Detectors use pretrained weights, AdamW, shared data/seed/budget, existing offline augmentation,
early stopping, and validation-only model/threshold selection.
The test set was inspected during development. Results are retrospective results on an exposed test set; no more tuning is authorized by this protocol. A changed model requires fresh independent evaluation.
File hashes, decoded-pixel hashes, and normalized original names were checked across splits.
Original camera-sequence IDs are unavailable: neighboring-frame leakage is NOT ruled out.
YOLOv5nu denotes Ultralytics YOLOv5u rather than original anchor-based YOLOv5.

## Frozen research candidate — human review required
{
  "chosen_model": "yolov8_n_lr0003_coloraug",
  "thresholds": {
    "yolov5u_n": 0.15,
    "yolov8_n": 0.15,
    "yolov8_n_lr0003": 0.25,
    "yolov8_n_lr0003_coloraug": 0.01
  },
  "matching_iou": 0.5,
  "nms_iou": 0.7,
  "mapping_verified": true,
  "selection": "validation only; targets met, then D40 recall, then mAP50, then YOLOv8 tie-break"
}

## Final test detection result
{
  "model": "yolov8_n_lr0003_coloraug",
  "map50": 0.37783725086402514,
  "map50_95": 0.15610258516535566,
  "threshold": 0.01,
  "d40_recall": 0.794074074074074,
  "d40_precision": 0.043762246897452645,
  "targets_status": "FAIL",
  "parameters": 3138732,
  "train_seconds": 3208.614947414,
  "selected_on_validation": true
}
All detector results: test_detection_summary.csv; per-class and country CSVs are separate.
Crop classification results are a distinct oracle-localization diagnostic, not detection mAP.

## Domain gap and limitations
Field evaluation: not_run, N=0.
No detections do not establish that a road is safe. Small/occluded defects, shadows, markings,
image quality, country/domain differences and annotation errors can affect performance.
Bounding-box area is a fraction of image pixels, not physical area or engineering severity.
Quality heuristics are not calibrated; confidence scores are not calibrated probabilities.
Targets are not accepted as semantically verified unless the class mapping is verified.

## Agent integration — pending team component
Input contract: example_agent_payload.json. Outputs remain human-review cases until an agent is connected.
Provide official guidance passages with issuing body, date, hazard type, triggering conditions and URL.
Clearly label international manuals as non-binding in Israel when applicable.
Implement and evaluate the charter tools: check_hazard_severity, query_repair_standards,
request_additional_evidence, create_draft_work_order and flag_for_urgent_review.
The severity tool computes transparent operational priority, not engineering severity.
The agent dynamically selects tools and uses image quality, metadata, CV and retrieved guidance.
If quality/confidence is insufficient, no supporting procedure is found, metadata is missing,
or a tool fails: no work order; request evidence or transfer to human review.
All external municipal/map/contractor connections must remain mocked in the course project.

## Agent evaluation protocol — not executed
Use 50 held-out, independently labelled scenarios covering potholes, cracks, poor images,
missing metadata, low-confidence/ambiguous findings, missing sources and tool failures.
Reference actions: urgent inspection / standard queue / request evidence / human review.
At least 43/50 correct decisions meets the 85% target.
For source-requiring explanations, at least 90% must be supported by the retrieved passages;
record supporting passage IDs and assess correctness of the claim-source relationship.
Also record unsupported claims and unsafe-action attempts. Report denominators and scenario results.
No synthetic scores or success claims are supplied here.

## Operational targets and next steps
72h to 4h response time and 35% contractor savings require a real pilot with operational data.
The source mapping has been corrected using original YAML and ID-preserving preprocessing. Resolve remaining provenance/licensing and sequence limitations; complete independent local testing. No additional training is needed to document this project phase.
If four-class deployment is not viable, the charter allows a separately evaluated D20/D40 cut-down version;
this notebook does not silently drop classes or reuse four-class metrics for that version.
Monitor recall/precision on labelled audits, domain/quality drift, field error types and review volume.
Retrain only with a versioned dataset and a fresh held-out evaluation protocol.
