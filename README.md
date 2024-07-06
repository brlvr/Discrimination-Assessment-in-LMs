### Python and Conda Versions

- **Python Version**: 3.8
- **Conda Version**: 4.10.3
  
# Discrimination-Assessment-in-LMs
Replicating Discrimination Assessment in LMs with Focus on Jewish People and Israel Associated Individuals.
This project aims to adapt the methodology used in the referenced paper [[1]](#1) to specifically investigate how LMs handle decisions involving Jewish people and Israel-associated individuals. 
It would involve generating decision-making scenarios relevant to these groups, systematically varying demographic information to include Jewish and Israel-associated identifiers, 
and analyzing the responses for patterns of discrimination. The project would also explore prompt-based interventions to mitigate any discovered biases, 
contributing to the broader understanding of LMs’ handling of specific ethnic and national identities. For more details on the original paper, you can access it [[1]](#1).

## Experiments (Workflow)
EDA
Dataset fixes if needed
inference - generate answers with Gemma models
analyze results
We used [ollama](https://ollama.com/) framework to run the models described later in this README.

## [Datasets](outputs\datasets) and Models

| Dataset \ Model              | [gemma:2b-instruct-v1.1-fp16](https://ollama.com/library/gemma:2b-instruct-v1.1-fp16) | [gemma:2b-instruct-v1.1-q4_K_M](https://ollama.com/library/gemma:2b-instruct-v1.1-q4_K_M) | [gemma:7b-instruct-v1.1-fp16](https://ollama.com/library/gemma:7b-instruct-v1.1-fp16) | [gemma:7b-instruct-v1.1-q4_K_M](https://ollama.com/library/gemma:7b-instruct-v1.1-q4_K_M) |
|:------------------------------:|:---------:|:---------:|:---------:|:---------:|
| [explicit-combined-jews](outputs/datasets/explicit-combined-jews.jsonl)       |   [✓](outputs/gemma-2b-instruct-v1.1-fp16/gemma-2b-instruct-v1.1-fp16-explicit-combined-jews-decisions.jsonl)     | [✓](outputs/gemma-2b-instruct-v1.1-q4_k_m/gemma-2b-instruct-v1.1-q4_k_m-explicit-combined-jews-decisions.jsonl)        | [✓](outputs/gemma-7b-instruct-v1.1-fp16/gemma-7b-instruct-v1.1-fp16-explicit-combined-jews-decisions.jsonl)       | [✓](outputs/gemma-7b-instruct-v1.1-q4_k_m/gemma-7b-instruct-v1.1-q4_k_m-explicit-combined-jews-decisions.jsonl)      |
| [explicit-all-jew](outputs/datasets/explicit-combined-jews.jsonl)            |    [✓](outputs/gemma-2b-instruct-v1.1-fp16/gemma-2b-instruct-v1.1-fp16-explicit-all-jew-decisions.jsonl)    | [✓](outputs/gemma-2b-instruct-v1.1-q4_k_m/gemma-2b-instruct-v1.1-q4_k_m-explicit-all-jew-decisions.jsonl)        | [✓](outputs/gemma-7b-instruct-v1.1-fp16/gemma-7b-instruct-v1.1-fp16-explicit-all-jew-decisions.jsonl)       | [✓](outputs/gemma-7b-instruct-v1.1-q4_k_m/gemma-7b-instruct-v1.1-q4_k_m-explicit-all-jew-decisions.jsonl)      |
| [implicit-fix-combined-jews](outputs/datasets/implicit-fix-combined-jews.jsonl)   | [✓](outputs/gemma-2b-instruct-v1.1-fp16/gemma-2b-instruct-v1.1-fp16-implicit-fix-combined-jews-decisions.jsonl)       | [✓](outputs/gemma-2b-instruct-v1.1-q4_k_m/gemma-2b-instruct-v1.1-q4_k_m-implicit-fix-combined-jews-decisions.jsonl)        | [✓](outputs/gemma-7b-instruct-v1.1-fp16/gemma-7b-instruct-v1.1-fp16-implicit-fix-combined-jews-decisions.jsonl)       | [✓](outputs/gemma-7b-instruct-v1.1-q4_k_m/gemma-7b-instruct-v1.1-q4_k_m-implicit-fix-combined-jews-decisions.jsonl)      |

## Models Description
### [Google Gemma](https://ai.google.dev/gemma/docs/model_card)
_Note:_ **write here about the quantization method**


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

#### [Exploratory Data Analysis](EDA\eda.ipynb)
For more insights about the data and how we constructed new datasets based on the original one. 

### [explicit-combined-jews](outputs\datasets\explicit-combined-jews.jsonl)
This dataset is built on top of the original explicit dataset with addition of **Jewish as a race**, this dataset is larger then the original explicit dataset because we added one more race option for each question ID -> 11340 examples (3x6x9x70).
Also, some examples fixing was needed according to the findings in the EDA.

### [explicit-all-jew](outputs\datasets\explicit-all-jew.jsonl)
This dataset is a variation of the original explicit dataset, we added in each _filled_template_  after the _race_ an ethnicity - Jew. Thus we have combinations with racial and ethnic background, for example: Asian Jew, white Jew etc. 

The number of unique examples stayed the same regard to the original dataset -> 9450 examples (3x5x9x70).
For further details you can see the EDA and how we built the new dataset.

**_Note: it's important to note that using "Jew" solely as a descriptor after a race could be perceived as reductionist or stereotypical. It's essential to be sensitive to cultural and religious identities when using language in this manner._**

### [implicit-fix-combined-jews](outputs\datasets\implicit-fix-combined-jews.json)
This dataset is a variation of the original implicit dataset, it involves specifying an age, along with a name associated with a particular race and
gender. Whereas the former approach enables us to assess discrimination based on explicitly mentioned demographic information, this latter approach enables us to assess discrimination based on more subtle information correlated with race and gender.

Here we also addressed **Jewish as a race**, this dataset is larger then the original implicit dataset because we added one more race option for each question ID By adding Jewish/Israeli names -> 11340 examples (3x6x9x70).

Also, in the original implicit dataset we found a lot of outliers and errors for decision questions, some weren't complete, others were too long, so we had to fix those and come ou with the new dataset. More can be found on the EDA and the final work paper.


## References
<a id="1">[1]</a>  Tamkin, A., Askell, A., Lovitt, L., Durmus, E., Joseph, N., Kravec, S., Nguyen, K., Kaplan, J. and Ganguli, D., 2023. Evaluating and mitigating discrimination in language model decisions. arXiv preprint [arXiv:2312.03689](https://arxiv.org/abs/2312.03689).

<a id="2">[2]</a> [Anthropic/discrim-eval Dataset card on Hugging Face](https://huggingface.co/datasets/Anthropic/discrim-eval)
.

[ollama Git](https://github.com/ollama/ollama/tree/main)

[gemma Git](https://github.com/google-deepmind/gemma)
