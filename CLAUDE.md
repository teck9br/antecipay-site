> **Responda sempre em português do Brasil.**

# Antecipay Precatórios — site

Site institucional de **antecipayprecatorios.com.br**: empresa de Natal-RN que compra e antecipa precatórios federais, estaduais e municipais de credores de todo o Brasil. Objetivo do site: gerar contatos pelo WhatsApp e ranquear para "vender precatório".

## Stack e deploy
- HTML/CSS/JS estático, sem framework. Fontes Montserrat + Inter hospedadas no próprio site (`assets/fonts/`, woff2 variável, subconjunto latino); não usar Google Fonts.
- Hospedagem: **Render** (static site `srv-datsbgmk1f9s739g200g`), deploy automático a cada commit na branch `main` de `github.com/teck9br/antecipay-site`.
- DNS no Registro.br: `A @ 216.24.57.1` e `CNAME www → antecipay-site.onrender.com`.
- Domínio canônico: `https://antecipayprecatorios.com.br/` (sem www).

## Estrutura
- `index.html` — home (editada à mão; foco SEO "vender precatório"). Tem FAQ com JSON-LD gerado a partir dos `<details>`.
- `build_blog.py` — **gerador** de todas as outras páginas. Rode `python3 build_blog.py` depois de editar. Gera:
  - `blog/` (índice + artigos da lista `POSTS`), `sobre/`
  - páginas de serviço: `vender-precatorio-inss/`, `-rn/`, `-federal/`, `-estadual/`, `-municipal/`, `empresa-que-compra-precatorio-natal/`, `melhor-empresa-para-vender-precatorio/`, `calculadora-precatorio/`, `antecipacao-de-precatorio/`
  - `sitemap.xml` e `llms.txt`
  - Para novo artigo: adicione um `dict` em `POSTS`. Para nova página de serviço: use a função `landing(...)`, depois inclua no `build_sitemap`, no rodapé (`FOOT`) e no `llms.txt`.
- `assets/blog.css` — estilos das páginas geradas (escala de espaçamento de 8 px). O gerador embute esse CSS no `<head>` de cada página; edite o arquivo e rode o build.
- `robots.txt` libera robôs de IA; `privacidade.html`; favicons e `og.png`.

## Dados da empresa (usar sempre iguais)
- Nome: **Antecipay Precatórios** (sempre com "Precatórios": existe outra "AnteciPay" da Ecx Pay)
- CNPJ 64.382.432/0001-97 · WhatsApp (84) 99493-8383 (`5584994938383`) · contato@antecipay.com.br
- Endereço: Av. Senador Salgado Filho, 1559 – Tirol, Incubadora do IFRN – Campus Natal Central, Natal-RN, CEP 59015-000
- Horário: seg–sex 8h–18h, sáb 8h–12h
- Pagamento em até 72 h após proposta aprovada e cessão assinada.

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
- Search Console (12/10/2026): 19 páginas indexadas; indexação solicitada para as 8 restantes (antecipação, trabalhista, vale a pena, golpe, herança, superpreferência, 2027 e artigo de Natal). Conferir em alguns dias em Indexação → Páginas. Cota diária esgotada em 12/10: pedir indexação de `/blog/consultar-rpv-precatorio-trf5/`, `/blog/expedicao-de-oficio-precatorio/`, `/blog/juntada-de-certidao/`, `/blog/consultar-rpv-precatorio-trf1/`, `/blog/consultar-rpv-precatorio-trf3/`, `/blog/consultar-precatorio-tjsp/` e `/blog/valor-incontroverso-precatorio/` em 13/10 (já estão no sitemap e no IndexNow).
- Redirecionamento: `http://www` faz 2 saltos (http→https www→apex). Criar Redirect Rule na Cloudflare direto para a canônica e ativar HSTS; usar sempre a URL canônica em perfis e links externos.
- **E-mail quebrado:** `antecipay.com.br` tem Null MX (não recebe e-mail) e o domínio do site não tem MX. Criar `contato@antecipayprecatorios.com.br` e trocar em todo lugar (index.html, build_blog.py, llms.txt, este arquivo).
- **Receita Federal diverge do site:** razão social "Antecipay Soluções Financeiras e Tecnológicas Ltda", início 09/01/2026, endereço cadastral em Parnamirim-RN. O `/sobre/` ainda mostra "Razão social: Antecipay Precatórios". Dono decide: atualizar o endereço na Receita ou explicar Natal como escritório de atendimento.
- Verificar Google Meu Negócio; conseguir backlinks (ITNC/IFRN, diretórios, perfis sociais).
