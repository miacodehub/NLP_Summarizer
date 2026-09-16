from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def _summarize(text: str, max_length: int, min_length: int) -> str:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        min_length=min_length,
        no_repeat_ngram_size=3,
        num_beams=4
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_summary(chunks_by_source: dict[str, str], query: str) -> str:
    """
    chunks_by_source: e.g. {
        "climate_text.txt": "<retrieved chunk text>",
        "climate_pdf.pdf": "<retrieved chunk text>",
        "climate_word.docx": "<retrieved chunk text>"
    }
    """

    # --- MAP step: elaborate summary per source ---
    per_doc_summaries = []
    for source_name, chunk_text in chunks_by_source.items():
        doc_summary = _summarize(chunk_text, max_length=180, min_length=90)
        per_doc_summaries.append(f"From {source_name}: {doc_summary}")

    for s in per_doc_summaries:
        print(f"\n--- MAP SUMMARY ---\n{s}\n")
   
    # --- REDUCE step: combine into one final summary ---
    combined_text = "\n\n".join(per_doc_summaries)
    combined_input = f"Regarding: {query}\n\n{combined_text}"

    final_summary = _summarize(combined_input, max_length=220, min_length=100)

    return final_summary