# AST To Code

## Project

The repo aims to convert a JSON AST file into readable, usable code.
It may not work completely, so don't hesitate to open an issue.

You can use an online beautifier to get a cleaner code to read, such as [js-beautifier](https://beautifier.io/).

## Options

- `-f`, `--file`: AST JSON file. Required.
- `-o`, `--output`: File to write content to. Not required. By default, content is written to the stdout.

## Examples

### Python

```python
$ ast-parser.py -f ./examples/python.json    
__pythonRuntime.functions.print("Hello world");
var num1=1.5;
var num2=6.3;
var sum=__pythonRuntime.ops.add(num1,num2);
__pythonRuntime.functions.print("The sum of {0} and {1} is {2}".format(num1,num2,sum));
var num=8;
var num_sqrt=Math.pow(num,0.5);
__pythonRuntime.functions.print("The square root of %0.3f is %0.3f"%(num,num_sqrt));
```

### JavaScript

```js
$ ast-parser.py -f ./examples/javascript.json
const number=parseInt(prompt("Enter a positive number: "));
let isPrime=True;
if(number===1){console.log("1 is neither prime nor composite number.");}elseif(number>1){for (let i=2;;i<number;i++){if(number%i==0){isPrime=False;break}}if(isPrime){console.log(`${number} is a prime number`);}else{console.log(`${number} is a not prime number`);}}
```
