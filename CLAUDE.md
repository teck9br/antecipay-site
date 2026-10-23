> **Responda sempre em português do Brasil.**

# Antecipay Precatórios — site

Site institucional de **antecipayprecatorios.com.br**: empresa de Natal-RN que compra e antecipa precatórios federais, estaduais e municipais de credores de todo o Brasil. Objetivo do site: gerar contatos pelo WhatsApp e ranquear para "vender precatório".

## Stack e deploy
- HTML/CSS/JS estático, sem framework. Fontes Montserrat + Inter hospedadas no próprio site (`assets/fonts/`, woff2 variável, subconjunto latino); não usar Google Fonts. As duas são pré-carregadas e têm fontes de reserva ("Inter Fallback"/"Montserrat Fallback", Arial com `size-adjust`) para o texto não pular na troca. O Render serve `/assets/fonts/*` com cache de 1 ano (`immutable`): se trocar um arquivo de fonte, **mude o nome do arquivo**.
- Hospedagem: **Render** (static site `srv-datsbgmk1f9s739g200g`), deploy automático a cada commit na branch `main` de `github.com/teck9br/antecipay-site`.
- DNS no Registro.br: `A @ 216.24.57.1` e `CNAME www → antecipay-site.onrender.com`.
- Domínio canônico: `https://antecipayprecatorios.com.br/` (sem www).

## Estrutura
- `index.html` — home (editada à mão; foco SEO "vender precatório"). Tem FAQ com JSON-LD gerado a partir dos `<details>`.
- `build_blog.py` — **gerador** de todas as outras páginas. Rode `python3 build_blog.py` depois de editar (no Windows: `PYTHONUTF8=1 python build_blog.py`, senão falha com UnicodeEncodeError). Gera:
  - `blog/` (índice + artigos da lista `POSTS`), `sobre/`
  - páginas de serviço: `vender-precatorio-inss/`, `-rn/`, `-federal/`, `-estadual/`, `-municipal/`, `empresa-que-compra-precatorio-natal/`, `melhor-empresa-para-vender-precatorio/`, `calculadora-precatorio/`, `antecipacao-de-precatorio/`
  - páginas por estado no modelo da de Natal (lista `ESTADOS` → `build_estados()`): `empresa-que-compra-precatorio-sao-paulo/`, `-paraiba/`, `-pernambuco/`, `-ceara/`. A empresa não tem escritório nesses estados: o texto diz "sede em Natal, atendimento 100% digital". Para um estado novo, acrescente um `dict` em `ESTADOS` com fatos próprios do estado (tribunais, devedores, como consultar), não texto copiado
  - `sitemap.xml` e `llms.txt`
  - Para novo artigo: adicione um `dict` em `POSTS`. Para nova página de serviço: use a função `landing(...)`, depois inclua no `build_sitemap`, no rodapé (`FOOT`) e no `llms.txt`.
- Autoria: os artigos são assinados pela advogada **Dra. Thayná Cabral** (`AUTORA` em `build_blog.py` → página `equipe/thayna-cabral/`, `author` Person no JSON-LD). Em 23/10/2026 foram preenchidos OAB (OAB/RN 21.175) e bio; a foto já estava. Ela tem escritório próprio, Thayná Cabral Advocacia (`thaynacabraladvocacia.com.br`, repositório `teck9br/thayna-cabral-site`): quando o domínio estiver no ar, acrescentar o site em `same_as` de `AUTORA` (vira link "Perfis" na página dela e `sameAs` no JSON-LD). Campos vazios não aparecem. Perfis da empresa ficam em `SAME_AS` (hoje só o Instagram @antecipayprecatorios); ao criar LinkedIn/Facebook/Google Meu Negócio, acrescente lá e no `sameAs` do JSON-LD do `index.html`.
- Visual (out/2026): cores originais (azul-marinho `--ink` #07111F, branco, verde) com camada de "liquid glass" no fim do CSS (bloco `liquid glass sobre as cores originais`, tokens `--gl-*`): menu em cápsula de vidro escuro, cartões de vidro escuro nas faixas escuras e de vidro branco nas claras (fundo `--mist` com brilhos verdes em `main::before`). Home com animações (bloco `movimento`): entrada do hero, traço lima desenhado sob "dinheiro na conta", palavras `.hl` que ficam verdes, revelação em cascata, linha das etapas e números de `.stat` contando. Faixa `.tribs` com os tribunais (TRFs, TJs, TRTs) rolando sob os números, no formato da Colina Tech (siglas soltas em cinza, sem cápsulas, título com destaque em verde `.circ`, sem círculo (o dono não gostou)); para incluir um tribunal, edite a lista `<ul class="track">` (as duas cópias). Logo em texto: `Antecipay<small>Precatórios</small>`. Não usar marca-texto lima de fundo nos títulos (o dono não gosta).
- `assets/blog.css` — estilos das páginas geradas (escala de espaçamento de 8 px). O gerador embute esse CSS no `<head>` de cada página; edite o arquivo e rode o build.
- `robots.txt` libera robôs de IA; `privacidade.html`; favicons e `og.png`.

## Dados da empresa (usar sempre iguais)
- Nome: **Antecipay Precatórios** (sempre com "Precatórios": existe outra "AnteciPay" da Ecx Pay)
- CNPJ 64.382.432/0001-97 · WhatsApp (84) 99493-8383 (`5584994938383`) · contato@antecipay.com.br
- Endereço: Av. Senador Salgado Filho, 1559 – Tirol, Incubadora do IFRN – Campus Natal Central, Natal-RN, CEP 59015-000
- Horário: seg–sex 8h–18h, sáb 8h–12h
- Pagamento em até 72 h após proposta aprovada e cessão assinada.
- Também compra **honorários advocatícios** (contratuais destacados e de sucumbência). Atua em todo o território nacional (sede em Natal, atendimento 100% digital).

## Regras de conteúdo
- Português do Brasil, linguagem simples, sem juridiquês.
- Fatos jurídicos usados: cessão permitida pelo art. 100 §13 CF (efeitos após comunicação, §14); EC 136/2025: data de corte 1º de fevereiro, estados/municípios pagam 1%–5% da RCL; RPV federal até 60 salários mínimos; superpreferência é pessoal e não passa ao cessionário.
- Não inventar números da empresa. As faixas da calculadora (`CALC_JS` em `build_blog.py`) são estimativas de mercado e precisam ser confirmadas pelo dono.
- Toda página nova: título ≤ 60 caracteres, description 120–160, um H1, canonical, JSON-LD (Service/FAQPage/Article), ≥ 3 links internos.
- Microsoft Clarity (`yqi1puom0k`) com evento `whatsapp_click` em todas as páginas.

## IndexNow (Bing, Yandex e outros)
Depois do deploy de páginas novas ou alteradas, rode `python3 indexnow.py blog/slug/ outra-pagina/` (sem argumentos, envia todo o sitemap). No Git Bash, escreva os caminhos **sem a barra inicial**: o terminal converte `/blog/...` em `C:/Program Files/Git/blog/...` e a API recusa com 422; para a home, use `""`. A chave está em `8082ba8677f2ebbf6a79e0da524d3676.txt`, na raiz; não apague esse arquivo.

## Auditoria de SEO
`python3 seo_audit.py . --base https://antecipayprecatorios.com.br --out auditoria.md` (script em `seo_audit.py`).

## Pendências (out/2026)
- Search Console (19/10/2026): a inspeção de URL confirma que as 35 URLs do sitemap estão no Google (o relatório Páginas ainda mostra 27 porque está atrasado). Propriedade é de prefixo de URL (`https://antecipayprecatorios.com.br/`), não de domínio. Em 19/10 o `/sitemap.xml` foi reenviado (processado, 35 páginas) e foram removidos 3 "sitemaps" que eram URLs de página. Em Sitemaps, envie só o `sitemap.xml`; para páginas, use a inspeção de URL. Em 21/10/2026 foi pedida a indexação das 4 páginas por estado (SP, PB, PE, CE), que entraram no ar nesse dia; conferir na inspeção de URL se já estão no Google. No mesmo dia, depois da revisão de títulos, foi pedida a reindexação de `blog/juntada-de-certidao/`, `blog/consultar-rpv-precatorio-trf3/`, `calculadora-precatorio/`, `sobre/` e a indexação de `equipe/thayna-cabral/` (nova). Medir o efeito dos títulos novos no relatório Desempenho a partir de meados de novembro/2026. Em 22/10/2026 a inspeção confirmou no Google as 4 páginas por estado, `equipe/thayna-cabral/` e `privacidade.html` (as 40 URLs antigas do sitemap estão indexadas); foi pedida a indexação de `blog/eleicoes-precatorios-rn-natal/` (nova) e a reindexação da home (faixa de tribunais), e o IndexNow recebeu as 41 URLs.
- Redirecionamento: `http://www` faz 2 saltos (http→https www→apex). Criar Redirect Rule na Cloudflare direto para a canônica e ativar HSTS; usar sempre a URL canônica em perfis e links externos.
- **E-mail quebrado:** `antecipay.com.br` tem Null MX (não recebe e-mail) e o domínio do site não tem MX. Criar `contato@antecipayprecatorios.com.br` e trocar em todo lugar (index.html, build_blog.py, llms.txt, este arquivo).
- **Receita Federal diverge do site:** razão social "Antecipay Soluções Financeiras e Tecnológicas Ltda", início 09/01/2026, endereço cadastral em Parnamirim-RN. O `/sobre/` ainda mostra "Razão social: Antecipay Precatórios". Dono decide: atualizar o endereço na Receita ou explicar Natal como escritório de atendimento.
- Verificar Google Meu Negócio; conseguir backlinks (ITNC/IFRN, diretórios, perfis sociais).
