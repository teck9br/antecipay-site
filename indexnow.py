"""Avisa o Bing (e os outros buscadores do IndexNow) sobre páginas novas ou alteradas.

Uso:
  python3 indexnow.py                 # envia todas as URLs do sitemap.xml
  python3 indexnow.py /blog/slug/ ... # envia só as páginas indicadas

A chave fica publicada em /<KEY>.txt, na raiz do site. Rode depois do deploy no Render,
para os buscadores encontrarem a página atualizada.
"""
import json, re, sys, urllib.request

SITE = "https://antecipayprecatorios.com.br"
HOST = "antecipayprecatorios.com.br"
KEY = "8082ba8677f2ebbf6a79e0da524d3676"

def urls_do_sitemap():
    xml = open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", xml)

def main():
    urls = [SITE + u if u.startswith("/") else u for u in sys.argv[1:]] or urls_do_sitemap()
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        # 200 = recebido; 202 = recebido, chave ainda em validação
        print(f"IndexNow: HTTP {r.status} para {len(urls)} URLs")

if __name__ == "__main__":
    main()
