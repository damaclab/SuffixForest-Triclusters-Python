**USER GUIDE**

Tri-clustering is a popular technique in data mining that can be used to uncover interesting patterns, association rules and relationships in large datasets. However, these techniques are often computationally expensive and can be challenging to apply to large datasets.

This program implements a novel approach that combines association rule mining, bi-clustering, and tri-clustering using suffix tree and suffix forest data structures. It is based on the frequent closed itemset framework and requires a unique scan of generated tree/forest. This data structure is used to reduce memory usage and at the same time provide more information on the association rules and frequent patterns. 

We will discuss how to use the source code of this python program, as well as how to directly use this program as a python module just by installing it using pip.

We will be briefly discussing the following topics:

- Environment & python installation
- Installation of external Libraries
- Using the source code or using the package
- Transforming input dataset to suitable form
- Integrating the dataset with the python program
- Generating outputs
- Results

**1. Environment & python installation:**

I have used an windows PC with 64-bit operating system, x64-based processor for running the python program.

To run the program, a suitable python installation is required. I have used Python 3.10.6.

To install Python 3 on your machine, Visit the official Python website [https://www.python.org](https://www.python.org/) and navigate to the Downloads section. Download a version of Python 3.10 or onwards.

**2. Installation of external libraries**

In this project we are using 2 external libraries on top of default python installation:

- Pandas
- PyDot

We are using pandas for the useful functionalities it provides for handling CSV files and DataFrames. PyDot is an interface to GraphViz which helps in creating graph based diagrams using python script.

To install Pandas use: python -m pip install pandas

To install PyDot: python -m pip install pydot

You may additionally need to install a Dot driver for PyDot to work properly.

**3. Using the source code or the package**

The source code of the program can be cloned from this git repository.

Source Code: <https://github.com/damaclab/SuffixForest-Triclusters-Python>

The program is also uploaded in pypi.org as a python package. The latest version is 2023.5.31.1

Package link: <https://pypi.org/project/triclustering/>

Instead of cloning the git repository, the package can be directly installed using the following pip install command.

|python -m pip install triclustering --user|
| :- |

This will also install the dependencies - pandas and pydot, automatically.

**4. Transforming Input Dataset into Suitable Form**

The input dataset must have the following 3 attributes:

- An ID attribute which is unique for each row
- An item\_list attribute which contains comma separated names or values – each name or value representing an item.
- A splitting attribute according to which the dataset can be split into multiple datasets each of which can further be transformed into an SFD.

We are assuming that the dataset has an item list column which contains comma separated items. But if the dataset does not have an item list column, and has an item column only, then suitable grouping and aggregation must be performed so that the item list column is created.

If the dataset has multiple attributes and we want to form clusters from attribute:value pairs, then we can add a column containing comma separated (attribute:value) pairs which will act as the item list column.

**5. Integrating the dataset with our python program**

Our python implementation has module named processor.py. This file acts as an interface between the user and the complete algorithmic process.

First import the class Processor from the processor module and initialize a Processor class.

If we are using the source code from git repository, we need to specify the processor.py file while importing Processor class.

|<p>from processor import Processor</p><p>processor = Processor()</p>|
| :- |

Otherwise, if we are directly using the package after installing it by pip, then we need to specify the package name ‘triclustering’.

|<p>from triclustering import Processor</p><p>processor = Processor()</p>|
| :- |

Next step is to integrate the input CSV file with the processor object. This is done using the Processor.set\_input\_dataset() method. The prototype and description of this method is given below.


|**triclustering.Processor.set\_input\_dataset()**|
| :-: |


|def set\_input\_dataset(<br>`                             `input\_file\_dir: str,<br>`                             `input\_file\_name: str,<br>`                             `oid\_attribute: str,<br>`                             `item\_list\_attribute: str,<br>`                             `split\_attribute: str<br>`                          `) -> None|
| :- |


<table><tr><th colspan="3" valign="top"><b>Parameters</b></th></tr>
<tr><td rowspan="3" valign="top"><b>input_file_dir</b></td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Description</td><td valign="top">Path to the directory where the input CSV file (dataset) is located.</td></tr>
<tr><td rowspan="3" valign="top"><b>input_file_name</b></td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Description</td><td valign="top">Filename of the input CSV file including its file extension.</td></tr>
<tr><td rowspan="3" valign="top"><b>oid_attribute</b></td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Description</td><td valign="top">Name of the ID column of the dataset. The ID column must have unique value for each row.</td></tr>
<tr><td rowspan="3" valign="top"><b>item_list_attribute</b></td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Description</td><td valign="top">Name of the Item List column of the dataset. This column should contain comma separated item names. These item names will form itemsets.</td></tr>
<tr><td rowspan="3" valign="top"><b>split_attribute</b></td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Description</td><td valign="top">Name of the column which will be used as the third dimension for tri-clustering. The dataset will be portioned into multiple SFDs according to the value of this column. The number of unique values this column contains will be number of SFDs that will be created.</td></tr>
</table>

**5. Generating Outputs**

Now we can execute the process() method on the processor class object to generate the outputs as files. A directory named ‘output’ will be created (if doesn’t already exist) in the same directory as the input file’s directory. All the output files will be stored in this output directory.

The prototype and description of this method is given below.


|**triclustering.Processor.process()**|
| :-: |


def process(<br>`                  `min\_support\_percentage\_number\_table: float = 0.0,<br>`                  `min\_support\_count: int = 1,<br>`                  `min\_confidence: float = 0.0,<br>`                  `produce\_intermediate\_imgs: bool = False,<br>`                  `produce\_final\_img: bool = False,<br>`                  `custom\_name\_mapping: Any | None = None,<br>`                  `dtype\_key: Any | None = None<br>`                `) -> None|
| :- |


<table><tr><th colspan="3" valign="top"><b>Parameters</b></th></tr>
<tr><td rowspan="4" valign="top"><b>min_support_percentage_number_table</b></td><td valign="top">Datatype</td><td valign="top">Float</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">0.0</td></tr>
<tr><td valign="top">Description</td><td valign="top"><p>If the provided value for this attribute is greater than 0.0, then that percentage of the total number of rows will be used as minimum support count for constructing the number table.</p><p>If not provided, then min support count = 1 will be used for constructing the number table.</p></td></tr>
<tr><td rowspan="4" valign="top"><b>min_support_count</b></td><td valign="top">Datatype</td><td valign="top">Integer</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">1</td></tr>
<tr><td valign="top">Description</td><td valign="top"><p>If provided, this value will be used as the minimum support count for generating FCPs and Association Rules.</p><p>If min support percentage for number table is not provided, then this min support count will be used for constructing the number table as well.</p><p></p><p>This value will also be embedded within the file names of the generated files.</p></td></tr>
<tr><td rowspan="4" valign="top"><b>min_confidence</b></td><td valign="top">Datatype</td><td valign="top">Float</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">0.0</td></tr>
<tr><td valign="top">Description</td><td valign="top"><p>This value will be used as minimum confidence for generating the association rules.</p><p>This value will also be embedded within the file names of the association rule files.</p></td></tr>
<tr><td rowspan="4" valign="top"><b>produce_intermediate_imgs</b></td><td valign="top">Datatype</td><td valign="top">Boolean</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">False</td></tr>
<tr><td valign="top">Description</td><td valign="top">If set to True, intermediate images of the suffix forest (during its building process) will be generated in the output directory.</td></tr>
<tr><td rowspan="4" valign="top"><b>produce_final_img</b></td><td valign="top">Datatype</td><td valign="top">Boolean</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">False</td></tr>
<tr><td valign="top">Description</td><td valign="top">If set to True, the final image of the fully constructed suffix forest will be generated in the output directory.</td></tr>
<tr><td rowspan="4" valign="top"><b>custom_name_mapping</b></td><td valign="top">Datatype</td><td valign="top">Dictionary</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">None</td></tr>
<tr><td valign="top">Description</td><td valign="top">This dictionary can be used to add an extra layer of decoding process on the item number. The dictionary should hold key-value pairs where the keys are item names as given in the input CSV file and values are the ‘names’ that we want to show on output instead of the given item names.</td></tr>
<tr><td rowspan="4" valign="top"><b>dtype_key</b></td><td valign="top">Datatype</td><td valign="top">Type specifier</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">None</td></tr>
<tr><td valign="top">Description</td><td valign="top">Required only if custom_name _mapping is provide. Its value is the datatype of the keys in custom_name_mapping</td></tr>
</table>

**6. Results**

A directory named ‘output’ is created in the same directory as the input file’s directory. All the output files are stored in this directory.

These are the results:

  Here, x is the minimum support count (integer) and y is the minimum confidence value (float).

- Triclusters:
  - Encoded version is stored in these files:
    - < input file name>.triclusters.ms=x.encoded.csv
    - < input file name>.triclusters.ms=x.encoded.json
  - Decoded version is stored in the following file:
    - < input file name>.triclusters.ms=x.decoded.csv
- Association Rules:
  - Encoded version of exact association rules is stored in:
    - < input file name>.rule.E.ms=x.mc=y.encoded.csv
    - < input file name>.rule.E.ms=x.mc=y.encoded.json
  - Decoded version of exact association rules is stored in:
    - < input file name>.rule.E.ms=x.mc=y.decoded.csv
  - Encoded version of approximate association rules is stored in:
    - < input file name>.rule.SB.ms=x.mc=y.encoded.csv
    - < input file name>.rule.SB.ms=x.mc=y.encoded.json
  - Decoded version of approximate association rules is stored in:
    - < input file name>.rule.SB.ms=x.mc=y.decoded.csv
  - Encoded version of proper base approximate association rules is stored in:
    - < input file name>.rule.PB.ms=x.mc=y.encoded.csv
    - < input file name>.rule.PB.ms=x.mc=y.encoded.json
  - Decoded version of proper base approximate association rules is stored in:

    - < input file name>.rule.PB.ms=x.mc=y.decoded.csv

  - Generator Closure Pairs:
    - < input file name>.generators.ms=x.csv
  - Suffix Forest:
    - < input file name>.forest.ms=x.encoded.json
    - The intermediate and final image of the forest are also generated if produce\_final\_img and produce\_intermediate\_imgs flags are set. They are stored in files:
    - < input file name>.forest.final.png
    - < input file name>.forest.intermediate<step count>.png
  - Number Table:
    - The number table or the item name to item number mapping is also generated and stored in the file < input file name>.number\_table.ms=x.csv


**7. References:**

[1] Kartick Chandra Mondal, Moumita Ghosh, Rohmatul Fajriyah, Anirban Roy<a name="_hlk135867462"></a> (2022) **·** Introducing Suffix Forest for Mining Tri-clusters from Time Series Data [Link]

[2] <a name="_hlk135867581"></a>Kartick Chandra Mondal, Nicolas Pasquier, Anirban Mukhopadhyay, Ujjwal Maulik, and Sanghamitra Bandhopadyay <a name="_hlk135867504"></a>(2012<a name="_hlk135867594"></a>) **·** A New Approach for Association Rule Mining and Bi-clustering Using Formal Concept Analysis [[Link](https://link.springer.com/chapter/10.1007/978-3-642-31537-4_8)]

[3] Kartick Chandra Mondal (2016) **·** Algorithms for Data Mining and Bio-informatics [[Link](https://hal.science/tel-01330152/document)]

[4] Python Software Foundation  (2021). Python Language Reference, version 3.9.6. Retrieved from https://docs.python.org/3/reference/

