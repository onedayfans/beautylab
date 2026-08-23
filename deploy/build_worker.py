import re, pathlib

HTML = pathlib.Path(__file__).parent.parent.joinpath('beautylab.html').read_text(encoding='utf-8')

# escape for JS template literal
HTML = HTML.replace('\\', '\\\\')
HTML = HTML.replace('`', '\\`')
HTML = HTML.replace('${', '\\${')

JS = f"""export default {{
  async fetch(request, env, ctx) {{
    const html = `{HTML}`;
    return new Response(html, {{
      headers: {{ 'content-type': 'text/html;charset=UTF-8' }}
    }});
  }}
}};
"""

pathlib.Path(__file__).parent.joinpath('index.js').write_text(JS, encoding='utf-8')
print(f'index.js written ({len(JS):,} chars)')
