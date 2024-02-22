# SIGFRID: Unsupervised, Platform-Agnostic Interference Detection in IoT Automation Rules

This repository contains the supplementary material for the paper "SIGFRID: Unsupervised, Platform-Agnostic Interference Detection in IoT Automation Rules" submitted to ACM Transactions on Internet of Things.

This material comprises the source codes useful for the repeatability of the experiments.

# Creators

Gaetano Cimino (gcimino@unisa.it) and Vincenzo Deufemia (deufemia@unisa.it)

University of Salerno

# Overview

In this paper, we present an unsupervised, platform-agnostic tool called <b>S</b>cene <b>I</b>nteraction <b>G</b>raphs <b>f</b>or <b>I</b>nterference <b>D</b>etection (SIGFRID). Driven by Large Language Models (LLMs), SIGFRID autonomously discerns diverse interference manifestations arising from unanticipated rule interactions. Specifically, SIGFRID deduces causal relations among events in the smart home domain, thereby formulating an exhaustive Scene Interaction Graph (SIG) that encapsulates interconnections among rules. The proficient exploration of SIG facilitates the extraction of interference instances.

# SIGFRID architecture

When presented with a set of trigger-action rules derived from various Trigger-Action Platforms integrated within an IoT ecosystem, SIGFRID represents the interactions between these rules by constructing a SIG. This construction
process involves the use of LLMs queried using distinct prompts tailored for the TAP domain via a prompt engineering methodology. Subsequently, the Inter-Rule Interference Vulnerabilities Detector is responsible for examining the SIG and presenting the results to the user, enabling informed decision-making. 

<p align="center">
  <img width="600" height="270"
    src="https://github.com/damocles-unisa/Sigfrid/blob/main/SIGFRID_architecture.png"
  >
</p>

# Usage
The SIG construction process and the extraction of the corresponding interference relations are performed by running the following command

```
python main_ChatGPT.py
```

The modeling of a SIG is achieved through the utilization of the class <b>SceneInteractionGraph</b> within the module <b>scene_interaction_graph.py</b>. This class employs the Python package <i>NetworkX</i> for the representation of the graph structure.

Within this implementation, ChatGPT serves dual purposes, encompassing both system element identification and interference detection tasks. Specifically, the functionality resides in the class <b>QuestionAnswerChatGPT</b> within the module <b>utils_ChatGPT.py</b>, housing the instructions employed for querying the <i>gpt-3.5-turbo</i> version of ChatGPT. The templates utilized during experimental procedures are delineated as follows:

<table align="center">
    <tr> <td align="center"><b>t<sub>S(T)</sub></b></td>
     <td align="center">Does the activation of the trigger event [X] rely on the system
element [Y]? Answer with yes or no and explain why.
</td>
    </tr>
    <tr> <td align="center"><b>t<sub>S(A)</sub></td>
        <td align="center">Does executing the action event [X] cause changes to the system
element [Y]? Answer with yes or no and explain why.
</td>
    </tr>
    <tr> <td align="center"><b>t<sub>RC</sub></td>
        <td align="center">Can the execution of the action event [X] directly or indirectly cause
the activation of the trigger event [Y]? Answer with yes or no and explain
why.
</td>
    </tr>
<tr> <td align="center"><b>t<sub>AD</sub></td>
        <td align="center"> Do the action event [X] and the action event [Y] express the same
meaning? Answer with yes or no and explain why.
</td>
    </tr>
<tr> <td align="center"><b>t<sub>TB</sub></td>
        <td align="center"> Can the execution of the action event [X] directly or indirectly block
the activation of the trigger event [Y]? Answer with yes or no and explain
why. Please do not consider conflicts in terms of resources.

</td>
    </tr>
<tr> <td align="center"><b>t<sub>AB</sub></td>
        <td align="center"> Can the execution of the action event [X] directly or indirectly block
the execution of the action event [Y]? Answer with yes or no and explain
why. Please do not consider conflicts in terms of resources.
</td>
    </tr>
  <tr> <td align="center"><b>t<sub>AC</sub></td>
        <td align="center"> Is there a potential conflict between the execution of the action
event [X] and the execution of the action event [Y]? Answer with yes or no
and explain why. Please do not consider conflicts in terms of resources.
</td>
    </tr>  
</table>


Ultimately, the extraction of interferences is executed through the application of methods encapsulated within the module named <b>search_engine.py</b>.
