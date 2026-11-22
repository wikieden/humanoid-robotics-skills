# Research Notes for Robot Policy Training Decisions

Primary sources reviewed on November 21, 2026. The comparisons below are proposed local experiments. Each source describes its own data, embodiment, and evaluation setting.

| Method and public evidence | When it is worth trying | Control to include |
| --- | --- | --- |
| **Paired corrections for VLA post-training.** A November technical report pairs a replaced policy segment with a human correction. Its broader recipe moves from discrete action-token pretraining to continuous flow matching and embodiment-specific post-training. [Technical report, Nov 12 revision](https://arxiv.org/abs/2611.08577v3) | The recording identifies the replaced segment, the operator's correction, and their starting context. With demonstrations alone, start with supervised fine-tuning. | Compare correction-only imitation with a learner that uses both members of each pair. Keep the correction budget fixed. |
| **Latent world-action conditioning.** A world-action policy predicts future visual features and conditions its action generator on them. Its released configuration assigns separate learning rates to the flow head, world decoder, and internal vision-language model. [Paper, Oct 25 revision](https://arxiv.org/abs/2606.15768v2) · [Official training configuration](https://raw.githubusercontent.com/RLinf/LaWAM/main/starVLA/config/training/train_robotwin.yaml) | Synchronized future observations are available in training, and the deployed policy can predict the conditioning signal from its current inputs. Record the exact source revision used in the run. | Compare action-only and predicted-feature variants. Verify which tensors actually change. Evaluate prediction error and task success separately. |
| **World-model-assisted policy updates.** One study refreshes a learned simulator with observed policy rollouts and generates additional training trajectories. A Nov 18 preprint combines simulation play data and deployment observations to align a video world model, then runs closed-loop RL inside it. [ICML paper](https://proceedings.mlr.press/v306/guo26i.html) · [Nov 18 preprint](https://arxiv.org/abs/2611.25251v1) | There is independent observed evidence to check the modeled transitions that determine reward, including failed contact and release. A WAM action predictor alone need not implement a simulator that accepts arbitrary actions. | Compare observed-only training with observed plus imagined data. Measure outcomes outside the model used to generate training rollouts. |
| **Stage-specific RSI with retention.** A Nov 4 preprint localizes a failed stage, refines the policy on relevant experience using behavior-regularized offline RL, and evaluates candidates for retention across a simulated task suite. [Preprint](https://arxiv.org/abs/2611.06654v1) | A recurring development failure can be localized and suitable experience exists. A stronger early stage can expose failures that were previously rare downstream. | Report how many trials reached each stage, conditional stage success, full-task success, and losses on previously solved cases. Select on development validation and keep final acceptance sealed. |

## Worked decision

Suppose an action adapter is proposed for a placement error. The team predeclares two criteria for this synthetic example: a positive paired success change and zero regressions on a designated retention subset. All 12 independent initial layouts yield a complete pair.

| Pair outcome | Layouts |
| --- | ---: |
| Both succeed | 4 |
| Candidate alone succeeds | 3 |
| Baseline alone succeeds | 1 |
| Both fail | 4 |

The baseline succeeds on 5/12 and the candidate on 7/12. The net gain is 2/12, about 16.7 percentage points. The single lost layout is in the designated retention subset, so the decision is to retain the baseline. A follow-up can diagnose that regression on development data. Any acceptance layout inspected for tuning must be retired from future sealed confirmation.
