import numpy as np
import bz2
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
import torch
from tqdm import tqdm


train_file = bz2.BZ2File('dataset/7/train.ft.txt.bz2')
test_file = bz2.BZ2File('dataset/7/test.ft.txt.bz2')
model_name = "distilbert-base-uncased"


# Extract and Load Dataset from bz2 files
def load_extract(file):
    texts, labels = [], []
    for line in tqdm(file, desc="Extracting and Loading Data", ):
        x = line.decode('utf-8')
        labels.append(int(x[9]) - 1) 
        texts.append(x[10:].strip()) 
    print('Done !') 
    return np.array(labels), texts

train_labels, train_texts = load_extract(train_file)
test_labels, test_texts = load_extract(test_file)

# remove unwanted large data variables
del train_file; del test_file


# Text Essential Cleaning
def clean_texts(texts):
    temp_texts = []

    for text in tqdm(texts, desc="Cleaning Texts"):

        # Replace digits with '0'
        text = re.sub(r'\d', '0', text)

        # Remove links and URLs
        if 'www.' in text or 'http:' in text or 'https:' in text or '.com' in text:
            text = re.sub(r"(?:https?://|www\.)\S+|\b\S*\.com\S*", " ", text)

        # Remove non-alphabetic characters (except spaces)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Remove extra spaces and strip leading/trailing whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        temp_texts.append(text)

    return temp_texts

print('\nCleaning Training data')
train_texts = clean_texts(train_texts)
print('\nCleaning Test data')
test_texts = clean_texts(test_texts)

# split Train data into training and validation
from sklearn.model_selection import train_test_split

train_texts, valid_texts, train_labels, valid_labels = train_test_split(train_texts, train_labels, test_size=0.1, random_state=1234)

# Label Mapping
label_mapping = {0: "negative", 1: "positive"}
num_labels = len(label_mapping)

print(f"Number of training samples: {len(train_texts)}")
print(f"Number of validation samples: {len(valid_texts)}")
print(f"Number of test samples: {len(test_texts)}")
print(f"Number of sentiment classes: {num_labels}")


# We'll use DistilBERT for its balance of performance and speed.
tokenizer = AutoTokenizer.from_pretrained(model_name)

print('Tokenization in progress..')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
valid_encodings = tokenizer(valid_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

# Create a custom PyTorch Dataset
class AmazonReviewDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


# Create PyTorch Dataset objects
train_dataset = AmazonReviewDataset(train_encodings, train_labels)
valid_dataset = AmazonReviewDataset(valid_encodings, valid_labels)
test_dataset = AmazonReviewDataset(test_encodings, test_labels)

print("\nDataset preparation complete.")
print(f"Example of tokenized input_ids (first training sample): {train_dataset[0]['input_ids']}")
print(f"Example of attention_mask (first training sample): {train_dataset[0]['attention_mask']}")
print(f"Example of label (first training sample): {train_dataset[0]['labels']}")

# Load the pre-trained DistilBERT model with a classification head
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
print("\nModel loaded with a classification head.")

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
    evaluation_strategy="steps",
    save_strategy="best",
    save_total_limit=1,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    report_to="none"
)

# This function will be passed to the Trainer for calculating metrics during evaluation.
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    compute_metrics=compute_metrics
)

print("\nStarting model training...")
trainer.train()

print("\nEvaluating model on the test set...")
test_results = trainer.evaluate(test_dataset)
print(f"Test Set Evaluation Results: {test_results}")

output_model_dir = "./fine_tuned_sentiment_model"
model.save_pretrained(output_model_dir)
tokenizer.save_pretrained(output_model_dir)

print(f"\nFine-tuned model and tokenizer saved to: {output_model_dir}")