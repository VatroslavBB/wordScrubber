import numpy as np
import cv2
from datetime import datetime
from pathlib import Path


def resizeImage(num):
    return max(32, (num // 32) * 32)


def scrubImage(image) -> None:
    image = cv2.resize(image, (resizeImage(image.shape[1]), resizeImage(image.shape[0])))
    
    annotated_db50_image = image.copy()
    orig_db50_image = image.copy()
    
    inputSize = (image.shape[1], image.shape[0])
    
    textDetectorDB50 = cv2.dnn_TextDetectionModel_DB(r"models/DB50.onnx")
    
    bin_thresh = 0.3
    poly_thresh = 0.5
    mean = (122.67891434, 116.66876762, 104.00698793)
    textDetectorDB50.setBinaryThreshold(bin_thresh).setPolygonThreshold(poly_thresh)
    textDetectorDB50.setInputParams(1.0/255, inputSize, mean, True)
    
    inpaint_mask_db50 = np.zeros(image.shape[:2], dtype=np.uint8)
    
    boxesDB50, _ = textDetectorDB50.detect(image)
    
    for box in boxesDB50:
        cv2.fillPoly(inpaint_mask_db50, [np.array(box, np.int32)], 255)
        cv2.polylines(annotated_db50_image, [np.array(box, np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)

    inpainted_db50_image = cv2.inpaint(orig_db50_image, inpaint_mask_db50, inpaintRadius=5, flags=cv2.INPAINT_NS)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputDir = Path.home() / "Desktop" / "WordScrubberImg"
    outputDir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(outputDir / f"screen_{timestamp}.jpg"), inpainted_db50_image)

    return None


