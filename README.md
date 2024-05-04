# Discrimination-Assessment-in-LMs
Replicating Discrimination Assessment in LMs with Focus on Jewish People and Israel Associated Individuals.
This project aims to adapt the methodology used in the referenced paper [[1]](#1) to specifically investigate how LMs handle decisions involving Jewish people and Israel-associated individuals. 
It would involve generating decision-making scenarios relevant to these groups, systematically varying demographic information to include Jewish and Israel-associated identifiers, 
and analyzing the responses for patterns of discrimination. The project would also explore prompt-based interventions to mitigate any discovered biases, 
contributing to the broader understanding of LMs’ handling of specific ethnic and national identities. For more details on the original paper, you can access it [[1]](#1).


## Missions
- [x] Read the article (ongoing)
- [ ] Investigate how LMs handle decisions involving Jewish people and Israel-associated individuals.
- [ ] Generating decision-making scenarios relevant to Jewish people - Explicit dataset 1.
  - [x] Explicit EDA.
  - [ ] Add to RACE category "Jewish".
- [ ] Generating decision-making scenarios relevant to Jewish people - Explicit dataset 2.
  - [ ] Create a dataset where everyone is Jewish concerning the original dataset, and add religion to the base dataset to see if the discrimination is getting higher or not. (We haven't done it since we need Claude 2.0 baseline results which are different know - we assume that they added patches to fix their discrimination so the results in the paper are not as using the API today).
- [ ] Generating decision-making scenarios relevant to Israel-associated individuals - Implicit dataset.
  - [ ] Implicit EDA.
  - [ ]  Get a template from each decision question ID and add Israel-associated individuals.
  - [ ] Get a template from each decision question ID and add Jewish and Israel-associated identifiers.
- [ ] Analyzing the responses for patterns of discrimination.
  - [ ] Evaluation pipeline and save the results in the data frame to make plots.
- [ ] Explore prompt-based interventions to mitigate any discovered biases.

## Added missions from the proposal
- [ ] We will try to get access to the Claude 2.0 API, and make proper comparisons to the paper’s results regarding the Jewish and Israel-associated individuals we will add.
- [ ] Inference on different models and compare the results to our Cluade 2.0 baseline or paper's results.
- [ ] Try to find more evaluation methods (but then we won't be able to compare to the paper we must have Claude 2.0 baseline results)

## Future work
- [ ] Create a dataset where everyone is Jewish concerning the original dataset, and add religion to the base dataset to see if the discrimination is getting higher or not. (We haven't done it since we need Claude 2.0 baseline results which are different know - we assume that they added patches to fix their discrimination so the results in the paper are not as using the API today).
  - [ ] Add the word Jewish to every example in the Explicit dataset.
  - [ ] Evaluate concerning to white males age 60 all the new Jewish dataset.
  - [ ] Analyzing the responses for patterns of discrimination.
     
  
- [ ] Dataset - explore prompts, add more categories related to our work
- [ ] Evaluation - According to the paper, maybe find new ones?
- [ ] Models - Gemma-2b, Gemma-7b, Claude?, more?
- [ ] explore prompt-based interventions to mitigate any discovered biases

## 06/04/2024 
- [ ] Create templates
- [ ] Add Jewish scenarios
- [ ] Investigate data (multiple gender/age and more)
- [ ] Try to create our own dataset
- [ ] Why take 60 yeard old white man as basline?
- [ ] .

## 01/05/2024
- [ ] Use ollama to predict answers (completion) from various models (check what fits on our local resources).
- [X] Read the Article (ongoing).
- [ ] Implicit dataset - add jewish examples.
- [ ] Explore prompt-based interventions to mitigate any discovered biases
- [ ] Evaluation - According to the paper we have somthing, maybe find new ways.

## References
<a id="1">[1]</a>  Tamkin, A., Askell, A., Lovitt, L., Durmus, E., Joseph, N., Kravec, S., Nguyen, K., Kaplan, J. and Ganguli, D., 2023. Evaluating and mitigating discrimination in language model decisions. arXiv preprint [arXiv:2312.03689](https://arxiv.org/abs/2312.03689).
