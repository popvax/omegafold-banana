# In this file, we define download_model
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

from torch import hub
import os
def download_model():
    # do a dry run of loading the huggingface model, which will download weights
    weights_url = "https://helixon.s3.amazonaws.com/release1.pt"
    weights_file = os.path.expanduser("~/.cache/omegafold_ckpt/model.pt")
    hub.download_url_to_file(weights_url, weights_file)

if __name__ == "__main__":
    download_model()