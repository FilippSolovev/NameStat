# Name Stat
NameStat shows the most frequent verbs that were used in naming python functions and methods.

# Example

To perform an analysis in current directory use:

~~~~
$ python namestat.py
total 658 files
trees generated
total 9347 functions
total 10 words, 10 unique
get 560
add 112
find 87
make 81
run 67
apply 63
tokenize 53
remove 51
initialize 31
replace 23
~~~~

It is possible to specify a directory to look for as a command line argument like:

`$ python namestat.py project/env`

# Installation

Clone the project and install the requirements:

~~~~
$ git clone https://github.com/FilippSolovev/NameStat
$ pip install -r requirements.txt
~~~~

Since the project uses NLTK it needs ‘averaged_perceptron_tagger’, to obtain this resource use [NLTK Downloader](https://www.nltk.org/data.html "NLTK Downloader") typing in python:

~~~~
>>> import nltk
>>> nltk.download('averaged_perceptron_tagger')
~~~~

See NLTK documentation for details.

# Built With
* [NLTK](https://www.nltk.org "NLTK") - Used to parse function names 

# Authors
* Ilya Lebedev - Initial work - [Melevir](https://github.com/Melevir "Melevir")
* Filipp Solovev - Deep code refactoring - [FilippSolovev](https://github.com/FilippSolovev "FilippSolovev")

# License
This project is licensed under the MIT License - see the [LICENSE.md](NameStat/LICENSE) file for details
