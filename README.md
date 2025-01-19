We set out to understand the internal representation of LLMs when solving planning problems. 

We use the [Blockworld](https://huggingface.co/datasets/NanQiangHF/BlocksWorldTrainingDataFull3-8?row=5) dataset, which is a planning task aimed at rearranging a set of blocks.

We have 4 tasks:

1. Task 1: Given a state $s$ and a legal action $x_t$. The model's judgment is whether the action is legal or not. 
2. Task 2: Given a state $s$ and an action $x_t$. The model's judgment is whether the action is legal or not. 50% of the actions are legal and 50% of them are not
3. Task 3: Given a state $s$, the model generates an action. We test whether the action is legal. This task tests the model's ability to generate legal states.
4. Task 4: Given an initial state and a list of actions that were taken, the model outputs the next action $x_t$ that is legal. This task ensures that the model can follow through intermediary states, and output a final legal action on the second to last state.

We randomly select 1000 data points for each task. The accuracy of gpt4-o on these tasks are
Task 1: $0.950497287522604$

Task 2: $0.9570858283433133$

Task 3: $0.964035964035964$

Task 4: $0.96$

