// Adversarial — XSS + eval injection sinks.
function advRender(userInput) {
  const node = document.createElement('div');
  node.innerHTML = userInput;
  eval('var x = ' + userInput);
  return Function('return ' + userInput)();
}