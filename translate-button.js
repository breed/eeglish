(function() {
  var DICT_URL = 'https://inglish.us/dikshuneree.json';
  var dictionary = null;
  var isInglish = false;
  var saved = [];

  var TOKEN_RE = /<[^>]*>|[^<\s]+|\s+/g;
  var PUNCT_RE = /^([^\w]*)(\w.*\w|\w)([^\w]*)$/u;

  function applyCase(orig, trans) {
    if (orig === orig.toUpperCase() && orig !== orig.toLowerCase()) return trans.toUpperCase();
    if (orig[0] === orig[0].toUpperCase() && orig.slice(1) === orig.slice(1).toLowerCase())
      return trans.charAt(0).toUpperCase() + trans.slice(1);
    return trans;
  }

  function translate(text) {
    var tokens = text.match(TOKEN_RE);
    if (!tokens) return text;
    var parts = [];
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (/^\s+$/.test(t) || (t.charAt(0) === '<' && t.charAt(t.length - 1) === '>')) {
        parts.push(t);
        continue;
      }
      var m = t.match(PUNCT_RE);
      if (!m) { parts.push(t); continue; }
      var word = m[2];
      var lookup = word.toLowerCase();
      if (dictionary[lookup] !== undefined) {
        parts.push(m[1] + applyCase(word, dictionary[lookup]) + m[3]);
      } else {
        parts.push(t);
      }
    }
    return parts.join('');
  }

  function shouldSkip(node) {
    var skip = { CODE: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1, INPUT: 1, PRE: 1 };
    var el = node.parentElement;
    while (el) {
      if (skip[el.tagName]) return true;
      if (el.id === 'inglish-btn') return true;
      el = el.parentElement;
    }
    return false;
  }

  function toggle() {
    if (isInglish) {
      for (var i = 0; i < saved.length; i++) {
        saved[i].node.textContent = saved[i].original;
      }
      saved = [];
      btn.textContent = 'inglish';
      isInglish = false;
    } else {
      var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      var nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        if (!node.textContent.trim() || shouldSkip(node)) continue;
        var original = node.textContent;
        var translated = translate(original);
        if (translated !== original) {
          saved.push({ node: node, original: original });
          node.textContent = translated;
        }
      }
      btn.textContent = 'english';
      isInglish = true;
    }
  }

  // create button
  var btn = document.createElement('button');
  btn.id = 'inglish-btn';
  btn.textContent = 'inglish';
  btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:99999;'
    + 'padding:8px 16px;border:1px solid #ccc;border-radius:6px;'
    + 'background:#fff;color:#333;font:14px system-ui,sans-serif;'
    + 'cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);';
  document.body.appendChild(btn);

  btn.addEventListener('click', function() {
    if (!dictionary) {
      btn.textContent = '...';
      btn.disabled = true;
      fetch(DICT_URL)
        .then(function(r) { return r.json(); })
        .then(function(d) {
          dictionary = d;
          btn.disabled = false;
          toggle();
        })
        .catch(function() {
          btn.textContent = 'error';
          btn.disabled = false;
        });
    } else {
      toggle();
    }
  });
})();
