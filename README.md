# ctf-point-analysis
A simple python script that makes a graph and analyze the score of selected participant using normal distribution 

syntax:
python3 graph.py {year} {name/event id} {team id}
or 
python3 graph.py {year} {name/event id} "pos" {ranking of event}

example:

`python3 graph.py 2015 "RCTF 2015 Quals" pos 45 `

`python3 graph.py 2015 266 3329 ` 


![Screenshot (111)](https://user-images.githubusercontent.com/36957890/134520122-d2d2f6a5-0233-44de-a28a-0e2bb49f0067.png)


packages:

```
urllib.request
matplotlib
json
math
numpy
```
