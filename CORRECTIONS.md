# Corrections applied to the SARA Monte Carlo post-processing script

The Monte Carlo campaign of the controlled re-entry was run with the SARA Monte Carlo
scripts published by the ESA Space Debris Office in the Space Debris User Portal forum:

https://debris-forum.sdo.esoc.esa.int/t/updated-example-scripts-for-probabilistic-re-entry-analyses/1269

- `SARA_MC_uncertainties_main.py`
- `SARA_MC_helper.py`
- `post_processing.py`

Those scripts are property of ESA and the DRAMA Licence applies to them, so they are not
included in this repository and therefore have to be downloaded from the post above, which also
gives the installation and usage steps. What is documented here are the three
corrections that `post_processing.py` needs in order to read the output of a
**controlled** re-entry. The script is written for the uncontrolled case, and without
these changes it returns zeros.

The version used here was downloaded in August 2026. The forum post is updated from time
to time, so it is worth checking to see if a newer version already covers any of this.

## 1. Fragment key

The results XML nests `<fragment>`, in singular, inside `<fragments>`. The script reads
the plural key, which silently returns an empty list instead of raising an error.
Every casualty and area sum therefore gives zero.

Read the singular tag nested inside the plural one.

## 2. Header totals

The script takes the totals by slicing a fixed range of lines from the top of the file and
unpacking four values. That matches an uncontrolled results file, because its totals block has
four entries. A controlled results file has six, because it adds `totalCasualty2D` and
`totalFatality2D`. Then, the unpacking is shifted by one position, and the fatality
probability and the impact mass come back as zeros.

Read each total by its tag name instead of by its position in the file.

## 3. The 2D projection is never read

The script only reads the 1D casualty probability. For a controlled re-entry the 2D
projection is the one that corresponds to the scenario, since the footprint is a bounded
area and not a latitude band.

Parse `totalCasualty2D` as well and report it alongside the 1D value.
