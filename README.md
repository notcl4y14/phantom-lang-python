# phantom-lang

Yep, archived now. "Because I kind of felt that python is a little bit overwhelming"

Just a programming language in development.
The syntax is JS/TS-like.

```ts
let x: int = 10;
let y: float = 0.4;

log.writeln(x + y); // float: 10.4

let num: int = 4;
let str: string = "4";

log.writeln( (string) num + str ); // string: "44"
log.writeln( num + (int) str ); // int: 8
log.writeln( num + str ); // Error: Cannot do int + string
```
