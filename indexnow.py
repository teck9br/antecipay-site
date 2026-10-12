"""Avisa o Bing (e os outros buscadores do IndexNow) sobre páginas novas ou alteradas.

Uso:
  python3 indexnow.py                 # envia todas as URLs do sitemap.xml
  python3 indexnow.py /blog/slug/ ... # envia só as páginas indicadas

A chave fica publicada em /<KEY>.txt, na raiz do site. Rode depois do deploy no Render,
para os buscadores encontrarem a página atualizada.
"""
import json, re, sys, urllib.error, urllib.request

SITE = "https://antecipayprecatorios.com.br"
HOST = "antecipayprecatorios.com.br"
KEY = "8082ba8677f2ebbf6a79e0da524d3676"

def urls_do_sitemap():
    xml = open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", xml)

def enviar(urls):
    """Envia a lista e devolve o código HTTP (200 = recebido; 202 = recebido, chave em validação)."""
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:200]!r}")
        return e.code

def para_url(arg):
    """Aceita URL completa, '/caminho/' ou 'caminho/'."""
    if re.match(r"^[A-Za-z]:/", arg):
        # O Git Bash troca '/blog/x/' por 'C:/Program Files/Git/blog/x/'.
        sys.exit(f"Caminho convertido pelo terminal: {arg}\nUse 'blog/x/' sem a barra inicial, ou MSYS_NO_PATHCONV=1, ou o PowerShell.")
    if arg.startswith("http"):
        return arg
    return SITE + "/" + arg.lstrip("/")

def main():
    urls = [para_url(a) for a in sys.argv[1:]] or urls_do_sitemap()
    status = enviar(urls)
    if status in (200, 202):
        print(f"IndexNow: HTTP {status} para {len(urls)} URLs")
        return
    # A API às vezes recusa o lote (422) e aceita as mesmas URLs uma a uma.
    print(f"Lote recusado (HTTP {status}); reenviando uma a uma:")
    falhas = [u for u in urls if enviar([u]) not in (200, 202)]
    print(f"IndexNow: {len(urls) - len(falhas)} de {len(urls)} URLs aceitas")
    if falhas:
        print("Recusadas:", *falhas, sep="\n  ")
        sys.exit(1)

if __name__ == "__main__":
    main()
