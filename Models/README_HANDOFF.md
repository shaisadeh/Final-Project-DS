# RoadGuard — webapp/agent handoff

Required paths:
- webapp/assets/models/yolov8n-roadguard.onnx
- data/batch_eval/yolo_predictions.csv

This is the frozen validation-selected YOLOv8n color-augmentation experiment. No new training was performed. The exported ONNX graph reorders actual class-score channels to 0=D00, 1=D10, 2=D20, 3=D40. The native PyTorch checkpoints retain 0=D20, 1=D00, 2=D40, 3=D10. Do not apply another class-order permutation in the browser.

Input: float32 RGB NCHW [1,3,640,640], divided by 255. Preserve aspect ratio using letterbox padding with value 114, not a stretched resize. Raw output: [1,8,8400] for the standard 640 YOLOv8n graph; read the actual shape in handoff_contract.json. Channels are cx,cy,w,h,D00,D10,D20,D40. There is no separate objectness channel; do not apply another sigmoid. Implement confidence filtering and class-aware NMS externally. Remove padding and undo the resize scale for original-image xyxy pixel boxes. Frozen confidence and NMS parameters are in handoff_contract.json. The model is float32, static batch 1, without embedded NMS.

CSV uses the requested six columns and one row per test image. bbox uses COLONS, following the two supplied example rows (the prose specification instead mentioned commas). Boxes refer to original image pixels. top1 is the highest-confidence retained detection across all four classes, not necessarily a pothole. Multiple detections are intentionally reduced to one; this CSV cannot reproduce full detection mAP or pothole recall. Use the per-detection/per-class evaluation reports in the full results ZIP for those metrics.

No-detection rows are retained with blank top1_class, blank bbox, confidence 0.0. Treat these as missing visual evidence requiring review; do not assign a fake damage class or zero-size box, and do not interpret them as a safe road. Check the count in handoff_contract.json. The agent must skip area_ratio calculation for blank boxes.

Conversion checks compare PyTorch vs native ONNX and verify the actual output permutation on up to three validation images. The CSV reuses completed PyTorch test inference. This is not a full ONNX evaluation or an onnxruntime-web browser test. Match the documented preprocessing/postprocessing and test browser loading on sample images before integration is accepted.

Research prototype: test D40 recall 0.7941, precision 0.0438, overall mAP50 0.3778 at threshold 0.01; both charter targets failed. Every result requires human review. Model scores are not calibrated probabilities, bbox area is not physical damage severity, and no autonomous work orders or road closures are authorized. Field and agent evaluation remain pending. A connected agent does not remove the CV limitations.
