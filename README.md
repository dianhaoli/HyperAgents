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

## ARC-AGI-2 coach experiment (branch `arc2-improver`)

**Question.** Does a coach (meta agent) that rewrites itself train a better player (task agent) than the original
coach, given the same compute? Tested on ARC-AGI-2 with a pre-registered design.

**Answer.** No. On the 120-puzzle exam, players trained by the original coach scored 29.7%, players trained by
self-improved coaches 27.9%, and the uncoached player 29.3%; none of the differences is distinguishable from
run-to-run noise. Coaches picked at later generations (20 and 40) were no better. Letting the model think longer
(higher reasoning effort, no coaching) scored 41.1%. Total cost $152.23.

| Read | What it is |
|---|---|
| [`WRITEUP.md`](WRITEUP.md) | The plain-language write-up, with a list of every experiment at the end |
| [`RESULTS.md`](RESULTS.md) | All numbers and the analysis output |
| [`explorer/`](explorer/) | Interactive explorer (static web page): try a puzzle, results, evolution trees, every exam answer, every coaching session, a traced coaching round. Run with `python3 -m http.server -d explorer` |
| [`DESIGN.md`](DESIGN.md), [`DESIGN_v2.md`](DESIGN_v2.md) | Pre-registered design (`f577cc7`) and follow-up plan (`991a237`) |
| [`DECISIONS.md`](DECISIONS.md) | Every deviation, bug and re-run, numbered |
| [`REPRODUCE.md`](REPRODUCE.md) | Setup and the exact commands, in order |
| [`STATUS.md`](STATUS.md) | What has run (everything is finished) |

**Layout.**
- `arcexp/`: experiment infrastructure (root-only, never visible to agents): the budget gateway (`gateway.py`, the
  only route to the model), sandbox, loop adapter, scoring, orchestration, analysis helpers, explorer data builders.
- `agent_template/`: the starting player A_0 and original coach I_0. `domains/arc/`: the ARC domain.
- `analysis.py` (pre-registered analysis), `analysis_ext.py` (follow-up), `splits.json` (all task splits).
- `exp/`: every record: `results/` (rollouts and analysis outputs), `runs/` (configs, snapshots, per-generation
  logs and transcripts), `archive_export/` (every agent's code), `ledger/` (every model call and its cost), `logs/`,
  `crashed/` (runs restarted after harness bugs), `demo/` (the traced demo run, not part of the results).

The rest of this README is the upstream HyperAgents documentation.

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

