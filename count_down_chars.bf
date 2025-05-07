,                   Read one ASCII digit into cell0
> ++++++++++        Cell1 = 10   (store newline constant)
<                   Back to cell0
.                   Write out written digit
------------------------------------------------  Subtract 48 → numeric value 0-9
> .                 Write out a newline
<                   Move back to cell 0
[                   Loop while value ≠ 0
    ++++++++++++++++++++++++++++++++++++++++++++++++  Add 48 → ASCII digit
    .               Print the digit
    > .             Print newline from cell1
    <               Back to cell0
    ------------------------------------------------  Subtract 48 → numeric again
    -               Decrement the counter
]                   End loop when counter is 0

++++++++++++++++++++++++++++++++++++++++++++++++    Convert 0 → ASCII '0'
.                   Print the final zero
> .                 Print the final newline
