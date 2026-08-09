# CricketGPT ML Data

This directory contains generated machine-learning datasets.

## Training Dataset

The primary training dataset is:

`match_training_data.csv`

The dataset should contain the feature columns defined in:

`app/ml/config.py`

and the target:

`team1_win`

Target values:

- `1` = Team 1 won
- `0` = Team 2 won

Generated datasets should not contain credentials,
secrets, or personally identifiable information.