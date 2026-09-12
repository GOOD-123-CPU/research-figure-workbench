# Scientific Diagram Workflow

Use for method overviews, system block diagrams, signal chains, experiment pipelines, architecture figures, and algorithm flows. Do not use conceptual drawing to replace quantitative evidence.

## Workflow

1. State the diagram's one-sentence message and intended reader.
2. Write the logical sequence as a short structured list.
3. Draft structure in Mermaid while nodes/order are still changing.
4. Separate inputs, processing, outputs, validation, optional paths, and failure paths.
5. Move to draw.io/diagrams.net when precise alignment, grouped containers, editable connectors, or publication handoff is needed.
6. Export SVG/PDF and keep Mermaid/`.drawio` source.
7. Inspect at final physical size and, for composites, align typography/panel labels with data panels.

## Layout defaults

- Left-to-right for pipelines and signal paths.
- Top-to-bottom for staged procedures when page shape favors vertical flow.
- Keep labels short, technical, and parallel in grammar.
- Use one neutral base plus restrained semantic accents.
- Warning colors indicate actual warnings/failures, not decoration.
- Repeated blocks should use consistent shape/size/label grammar.
- Keep arrow semantics stable: data flow, control flow, dependency, and feedback should be distinguishable when they differ.

## Fast-comprehension check

A technically literate new reader should identify input, main method, output, and validation rapidly.

- Every connector has an unambiguous direction.
- Crossings are minimized.
- Optional/failure paths are visually distinct from the main path.
- Acronyms are expanded when the audience may not know them.
- The figure does not encode scientifically important distinctions only through color.

## Integrity and provenance

- Do not copy or trace published artwork.
- Do not include fabricated mechanisms as if experimentally established.
- Do not embed private paths, emails, hidden signatures, unauthorized logos, or screenshots when vector shapes can express the concept.
- Keep text editable in source.
- Record external icon/source licenses when used.

## Generative-image gate

If the user requests an AI-generated graphical abstract, mechanism illustration, or schematic:

1. verify the exact target venue's current AI-generated/AI-edited image policy using `journal-source-policy.md`;
2. treat the image as conceptual, never quantitative evidence;
3. preserve prompts/tool/version/provenance when generated;
4. require human scientific review for every depicted mechanism and label;
5. mark submission eligibility `UNVERIFIED` until official policy is checked.

Prefer deterministic vector diagrams for method/architecture figures when they communicate the same information.
