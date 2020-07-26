# OTtools
OTtools provides some structures for working with Optimality Theory data in Python.

## What OTtools is
"*Optimality Theory is a general model of how grammars are structured*" ([McCarthy 2007](https://scholarworks.umass.edu/linguist_faculty_pubs/93/)). OTtools provides Python representations for the structures hypothesized in [Optimality Theory: Constraint Interactions in Generative Grammar](http://roa.rutgers.edu/article/view/547) (Prince and Smolensky 2002) and other works stemming from this area of Linguistics. If you want to learn more about Optimality Theory, [What is Optimality Theory?](https://scholarworks.umass.edu/linguist_faculty_pubs/93/) (McCarthy 2007) is a  good place to start, but Optimality Theory and OTtools likely won't make much sense without a solid understanding of Linguistics in general and Generative Phonology more specifically.

## Why OTtools Exists
OTtools is primarily a constructed motivation for the author to practice Python, but it is also intended to provide a convenient means of accomplishing certain tasks related to Optimality Theory research. The following basic example illustrates the utility of OTtools:

* [SPOT](https://github.com/syntax-prosody-ot/main) (Bellik et al.) can produce tableaux with millions of candidates.
* The output for SPOT is formatted for import into [OTWorkplace](https://sites.google.com/site/otworkplace/) (Prince et al.) where it can be analyzed.
* OTWorkplace is built on Microsoft Excel and each candidate in a tableau requires its own row in an Excel worksheet.
* OTWorkplace therefore cannot import tableaux with more candidates than the row limit of Excel (1,048,576).
* OTtools can pare down large tableaux of this sort by removing harmonically bounded candidates so the relevant candidates can be analyzed in OTWorkplace.

## How to Install and Use OTtools
At the moment, OTtools is only available by cloning the [GitHub repository](https://github.com/maxTarlov/OTtools). Updating to the [latest version of Python](https://www.python.org/downloads/) is recommended.

The included script `findOptima.py` can be used as a tutorial for OTtools. `findOptima.py` imports tableaux in the OTWorkplace format, removes harmonically bounded candidates, then exports the pared down tableaux back to the OTWorkplace format, as described in the example at the end of the previous section.

Unfortunately, there is currently no formal documentation for OTtools, but the source code is intended to be self-documenting.

## How to Help or Get Help
New GitHub Issues and Pull Requests are welcome. Please follow the guidelines below:

1. If you have a question about how to use existing features, create an issue and label it as a **question**.
2. If you think you have found a bug, make sure there is not already an open issue before opening a new issue and labeling it as a **bug**.
3. If there is something you would like OTtools to do but do not know how to implement it, open an issue and label it as an **enhancement** and as **help wanted**.
4. If you want to contribute to the source code, either find an existing issue or create your own and make sure the issue you are working your involvement. Open a pull request once you are done and mention the issue(s) in the description. Additionally, keep in mind the following things:

    * OTtools is structured with intention. Endeavor to understand why something is structured the way it is before changing its structure. 
    * OTtools uses Python's built-in unittest module. Ideally, each class should have a test case and each method in that class should have a test fixture.
    * Feel free to ask for help.

## License
OTtools is distributed under the [MIT License](https://opensource.org/licenses/MIT). Some additional things to keep in mind include:

* While the license does not require it, the author prefers projects using OTtools to be free and open source. (This does not apply to the publishing of research, which should be done however the researcher sees fit.)
* The author prefers that OTtools be mentioned if its use is substantial in any work.
* The user should not expect OTtools to be a flawless program. The author cannot guarantee that any part of OTtools will work as intended.
