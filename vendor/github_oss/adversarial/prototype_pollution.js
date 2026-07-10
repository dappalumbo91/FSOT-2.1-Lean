// Adversarial — prototype pollution pattern.
function advMerge(target, source) {
  for (const key in source) {
    target[key] = source[key];
  }
  Object.prototype.polluted = true;
  return target;
}