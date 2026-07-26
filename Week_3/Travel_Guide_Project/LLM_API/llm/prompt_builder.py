def build_messages(query, intent, entities, documents):
    context = "\n\n".join(documents[:3])
    entity_text = ", ".join([e["text"] for e in entities]) or "None"

    system_prompt = (
        "You are an AI assistant answering questions from a knowledge base. "
        "Answer ONLY from the given context. Be clear and concise. "
        "If the answer is not in the context, say: "
        "\"I could not find that information in the knowledge base.\""
    )

    user_prompt = f"""User Query: {query}
Detected Intent: {intent}
Extracted Entities: {entity_text}

Relevant Context:
{context}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]