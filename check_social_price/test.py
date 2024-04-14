import cv2
import pathlib
import torch

pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')
image = cv2.imread('test.jpg')
results = model(image)
results.save('result.png')

detections = results.xyxy[0].tolist()
for detection in detections:
    if detection[5] > 0.5:
        print(f"Обнаружен {results.names[int(detection[5])]} на координатах {detection[:4]}")
        cropped_image = image[int(detection[1]):int(detection[3]), int(detection[0]):int(detection[2])]
        cv2.imwrite(f'result_{detection[5]}.jpg', cropped_image)
