# The chunk that lost the company name

Fixed windows ignore headings.

In `data/acme/filings/q2_2023_excerpt.md` the sentence "The company's revenue grew by 3%" sits under a heading that names ACME and Q2 2023. A size-80, overlap-0 splitter often cuts the heading away.

The orphan sentence still embeds. The vector has no company token. A question that names ACME can miss, or an answer can say "3%" with no company.

S5 and S8 fix this with better cuts and a context prepend. First you have to print the orphan.
