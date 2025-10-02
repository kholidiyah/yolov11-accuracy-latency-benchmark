# yolov11-accuracy-latency-benchmark
Scripts and pipeline for benchmarking Ultralytics YOLOv11 in real-time video object detection. Includes dataset preprocessing, pseudo-labeling, accuracy–latency profiling, and computational complexity analysis. Companion code for the paper on YOLOv11 trade-offs.

## Dataset
The dataset is derived from short surveillance-style CCTV clips.  
👉 You can watch one of the original reference clips here: 
Video Training (https://youtu.be/xtffU4dk4YI)
Video Validation (https://youtu.be/pw8T_aSRcx0)

## Pipeline & Scripts

> Generate pseudo-labels for train/val, sync to YOLO format folders, then run validation.
> Tested with Ultralytics >= 8.3.

### 0) Environment (once)
pip install ultralytics==8.3.203
yolo checks

# 1. Define paths (edit to your machine)
ROOT=/mnt/c/Data/2025/Bimbingan/Semester_7/Dataset_Video
DATA=$ROOT/data
RUNS=$ROOT/runs/detect

# 2. Predict on validation images → save labels (txt) + confidences
yolo detect predict model=yolo11s.pt \
  source=$DATA/dataset/images \
  save_txt=True save_conf=True \
  project=$RUNS name=val_labels

# 3. Predict on training images → save labels (txt) + confidences
yolo detect predict model=yolo11s.pt \
  source=$DATA/clip/images \
  save_txt=True save_conf=True \
  project=$RUNS name=train_labels

# 4. Prepare label folders (YOLO 5-column layout) 
mkdir -p $DATA/dataset/labels
mkdir -p $DATA/clip/labels

# 5. Sync predicted labels into the dataset structure
rsync -a $RUNS/val_labels/labels/   $DATA/dataset/labels/
rsync -a $RUNS/train_labels/labels/ $DATA/clip/labels/

# 6. Clean labels → keep only 5 columns (drop confidence)
python - << 'PY'
from pathlib import Path
for d in [
    Path('/mnt/c/Data/2025/Bimbingan/Semester_7/Dataset_Video/data/dataset/labels'),
    Path('/mnt/c/Data/2025/Bimbingan/Semester_7/Dataset_Video/data/clip/labels')
]:
    if not d.exists():
        continue
    for p in d.glob('*.txt'):
        rows=[]
        for L in p.read_text().splitlines():
            parts=L.split()
            if len(parts) >= 5:
                rows.append(' '.join(parts[:5]))
        p.write_text('\n'.join(rows)+('\n' if rows else ''))
print('OK: confidence removed; labels now 5 columns.')
PY

# 7. Validate YOLOv11s @640 on the prepared dataset
yolo detect val model=yolo11s.pt \
  data=$DATA/dataset.yaml \
  imgsz=640

# dataset.yaml example:
train: /mnt/c/Data/2025/Bimbingan/Semester_7/Dataset_Video/data/clip/images
val:   /mnt/c/Data/2025/Bimbingan/Semester_7/Dataset_Video/data/dataset/images
names: [person]
