/** FSOT code-genome sample — legacy XSS sinks (hole detection target). */
function fsotRenderHtml(target, html) {
  document.getElementById(target).innerHTML = html;
}

function fsotRunUserCode(src) {
  return eval(src);
}

function fsotDynamicFn(body) {
  return new Function("return " + body)();
}