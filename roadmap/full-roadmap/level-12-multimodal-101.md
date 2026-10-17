# Level 12 · Multimodal 101: Beyond Text

> **Phase 6 · Frontier & Proof** · 13 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/12/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Build a strong mental model of how models handle images, audio, and video, why they fail differently from text models, and how to choose and use the right model when a task stops being text-only.

## Why this level matters

**Interview weight: 4/10**

**Seldom asked** unless the role is specifically about vision, speech, or documents. **Low payoff** for general applications.

**On-the-job weight: 5/10**

**Very important in some domains** (documents, speech, vision), **not needed in many others**.

---

## Modules

### 01 · Beyond text: what a multimodal model is (M12.1 · 1 session)

- **What makes a model multimodal** — Understand what makes a model multimodal: images, audio, and video are converted into tokens and fed into the same transformer that already processes text.
- **Native multimodal vs bolted-on pipeline** — Distinguish a natively multimodal model, trained on mixed data from the start, from a pipeline that bolts a separate transcription, **OCR**, or captioning model in front of a text-only LLM.
- **Text as the interlingua** — Understand why text remains the interlingua: whatever enters the model, the reasoning and almost always the output happen in tokens that behave like text.
- **What carries over from text LLMs** — Build intuition for what changes and what does not: the context window, tokenization, sampling, and failure modes you learned for text all still apply.
- **What "any-to-any" really means** — Recognize what "any-to-any" marketing does and does not mean today, since most models accept several input modalities but produce only text.
- **What a pipeline throws away** — Understand why a bolted-on pipeline loses information that a native model keeps, such as tone in speech or layout in a scanned page.

**Mental model** · Image / audio / video → tokens → the same transformer you already understand → text out

**Try it** · Send the same chart as an image to a natively multimodal model and as OCR-extracted text to a text-only model, then compare what each one can answer.

**Outcome** · Explain to someone what a multimodal model actually is, and tell whether a given product is using a native model or a pipeline stitched together around a text model.

### 02 · Vision: how images become tokens (M12.2 · 1 session)

- **Patches & the vision encoder** — Understand how a vision encoder splits an image into a grid of patches and turns each patch into a vector the transformer can consume.
- **Why one image costs many tokens** — Build intuition for why a single image can cost hundreds or thousands of tokens, and why that cost scales with resolution rather than with file size.
- **Tiling & detail settings** — Understand tiling and detail settings: high-detail modes slice a large image into multiple tiles, each priced as its own set of tokens.
- **What downscaling destroys** — Recognize what downscaling and aspect-ratio changes destroy, especially small text, thin lines, dense tables, and fine chart labels.
- **Images share the context window** — Understand that image tokens occupy the same context window as text tokens, so a handful of screenshots can crowd out the instructions and history around them.
- **Full image, crops, or overview** — Understand the practical trade-off between sending one large detailed image, several cropped regions, or a downscaled overview.

**Try it** · Send the same screenshot at full resolution, at half resolution, and cropped to the region that matters, then compare token usage, cost, and answer quality.

**Outcome** · Predict roughly what an image will cost in tokens and choose a resolution and cropping strategy instead of uploading whatever the camera produced.

### 03 · Vision: capabilities & failure modes (M12.3 · 1 session)

- **What vision models do well** — Understand what vision models genuinely do well: reading text in images, describing scenes, extracting named fields from documents, and interpreting charts at a coarse level.
- **Counting, space & dense tables** — Understand the failure modes that repeat across models: precise counting, spatial and geometric reasoning, dense small text, and exact row-to-column alignment in tables.
- **Fabricated visual detail** — Recognize fabricated detail, where a model confidently reports values, labels, or objects that a low-resolution or ambiguous image never actually contained.
- **Why vision failures happen** — Understand why these failures happen: the model is generating a plausible description of an image it perceives as patches, not measuring or verifying anything.
- **Asking "how reliably?" for images** — Adopt the engineering question for vision too: not "can this model read invoices?", but "how reliably does it read my invoices, at my resolution, in my formats?".
- **Safeguards when reliability is short** — Understand which safeguards apply when reliability is not enough, such as higher resolution, cropping, structured output, verification passes, or human review.

**Try it** · Build ten test images that include a crowded shelf, a dense table, a low-resolution receipt, and a handwritten note, then score how often the model is exactly right.

**Outcome** · Predict which visual tasks a model will handle unaided and which need cropping, higher resolution, or a verification step before you can ship them.

### 04 · Vision: documents, charts & visual RAG (M12.4 · 3 sessions)

Reading a document as an image

- **Text-layer PDFs vs scans** — Distinguish a digital **PDF** that carries its own text layer from a scan or photograph where every character has to be recovered from pixels.
- **OCR vs native vision reading** — Compare **OCR**-based reading with native vision reading by a multimodal model on accuracy, cost, latency, and how much layout they preserve.
- **Layout & reading order** — Understand why reading order matters: multi-column pages, headers, footers, footnotes, and sidebars can turn a correct page into nonsense when flattened badly.
- **Tables, forms & merged cells** — Read tables and forms reliably, including merged cells, multi-page tables, checkboxes, and key-value layouts where the label and the value sit far apart.
- **How models read charts** — Understand what a model actually does with a chart: it reads axes, labels, and legends rather than the underlying numbers, so precise values are often estimated.

Extraction into structured fields

- **Schema before prompt** — Define the schema before the prompt: name the fields you need, their types, and which of them are required, instead of asking for a free-form summary.
- **Extract & validate fields** — Extract fields from a document with a vision model and validate the result against that schema, checking types, ranges, dates, totals, and required values.
- **Grounding fields to page regions** — Ground every extracted field in its source by returning the page number or region it came from, so a human can verify a value without rereading the document.
- **Document failure modes** — Recognize document-specific failure modes: invented values in blank cells, rows merged across page breaks, confused units or currencies, and misread handwriting.
- **Routing low confidence to review** — Route low-confidence extractions to human review rather than letting an uncertain value flow silently into a database.

Visual RAG

- **Pages & regions as retrieval units** — Understand what changes when the retrieval unit is a page image or a region of a page rather than a chunk of text, and how embeddings are produced for it.
- **Hybrid text + visual retrieval** — Build hybrid retrieval that searches extracted text and page images together, and recognize which of the two wins for a given question.
- **Citing the page you answered from** — Cite the page or region an answer came from, so the reader can open the document at the right place and check it.
- **When plain text beats visual** — Compare a visual pipeline with a plain text pipeline on cost, latency, and accuracy, and understand why clean digital text rarely needs page images at all.
- **The token cost of page images** — Understand the practical cost of visual RAG: page images consume far more tokens than the equivalent text, which changes both latency and price per query.

**Mental model** · Document → Pages → Text layer + page images → Layout & regions → Structured fields or retrievable units

**Try it** · Take one scanned invoice and one clean digital PDF, run both through a text pipeline and a vision pipeline, and compare accuracy, cost, and latency.

**Outcome** · Build a document pipeline that reads real-world PDFs and scans, extracts validated fields, and answers questions with a citation back to the page it used.

### 05 · Vision: image & video generation (M12.5 · 2 sessions)

How generation differs from prediction

- **Denoising, not next-token prediction** — Understand that a generative image model starts from random noise and repeatedly removes it, rather than predicting the next token the way an LLM does.
- **What a prompt controls** — Understand what a prompt actually controls in image generation: subject, composition, style, and detail, with far less literal instruction-following than a text model offers.
- **Seeds & reproducibility** — Understand seeds and reproducibility: the same prompt with the same seed returns the same image, while a new seed produces a different interpretation of the same words.
- **Resolution, steps & cost** — Understand how resolution, aspect ratio, and step count affect quality, generation time, and cost.

Control, video and rights

- **img2img, inpainting & outpainting** — Distinguish text-to-image from image-to-image, inpainting, and outpainting, and recognize which one a given editing task actually needs.
- **Style & structural control** — Understand reference and style conditioning, along with structural control such as pose, depth, or edge guidance, for when a prompt alone cannot hold a layout steady.
- **Cost per accepted image** — Build intuition for iteration cost: generation is cheap per image but expensive per accepted image, because most candidates are discarded.
- **What video adds: time & motion** — Understand what video generation adds: time, motion, and consistency across frames, which makes length, cost, and failure modes grow quickly.
- **Provenance, watermarks & rights** — Understand provenance and rights: watermarking, content credentials, training-data licensing, and the commercial-use terms attached to generated assets.

**Mental model** · Noise → repeated denoising guided by the prompt → image

**Try it** · Generate the same prompt at three seeds and three aspect ratios, then edit the best result with inpainting instead of re-prompting it.

**Outcome** · Produce and iteratively control generated images, and judge whether a generation task is worth its cost in review time and rights risk.

### 06 · Audio: how sound becomes tokens (M12.6 · 1 session)

- **Waveform to spectrogram to tokens** — Understand the path from a waveform to model input: audio is sampled, converted into a spectrogram or learned audio tokens, and then treated as another token stream.
- **Cost per second, not per word** — Build intuition for audio cost and latency, where tokens accumulate per second of duration rather than per word, so silence and background noise are paid for too.
- **Transcribe-then-prompt vs audio-native** — Distinguish transcribe-then-prompt pipelines, where a speech-to-text model produces text for an LLM, from audio-native models that consume the sound itself.
- **What a transcript discards** — Understand what a transcript discards: tone, emphasis, hesitation, overlapping speakers, emotion, and everything that separates "fine" said warmly from "fine" said flatly.
- **Why audio is latency-sensitive** — Recognize why audio input and output are latency-sensitive, since a conversation is judged on response delay in a way that a document summary never is.
- **Where speech recognition breaks** — Understand common audio failure modes such as accented speech, code-switching between languages, domain jargon, poor microphones, and long silences.

**Try it** · Run the same 30-second clip through a speech-to-text model and through an audio-native model, and ask both what the speaker's mood was.

**Outcome** · Choose between a transcription pipeline and an audio-native model for a given task, and explain what each choice costs you in fidelity, latency, and money.

### 07 · Audio: speech to text & text to speech (M12.7 · 2 sessions)

Speech to text

- **What Whisper actually returns** — Understand what a speech-to-text model such as Whisper produces: a transcript, optional word timestamps, and confidence signals rather than clean edited prose.
- **Batch vs streaming transcription** — Distinguish batch transcription of a complete recording from streaming transcription, where partial text is emitted while the speaker is still talking.
- **Accents, code-mixing & noise** — Understand what degrades transcription in practice — accents, code-mixed Hindi-English speech, background noise, and poor microphones — and supply domain vocabulary as hints.
- **Speaker diarization** — Use speaker diarization to attribute each segment to a speaker, and understand why it is a separate step that fails in its own ways.
- **Word error rate in practice** — Read word error rate as a measure of transcription quality, and reason about which errors actually matter for whatever happens downstream.

Text to speech

- **What Kokoro turns text into** — Understand what a text-to-speech model such as Kokoro turns text into: sampled audio in a chosen voice, produced in one pass or streamed as it is generated.
- **Voice choice & prosody** — Choose a voice and shape prosody through pace, pauses, and emphasis, and understand how much control a given model actually exposes.
- **Pronunciation control** — Control the pronunciation of names, acronyms, numbers, and code-mixed text, since these are where synthetic speech usually embarrasses itself.
- **Streaming synthesis** — Stream synthesis so the first audio reaches the listener while the rest is still being generated, instead of waiting for the whole utterance.
- **Hosted vs local speech models** — Compare hosted and locally run speech models on cost, latency, privacy, and voice quality, and choose per workload rather than by default.

**Mental model** · Audio → Transcript + timestamps + speakers → Text → Synthesized audio

**Try it** · Transcribe a five-minute recording that mixes Hindi and English, then read the transcript back with a synthetic voice and note where each step breaks.

**Outcome** · Build a speech pipeline that transcribes real recordings and speaks generated text back, with a clear view of where accuracy and latency are lost.

### 08 · Audio: realtime voice agents (M12.8 · 3 sessions)

The latency budget

- **Latency as the design constraint** — Understand why a voice conversation feels broken above roughly a second of silence, and treat end-to-end latency as the primary design constraint.
- **Where the milliseconds go** — Break the latency budget into its parts: capture, network, transcription, model thinking, synthesis, and playback.
- **Cascaded vs speech-to-speech** — Distinguish a cascaded pipeline, where speech-to-text, an LLM, and text-to-speech run in sequence, from a speech-to-speech realtime API that takes audio in and returns audio.
- **Comparing the two architectures** — Compare the two architectures on latency, control, cost, debuggability, and how much of the conversation you can inspect afterwards.
- **What can overlap** — Understand which parts can overlap: synthesis can begin before the model has finished, and transcription can run while the user is still speaking.

Turn-taking

- **Voice activity detection & endpointing** — Understand voice activity detection and endpointing as the mechanism that decides when the user has actually stopped speaking.
- **Why endpointing is hard** — Recognize why endpointing is hard: pauses for thought, slow speakers, and background chatter all look like the end of a turn.
- **Barge-in & interruption** — Handle barge-in, where the user interrupts mid-answer, by stopping playback and discarding the rest of the planned response.
- **Acting on partial transcripts** — Use partial transcripts to start work early, and understand the risk of acting on text the user has not finished saying.
- **State after a cut-short turn** — Keep conversation state consistent when a turn is cut short, so the model does not believe it said something the user never heard.

Failure, noise & tools

- **Silence, dead air & dropped calls** — Handle silence, dead air, and network loss with holding phrases, reconnection, and a graceful exit rather than an unexplained pause.
- **Noise, crosstalk & bad mics** — Understand what background noise, crosstalk, and poor microphones do to a live pipeline, and where to place the safeguards.
- **Staying alive during tool calls** — Keep the conversation alive while a tool call runs, since a lookup that takes three seconds is silence the user will not tolerate.
- **What to say while waiting** — Decide what the agent says while it waits, and what it does when the tool fails or returns nothing useful.
- **Reconstructing a bad call** — Capture what a voice session needs for later reconstruction: audio, transcript, timings, and turn boundaries.

**Mental model** · User speech → VAD & endpointing → Transcript → Model → Speech, with barge-in resetting the loop

**Try it** · Build a small voice loop with speech-to-text, an LLM, and text-to-speech, then measure the delay from the end of your sentence to the first sound of the reply.

**Outcome** · Ship a voice agent that holds a natural conversation: it knows when you stopped talking, it can be interrupted, and it keeps silence short enough to feel human.

### 09 · Cross-modal search & retrieval (M12.9 · 1 session)

- **A shared embedding space** — Understand a shared embedding space, where an image and a caption that describe the same thing land close together as vectors.
- **CLIP-style joint embeddings** — Understand CLIP-style joint embeddings, where two encoders are trained so that matching image-text pairs are pulled together and mismatched pairs pushed apart.
- **Searching across modalities** — Search images with a text query and search text with an image query, using the same vector-search machinery Level 4 introduced for text.
- **Cross-modal vs caption-then-search** — Distinguish cross-modal retrieval from captioning every image first and searching the captions, and recognize when each approach wins.
- **Where cross-modal retrieval fails** — Recognize where cross-modal retrieval fails: fine-grained detail, text inside images, counting, and domain-specific imagery the encoder never saw.
- **Evaluating on your own collection** — Evaluate retrieval quality on your own images and queries rather than trusting a benchmark score measured on a general image collection.

**Mental model** · Different modalities → one shared vector space → distance means similarity

**Try it** · Build a small image index, query it in plain language, and compare the results with a caption-then-search baseline over the same images.

**Outcome** · Decide when a task needs cross-modal retrieval and build a small image-and-text search over your own collection.

### 10 · Choosing a multimodal model (M12.10 · 1 session)

- **Start from the modalities** — Start from the modalities themselves: list what must go in, whether text, images, audio, video, or documents, and what must come out.
- **Per-image & per-minute pricing** — Understand how multimodal pricing works, since per-image and per-audio-minute charges sit alongside per-token pricing and cost stops being about text length alone.
- **The context cost of images** — Understand the context cost of images, where a single image consumes a large, resolution-dependent share of the context window and limits how many you can pass at once.
- **Latency by modality** — Compare latency expectations by modality, including time to first audio for streaming voice, where a delay is heard by the user rather than merely measured.
- **API vs self-hosting** — Weigh API access against self-hosting for vision and speech, where open models are strong and per-minute costs at volume can outgrow the operational effort.
- **Privacy for voice, faces & scans** — Treat privacy as a harder constraint here, because voices, faces, and scanned documents carry consent and data-residency obligations that plain text often does not.
- **Managed speech, vision & document services** — Consider managed speech, vision, and document services from the cloud platforms alongside general multimodal models, since a narrow managed service is often cheaper and more accurate at one job.
- **Shortlist, then test your own data** — Shortlist two or three candidates, then test them on your own images, recordings, and documents before committing, exactly as you would for a text model.

**Outcome** · Choose a model for a multimodal task on modality support, cost per unit, latency, and privacy, verified against your own examples.

### 11 · Deep research & long-horizon scenarios (M12.11 · 2 sessions)

Planning a long run

- **Why long runs are different** — Understand what changes when a task runs for many minutes across many sources instead of resolving inside a single prompt and a single response.
- **Decomposing a research question** — Decompose a research question into sub-questions that can be investigated independently, and recognize when a question is too vague to decompose yet.
- **Breadth first, then depth** — Search broadly before going deep: gather many candidate sources first, judge which few are worth reading closely, and discard the rest deliberately.
- **Reading sources critically** — Read sources critically rather than accumulating them, distinguishing primary evidence, secondary commentary, marketing material, and outdated claims.
- **Reconciling disagreement** — Reconcile sources that disagree by preferring better evidence, stating the disagreement explicitly, or reporting genuine uncertainty instead of averaging the answers.

Finishing a long run

- **Claims attached to sources** — Keep every claim attached to the source it came from, so a reader can verify any individual statement without repeating the whole search.
- **Notes and interim summaries** — Manage a run that outlives its context by writing notes and interim summaries as the work proceeds, and by carrying forward findings rather than raw source text.
- **Knowing when to stop** — Recognize the stopping conditions of a research run: the question is answered, the sources have started repeating, or the remaining uncertainty cannot be resolved by more searching.
- **A report a human can audit** — Produce a structured report a human can audit, with the question, the answer, the supporting evidence, the contradictions found, and the gaps that remain.
- **How long runs fail** — Understand the characteristic failures of long-horizon runs: drifting away from the original question, confident synthesis of thin evidence, and citations that do not support the sentence attached to them.

**Try it** · Run the same research question twice, once with a five-minute budget and once with a thirty-minute budget, and compare what the extra time actually bought.

**Outcome** · Run a long-horizon research task that produces a cited, structured report whose claims a reader can check individually.

### 12 · On-device & edge modalities (M12.12 · 1 session)

- **Why modalities suit the device** — Understand why speech and vision suit on-device execution, since the models are small, the input is private, and the network round trip is often the slowest part.
- **Quantization & what it costs** — Understand quantization as trading numerical precision for size and speed, and recognize the tasks where that trade shows up first as degraded quality.
- **Phone & laptop hardware limits** — Build intuition for hardware limits on phones and laptops, including memory ceilings, thermal throttling, and battery cost during sustained inference.
- **What on-device buys you** — Understand what on-device execution buys you: offline operation, no per-request cost, predictable latency, and data that never leaves the user's machine.
- **On-device, self-hosted or API** — Choose deliberately between on-device, self-hosted, and API execution for each modality, since one application can reasonably use all three at once.

**Try it** · Run a small quantized speech-to-text model locally and compare its accuracy, latency, and cost against a hosted API on the same audio.

**Outcome** · Decide which parts of a multimodal system belong on the user's device and accept the quality trade knowingly.

#### Capstone: ship a multimodal build

- Pick one realistic build Choose one realistic build and take it all the way: a voice agent, a document-understanding pipeline, a visual search tool, or a research-report generator.
- At least two modalities Combine at least two modalities in a single application so the build exercises a real cross-modal boundary rather than one model in isolation.
- Real inputs, not samples Feed the system real inputs from your own domain, including the messy scans, accented speech, and awkward layouts that curated sample files never contain.
- Modality-specific failures Handle the modality-specific failures your build will actually hit, such as unreadable regions, silence and background noise, hallucinated chart values, or ambiguous references.
- Latency and cost per request Measure latency and cost per request, and report them broken down by modality so the expensive part of the pipeline is visible.
- Document one real failure Document one failure you found by testing on real inputs, explaining what broke, how you detected it, and what you changed in response.
- Runnable by someone else Package the build so another person can run it from a **README** with their own inputs, their own credentials, and no help from you.

a working multimodal application that survives real inputs, whose latency and cost you can quote, and whose limitations you can state precisely.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [OpenAI — Vision and image understanding docs](https://platform.openai.com/docs/guides/images-vision?api-mode=responses) — how images become tokens, detail settings and pricing.
- [Anthropic — Vision guide](https://platform.claude.com/docs/en/build-with-claude/vision) — prompting with images, cost and best practices.
- [Whisper (GitHub)](https://github.com/openai/whisper) — the open-source speech-to-text reference model; free to run.
- [Kokoro TTS (GitHub)](https://github.com/hexgrad/kokoro) — lightweight open-weight text-to-speech model used in modern voice stacks.
- [CLIP (OpenAI research)](https://openai.com/index/clip/) — the foundational joint image-text embedding model behind cross-modal search.
- [OpenAI Realtime API docs](https://platform.openai.com/docs/guides/realtime) and [Google Live API docs](https://ai.google.dev/gemini-api/docs/live-guide) — speech-to-speech realtime voice agents.
- [Hugging Face — Audio course (free)](https://huggingface.co/learn/audio-course/chapter0/introduction) — audio pipelines, ASR evaluation and streaming.
- [Pyannote.audio (GitHub)](https://github.com/pyannote/pyannote-audio) — open-source speaker diarization.
- [Gemini API multimodal docs](https://ai.google.dev/gemini-api/docs/document-processing) — native document/PDF understanding and video input.

## In this repository

- [Curated multimodal resources](../../awesome.md)
- [Portfolio project ideas](../../portfolio/README.md)

---

[← Level 11 · Managed AI Platforms](level-11-managed-ai-platforms.md) | [Roadmap map](README.md) | [Level 13 · Fine-Tuning →](level-13-fine-tuning.md)
