Postag
======

Overview
--------
Postag is a simple part of speech tagger which is capable of two modes, a naive baseline mode and a second order Hidden Markov Model mode.

Usage
-----
postag.py [mode] [train_data] [test_data]

- mode is either baseline which tags words with their most common part of speech from the training data or hmm which uses a second order Hidden Markov Model
- train_data and test_data must be of the same format as the included train.txt and test.txt
