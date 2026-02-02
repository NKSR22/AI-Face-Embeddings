# Theory & Concept

## Face Detection: YuNet
YuNet is a lightweight and efficient face detection model based on Convolutional Neural Networks (CNN). 
- **Efficiency**: Optimized for CPU/Edge devices.
- **Accuracy**: Robust against various scales, viewpoints, and occlusions.
- **Output**: 15 key points including bounding box coordinates and facial landmarks (eyes, nose, mouth).

## Face Recognition: SFace
SFace is a deep learning-based face recognition model that generates a feature vector (embeddings) from a cropped and aligned face image.
- **Embeddings**: A face is compressed into a 128-dimensional or higher vector.
- **Metric Learning**: The model is trained so that images of the same person are "close" in mathematical space.

## Comparison Logic: Cosine Similarity
Unlike the old dlib-based systems that used Euclidean Distance, SFace works best with **Cosine Similarity**.
- **Formula**: Measures the cosine of the angle between two vectors.
- **Range**: -1 to 1.
- **Threshold**: In this project, we use a threshold of ~0.36. 
    - If `score > 0.36`, the identity is considered a match.

## Data Storage
- **Feature Extraction**: Features are extracted from images in `known_faces/` upon startup.
- **On-Device**: All computations happen locally. No biometric data is sent to the cloud.
