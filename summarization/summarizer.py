from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)
# loads pretrained transformer model , tokenizer, inference pipeline


def generate_summary(text):
    result = summarizer(text, max_length = 200, min_length = 20, do_sample = False)

    return result[0]["summary_text"]


# the model loads once when the server starts 