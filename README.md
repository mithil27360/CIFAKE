# Real vs Fake Image Classifier

**ResNet-18 · Transfer Learning · PyTorch · Apple MPS**

A binary image classifier that detects whether an image is **real**  or **AI-generated** , trained on the CIFAKE dataset. Achieves **97.67% test accuracy** with an AUC of **0.9971**.



## Results

| Metric | Score |
|||
| Test Accuracy | 97.67% |
| Precision | 0.9803 |
| Recall | 0.9728 |
| F1 Score | 0.9766 |
| AUC Score | 0.9971 |

### Confusion Matrix (20,000 test images)

|  | Predicted FAKE | Predicted REAL |
||||
| **Actual FAKE** | 9,805 (True Negatives) | 195 (False Positives) |
| **Actual REAL** | 272 (False Negatives) | 9,728 (True Positives) |



## Dataset

[CIFAKE](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images) — 120,000 images total.

- **Train**: 50,000 REAL + 50,000 FAKE
- **Test**: 10,000 REAL + 10,000 FAKE

REAL images come from CIFAR-10 (photographs). FAKE images were generated using Stable Diffusion 1.4.

```
archive/
├── train/
│   ├── REAL/
│   └── FAKE/
└── test/
    ├── REAL/
    └── FAKE/
```



## Approach

### Architecture

Pre-trained **ResNet-18** (ImageNet weights) with the final fully-connected layer replaced for binary classification (1 output neuron + sigmoid).

### Two-Phase Training

**— FC Layer Only (3 epochs)**
- Backbone fully frozen
- Only the final classification layer trains
- Learning rate: `1e-3` with StepLR scheduler
- Best model saved on validation accuracy

**— Full Fine-Tuning (early stopping)**
- All layers unfrozen
- Very low learning rate: `1e-5` to avoid destroying pretrained features
- Early stopping with patience=2 to prevent overfitting
- Best checkpoint restored automatically

### Key Design Decisions

- **BCEWithLogitsLoss** instead of BCE — numerically stable, sigmoid applied only at inference
- **128×128 resize** — CIFAKE is originally 32×32; upscaling improves feature extraction with pretrained models
- **ImageNet normalization** (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`) — matches ResNet's pretraining distribution
- **80/20 train/val split** — test set is completely untouched until final evaluation
- **Clean validation transform** — augmentation applied only to training data, not validation




## Limitations

This model is optimized for the CIFAKE distribution — REAL images from CIFAR-10 and FAKE images from Stable Diffusion 1.4. Real-world performance will vary on images from other generators (Midjourney, DALL-E, etc.) or high-resolution photography, due to domain shift.

