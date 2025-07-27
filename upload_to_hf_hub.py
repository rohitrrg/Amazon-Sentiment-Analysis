
from huggingface_hub import HfApi
import os

api = HfApi(token=os.getenv("HF_TOKEN"))

api.upload_folder(
    folder_path="fine_tuned_sentiment_model",
    repo_id="rohitgadhwar/amazon-review-sentiment-analysis",
    repo_type="model",
)