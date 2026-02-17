# Writeup Prompt
Help me come up with a codex prompt to help me write the following problems in my textbook verbatim as they appear in my textbook into my latex writeup: 

<!-- Enter homework problems here --->
2.20, 2.58, 2.61, 2.70, 2.71 (a)-(c), 3.2, 3.4, 3.25, 3.26 (a), 3.31 (a)-(d)

So I am doing this on vscode on my mac. My homework folder is at the path: 
<!-- HW# folder path --->
/Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Homework/HW4


My latex writeup for the homework is at the pathname: 
<!-- adlt_hw#.tex path --->
/Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Homework/HW4/adlt_hw4.tex


The pdf of the compiled latex writeup is the file at the path: 
<!-- adlt_hw#.pdf path --->
/Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Homework/HW4/adlt_hw4.pdf


My textbook is the pdf saved at the pathname: 
<!-- textbook path --->
/Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Books/Introduction To Probability - Anderson, Seppalainen, Valko.pdf


Make sure codex is familiar with the codebase and the organization of the files and folders before starting. I need the problems verbatim written as they appear in the exercise sections in the textbook into my latex writeup for reference. Please add packages to the latex writeup if necessary to make the problem appear as it is, but make sure to document it with a clear comment in the latex writeup. Please make sure to leave the space for any scratch work and the solutions when I write this up please like the example below:

```latex
% Here's an example problem and solution:
\problem[Sample space and probability]{1.4}
State the problem here (paste from PDF).

\begin{solution}

We model the experiment using a probability space
\[
(\OmegaSpace, \FField, P).
\]

\begin{scratch}
The sample space is
\[
\OmegaSpace = \{H,T\}^3,
\]
the set of all length–3 sequences of coin flips.  
The $\sigma$-field is the power set $\FField = 2^{\OmegaSpace}$.

Assuming the coin is fair, we assign equal probability to each outcome:
\[
P(\{\omega\}) = 2^{-3} \quad \text{for all } \omega \in \OmegaSpace.
\]
\end{scratch}

Let
\[
A = \{\omega \in \OmegaSpace : \text{exactly two heads occur}\}.
\]
There are $\binom{3}{2} = 3$ such outcomes, so $|A| = 3$ and
\[
|\OmegaSpace| = 2^3 = 8.
\]

Since all outcomes are equally likely,
\[
P(A) = \frac{|A|}{|\OmegaSpace|} = \frac{3}{8}.
\]

\finalanswer{P(A) = \frac{3}{8}}

\end{solution}
```


Lastly, make sure to give me the prompt in plain-text and in a code-block cell so I can easily copy it please.