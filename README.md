
# 🍌 OmegaFold on Banana

This is a repo that lets you run [OmegaFold](https://github.com/HeliXonProtein/OmegaFold) on [Banana](https://banana.dev), which is a platform to run GPU accelerated code serverlessly. This essentially means you have a quick, autoscaling API to run OmegaFold.

It takes ~3 minutes to get the model loaded and ready for inference; so expect your first call after cold start to take a while. API calls right after that should be quick! You can change the `IDLE TIMEOUT` in Banana settings, which is 10s by default (i.e your instance will shut down after 10s of no activity, and will be cold booted again next time you call it.)

## Setup

First you need to create a Banana account and get your API key. You can do that [here](https://banana.dev). Next, deploy this repo as a model in Banana, and find the key too.

## Usage

To call inference, first install the Banana sdk:
```bash
pip install banana-dev
```

Then, you can call the API like this:
```python
import banana_dev as banana
import os

api_key = "<YOUR_API_KEY>"
model_key = "<YOUR_MODEL_KEY>"
model_inputs = {"sequence": "LLEECLERLKKRSFIEDLLFNLKLLKEAEKK"}

out = banana.run(api_key, model_key, model_inputs)

pdb_string = out["modelOutputs"][0]["pdb_string"]

with open("out.pdb", "w") as f:
    f.write(pdb_string)
```