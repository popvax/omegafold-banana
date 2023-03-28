# -*- coding: utf-8 -*-
# =============================================================================
# Copyright 2022 HeliXon Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
The main function to run the prediction
"""
# =============================================================================
# Imports
# =============================================================================
import gc
import logging
import os
import sys
import time

import torch

import omegafold as of
from . import pipeline
import random
import string
import argparse
# =============================================================================
# Functions
# =============================================================================
@torch.no_grad()
def init():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    global forward_config
    forward_config = argparse.Namespace(
        subbatch_size=None,
        num_recycle=10,
    )
    weights = pipeline._load_weights("https://helixon.s3.amazonaws.com/release1.pt", os.path.expanduser("~/model.pt"))
    weights = weights.pop('model', weights)

    # get the model
    logging.info(f"Constructing OmegaFold")
    global model
    model = of.OmegaFold(of.make_config(1))

    if "model" in weights:
        weights = weights.pop("model")
    model.load_state_dict(weights)
    model.eval()
    model.to("cuda:0")
    logging.info("Constructed model")

@torch.no_grad()
def inference(model_inputs:dict) -> dict:
    save_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdb"

    inputs = pipeline.fasta2inputs(
        model_inputs["sequence"],
        device=torch.device("cuda:0"),
    )

    input_data = list(inputs)[0]
    try:
        output = model(
                input_data,
                predict_with_confidence=True,
                fwd_cfg=forward_config
            )
    except RuntimeError as e:
        logging.info(f"Failed to generate due to {e}")
    pipeline.save_pdb(
        pos14=output["final_atom_positions"],
        b_factors=output["confidence"] * 100,
        sequence=input_data[0]["p_msa"][0],
        mask=input_data[0]["p_msa_mask"][0],
        save_path=save_path,
        model=0
    )
    pdb_string = open(save_path, "r").read()
    os.remove(save_path)
    return {"pdb_string": pdb_string}
