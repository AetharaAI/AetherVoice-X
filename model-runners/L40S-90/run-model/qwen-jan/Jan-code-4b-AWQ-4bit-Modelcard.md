

Jan-Code-4B: a small code-tuned model

GitHub License Jan App

image
Overview

Jan-Code-4B is a code-tuned model built on top of Jan-v3-4B-base-instruct. It’s designed to be a practical coding model you can run locally and iterate on quickly—useful for everyday code tasks and as a lightweight “worker” model in agentic workflows.

Compared to larger coding models, Jan-Code focuses on handling well-scoped subtasks reliably while keeping latency and compute requirements small.
Intended Use

    Lightweight coding assistant for generation, editing, refactoring, and debugging
    A small, fast worker model for agent setups (e.g., as a sub-agent that produces patches/tests while a larger model plans)
    Replace Haiku model in Claude Code setup

Quick Start
Integration with Jan Apps

Jan-code is optimized for direct integration with Jan Desktop, select the model in the app to start using it.
Local Deployment

Using vLLM:

vllm serve janhq/Jan-code-4b \
    --host 0.0.0.0 \
    --port 1234 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes 
    

Using llama.cpp:

llama-server --model Jan-code-4b-Q8_0.gguf \
    --host 0.0.0.0 \
    --port 1234 \
    --jinja \
    --no-context-shift

Recommended Parameters

For optimal performance in agentic and general tasks, we recommend the following inference parameters:

temperature: 0.7
top_p: 0.8
top_k: 20

🤝 Community & Support

    Discussions: Hugging Face Community
    Jan App: Learn more about the Jan App at jan.ai

📄 Citation

Updated Soon

