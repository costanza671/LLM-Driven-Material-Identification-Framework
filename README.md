
# LLM-Driven Material Identification Framework (SDU postdoc excercise)

## General Overview

This program is a Python-based framework that converts a natural language description of a material into a fully resolved crystal structure and generates simulation-ready outputs.

The workflow includes:
- LLM-based parsing of material descriptions (Gemini)
- Materials Project database query and ranking
- Atomic structure construction using ASE
- Export of atomic structure metadata (`*.json`) and of simulation inputs (`POSCAR` via ASE, `QE`/`CIF` via c2x)
- An interactive viewer (ASE gui) is launched to inspect the final structure


## Requirements and General Instructions for Set-Up

This code requires a Python environment and a set of external dependencies not included in the standard library. It follows a modular architecture consisting of a main execution script (`main.py`) that controls the overall workflow, and a set of dedicated modules responsible for each task.

The environment can be created using tools such as Conda or Python’s built-in virtual environment system (venv). Both approaches are valid; A Conda-based setup is provided as a standard example.

### Environment setup (Conda)
Create a new Conda environment, optionally specifying the Python version (adding the flag `python=<python-version>`), with the following command:
```bash
conda create --name sdu-llm
```
Once the environment is created, it should be activated before installing any packages. 
```bash
conda activate sdu-llm
```
All required dependencies can then be installed inside this environment, using:
```bash
conda install anaconda::termcolor
conda install conda-forge::google-generativeai
conda install conda-forge::mp-api
conda install conda-forge::ase
``` 

### External tools
c2x is an external structure conversion tool used to generate simulation input files. It is required for producing outputs compatible with electronic structure codes (e.g. VASP, Quantum ESPRESSO). The tool must be installed separately and must be available in your system PATH (it should be callable from the terminal using the command `c2x`). Instructions for quick install can be found at: https://www.c2x.org.uk/downloads/quick_install.html

### API keys
This code requires two external API keys to access remote services.
- `GOOGLE_API_KEY` → used to access the Gemini model for natural language parsing of material descriptions
- `MP_API_KEY` → used to query the Materials Project database for crystal structures

The keys can be obtained from:
- Google AI Studio (for Gemini access)
- Materials Project website (for database access)

These keys must be set as environment variables before running the code. If they are not provided, the program will not execute. 
Once you have them, export the required API keys as:

```bash
export GOOGLE_API_KEY="your_google_api_key"
export MP_API_KEY="your_materials_project_api_key"
```

## Usage
 The repository must be cloned locally so that all scripts and modules are available in the same working directory:
```bash 
git clone <repository-url>
```
 Move into the project folder: 
 ```bash 
 cd <repository-folder>
```
Activate the Conda environment and export the required API keys.

Finally, execute the program: 
 ```bash 
 python main.py
```

## Additional Notes and Remarks

### 

