---
name: technical-study-lab
description: Turn a paper, algorithm or engineering concept into a resumable lesson with a small runnable experiment, an independent learner attempt and review cards. Use when teaching interactively or resuming a technical study sequence.
metadata:
  title: Technical Study Labs and Review Cards
---

# Technical Study Labs and Review Cards

Begin at the last question the learner actually attempted. Read the corresponding lesson, exercise result and due review cards. A written chapter establishes that material exists. A learner's independent explanation or worked answer establishes what they can use.

1. Pick one claim from the supplied paper, derivation or implementation and record where to check it. State assumptions and define symbols. Ask for a prediction on a small case before revealing the result. If the user wants materials only, put the prediction, answer key and future progress record in separate sections.
2. Design a small executable comparison that changes one variable and makes two plausible explanations yield different results. Give the expected output, how to run it, and the assumptions it tests. In an interactive session show the prompt first and wait for the learner's attempt. Make the solution available when reviewing the attempt or when requested.
3. Check the learner's reasoning and output independently. If an answer is wrong, identify the first mistaken step, explain it, and ask a nearby question with different inputs. If a hint was needed, preserve that fact. An unanswered question stays open.
4. Turn a recurring error or useful distinction into a review card. Include an independent prompt, a separately revealed answer, a source pointer, and the last observed attempt. Reuse the existing review schedule when present. End with a precise resume point, such as “predict the returned index when two values tie.”

**Worked lab for the instructor.** A five-sample action logger gives one tick per sample. Ask how many elapsed intervals separate the first and last timestamps. Use the student's prediction to distinguish counting samples from counting intervals.

```python
ticks = [8, 9, 10, 11, 12]
assert len(ticks) == 5
assert ticks[-1] - ticks[0] == 4
```

If the learner answered five intervals, ask about two timestamps separated by one tick before making a card. For transfer, present irregularly spaced timestamps and ask which parts of the original reasoning still hold. Mark the transfer question as attempted only after a response.

**Deliverable.** Produce the source-backed question, reproducible lab, answer key and resume point. Record a learner result or a due review card only when an actual response supplies the evidence.
