# LLM-Powered Scene Interaction Graphs for Interference Detection in Trigger-Action Rules

This repository contains the supplementary material for the paper "LLM-Powered Scene Interaction Graphs for Interference Detection in Trigger-Action Rules" submitted to IEEE Internet of Things Journal.

This material comprises the source codes useful for the repeatability of the experiments.

# Creators

Gaetano Cimino (gcimino@unisa.it) and Vincenzo Deufemia (deufemia@unisa.it)

University of Salerno

# Overview

In this paper, we present an unsupervised, platform-agnostic tool called <b>S</b>cene <b>I</b>nteraction <b>G</b>raphs <b>f</b>or <b>I</b>nterference <b>D</b>etection. Driven by Large Language Models (LLMs), SIGFRID autonomously discerns diverse interference manifestations arising from unanticipated rule interactions. Specifically, SIGFRID deduces causal relations among events in the smart home domain, thereby formulating an exhaustive Scene Interaction Graph (SIG) that encapsulates interconnections among rules. The proficient exploration of SIG facilitates the extraction of interference instances.

# SIGFRID architecture

When presented with a set of trigger-action rules derived from various TAPs integrated within an IoT ecosystem, SIGFRID represents the interactions between these rules by constructing a SIG. This construction
process involves the use of LLMs queried using distinct prompts tailored for the TAP domain via a prompt engineering methodology. Subsequently, the Inter-Rule Interference Vulnerabilities Detector is responsible for examining the SIG and presenting the results to the user, enabling informed decisionmaking. In the following, we introduce the SIG definition and the various phases of the SIGFRID detection process.

<p align="center">
  <img width="500" height="270"
    src="https://github.com/damocles-unisa/Sigfrid/blob/main/SIGFRID_architecture.png"
  >
</p>



