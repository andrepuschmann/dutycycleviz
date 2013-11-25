dutycycleviz
============

This is a tool to visualize PU activity patterns generated through continuous 
probability distributions.
Specifically, it implements an algorithm proposed by Miguel Lopez-Benitez 
in his paper entitled "Time-Dimension Models of Spectrum Usage for 
the Analysis, Design, and Simulation of Cognitive Radio Networks" [0]
using a Generalized Pareto Distribution (GPD) that can be fed with 
specific parameters for different PU activity patterns 
from "very low" to "very high".

Other distribution like the Kumaraswamy or Beta distribution may
be used as well.

[0](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6410055)

![Example](/example.png "Example output created using the GPD parameter mentioned in the paper")
