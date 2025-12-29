# Grammar

```
program          = { statement }
statement        = block | line-comment | text-fragment
line-comment     = "--" , { character - EOL } , ( EOL | EOF )

block            = standard-block | shorthand-block
standard-block   = block-header , "{" , { statement } , "}"
shorthand-block  = block-header , ":" , text-node , ";"

block-header     = block-type-chain , [ block-label ]
block-label      = { group-label | anchor-label | link-label }
block-type-chain = block-type , { "." , block-type }
block-type       = identifier

group-label      = "@" , identifier
anchor-label     = "#" , identifier
link-label       = "$" , identifier

text-node        = [ "*" ] , string , [ "*" ]
string           = '"' , { string-character } , '"'
string-character = escape-sequence | ( character  - '"' - "\\" )
escape-sequence  = "\\" ( '"' | "\\" | "n" | "r" | "t" )
identifier       = letter , { letter | digit | "_" | "-" } ,
                   ( letter | digit | "_" )

letter           = ? any ASCII alphabetic character ?
digit            = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
character        = ? any character ?
EOL              = "\n" | "\r" | "\r\n"
EOF              = ? end of file ?
```
