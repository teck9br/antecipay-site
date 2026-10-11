#!/usr/bin/env python3
"""Auditoria de SEO on-page reutilizável.

Uso:
  python3 seo_audit.py https://meusite.com.br          # site no ar (lê o sitemap.xml)
  python3 seo_audit.py ./pasta-do-site --base https://meusite.com.br   # arquivos HTML locais
Opções: --out relatorio.md  --max 300 (máx. de páginas)

Gera um relatório em Markdown com nota por página, problemas por prioridade
e checagens do site (robots.txt, sitemap, llms.txt, favicon, https).
Só usa a biblioteca padrão do Python.
"""
import argparse, html, json, os, re, sys, urllib.parse, urllib.request
from html.parser import HTMLParser
from collections import Counter, defaultdict

UA = "Mozilla/5.0 (SEO-Audit; +https://claude.ai)"

# ---------- leitura ----------
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", url
    except Exception as e:
        return 0, str(e), url

class Source:
    """Abstrai site no ar ou pasta local."""
    def __init__(self, target, base):
        self.local = os.path.isdir(target)
        self.root = target.rstrip("/")
        self.base = (base or (target if not self.local else "")).rstrip("/")
    def get(self, path):
        if not self.local:
            return fetch(self.base + path)
        p = path.split("?")[0].split("#")[0]
        f = os.path.join(self.root, p.lstrip("/"))
        if p.endswith("/") or p == "":
            f = os.path.join(f, "index.html")
        if os.path.isfile(f):
            return 200, open(f, encoding="utf-8", errors="replace").read(), self.base + path
        return 404, "", self.base + path
    def exists(self, path):
        return self.get(path)[0] == 200

# ---------- parser ----------
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self._in = None; self.meta = {}; self.links_rel = {}
        self.h = defaultdict(list); self.imgs = []; self.a = []; self.ld = []
        self.text = []; self.lang = ""; self._skip = 0; self._hbuf = None; self._ld = None
    def handle_starttag(self, t, attrs):
        a = dict(attrs)
        if t == "html": self.lang = a.get("lang", "")
        if t == "title": self._in = "title"
        if t == "meta":
            k = (a.get("name") or a.get("property") or "").lower()
            if k: self.meta[k] = a.get("content", "")
        if t == "link" and a.get("rel"):
            self.links_rel.setdefault(a["rel"].lower(), []).append(a.get("href", ""))
        if t in ("h1","h2","h3"): self._hbuf = (t, [])
        if t == "img": self.imgs.append(a)
        if t == "a" and a.get("href"): self.a.append(a["href"])
        if t == "script" and a.get("type") == "application/ld+json": self._ld = []
        elif t in ("script","style","noscript"): self._skip += 1
    def handle_endtag(self, t):
        if t == "title": self._in = None
        if t in ("h1","h2","h3") and self._hbuf and self._hbuf[0] == t:
            self.h[t].append(" ".join("".join(self._hbuf[1]).split())); self._hbuf = None
        if t == "script" and self._ld is not None:
            self.ld.append("".join(self._ld)); self._ld = None
        elif t in ("script","style","noscript") and self._skip: self._skip -= 1
    def handle_data(self, d):
        if self._ld is not None: self._ld.append(d); return
        if self._skip: return
        if self._in == "title": self.title += d
        if self._hbuf: self._hbuf[1].append(d)
        self.text.append(d)

def ld_types(blocks):
    types, errors = [], 0
    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t: types.extend(t if isinstance(t, list) else [t])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for b in blocks:
        try: walk(json.loads(b))
        except Exception: errors += 1
    return types, errors

# ---------- regras ----------
# (id, prioridade, descrição, como corrigir)
RULES = {
 "status":      ("Alta",  "Página não responde 200", "Corrigir o link ou recriar a página."),
 "noindex":     ("Alta",  "Página marcada como noindex", "Remover o meta robots noindex se a página deve aparecer no Google."),
 "title_miss":  ("Alta",  "Sem <title>", "Escrever um título com a palavra-chave principal."),
 "title_long":  ("Média", "Título com mais de 65 caracteres", "Encurtar para até ~60 caracteres para não ser cortado no Google."),
 "title_short": ("Baixa", "Título com menos de 25 caracteres", "Detalhar mais o título com a palavra-chave e a marca."),
 "title_dup":   ("Média", "Título repetido em outra página", "Cada página precisa de um título único."),
 "desc_miss":   ("Média", "Sem meta description", "Escrever um resumo de 120–160 caracteres com chamada para ação."),
 "desc_len":    ("Baixa", "Meta description fora de 70–165 caracteres", "Ajustar o tamanho para 120–160 caracteres."),
 "desc_dup":    ("Baixa", "Meta description repetida", "Escrever uma descrição única por página."),
 "h1_miss":     ("Alta",  "Sem H1", "Incluir um H1 com a palavra-chave principal."),
 "h1_multi":    ("Baixa", "Mais de um H1", "Manter só um H1 por página."),
 "canon_miss":  ("Média", "Sem link canonical", "Adicionar <link rel=canonical> apontando para a URL oficial."),
 "canon_off":   ("Média", "Canonical aponta para outra URL", "Conferir se é intencional; senão, apontar para a própria página."),
 "thin":        ("Alta",  "Conteúdo curto (menos de 300 palavras)", "Ampliar o texto com respostas às dúvidas reais do cliente."),
 "lang":        ("Baixa", "Sem atributo lang no <html>", "Usar <html lang=\"pt-BR\">."),
 "viewport":    ("Alta",  "Sem meta viewport (mobile)", "Adicionar <meta name=viewport content=\"width=device-width, initial-scale=1\">."),
 "og":          ("Baixa", "Sem Open Graph (og:title/og:image)", "Adicionar og:title, og:description e og:image para compartilhamento."),
 "schema_miss": ("Média", "Sem dados estruturados (JSON-LD)", "Adicionar schema (Organization/LocalBusiness, FAQPage, Article, Service)."),
 "schema_err":  ("Alta",  "JSON-LD com erro de sintaxe", "Validar em search.google.com/test/rich-results."),
 "img_alt":     ("Baixa", "Imagens sem texto alternativo (alt)", "Descrever cada imagem no atributo alt."),
 "few_links":   ("Média", "Poucos links internos (menos de 3)", "Linkar para páginas relacionadas do próprio site."),
 "broken":      ("Alta",  "Link interno quebrado", "Corrigir o endereço do link."),
 "orphan":      ("Média", "Página órfã (nenhum link interno aponta para ela)", "Linkar a página a partir da home, menu, rodapé ou artigos."),
}

def audit_page(src, path, html_text, status):
    p = Page(); p.feed(html_text)
    issues = []
    if status != 200: return {"path": path, "status": status, "issues": ["status"]}, p
    title = " ".join(html.unescape(p.title).split())
    desc = p.meta.get("description", "").strip()
    words = len(re.findall(r"\w+", " ".join(p.text)))
    canon = (p.links_rel.get("canonical") or [""])[0]
    types, ld_err = ld_types(p.ld)
    if "noindex" in p.meta.get("robots", "").lower(): issues.append("noindex")
    if not title: issues.append("title_miss")
    elif len(title) > 65: issues.append("title_long")
    elif len(title) < 25: issues.append("title_short")
    if not desc: issues.append("desc_miss")
    elif not 70 <= len(desc) <= 165: issues.append("desc_len")
    if not p.h["h1"]: issues.append("h1_miss")
    elif len(p.h["h1"]) > 1: issues.append("h1_multi")
    if not canon: issues.append("canon_miss")
    elif src.base and urllib.parse.urlparse(canon).path.rstrip("/") != path.split("?")[0].rstrip("/").replace("index.html", "").rstrip("/") and not canon.endswith(path):
        issues.append("canon_off")
    if words < 300: issues.append("thin")
    if not p.lang: issues.append("lang")
    if "viewport" not in p.meta: issues.append("viewport")
    if "og:title" not in p.meta or "og:image" not in p.meta: issues.append("og")
    if not p.ld: issues.append("schema_miss")
    if ld_err: issues.append("schema_err")
    if any(not (i.get("alt") or "").strip() for i in p.imgs): issues.append("img_alt")
    host = urllib.parse.urlparse(src.base).netloc
    internal = set()
    for h in p.a:
        u = urllib.parse.urlparse(urllib.parse.urljoin(src.base + path, h))
        if u.scheme in ("http","https") and (u.netloc == host or not host) and not h.startswith(("mailto:","tel:","#")):
            internal.add(u.path or "/")
    internal.discard(path)
    if len(internal) < 3: issues.append("few_links")
    return {"path": path, "status": status, "title": title, "desc": desc, "words": words,
            "h1": p.h["h1"][:1], "h2": len(p.h["h2"]), "schema": sorted(set(types)),
            "internal": sorted(internal), "issues": issues}, p

def score(issues):
    w = {"Alta": 15, "Média": 7, "Baixa": 3}
    return max(0, 100 - sum(w[RULES[i][0]] for i in issues))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--base", default="")
    ap.add_argument("--out", default="auditoria-seo.md"); ap.add_argument("--max", type=int, default=300)
    a = ap.parse_args()
    src = Source(a.target, a.base)
    site = {}
    for f in ("/robots.txt", "/sitemap.xml", "/llms.txt", "/favicon.ico"):
        site[f] = src.get(f)
    robots = site["/robots.txt"][1] if site["/robots.txt"][0] == 200 else ""
    sm = site["/sitemap.xml"][1] if site["/sitemap.xml"][0] == 200 else ""
    urls = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", sm)
    paths = [urllib.parse.urlparse(u).path or "/" for u in urls] or ["/"]
    if not src.base and urls:
        src.base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(urls[0]))
    paths = list(dict.fromkeys(paths))[: a.max]

    results, linked = [], Counter()
    for path in paths:
        st, body, _ = src.get(path)
        r, _ = audit_page(src, path, body, st)
        results.append(r)
        for l in r.get("internal", []): linked[l.rstrip("/") or "/"] += 1
    known = {p.rstrip("/") or "/" for p in paths}
    # links quebrados (internos para páginas fora do sitemap que não existem)
    checked = {}
    for r in results:
        bad = []
        for l in r.get("internal", []):
            if l.rstrip("/") in known or l in known: continue
            if re.search(r"\.(png|jpe?g|svg|webp|ico|css|js|pdf|txt|xml)$", l): continue
            if l not in checked: checked[l] = src.exists(l)
            if not checked[l]: bad.append(l)
        if bad: r["issues"].append("broken"); r["broken"] = bad
    for r in results:
        if r["path"] != "/" and linked[r["path"].rstrip("/") or "/"] == 0: r["issues"].append("orphan")
    dup_t = Counter(r.get("title") for r in results if r.get("title"))
    dup_d = Counter(r.get("desc") for r in results if r.get("desc"))
    for r in results:
        if r.get("title") and dup_t[r["title"]] > 1: r["issues"].append("title_dup")
        if r.get("desc") and dup_d[r["desc"]] > 1: r["issues"].append("desc_dup")
        r["score"] = score(r["issues"])

    # ---------- checagens do site ----------
    sitewide = [
        ("robots.txt existe", site["/robots.txt"][0] == 200),
        ("robots.txt aponta o sitemap", "sitemap" in robots.lower()),
        ("robots.txt não bloqueia o site inteiro", not re.search(r"(?im)^user-agent:\s*\*\s*\n(?:.*\n)*?disallow:\s*/\s*$", robots)),
        ("Robôs de IA liberados (GPTBot, ClaudeBot, PerplexityBot)", not re.search(r"(?is)user-agent:\s*(gptbot|claudebot|perplexitybot)[^\n]*\n\s*disallow:\s*/\s*$", robots)),
        ("sitemap.xml existe", bool(sm)),
        ("llms.txt existe (busca por IA)", site["/llms.txt"][0] == 200),
        ("favicon.ico existe", site["/favicon.ico"][0] == 200),
        ("Domínio em HTTPS", src.base.startswith("https")),
    ]
    schema_all = sorted({t for r in results for t in r.get("schema", [])})
    avg = round(sum(r["score"] for r in results) / max(1, len(results)))
    cnt = Counter(i for r in results for i in r["issues"])

    L = [f"# Auditoria de SEO — {src.base or a.target}", "",
         f"**Nota média on-page: {avg}/100** · {len(results)} páginas analisadas (do sitemap.xml)", "",
         "## 1. Checagens do site", "", "| Item | Status |", "|---|---|"]
    L += [f"| {n} | {'✅' if ok else '❌'} |" for n, ok in sitewide]
    L += ["", f"Tipos de schema encontrados: {', '.join(schema_all) or 'nenhum'}", "",
          "## 2. Problemas por prioridade", "", "| Prioridade | Problema | Páginas | Como corrigir |", "|---|---|---|---|"]
    order = {"Alta": 0, "Média": 1, "Baixa": 2}
    for k in sorted(cnt, key=lambda k: (order[RULES[k][0]], -cnt[k])):
        pr, d, fix = RULES[k]; L.append(f"| {pr} | {d} | {cnt[k]} | {fix} |")
    if not cnt: L.append("| — | Nenhum problema encontrado | 0 | — |")
    L += ["", "## 3. Páginas", "", "| Página | Nota | Palavras | Título (caract.) | Description | Schema | Problemas |", "|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: r["score"]):
        if r["status"] != 200:
            L.append(f"| {r['path']} | 0 | — | — | — | — | HTTP {r['status']} |"); continue
        probs = "; ".join(RULES[i][1] for i in r["issues"]) or "—"
        L.append(f"| {r['path']} | {r['score']} | {r['words']} | {len(r['title'])} | {len(r['desc'])} | {', '.join(r['schema']) or '—'} | {probs} |")
    broken = [(r['path'], b) for r in results for b in r.get("broken", [])]
    if broken:
        L += ["", "### Links internos quebrados", ""] + [f"- {p} → {b}" for p, b in broken]
    L += ["", "## 4. Fora do código (conferir manualmente)", "",
          "- [ ] Google Search Console: sitemap enviado, páginas indexadas, erros de cobertura",
          "- [ ] Bing Webmaster Tools: sitemap enviado (alimenta ChatGPT/Copilot)",
          "- [ ] Google Business Profile verificado, com categoria, horário, fotos e avaliações",
          "- [ ] Backlinks: diretórios, parceiros, imprensa, associações (autoridade do domínio)",
          "- [ ] Velocidade: PageSpeed Insights acima de 90 no celular",
          "- [ ] Analytics/Clarity instalado e medindo conversões (ex.: cliques no WhatsApp)",
          "- [ ] Palavras-chave: cada página mira um termo diferente, sem canibalização", ""]
    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    json.dump(results, open(os.path.splitext(a.out)[0] + ".json", "w"), ensure_ascii=False, indent=1)
    print(f"Nota média {avg}/100 · {len(results)} páginas · relatório: {a.out}")

if __name__ == "__main__":
    main()
