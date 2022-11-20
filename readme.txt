MiaLang Rules:
start--> `<mia>` <stmt> 
<stmt> --> <while_stmt>|<if_stmt>|<block>|<varOp>
<block> --> `{` <stmt> `;` `}`
<while_stmt> --> `whilst` <boolexpr> <block> [ `elsey` <block> ]
<if_stmt> --> `iffy` <boolexpr> <block>
<varOp> --> `id` (<declare>|<assign>)
<declar> --> `intOne`|`intTwo`|`intThree`|`intFour`
<assign> --> `=` <expr>
<expr> --> <term> {(`*`|`/`|`%`) <term>}
<term> --> <factor> {(`+`|`-`) <factor>}
<factor> --> `id`|`int_lit`|`(` <expr> `)`
<boolexpr> --> <boo>{`and` <boo>}
<boo> --> <equalityOp> {`or` <equalityOp>}
<equalityOp> --> <relationOp> {(`!=`|`==`) <relationOp>}
<relationOp> --> <booExpr> {(`<=`|`>=`|`<`|`<`) <booExpr>}
<booExpr> --> <booTerm> {(`*`|`/`|`%`) <booTerm>}
<booTerm> --> <booFactor> {(`+`|`-`) <booFactor>}
<booFactor>--> `id`|`int_lit`|`bool_lit`s

Allowed Characters:
if_stmt = iffy
while_stmt = whilst
else_stmt = elsey
math operations = +,-,*,/,%
bool expressions = <,>,<=.>=,!=,==
