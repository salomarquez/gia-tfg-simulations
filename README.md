# DRAMA re-entry simulations — *Melpomene*

This repository contains the two DRAMA projects used in the Bachelor Thesis *On-Ground Casualty Risk and Disposal Reliability Analysis for the Re-entry of a Satellite in Low Earth Orbit*
(Universidad Carlos III de Madrid). `Uncontrolled_Case` corresponds to Scenario 1 and
`Controlled_Case` to Scenario 2, both built on the *Melpomene* model distributed with
DRAMA.

## Requirements

The projects were conducted with **DRAMA 4-1.2**, which can be obtained from the ESA Space
Debris User Portal:

https://sdup.esoc.esa.int/drama/downloads

A later release opens them as well, but it is important to update the project files when the tool
asks for it, which is step 3 below.

## How to open and run the simulations

1. Run DRAMA **as administrator**.
2. Once the interface is shown, select **Open → Open project** and choose either
   `Uncontrolled_Case` or `Controlled_Case`.
3. Accept all the updates that DRAMA prompts for when the project is loaded. This is also
   what rewrites the internal paths of the project to the folder it is being opened from.
4. Copy the file `example_population.sim` from your own DRAMA installation into the
   `population_files` folder of the project. That file belongs to ESA and to the providers
   of the population data, so it is not redistributed here, but it comes with every
   installation.
5. Run the simulation. As soon as it finishes, the results can be checked and
   downloaded from the **Outputs** tab of the interface. The ones obtained for this
   thesis were saved in the `results` folder of each project.

Two red *File not found* messages appear when the project is opened. They refer to
`environment.csv` and `proof.mask`, which belong to the MIDAS and PROOF modules. This
study uses only SARA, so the messages can be dismissed and the run completes normally.

## What is in each project

- `input` holds the definition of the spacecraft: geometry, materials, masses and entry
  conditions.
- `data` holds the aerodynamic coefficients, cross sections and shading matrices that
  DRAMA computed from that geometry. The database files that DRAMA copies from its own
  installation are not included, for the same reason as the population file, and are
  restored by the update of step 3.
- `results` holds the output of the runs reported in the thesis.

## Monte Carlo analysis of the footprint

`Controlled_Case` contains `input.yml`, the configuration of the Monte Carlo simulations of
three hundred samples described in the thesis, with the uncertainties applied to the heat
flux in the three flow regimes, to the atmospheric density and to the position at the
interface. The Python dependencies are listed in `requirements.txt`.

The campaign itself is run with the SARA Monte Carlo scripts published by the ESA Space
Debris Office in the Space Debris User Portal forum, where the installation and usage
steps are also given:

https://debris-forum.sdo.esoc.esa.int/t/updated-example-scripts-for-probabilistic-re-entry-analyses/1269

Those scripts are property of ESA and the DRAMA Licence applies to them, so they are not
redistributed here and have to be downloaded from that post. `CORRECTIONS.md` documents
the three changes that the post-processing script needs in order to read the output of a
controlled re-entry.
