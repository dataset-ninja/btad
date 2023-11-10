**BTAD: beanTech Anomaly Detection Dataset** is a dataset for instance segmentation, semantic segmentation, object detection, and semi supervised learning tasks. It is used in the manufacturing industry, and in the anomaly detection research. 

The dataset consists of 2540 images with 691 labeled objects belonging to 3 different classes including *product_2*, *product_1*, and *product_3*.

Images in the BTAD dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 2261 (89% of the total) unlabeled images (i.e. without annotations). There are 2 splits in the dataset: *train* (1799 images) and *test* (741 images). Alternatively, the dataset could be split into 2 image sets: ***ok*** (2250 images) and ***ko*** (290 images). The dataset was released in 2021 by the beanTech, Italy and University of Udine, Italy.

<img src="https://github.com/dataset-ninja/btad/raw/main/visualizations/poster.png">
