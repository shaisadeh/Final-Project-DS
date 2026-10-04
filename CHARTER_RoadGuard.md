# **RoadGuard Project Charter**

**AI-Powered Road Hazard Detection and Prioritization System**  
Team members: Benny Saliroses, Ovad Biton, Or Arbeli, Shai Sadeh

# **1  Problem and User**

A municipal infrastructure control-center manager or public works manager receives road-hazard reports and photographs of inconsistent quality and must quickly determine the hazard type and whether it requires urgent inspection, scheduling in the maintenance plan, or additional evidence. Uniform manual triage delays important cases and may dispatch crews to false alarms. RoadGuard will analyze an image, detect cracks and potholes, and recommend a justified next action. It is a decision-support system only: it will not determine engineering fitness or close a road without approval from an authorized professional.  
The long-term operational objective is to shorten triage and repair times and reduce unnecessary site visits. Reducing response time from 72 hours to 4 hours and contractor costs by 35% will be treated as future pilot targets, because the public dataset does not contain repair-time, cost, or claim data with which to measure them during the course project.

# **2  Success Metrics**

| Component | Target and Evaluation |
| :---- | :---- |
| Primary metric | At least 80% recall for pothole class D40 on the test set |
| Secondary metric | mAP@0.5 of at least 0.55 across all classes, reported by class and country |
| Baseline | HOG with SVM or Random Forest on annotated damage regions, compared with YOLO or Faster R-CNN |
| Agent evaluation | 85% correct decisions across 50 scenarios; 90% of explanations grounded in a retrieved source |

Where metadata permits, the split will be performed by country or image sequence to prevent leakage between neighboring frames. We will also conduct a field test on 30–50 local images that will not be used for training.

# **3  Data and Plan B**

**Primary source**  
RDD2022 contains 47,420 road images from six countries and more than 55,000 annotated damage instances. Its four shared classes are longitudinal crack D00, transverse crack D10, alligator crack D20, and pothole D40. The annotations support object detection, and the dataset is distributed under the CC BY-SA 4.0 license. Source: https\://github.com/sekilab/RoadDamageDetector  
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
The agent combines the computer-vision output, image quality, road type, lane obstruction, model confidence, and retrieved procedure. It selects urgent inspection, the standard queue, a request for additional evidence, or human review. A pothole obstructing a lane on a major road will be escalated for urgent inspection; an uncertain finding will be routed for a new photograph or human review. An agentic architecture is strictly required for RoadGuard because the hazard triage and dispatch workflow cannot be reduced to a static script or a fixed \`if-else\` rule chain. The operational sequence and tool usage must adapt dynamically at runtime based on unstructured and variable inputs.  
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
| Domain gap between dataset countries and Israel | Evaluate by country and on a local field set; report performance degradation explicitly |
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

At the mid-project checkpoint, we will make a Go or No-Go decision on supporting all four classes. Expansion will occur only after the two-class version works end to end. Every substantial pull request will be reviewed by another team member.
