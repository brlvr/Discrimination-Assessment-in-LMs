# Discrimination-Assessment-in-LMs
Replicating Discrimination Assessment in LMs with Focus on Jewish People and Israel Associated Individuals.
This project aims to adapt the methodology used in the referenced paper [[1]](#1) to specifically investigate how LMs handle decisions involving Jewish people and Israel-associated individuals. 
It would involve generating decision-making scenarios relevant to these groups, systematically varying demographic information to include Jewish and Israel-associated identifiers, 
and analyzing the responses for patterns of discrimination. The project would also explore prompt-based interventions to mitigate any discovered biases, 
contributing to the broader understanding of LMs’ handling of specific ethnic and national identities. For more details on the original paper, you can access it [[1]](#1).


## Datasets and Models

| Dataset \ Model              | [gemma-1.1-2b-it](https://huggingface.co/google/gemma-1.1-2b-it) | [gemma-1.1-2b-it-GGUF](https://huggingface.co/google/gemma-1.1-2b-it-GGUF) | [gemma-1.1-7b-it](https://huggingface.co/google/gemma-1.1-7b-it) | [gemma-1.1-7b-it-GGUF](https://huggingface.co/google/gemma-1.1-7b-it-GGUF) |
|:------------------------------:|:---------:|:---------:|:---------:|:---------:|
| explicit-combined-jews       | ✖️       | ✖️        | ✖️       | ✖️      |
| explicit-all-jew            | ✖️       | ✖️        | ✖️       | ✖️      |
| implicit-fix-combined-jews   | ✖️       | ✖️        | ✖️       | ✖️      |
| more?                        | ✖️       | ✖️        | ✖️       | ✖️      |

## Models Description
### [gemma-1.1-2b-it](https://huggingface.co/google/gemma-1.1-2b-it)

### [gemma-1.1-2b-it-GGUF](https://huggingface.co/google/gemma-1.1-2b-it-GGUF)

### [gemma-1.1-7b-it](https://huggingface.co/google/gemma-1.1-7b-it)

### [gemma-1.1-7b-it-GGUF](https://huggingface.co/google/gemma-1.1-7b-it)


## Datasets Description
### [discrim-eval](https://huggingface.co/datasets/Anthropic/discrim-eval) [[2]](#2)
As stated in the Dataset Card on Hugging Face: "The data contains a diverse set of prompts covering 70 hypothetical decision scenarios, ranging from approving a loan to providing press credentials. Each prompt instructs the model to make a binary decision (yes/no) about a particular person described in the prompt. Each person is described in terms of three demographic attributes: age (ranging from 20 to 100 in increments of 10), gender (male, female, non-binary) , and race (white, Black, Asian, Hispanic, Native American), for a total of 135 examples per decision scenario. The prompts are designed so a 'yes' decision is always advantageous to the person (e.g. deciding to grant the loan)."
Total of 3x5x70x9 = 9,450 unique examples.

#### Data Format
The data are in two jsonl files, [explicit.jsonl](discrim-eval-2\explicit.jsonl) and [implicit.jsonl](discrim-eval-2\implicit.jsonl). Each line of json has the following keys:

- _filled_template_: The decision question prompt
- decision_question_id: An ID corresponding to one of 70 decision scenarios.
- _age_: Age of person who is the subject of the decision (ranging from 20 to 100 in increments of 10).
- _gender_: Gender of person who is the subject of the decision (male, female, non-binary).
- _race_: Race of person who is the subject of the decision (white, Black, Asian, Hispanic, Native American).
 
The implicit.jsonl file does not have an explicit mention of race or gender, but rather relies on an implicit version of these attributes based on a name and pronouns.

####  [Exploratory Data Analysis](EDA\eda.ipynb)
For more insights about the data and how we constructed new datasets based on the original one. 

### [explicit-combined-jews](outputs\datasets\explicit-combined-jews.jsonl)
This dataset is built on top of the original explicit dataset with addition of **Jewish as a race**, this dataset is larger then the original explicit dataset because we added one more race option for each question ID -> 11340 examples (3x6x9x70).
Also, some examples fixing was needed according to the findings in the EDA.

### [explicit-all-jew](outputs\datasets\explicit-all-jew.jsonl)
This dataset is a variation of the original explicit dataset, we added in each _filled_template_  after the _race_ an ethnicity - Jew. Thus we have combinations with racial and ethnic background, for example: Asian Jew, white Jew etc. 

The number of unique examples stayed the same regard to the original dataset -> 9450 examples (3x5x9x70).
For further details you can see the EDA and how we built the new dataset.

**_Note: it's important to note that using "Jew" solely as a descriptor after a race could be perceived as reductionist or stereotypical. It's essential to be sensitive to cultural and religious identities when using language in this manner._**

### implicit-fix-combined-jews
- [ ] add explenation and add link inside repo to the data
### more?
- [ ] add explenation and add link inside repo to the data


## Missions
- [x] Read the article (ongoing)
- [ ] Investigate how LMs handle decisions involving Jewish people and Israel-associated individuals.
- [ ] Generating decision-making scenarios relevant to Jewish people - Explicit dataset 1.
  - [x] Explicit EDA.
  - [x] Add to RACE category "Jewish".
- [ ] Generating decision-making scenarios relevant to Jewish people - Explicit dataset 2.
  - [ ] Create a dataset where everyone is Jewish concerning the original dataset, and add religion to the base dataset to see if the discrimination is getting higher or not. (We haven't done it since we need Claude 2.0 baseline results which are different know - we assume that they added patches to fix their discrimination so the results in the paper are not as using the API today).
- [ ] Generating decision-making scenarios relevant to Israel-associated individuals - Implicit dataset.
  - [ ] Implicit EDA.
  - [ ] Get a template from each decision question ID and add Israel-associated individuals.
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
- [ ] Read the evaluation part

## 27/04/2024
- [ ] Activate API (Gemini 2/7,Llama3 8/70) - Gal
    - [ ] Try to create our own dataset
    - [ ] Create inference pipline
- [ ] Create/edit Implicit data (Maybe with LLM's, try chatGPT/claude, NER) - Ron 
    - [ ] Have a look at the current data - maybe there are already jewish scenarios
- [ ] Evaluation - 
    - [ ] Read the article evaluation
    - [ ] Explore for more evaluation techniques


## 01/05/2024
- [ ] Use ollama to predict answers (completion) from various models (check what fits on our local resources).
- [X] Read the Article (ongoing).
- [ ] Implicit dataset - add jewish examples.
- [ ] Explore prompt-based interventions to mitigate any discovered biases
- [ ] Evaluation - According to the paper we have somthing, maybe find new ways.

## Disclaimers

## References
<a id="1">[1]</a>  Tamkin, A., Askell, A., Lovitt, L., Durmus, E., Joseph, N., Kravec, S., Nguyen, K., Kaplan, J. and Ganguli, D., 2023. Evaluating and mitigating discrimination in language model decisions. arXiv preprint [arXiv:2312.03689](https://arxiv.org/abs/2312.03689).

<a id="2">[2]</a> [Anthropic/discrim-eval Dataset card on Hugging Face](https://huggingface.co/datasets/Anthropic/discrim-eval)
.