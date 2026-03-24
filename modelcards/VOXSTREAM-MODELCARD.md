
Model Card for VoXtream

VoXtream, a fully autoregressive, zero-shot streaming text-to-speech system for real-time use that begins speaking from the first word.
Key features

    Streaming: Support a full-stream scenario, where the full sentence is not known in advance. The model takes the text stream coming word-by-word as input and outputs an audio stream in 80ms chunks.
    Speed: Works 5x times faster than real-time and achieves 102 ms first packet latency on GPU.
    Quality and efficiency: With only 9k hours of training data, it matches or surpasses the quality and intelligibility of larger models or models trained on large datasets.

Model Sources

    Repository: repo
    Paper: paper
    Demo: demo

Get started
Installation

pip install voxtream==0.1.5

Usage
Output streaming

voxtream \
    --prompt-audio assets/audio/male.wav \
    --prompt-text "The liquor was first created as 'Brandy Milk', produced with milk, brandy and vanilla." \
    --text "In general, however, some method is then needed to evaluate each approximation." \
    --output "output_stream.wav"

    Note: Initial run may take some time to download model weights.

Full streaming

voxtream \
    --prompt-audio assets/audio/female.wav \
    --prompt-text "Betty Cooper helps Archie with cleaning a store room, when Reggie attacks her." \
    --text "Staff do not always do enough to prevent violence." \
    --output "full_stream.wav" \
    --full-stream

Out-of-Scope Use

Any organization or individual is prohibited from using any technology mentioned in this paper to generate someone's speech without his/her consent, including but not limited to government leaders, political figures, and celebrities. If you do not comply with this item, you could be in violation of copyright laws.
Training Data

The model was trained on a 9k-hour subset from Emilia and HiFiTTS2 datasets. You can download it here. For more details, please check our paper.
Citation

@inproceedings{torgashov2026voxtream,
  title={Vo{X}tream: Full-Stream Text-to-Speech with Extremely Low Latency},
  author={Torgashov, Nikita and Henter, Gustav Eje and Skantze, Gabriel},
  booktitle={Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2026},
  note={to appear},
  url={https://arxiv.org/abs/2509.15969}
}

