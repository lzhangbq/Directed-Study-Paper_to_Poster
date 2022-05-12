# Directed-Study-Paper_to_Poster
## LayoutTransformer:
The model is LayoutTransformer. We referenced the code from LayoutTransformer by Kamal Gupta (https://github.com/kampta/DeepLayout). However, based on pre-training on Publaynet, we fine-tuned it through annotated poster layouts. We need to remap the label of the layouts from posters to the Publaynet. In the experiment, we remain the hyperparameters on reports and pre-train by 15 epochs, and fine-tune by 100 epochs.

Reference: Gupta, Kamal et al. “LayoutTransformer: Layout Generation and Completion with Self-attention.” 2021 IEEE/CVF International Conference on Computer Vision (ICCV) (2021): 984-994.
## Turk:
This part of code records our part on processing posters in S3 bucket and extracting the result from the annotation result from Amazon Mechanical Turk.
