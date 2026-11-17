<div align="center">

<!-- Logo/Banner placeholder - uncomment and add your image -->
<!-- <img src="assets/banner.png" alt="HyperAgents Banner" width="800"> -->

<h1>HyperAgents</h1>

<p>Self-referential self-improving agents that can optimize for any computable task</p>

<p>
<a href="LICENSE.md"><img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg?style=for-the-badge" alt="License: CC BY-NC-SA 4.0"></a>
<a href="https://arxiv.org/abs/2603.19461"><img src="https://img.shields.io/badge/arXiv-2603.19461-b31b1b.svg?style=for-the-badge&logo=arxiv" alt="arXiv"></a>
<a href="https://ai.meta.com/research/publications/hyperagents/"><img src="https://img.shields.io/badge/-Blog-%238D6748?style=for-the-badge&logo=Website&logoColor=white"></a>
<a href="https://x.com/jennyzhangzt/status/2036099935083618487"><img src="https://img.shields.io/badge/twitter-%230077B5.svg?&style=for-the-badge&logo=twitter&logoColor=white&color=00acee"></a>
</p>

---

</div>

## ARC-AGI-2 improver experiment (branch `arc2-improver`)

Pre-registered experiment: does a self-evolved meta agent improve a fresh task agent more than the original
meta agent does, given equal pay-off compute? See `DESIGN.md` (pre-registration), `DECISIONS.md` (every choice
and deviation), `STATUS.md` (progress and resume), and `RESULTS.md`.

Layout: `arcexp/` holds the experiment infrastructure (root-only, never visible to agents). It contains
`gateway.py` (budget gateway and the only route to the model), `sandbox.py`, `run_loop.py` (the repo's
`generate_loop.py` without Docker), `arc_eval.py`, `phases.py`, `evolved.py` (I_g selection and transplant),
`orchestrate.py` and `isolation_check.py`. The rest: `agent_template/` (A_0 + I_0), `domains/arc/`, `analysis.py`,
`exp/` (all logs, results JSONL, ledger, runs) and `splits.json`.

Exact commands, in order (each is resumable; long ones run detached via `arcexp/run_bg.sh`):

```bash
bash arcexp/setup_env.sh                      # once per VM: deps, agent user, private ARC data, sysctls
bash arcexp/start_gateway.sh                  # budget gateway (idempotent)
python3 -m arcexp.isolation_check <phase>     # answer-isolation check; run before each phase
python3 -m arcexp.make_splits stage1          # held-out / screen / smoke ids
python3 -m arcexp.run_loop --config exp/runs/smoke/config.json            # step 1 smoke test
python3 -m arcexp.phases screen               # step 3: 100 training tasks x 3 single calls
python3 -m arcexp.make_splits stage2 --set_size 25                        # source / pay-off sets
for r in 0 1 2; do python3 -m arcexp.phases b0 --only $r; done            # step 3: B0 x3
python3 -m arcexp.phases xhigh                # step 3: one held-out pass at xhigh
python3 -m arcexp.orchestrate pilot           # step 5: 2 I_0 pay-off runs
python3 -m arcexp.phases final --run payoff_I0_1; python3 -m arcexp.phases final --run payoff_I0_2
python3 -m arcexp.orchestrate source          # step 6: 6 source runs x 12 generations
python3 -m arcexp.evolved select              # step 6: choose I_g per seed
python3 -m arcexp.evolved transplant          # transplant each I_g's meta code onto A_0
python3 -m arcexp.orchestrate trial           # step 7: one trial iteration per I_g
python3 -m arcexp.orchestrate payoff          # step 8: I_g pay-off runs + remaining I_0 runs (freeze mode)
python3 -m arcexp.phases final --run <run>    # step 9: per pay-off run
python3 -m arcexp.evolved stats               # self-edit statistics
python3 analysis.py                           # results
```

## Setup
```bash
# API keys, put these into .env file
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
```

```bash
# Install things
sudo dnf install -y python3.12-devel
sudo dnf install -y graphviz graphviz-devel cmake ninja-build bzip2-devel zlib-devel ncurses-devel libffi-devel
```

```bash
# Create virtual environment
python3.12 -m venv venv_nat
source venv_nat/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
# To build the docker container
docker build --network=host -t hyperagents .
```

```bash
# Setup initial agents
bash ./setup_initial.sh
```

## Running HyperAgents

```bash
# See the script for args, and baseline selections
python generate_loop.py --domains <domain>
```

By default, outputs will be saved in `outputs/` directory.

## File Structure
- `agent/` code for using foundation models
- `analysis/` scripts used for plotting and analysis
- `domains/` code for each domain
- `utils/` common code used in the repo
- `run_meta_agent.py` script to help run the meta agent and get the diffs
- `meta_agent.py` main implementation of the meta agent
- `task_agent.py` main implementation of the task agent
- `generate_loop.py` entry point for running the algorithm

## Logs from Experiments

The experiment logs can be downloaded here: https://drive.google.com/drive/folders/164fKQWgLM18foOzSnpv0F_I3TNpX8u8-?usp=sharing

## Safety Consideration
> [!WARNING]  
> This repository involves executing untrusted, model-generated code. We strongly advise users to be aware of the associated safety risks. While it is highly unlikely that such code will perform overtly malicious actions under our current settings and with the models we use, it may still behave destructively due to limitations in model capability or alignment. By using this repository, you acknowledge and accept these risks.

## Citing
If you find this project useful, please consider citing:
```bibtex
@misc{zhang2026hyperagents,
      title={Hyperagents}, 
      author={Jenny Zhang and Bingchen Zhao and Wannan Yang and Jakob Foerster and Jeff Clune and Minqi Jiang and Sam Devlin and Tatiana Shavrina},
      year={2026},
      eprint={2603.19461},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2603.19461}, 
}
```

