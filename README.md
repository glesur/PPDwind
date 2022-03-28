# Self-Similar wind solutions for protoplanetary discs

## Disclaimer

These solutions are distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE**. These solutions and the code source attached to it are published under the CECILL 2.1 license.

## Using these self-similar solutions

The numerical self-similar wind solutions which can be downloaded from this web page are a sub-sample of the solutions described in Lesur (2021) ( https://ui.adsabs.harvard.edu/abs/2021A%26A...650A..35L/abstract ), published in Astronomy & Astrophysics. Each solution for a particular set of parameter is found in a single .dat containing the field value as a function of the latitudinal angle theta. A python script read_solution.py is provided to demonstrate how one can plot streamlines and fieldlines of a given dataset. To use it, simply launch the script with a python3 interpreter with the name of the desire dataset in argument, e.g.:

```console
python3 read_solution.py beta=1.0e+05-Am=1-Rm=inf.dat 
```

## Contact

If you need help using these solutions, contact Geoff Lesur (geoffroy.lesur@univ-grenoble-alpes.fr)

## Acknowledgement

This work has received funding from the European Research Council (ERC) under the European Union Horizon 2020 research and innovation programme (Grant agreement No. 815559 (MHDiscs)).
