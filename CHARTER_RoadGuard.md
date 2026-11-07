# **RoadGuard Project Charter**

**AI-Powered Road Hazard Detection and Prioritization System**  
Team members: Benny Saliroses, Ovad Biton, Or Arbeli, Shai Sadeh

# **1  Problem and User**

A municipal infrastructure control-center manager or public works manager receives road-hazard reports and photographs of inconsistent quality and must quickly determine the hazard type and whether it requires urgent inspection, scheduling in the maintenance plan, or additional evidence. Uniform manual triage delays important cases and may dispatch crews to false alarms. RoadGuard will analyze an image, detect cracks and potholes, and recommend a justified next action. It is a decision-support system only: it will not determine engineering fitness or close a road without approval from an authorized professional.  
The long-term operational objective is to shorten triage and repair times and reduce unnecessary site visits. Reducing response time from 72 hours to 4 hours and contractor costs by 35% will be treated as future pilot targets, because the public dataset does not contain repair-time, cost, or claim data with which to measure them during the course project.

# **2  Success Metrics and Evaluation**

| Component | Target and Evaluation |
| :---- | :---- |
| Original CV targets | D40 recall ≥ 0.80 and overall mAP@0.5 ≥ 0.55. These remain the original project targets; the currently documented exported model did not meet them. |
| Operating-point selection | Compare confidence thresholds on validation data and report D40 precision, recall, F1, and false-positive counts. The team's revised working criterion is to maximize D40 recall subject to D40 precision ≥ 0.30. This is a project selection criterion, not a demonstrated operational requirement. |
| Detection benchmarks | Compare YOLOv5nu and YOLOv8n experiments using the same prepared data split. Report overall and per-class precision, recall, mAP@0.5, and mAP@0.5:0.95. |
| Classical baseline | HOG + SVM on annotated damage crops. This evaluates classification with known object locations and is reported separately from full-image object detection. |
| Agent evaluation | Target ≥ 85% correct actions on 50 held-out scenarios based on real images, including at least 20 with free-text reports. Two reviewers independently label reference actions without seeing system outputs; disagreements are adjudicated. Compare the agent with a fixed-rule baseline on the same cases. |
| Explanation grounding | Target ≥ 90% supported explanations among cases requiring a source. Review whether each cited passage supports the recommendation, rather than checking citation presence alone. |
| RAG evaluation | Use 30 reference questions plus approximately 10 questions for which the corpus contains no sufficient answer. Assess retrieval relevance, answer correctness, citation support, and appropriate abstention. |

Report sample sizes, denominators, errors, and evaluation status alongside every result. Software tests and synthetic scenarios verify implementation behavior but do not establish real-world decision quality.

The prepared train/validation/test split was retained. Cross-split checks were performed, but original camera-sequence identifiers are unavailable, so neighboring-frame leakage cannot be ruled out. Country-level evaluation is reported only where reliable metadata exists.

The existing test set has already been inspected during development. Results on it must be described as retrospective; an independently held-out set is required for an unbiased assessment after further model or threshold selection. A local field evaluation remains planned and must not be presented as completed.

# **3  Data and Plan B**

**Primary source**  
The implemented CV experiments use the team's processed archive of the Roboflow “road-damage-10k” dataset, version 1:
https://universe.roboflow.com/xjsj/road-damage-10k/dataset/1

This archive must not be described as the complete canonical RDD2022 dataset. Dataset provenance, preprocessing, split composition, and class mapping are documented in the model notebook and model card.

The native training class order is 0=D20, 1=D00, 2=D40, 3=D10. The exported ONNX model reorders its class-score channels to 0=D00, 1=D10, 2=D20, 3=D40. Consumers must follow the export contract and must not apply a second permutation.

The source listing specifies CC BY 4.0. Preserve attribution and document applicable terms for the processed data, pretrained models, exported weights, and RAG documents separately.

The dataset does not include pothole depth, engineering severity, repair time, or cost. Bounding-box area will not be presented as physical damage area or true severity. Operational priority will be calculated from the hazard class, model confidence, and user-provided metadata such as road type and lane obstruction.  
**RAG corpus**  
We will build a controlled corpus of official road-maintenance guidance and response procedures. Each passage will retain the issuing body, date, hazard type, triggering conditions, and source link. If sufficiently detailed Israeli guidance is unavailable, official international manuals will be used and clearly labeled as non-binding in Israel.  
Plan B: If dataset size or training time becomes a constraint, we will use a subset containing potholes and alligator cracks. If object detection does not converge, we will switch to crop classification without precise localization. The thematic fallback is TACO, a public-space litter detection dataset licensed under CC BY 4.0.

# **4  System Architecture**

| Image and metadata  →  Quality check  →  CV model  →  Prioritization agent  →  Recommended action |
| :---: |

The agent also receives the procedures corpus and safety rules, then chooses among urgent inspection, the standard work queue, and human review. The first version will process an uploaded image through validation, detection, bounding-box display, procedure retrieval, and recommendation generation. Connections to a municipal call center, map, or contractor-management system will be demonstrated with mock tools only.

# **5  The Agent's Seat**

**Decision**  
The agent combines the computer-vision output, image quality, road type, lane obstruction, model confidence, and retrieved procedure. It selects urgent inspection, the standard queue, a request for additional evidence, or human review. A pothole obstructing a lane on a major road will be escalated for urgent inspection; an uncertain finding will be routed for a new photograph or human review. The agentic architecture is intended to handle incomplete or unstructured reports, request missing evidence, retrieve relevant procedures, and select appropriate tools within a bounded workflow. Its added value over a fixed-rule implementation is an evaluation question, not an assumed result. Both approaches will be compared on the same independently labelled real-image scenarios, including ambiguous findings, missing metadata, unsupported queries, and tool failures. Evaluation will report action correctness, source support, unsafe recommendations, and processing time.

**Tools**

* check\_hazard\_severity — calculates operational priority using transparent rules.  
* query\_repair\_standards — retrieves the relevant guidance and source from the corpus.  
* request\_additional\_evidence — requests another photograph or missing information.  
* create\_draft\_work\_order — creates a local draft task only.  
* flag\_for\_urgent\_review — alerts a human supervisor and does not close a road.

Fallback: If the image is insufficient, confidence is low, no supporting procedure is found, or a tool fails, the agent will not create a work order. The case will be transferred to human review. Without the agent, the system will still display bounding boxes and a findings list, but will not prioritize cases automatically.

# **6  Risks and Cut-Down Version**

| Risk | Mitigation |
| :---- | :---- |
| Domain gap between the development data and Israeli deployment conditions | Evaluate on an independent local image set before operational use. Report country-level results only when reliable metadata exists; explicitly disclose unavailable metadata and untested deployment conditions. |
| No severity or depth labels | Do not train a severity target; use rule-based operational priority and metadata |
| An incorrect action creates safety risk or expense | Keep external actions mocked; require human approval for every urgent or uncertain case |

Cut-down version: If the advanced components are not working by the mid-project checkpoint, we will deliver a system that detects potholes and alligator cracks, retrieves relevant guidance, and classifies each case as urgent or routine using fixed rules. We will omit severity estimation, mapping, and work-order generation.

# **7  Milestones and Ownership**

| Date | Deliverable | Owner |
| :---- | :---- | :---- |
| \[Date 1\] | Download, licensing, EDA, and leakage-safe split | \[ovad\] Data Lead |
| \[Date 2\] | Baseline and image preprocessing | \[Shai\] CV Data Lead |
| \[Date 3\] | Detector training and error analysis | \[Shai\] CV ML Lead |
| \[Date 4\] | Corpus, retrieval, and groundedness | \[Benny\] RAG Lead |
| \[Date 5\] | Agent tools and evaluation scenarios | \[Or\] Agent Lead |
| \[Date 6\] | Integration, field test, demo, and presentation | Entire team |

The project has implemented four-class CV experiments and an integrated agent application. The current phase focuses on documenting the delivered artifacts, reassessing the detector operating point, evaluating agent decisions against a fixed-rule baseline, and evaluating RAG relevance, grounding, and abstention. Planned evaluations are marked as pending until their labelled cases, outputs, and results are available. Every substantial pull request will be reviewed by another team member.
