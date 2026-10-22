"""Gera as páginas do blog da Antecipay (HTML estático).
Para adicionar um artigo: inclua um dict em POSTS e rode `python3 build_blog.py`."""
import json, os, urllib.parse, html

SITE = "https://antecipayprecatorios.com.br"
WA = "5584994938383"
UPDATED = "2026-10-21"
UPDATED_BR = "21 de outubro de 2026"

# Perfis oficiais da empresa (entram no "sameAs" do JSON-LD e no rodapé)
SAME_AS = ["https://www.instagram.com/antecipayprecatorios/"]

# Advogada que assina os artigos. Campos vazios não aparecem na página:
# preencha e rode o build.
AUTORA = dict(
    slug="thayna-cabral",
    nome="Thayná Cabral",
    tratamento="Dra.",
    cargo="Advogada",
    oab="",        # ex.: "OAB/RN 12.345"
    foto="/assets/equipe/thayna-cabral.webp",  # quadrada, 400 px
    bio="",        # 2 a 4 frases: formação, experiência, área de atuação
    same_as=[],    # perfis profissionais dela: LinkedIn, Instagram, JusBrasil...
)
AUTORA_URL = f"/equipe/{AUTORA['slug']}/"

def wa(msg):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8a9.8 9.8 0 01-5-1.37l-.36-.21-3.72.97.99-3.63-.23-.37A9.8 9.8 0 012.2 12 9.85 9.85 0 0112.05 2.2c2.63 0 5.1 1.03 6.96 2.89A9.78 9.78 0 0121.9 12a9.86 9.86 0 01-9.85 9.8zm8.38-18.18A11.76 11.76 0 0012.05.15C5.5.15.16 5.48.16 12.03c0 2.1.55 4.14 1.59 5.94L.06 24l6.17-1.62a11.87 11.87 0 005.81 1.48c6.55 0 11.89-5.33 11.89-11.88 0-3.18-1.24-6.16-3.49-8.4z"/></svg>'

TEL_ICON = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

# CSS das páginas geradas vai embutido no <head> (evita uma requisição que bloqueia a renderização)
BLOG_CSS = open("assets/blog.css", encoding="utf-8").read()

def head(title, desc, url, extra_ld="", current="blog"):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#07111F">
<script>document.documentElement.classList.add('js')</script>
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Antecipay">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
{BLOG_CSS}</style>
{extra_ld}
<!-- Microsoft Clarity -->
<script>
if(!/^(localhost|127[.]0[.]0[.]1)$/.test(location.hostname))(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","yqi1puom0k");
document.addEventListener("click",function(e){{var a=e.target.closest&&e.target.closest('a[href*="wa.me"]');if(a&&window.clarity){{clarity("event","whatsapp_click");}}}});
document.addEventListener("click",function(e){{var t=e.target.closest&&e.target.closest('a[href^="tel:"]');if(t&&window.clarity){{clarity("event","phone_click");}}}});
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top">
  <div class="wrap nav">
    <a href="/" class="logo" translate="no">Antecipay<small>Precatórios</small></a>
    <nav class="menu" aria-label="Principal">
      <a href="/#como-funciona">Como funciona</a>
      <a href="/#vantagens">Vantagens</a>
      <a href="/#duvidas">Dúvidas</a>
      <a href="/sobre/"{' aria-current="page"' if current=="sobre" else ""}>Sobre</a>
      <a href="/blog/"{' aria-current="page"' if current=="blog" else ""}>Blog</a>
    </nav>
    <a class="btn btn-wa" href="{wa('Olá! Vim pelo blog da Antecipay e tenho um precatório.')}" target="_blank" rel="noopener">{WA_ICON}<span>Falar no WhatsApp</span></a>
  </div>
</header>
"""

FOOT = f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div><a href="/" class="logo" translate="no">Antecipay<small>Precatórios</small></a><p style="margin-top:12px;max-width:340px">Sediada em Natal-RN, atendendo credores de todo o Brasil.</p></div>
      <ul><li><a href="/">Vender precatório</a></li><li><a href="/calculadora-precatorio/">Calculadora de precatório</a></li><li><a href="/antecipacao-de-precatorio/">Compra de precatório</a></li><li><a href="/vender-precatorio-federal/">Precatório federal</a></li><li><a href="/vender-precatorio-estadual/">Precatório estadual</a></li><li><a href="/vender-precatorio-municipal/">Precatório municipal</a></li><li><a href="/vender-precatorio-trabalhista/">Precatório trabalhista</a></li><li><a href="/melhor-empresa-para-vender-precatorio/">Como escolher a empresa</a></li><li><a href="/sobre/">Sobre a Antecipay</a></li><li><a href="/vender-precatorio-inss/">Precatório do INSS</a></li><li><a href="/vender-precatorio-rn/">Precatório no RN</a></li><li><a href="/empresa-que-compra-precatorio-natal/">Empresa de precatórios em Natal</a></li><li><a href="/empresa-que-compra-precatorio-sao-paulo/">Precatórios em São Paulo</a></li><li><a href="/empresa-que-compra-precatorio-paraiba/">Precatórios na Paraíba</a></li><li><a href="/empresa-que-compra-precatorio-pernambuco/">Precatórios em Pernambuco</a></li><li><a href="/empresa-que-compra-precatorio-ceara/">Precatórios no Ceará</a></li><li><a href="/blog/">Blog</a></li><li><a href="/privacidade.html">Política de Privacidade</a></li></ul>
      <ul><li><a href="{wa('Olá! Vim pelo site da Antecipay.')}" target="_blank" rel="noopener">WhatsApp (84) 99493-8383</a></li><li><a href="mailto:contato@antecipay.com.br">contato@antecipay.com.br</a></li><li><a href="https://www.instagram.com/antecipayprecatorios/" target="_blank" rel="noopener">Instagram @antecipayprecatorios</a></li><li>Av. Senador Salgado Filho, 1559 – Tirol, Natal-RN</li></ul>
    </div>
    <div class="legal"><span>© 2026 Antecipay Precatórios</span><span>CNPJ 64.382.432/0001-97</span></div>
  </div>
</footer>
<a class="fab" href="{wa('Olá! Vim pelo blog e tenho um precatório para antecipar.')}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp"><svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8a9.8 9.8 0 01-5-1.37l-.36-.21-3.72.97.99-3.63-.23-.37A9.8 9.8 0 012.2 12 9.85 9.85 0 0112.05 2.2c2.63 0 5.1 1.03 6.96 2.89A9.78 9.78 0 0121.9 12a9.86 9.86 0 01-9.85 9.8zm8.38-18.18A11.76 11.76 0 0012.05.15C5.5.15.16 5.48.16 12.03c0 2.1.55 4.14 1.59 5.94L.06 24l6.17-1.62a11.87 11.87 0 005.81 1.48c6.55 0 11.89-5.33 11.89-11.88 0-3.18-1.24-6.16-3.49-8.4z"/></svg></a>
<script>
(function(){{var f=document.querySelector('.fab'),t=document.querySelector('main > section');
if(!f)return;if(!t||!('IntersectionObserver' in window)){{f.classList.add('on');return;}}
new IntersectionObserver(function(es){{f.classList.toggle('on',!es[0].isIntersecting);}}).observe(t);}})();
</script>
</body>
</html>
"""

NOTE = '<p class="note">Conteúdo informativo, atualizado em ' + UPDATED_BR + '. As regras de pagamento de precatórios mudam com frequência e cada processo tem particularidades. Para uma análise do seu caso, fale com a nossa equipe.</p>'

def cta(title, text, msg):
    return f'<div class="cta"><h2>{title}</h2><p>{text}</p><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Falar no WhatsApp</a><a class="btn btn-tel" href="tel:+5584994938383">{TEL_ICON}Ligar (84) 99493-8383</a></div>'

POSTS = [
 dict(
  slug="o-que-e-precatorio-e-rpv",
  tag="Primeiros passos",
  title="O que é precatório e RPV? Entenda a diferença",
  seo="O que é precatório e RPV? Diferença e prazos | Antecipay",
  desc="Precatório e RPV são as formas de o governo pagar dívidas reconhecidas na Justiça. Veja a diferença, o limite de valor e quanto tempo cada um leva.",
  lead="Ganhou uma ação contra o governo e ouviu falar em precatório ou RPV? Veja, de forma simples, o que cada um significa e por que isso muda o tempo que você vai esperar.",
  answer="Precatório e RPV são ordens de pagamento que a Justiça envia ao governo depois que uma ação é ganha. A RPV (Requisição de Pequeno Valor) é para valores menores e é paga em cerca de 60 dias. O precatório é para valores maiores e entra na fila do orçamento, podendo levar mais de um ano.",
  faq=[
   ("O que é precatório?","É a ordem de pagamento que o juiz envia ao governo (União, Estado ou Município) para quitar uma dívida reconhecida em ação judicial definitiva, quando o valor passa do limite da RPV."),
   ("O que é RPV?","RPV é a Requisição de Pequeno Valor: a ordem de pagamento para dívidas menores. Na esfera federal, o limite é de 60 salários mínimos e o pagamento ocorre em até 60 dias."),
   ("Qual o limite da RPV em estados e municípios?","Cada estado e município define o seu limite por lei. Sem lei própria, a Constituição usa 40 salários mínimos para estados e 30 para municípios."),
  ],
  body="""
<h2>O que é precatório</h2>
<p>Quando alguém vence uma ação contra o poder público e não cabe mais recurso, o governo não paga na hora como faria uma empresa. O juiz emite uma ordem de pagamento que é enviada ao tribunal e incluída no orçamento do ente devedor. Essa ordem é o <strong>precatório</strong>.</p>
<p>Ele pode ser <strong>federal</strong> (contra a União, o INSS e outras autarquias federais), <strong>estadual</strong> (contra o Estado) ou <strong>municipal</strong> (contra a prefeitura).</p>
<h2>O que é RPV</h2>
<p>A <strong>RPV</strong>, Requisição de Pequeno Valor, é o mesmo tipo de ordem de pagamento, mas para valores menores. Por ser de pequeno valor, ela não entra na fila anual do orçamento e é paga bem mais rápido.</p>
<h2>Diferença entre precatório e RPV</h2>
<div class="table-wrap"><table>
<tr><th></th><th>RPV</th><th>Precatório</th></tr>
<tr><td><strong>Valor</strong></td><td>Até o limite de pequeno valor (60 salários mínimos na esfera federal)</td><td>Acima do limite da RPV</td></tr>
<tr><td><strong>Prazo</strong></td><td>Em geral, até 60 dias após a requisição</td><td>Entra no orçamento do ano seguinte ou do outro, conforme a data de inscrição</td></tr>
<tr><td><strong>Fila</strong></td><td>Não entra na fila anual</td><td>Segue a ordem cronológica, com prioridades legais</td></tr>
</table></div>
<h2>Qual é o limite da RPV?</h2>
<ul>
<li><strong>União (federal):</strong> até 60 salários mínimos.</li>
<li><strong>Estados:</strong> cada estado define por lei. Sem lei, o limite é de 40 salários mínimos.</li>
<li><strong>Municípios:</strong> cada município define por lei. Sem lei, o limite é de 30 salários mínimos.</li>
</ul>
<p>Quem tem um crédito pouco acima do limite pode, em alguns casos, <strong>renunciar ao valor que excede</strong> para receber como RPV, bem mais rápido. É uma decisão que precisa ser feita no processo e vale a pena fazer as contas antes. E, quando o governo contesta só parte do cálculo, a parte aceita pode ser paga antes: veja <a href="/blog/valor-incontroverso-precatorio/">valor incontroverso</a>.</p>
<h2>E se eu não quiser esperar?</h2>
<p>O precatório é um direito de crédito e pode ser <strong>vendido (cedido)</strong> a terceiros, como a Antecipay. Você recebe um valor à vista agora e quem compra passa a receber do governo no futuro. Veja como <a href="/">vender precatório</a> com segurança e entenda o desconto no artigo <a href="/blog/desagio-precatorio/">Deságio: por que recebo menos ao antecipar</a>. Se a sua ação foi contra o INSS, veja <a href="/blog/precatorio-inss/">como funciona o precatório do INSS</a>.</p>
""",
  cta=("Tem um precatório ou RPV?","Envie o número do processo e receba uma análise da nossa equipe.","Olá! Li o artigo sobre precatório e RPV e quero uma análise do meu processo."),
  related=["quanto-tempo-demora-precatorio","como-saber-se-tenho-precatorio","desagio-precatorio"],
 ),
 dict(
  slug="quanto-tempo-demora-precatorio",
  tag="Prazos",
  title="Quanto tempo demora para receber um precatório?",
  seo="Quanto tempo demora um precatório em 2026? | Antecipay",
  desc="Veja os prazos de pagamento do precatório federal, estadual e municipal, a nova data de corte de 1º de fevereiro e quem tem prioridade na fila.",
  lead="A resposta depende de quem deve (União, Estado ou Município) e da data em que o precatório foi inscrito. Veja como funciona a fila em 2026.",
  answer="Precatórios federais inscritos até 1º de fevereiro são pagos até o fim do ano seguinte. Se a inscrição passar dessa data, o pagamento vai para o ano posterior. Nos estados e municípios, o prazo depende de quanto cada ente reserva por ano para pagar a fila, e muitos levam vários anos.",
  faq=[
   ("Qual a data de corte do precatório?","Desde a Emenda Constitucional 136/2025, precatórios apresentados até 1º de fevereiro entram no orçamento do ano seguinte. Antes, a data era 2 de abril."),
   ("Quanto tempo demora o precatório federal?","Em geral, até o fim do ano seguinte à inscrição, se ela ocorrer até 1º de fevereiro. Na prática, o prazo total pode passar de um ano e meio."),
   ("Quem tem prioridade para receber precatório?","Pessoas com 60 anos ou mais, com doença grave ou com deficiência podem receber uma parte do crédito com prioridade, até um limite fixado em lei."),
  ],
  body="""
<h2>Precatório federal</h2>
<p>A União costuma pagar os precatórios em dia. A regra é a data de inscrição:</p>
<ul>
<li>Inscrito até <strong>1º de fevereiro</strong>: pago até o fim do ano seguinte.</li>
<li>Inscrito depois de 1º de fevereiro: pago até o fim do segundo ano seguinte.</li>
</ul>
<p>Essa data mudou com a <a href="/blog/precatorios-2027-ec-136/"><strong>Emenda Constitucional 136/2025</strong></a>. Até então, o corte era 2 de abril. Na prática, entre a inscrição e o dinheiro na conta podem se passar de cerca de 11 meses a quase 3 anos, conforme a data de inscrição. Veja também <a href="/vender-precatorio-federal/">precatório federal</a> e, para ações contra o INSS, <a href="/blog/precatorio-inss/">precatório do INSS</a>.</p>
<h2>Precatório estadual e municipal</h2>
<p>Aqui a espera costuma ser bem maior. Com a EC 136/2025, estados e municípios passaram a pagar os precatórios dentro de um <strong>limite anual de 1% a 5% da receita corrente líquida</strong>, conforme o tamanho da dívida de cada um. Quem deve muito paga uma parte por ano e a fila anda devagar.</p>
<p>Por isso, dois credores com o mesmo valor podem esperar tempos muito diferentes: tudo depende de <strong>qual estado ou município</strong> deve e da sua posição na fila.</p>
<h2>RPV: o caminho mais rápido</h2>
<p>Se o valor estiver dentro do limite de pequeno valor, o pagamento sai como RPV, em geral em até 60 dias depois de a requisição chegar ao tribunal, após a <a href="/blog/expedicao-de-oficio-precatorio/">expedição do ofício</a>. Veja os limites em <a href="/blog/o-que-e-precatorio-e-rpv/">O que é precatório e RPV</a>.</p>
<h2>Quem tem prioridade na fila</h2>
<p>A Constituição garante prioridade a credores com <strong>60 anos ou mais</strong>, com <strong>doença grave</strong> ou com <strong>deficiência</strong>. Eles podem receber antes uma parte do crédito, até um limite legal. O restante segue a fila normal. Entenda quem tem direito em <a href="/blog/superpreferencia-precatorio/">superpreferência no precatório</a>.</p>
<h2>O valor é corrigido enquanto espero?</h2>
<p>Sim. Pelas regras atuais, o valor é atualizado pelo IPCA, com juros simples de 2% ao ano. Se essa soma passar da Selic, vale a Selic, que funciona como teto. Se o governo contestou só parte da conta, dá para pedir antes o pagamento da parte aceita (<a href="/blog/valor-incontroverso-precatorio/">valor incontroverso</a>). Ainda assim, esperar anos significa adiar planos, e é por isso que muitos credores preferem <a href="/">vender o precatório</a> e receber à vista. Para estimar quanto receberia, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Não quer esperar a fila?","A Antecipay compra o seu precatório e você recebe à vista.","Olá! Li o artigo sobre prazos e quero antecipar meu precatório."),
  related=["como-saber-se-tenho-precatorio","desagio-precatorio","o-que-e-precatorio-e-rpv"],
 ),
 dict(
  slug="como-saber-se-tenho-precatorio",
  tag="Consulta",
  title="Como saber se tenho precatório a receber",
  seo="Tenho precatório? Como consultar pelo CPF | Antecipay",
  desc="Passo a passo para consultar precatório e RPV pelo CPF ou número do processo nos tribunais federais (TRF) e estaduais (TJ).",
  lead="Muita gente tem valores a receber do governo e não sabe. Veja como consultar o seu precatório ou RPV pelo CPF ou pelo número do processo.",
  answer="Você consulta no site do tribunal onde correu a ação: no TRF da sua região, se for contra a União ou o INSS, e no Tribunal de Justiça do seu estado, se for contra o Estado ou o Município. Em geral basta o CPF ou o número do processo.",
  faq=[
   ("Como consultar precatório pelo CPF?","Acesse o portal de precatórios do tribunal responsável (TRF ou TJ) e procure a consulta por CPF/CNPJ ou por número do processo."),
   ("Qual tribunal consultar para precatório do INSS?","Ações contra o INSS correm na Justiça Federal. A consulta é feita no TRF da sua região. No Rio Grande do Norte, é o TRF5."),
   ("Onde consulto precatório do Estado ou do Município?","No site do Tribunal de Justiça do seu estado, na área de precatórios."),
  ],
  body="""
<h2>1. Descubra quem é o devedor</h2>
<ul>
<li><strong>União, INSS, universidades e autarquias federais:</strong> a ação correu na Justiça Federal. A consulta é no <strong>Tribunal Regional Federal (TRF)</strong> da sua região.</li>
<li><strong>Estado ou Município:</strong> a ação correu na Justiça Estadual. A consulta é no <strong>Tribunal de Justiça (TJ)</strong> do seu estado.</li>
</ul>
<h2>2. Encontre o TRF da sua região</h2>
<div class="table-wrap"><table>
<tr><th>Tribunal</th><th>Estados</th></tr>
<tr><td><a href="/blog/consultar-rpv-precatorio-trf1/">TRF1</a></td><td>DF, GO, TO, MT, BA, PI, MA, PA, AM, AC, RR, RO, AP</td></tr>
<tr><td>TRF2</td><td>RJ, ES</td></tr>
<tr><td><a href="/blog/consultar-rpv-precatorio-trf3/">TRF3</a></td><td>SP, MS</td></tr>
<tr><td>TRF4</td><td>RS, PR, SC</td></tr>
<tr><td><a href="/blog/consultar-rpv-precatorio-trf5/">TRF5</a></td><td>PE, CE, AL, SE, RN, PB</td></tr>
<tr><td>TRF6</td><td>MG</td></tr>
</table></div>
<h2>3. Faça a consulta</h2>
<ol>
<li>Entre no site do tribunal e procure a área <strong>"Precatórios e RPV"</strong> ou <strong>"Consulta de requisições"</strong>.</li>
<li>Pesquise pelo seu <strong>CPF</strong> (ou CNPJ) ou pelo <strong>número do processo</strong>.</li>
<li>Anote o número do precatório, o valor, o ano do orçamento e a situação (por exemplo, "inscrito", "pago" ou "aguardando pagamento").</li>
</ol>
<p>No Rio Grande do Norte, por exemplo, precatórios federais são consultados no portal do <strong>TRF5</strong> (veja <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>), e os estaduais e municipais no <strong>TJRN</strong>. Em São Paulo, veja <a href="/blog/consultar-precatorio-tjsp/">como consultar precatório no TJSP</a>.</p>
<h2>4. Não encontrou nada?</h2>
<p>A ação pode ainda não ter chegado à fase de pagamento, ou o precatório pode ter sido expedido com outros dados. Nesse caso, fale com o advogado que cuidou da ação ou envie o número do processo para a nossa equipe, que fazemos a análise. Se o andamento mostra termos como <a href="/blog/expedicao-de-oficio-precatorio/">expedição de ofício</a> ou <a href="/blog/juntada-de-certidao/">juntada de certidão</a>, veja o que cada um significa.</p>
<h2>Achei meu precatório. E agora?</h2>
<p>Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo ele deve levar para ser pago</a>. Se não quiser esperar, você pode <a href="/">vender o precatório</a>: a Antecipay compra e você recebe à vista. Se o seu é do INSS, veja <a href="/blog/precatorio-inss/">quando o INSS paga o precatório</a>.</p>
""",
  cta=("Quer ajuda para consultar?","Mande o número do processo ou o seu CPF e a nossa equipe verifica para você.","Olá! Li o artigo sobre consulta e quero ajuda para saber se tenho precatório."),
  related=["o-que-e-precatorio-e-rpv","quanto-tempo-demora-precatorio","desagio-precatorio"],
 ),
 dict(
  slug="desagio-precatorio",
  tag="Antecipação",
  title="Deságio: por que recebo menos ao antecipar o precatório?",
  seo="Deságio de precatório: o que é e como avaliar | Antecipay",
  desc="Entenda o que é deságio na venda de precatório, o que influencia o valor da proposta e o que conferir antes de assinar a cessão.",
  lead="Ao vender o seu precatório, você recebe menos que o valor de face. Essa diferença é o deságio. Entenda de onde ele vem e como avaliar uma proposta.",
  answer="Deságio é o desconto entre o valor do precatório e o valor pago à vista na antecipação. Ele existe porque quem compra paga agora e só recebe do governo no futuro, assumindo o tempo de espera e os riscos. O percentual varia conforme o devedor, o prazo previsto e a situação do processo.",
  faq=[
   ("O que é deságio de precatório?","É a diferença entre o valor do precatório e o valor pago à vista a quem vende. Ele remunera o tempo de espera e os riscos assumidos por quem compra."),
   ("Vender precatório é legal?","Sim. A Constituição (art. 100, §13) permite ceder o precatório a terceiros. A venda é feita por contrato de cessão de crédito, comunicado ao tribunal."),
   ("Do que depende o deságio?","Principalmente de quem deve (União, Estado ou Município), do prazo esperado para pagamento, do valor e de pendências no processo."),
  ],
  body="""
<h2>Por que existe o deságio</h2>
<p>Na <a href="/antecipacao-de-precatorio/">antecipação de precatório</a>, a empresa que compra o precatório <strong>paga agora</strong> e só vai <strong>receber do governo depois</strong>, às vezes anos depois. Durante esse tempo, o dinheiro dela fica parado e ela assume riscos, como atrasos no pagamento e mudanças nas regras. O deságio é o que remunera essa espera e esses riscos.</p>
<h2>O que influencia o valor da proposta</h2>
<ul>
<li><strong>Quem deve:</strong> precatórios federais costumam ter prazo mais previsível. Estados e municípios com muita dívida pagam mais devagar.</li>
<li><strong>Prazo esperado:</strong> quanto mais perto do pagamento, menor tende a ser o deságio.</li>
<li><strong>Situação do processo:</strong> pendências, discussões sobre o valor ou falta de documentos aumentam o risco.</li>
<li><strong>Descontos no crédito:</strong> honorários contratuais, imposto de renda e contribuições podem ser descontados do valor final.</li>
</ul>
<h2>Vale a pena antecipar?</h2>
<p>Depende da sua necessidade. Se você pode esperar, receber o valor cheio do governo pode compensar. Se precisa do dinheiro agora, para quitar dívidas com juros altos, investir ou realizar um plano, antecipar pode fazer mais sentido. O ideal é comparar a proposta com o tempo que você ainda esperaria. Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora cada tipo de precatório</a> e os critérios em <a href="/blog/vale-a-pena-vender-precatorio/">quando vale a pena vender precatório</a>.</p>
<h2>O que conferir antes de assinar</h2>
<ol>
<li><strong>Valor líquido:</strong> quanto cai na sua conta, já com todos os descontos.</li>
<li><strong>Prazo de pagamento</strong> depois da assinatura.</li>
<li><strong>Contrato de cessão</strong> claro, com a identificação do precatório e das partes.</li>
<li><strong>Comunicação ao tribunal</strong>, que é o que formaliza a troca de credor.</li>
<li><strong>Empresa séria:</strong> CNPJ ativo, endereço e canais de contato verdadeiros.</li>
</ol>
<p>Na Antecipay, a proposta é apresentada por escrito, com o valor líquido, antes de qualquer assinatura. Para uma estimativa rápida, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>; para entender o contrato, veja <a href="/blog/cessao-de-precatorio/">cessão de precatório</a>. Se decidir seguir, veja <a href="/blog/como-vender-precatorio/">como vender precatório passo a passo</a> ou <a href="/">venda o seu precatório</a> com a Antecipay.</p>
""",
  cta=("Quer saber quanto vale o seu precatório?","Receba uma proposta clara, com o valor líquido, antes de decidir.","Olá! Li o artigo sobre deságio e quero uma proposta para o meu precatório."),
  related=["quanto-tempo-demora-precatorio","o-que-e-precatorio-e-rpv","como-saber-se-tenho-precatorio"],
 ),
]

BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="precatorio-inss",
  tag="INSS",
  title="Precatório do INSS: como funciona e quanto tempo demora",
  seo="Precatório do INSS: prazo e como receber | Antecipay",
  desc="Ganhou ação contra o INSS? Entenda quando o pagamento sai por RPV ou precatório, os prazos, a prioridade para idosos e doentes graves e o imposto de renda.",
  lead="Aposentadoria, auxílio, BPC ou revisão: quem ganha uma ação contra o INSS recebe os atrasados por RPV ou por precatório. Veja como funciona cada caminho e quanto tempo leva.",
  answer="Os atrasados de uma ação contra o INSS são pagos pela Justiça Federal. Até 60 salários mínimos, o pagamento sai por RPV, em cerca de 60 dias. Acima disso, vira precatório federal: se for inscrito até 1º de fevereiro, é pago até o fim do ano seguinte. Idosos, pessoas com doença grave e pessoas com deficiência podem receber uma parte antes.",
  faq=[
   ("Quanto tempo demora o precatório do INSS?","Se o precatório for inscrito até 1º de fevereiro, o pagamento sai até o fim do ano seguinte. Inscrito depois dessa data, vai para o orçamento do ano posterior."),
   ("Qual o valor máximo da RPV do INSS?","60 salários mínimos. Acima disso, o crédito é pago por precatório, a não ser que o credor renuncie ao valor excedente para receber como RPV."),
   ("Precatório do INSS tem prioridade?","Sim. Por ser de natureza alimentar, tem preferência sobre os demais. Credores com 60 anos ou mais, doença grave ou deficiência podem receber antes uma parte de até 180 salários mínimos."),
   ("Tem imposto de renda no precatório do INSS?","Em geral, sim, calculado pelo regime de rendimentos recebidos acumuladamente, que distribui o valor pelos meses de atraso e costuma reduzir o imposto. Aposentados com doença grave prevista em lei podem ser isentos."),
  ],
  body="""
<h2>Quem paga os atrasados do INSS</h2>
<p>O INSS é uma autarquia federal. Por isso, as ações contra ele correm na <strong>Justiça Federal</strong>, e quem paga os atrasados é a União, por meio do Tribunal Regional Federal (TRF) da sua região. No Rio Grande do Norte, é o <strong>TRF5</strong>.</p>
<h2>RPV ou precatório?</h2>
<p>Depende do valor total dos atrasados na data da requisição:</p>
<div class="table-wrap"><table>
<tr><th></th><th>RPV</th><th>Precatório</th></tr>
<tr><td><strong>Valor</strong></td><td>Até 60 salários mínimos</td><td>Acima de 60 salários mínimos</td></tr>
<tr><td><strong>Prazo</strong></td><td>Cerca de 60 dias após a requisição</td><td>Até o fim do ano seguinte, se inscrito até 1º de fevereiro</td></tr>
</table></div>
<p>Quem tem um crédito pouco acima de 60 salários mínimos pode <strong>renunciar ao excedente</strong> para receber como RPV, bem mais rápido. Vale fazer as contas com o advogado antes de decidir.</p>
<h2>Quanto tempo demora o precatório do INSS</h2>
<p>A União costuma pagar os precatórios em dia, e a regra é a data de inscrição:</p>
<ul>
<li>Inscrito até <strong>1º de fevereiro</strong>: pago até o fim do ano seguinte.</li>
<li>Inscrito depois: pago até o fim do segundo ano seguinte.</li>
</ul>
<p>Na prática, entre a inscrição e o dinheiro na conta podem se passar de cerca de 11 meses a quase 3 anos, conforme a data de inscrição. Veja mais em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora para receber um precatório</a>.</p>
<h2>Prioridade para idosos, doentes graves e pessoas com deficiência</h2>
<p>Os atrasados de benefício do INSS são de <strong>natureza alimentar</strong> e têm preferência na fila. Além disso, credores com <strong>60 anos ou mais</strong>, com <strong>doença grave</strong> ou com <strong>deficiência</strong> podem receber antes uma parte do crédito, até o triplo do limite da RPV (180 salários mínimos). O restante segue a fila normal.</p>
<p><strong>Atenção:</strong> essa prioridade é pessoal. Se o precatório for vendido, quem compra não aproveita a preferência. Por isso, quem tem direito a ela deve avaliar com calma se vale antecipar todo o crédito ou só a parte que ainda ficaria na fila.</p>
<h2>Tem imposto de renda?</h2>
<p>Em geral, sim. Os atrasados previdenciários são tributados pelo regime de <strong>rendimentos recebidos acumuladamente (RRA)</strong>, que divide o valor pelos meses de atraso e costuma resultar em imposto menor. Aposentados com doença grave prevista em lei podem ser isentos, e os juros de mora sobre verbas alimentares não são tributados.</p>
<h2>Como consultar o seu precatório do INSS</h2>
<p>Entre no portal do TRF da sua região e pesquise pelo CPF ou pelo número do processo. O passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>. No Nordeste, veja <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar no TRF5</a>; também há guias para o <a href="/blog/consultar-rpv-precatorio-trf1/">TRF1</a> e o <a href="/blog/consultar-rpv-precatorio-trf3/">TRF3</a>.</p>
<h2>Não quer esperar?</h2>
<p>O precatório do INSS pode ser vendido, como qualquer precatório (entenda <a href="/blog/o-que-e-precatorio-e-rpv/">o que é precatório e RPV</a>). Você recebe um valor à vista agora e quem compra passa a receber da União no futuro. Veja <a href="/vender-precatorio-inss/">como funciona a venda do precatório do INSS na Antecipay</a> e, para os demais casos, como <a href="/">vender precatório</a>.</p>
""",
  cta=("Tem precatório do INSS?","Envie o número do processo e receba uma proposta por escrito.","Olá! Li o artigo sobre precatório do INSS e quero uma proposta."),
  related=["quanto-tempo-demora-precatorio","como-saber-se-tenho-precatorio","desagio-precatorio"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="como-vender-precatorio",
  tag="Vender precatório",
  title="Documentos e passo a passo para vender precatório com segurança",
  seo="Documentos para vender precatório: passo a passo | Antecipay",
  desc="Quais documentos são pedidos para vender precatório, quem pode vender, como a proposta é calculada e os cuidados para não cair em golpe na cessão.",
  lead="Já decidiu vender e quer saber o que separar? Veja os documentos, as etapas da cessão e o que conferir para fazer tudo com segurança.",
  answer="Para vender precatório, separe documento de identidade e CPF, o número do processo e os dados bancários. Com isso, a empresa compradora analisa o processo e apresenta uma proposta por escrito com o valor líquido. Se você aceitar, assina um contrato de cessão de crédito, que é comunicado ao tribunal, e recebe à vista. A venda é permitida pela Constituição (art. 100, §13).",
  faq=[
   ("Quem pode vender precatório?","O titular do crédito, seja pessoa física ou empresa. Herdeiros também podem vender, depois de regularizada a sucessão no processo."),
   ("Preciso de advogado para vender precatório?","Não é obrigatório, mas é recomendado avisar o advogado que cuidou da ação, porque os honorários contratuais dele costumam ser descontados do crédito."),
   ("Onde vender precatório com segurança?","Com uma empresa que tenha CNPJ ativo, endereço e contatos verdadeiros, que apresente a proposta por escrito e formalize a cessão no tribunal. Desconfie de quem pede pagamento antecipado."),
   ("Quanto tempo leva para vender precatório?","Depende da análise do processo. Na Antecipay, depois da proposta aprovada e da cessão assinada, o pagamento é feito em até 72 horas."),
  ],
  body="""
<p>Este guia mostra os documentos e as etapas da venda. Para pedir uma proposta agora, veja como <a href="/">vender precatório</a> com a Antecipay.</p>

<h2>Documentos normalmente pedidos</h2>
<ul>
<li>Documento de identidade e CPF (ou CNPJ, se for empresa).</li>
<li>Número do processo e, se tiver, o ofício requisitório.</li>
<li>Comprovante de endereço e dados bancários para o pagamento.</li>
<li>Em caso de herança, documentos da sucessão.</li>
</ul>

<h2>Quem pode vender precatório</h2>
<p>Pode vender quem é o <strong>titular do crédito</strong>: a pessoa física ou empresa que ganhou a ação. Se o titular faleceu, os <strong>herdeiros</strong> podem vender depois de regularizar a sucessão no processo (veja <a href="/blog/precatorio-de-heranca/">precatório de herança</a>). Precatórios federais, do INSS, estaduais, municipais e trabalhistas podem ser vendidos.</p>

<h2>Passo a passo para vender precatório</h2>
<ol>
<li><strong>Reúna o número do processo.</strong> Se não souber, veja <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>.</li>
<li><strong>Peça uma proposta.</strong> A empresa analisa o processo, o valor, os descontos e o prazo previsto de pagamento.</li>
<li><strong>Compare a proposta</strong> com o tempo que você ainda esperaria. Entenda o desconto em <a href="/blog/desagio-precatorio/">deságio de precatório</a>.</li>
<li><strong>Assine o contrato de cessão de crédito</strong>, que identifica o precatório, as partes e o valor pago.</li>
<li><strong>Receba à vista.</strong> A cessão é comunicada ao tribunal e quem comprou passa a receber do governo no futuro.</li>
</ol>

<h2>Como é calculada a proposta</h2>
<p>O valor oferecido leva em conta quem deve (União, Estado ou Município), o prazo previsto para o governo pagar, o valor do crédito e os descontos que incidem sobre ele, como honorários contratuais e imposto de renda. Quanto mais longa e incerta a espera, maior tende a ser o desconto.</p>

<h2>Cuidados para não cair em golpe</h2>
<ul>
<li><strong>Nunca pague nada antecipado</strong> para "liberar" a venda ou o precatório.</li>
<li>Confira o <strong>CNPJ</strong>, o endereço e os canais de contato da empresa.</li>
<li>Exija a <strong>proposta por escrito</strong>, com o valor líquido.</li>
<li>Leia o <strong>contrato de cessão</strong> antes de assinar e confirme que ele será comunicado ao tribunal.</li>
<li>Desconfie de contatos não solicitados dizendo que você tem valores a receber.</li>
</ul>
<p>Veja os truques mais comuns em <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>.</p>

<h2>Quando vale a pena vender</h2>
<p>Vender faz sentido para quem precisa do dinheiro agora, quer quitar dívidas com juros altos ou não quer esperar a fila do governo. Quem pode esperar recebe o valor cheio no futuro. Credores com 60 anos ou mais, doença grave ou deficiência devem considerar que a prioridade de pagamento deles é pessoal e não passa para quem compra. Os critérios estão em <a href="/blog/vale-a-pena-vender-precatorio/">quando vale a pena vender precatório</a>. Quando decidir, peça uma proposta para <a href="/">vender precatório</a> com a Antecipay.</p>
<p>Para precatórios do INSS, veja a página <a href="/vender-precatorio-inss/">vender precatório do INSS</a>. Para o Rio Grande do Norte, veja <a href="/vender-precatorio-rn/">vender precatório no RN</a>. Para estimar o valor, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>; para entender o contrato, leia <a href="/blog/cessao-de-precatorio/">cessão de precatório</a>; e, antes de assinar, veja <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa</a>.</p>
""",
  cta=("Quer vender seu precatório?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Quero vender meu precatório. Podem me enviar uma proposta?"),
  related=["desagio-precatorio","quanto-tempo-demora-precatorio","precatorio-inss"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="empresas-que-compram-precatorios-natal",
  tag="Natal-RN",
  title="Como escolher empresa de precatório em Natal: checklist e golpes",
  seo="Como escolher empresa de precatório em Natal | Antecipay",
  desc="Vai vender precatório em Natal? Veja o checklist para escolher a empresa, os sinais de golpe e como comparar com o acordo direto da Prefeitura.",
  lead="Quem tem um precatório a receber em Natal costuma receber propostas de vários compradores. Veja como comparar e escolher com quem negociar com segurança.",
  answer="Para escolher uma empresa que compra precatórios em Natal, confira se ela tem CNPJ ativo e endereço real, se apresenta a proposta por escrito com o valor líquido, se formaliza a cessão de crédito no tribunal e se não cobra nada antecipado. Compare também o prazo de pagamento e a clareza do contrato.",
  faq=[
   ("Como saber se uma empresa de precatório é confiável?","Confira se o CNPJ está ativo na Receita Federal, peça a proposta por escrito com o valor líquido, leia o contrato de cessão e desconfie de qualquer cobrança antecipada. Ter endereço real em Natal, como a Antecipay na Incubadora do IFRN, também facilita a conferência."),
   ("A Prefeitura de Natal faz acordo para pagar precatório?","A Prefeitura de Natal mantém um portal de precatórios com edital de credenciamento para acordos diretos com credores, mediante deságio. Vale comparar essa opção com as propostas de empresas compradoras."),
   ("Vender para uma empresa de Natal é melhor?","Ter sede na cidade facilita o contato e a conferência de que a empresa existe. O mais importante, porém, é a transparência da proposta e do contrato."),
  ],
  body="""
<h2>Quem faz propostas de compra em Natal</h2>
<p>Credores de Natal costumam receber propostas de três tipos de compradores:</p>
<ul>
<li><strong>Empresas especializadas</strong> em compra de precatórios, nacionais ou com sede no RN.</li>
<li><strong>Bancos e fundos de investimento</strong> que atuam nesse mercado.</li>
<li><strong>O próprio ente devedor</strong>, por meio de acordo direto. A Prefeitura de Natal, por exemplo, mantém um portal de precatórios com edital de credenciamento para acordos com deságio.</li>
</ul>
<p>Cada opção tem prazo, desconto e burocracia diferentes. Antes de <a href="/">vender precatório</a>, vale pedir mais de uma proposta e comparar. Os critérios estão em <a href="/melhor-empresa-para-vender-precatorio/">qual a melhor empresa para vender precatório</a>, e as regras do estado em <a href="/vender-precatorio-rn/">vender precatório no RN</a>.</p>

<h2>Checklist para escolher a empresa</h2>
<ol>
<li><strong>CNPJ ativo e endereço real.</strong> Confira na Receita Federal e, se possível, se a empresa tem sede em Natal ou no RN.</li>
<li><strong>Proposta por escrito</strong>, com o valor líquido que você vai receber, depois de honorários e impostos.</li>
<li><strong>Contrato de cessão de crédito claro</strong>, identificando o precatório, as partes e a forma de pagamento.</li>
<li><strong>Cessão comunicada ao tribunal</strong> (TRF5, para precatórios federais, ou TJRN, para estaduais e municipais).</li>
<li><strong>Prazo de pagamento definido</strong> depois da assinatura.</li>
<li><strong>Nenhuma cobrança antecipada.</strong> Empresa séria não pede taxa para "liberar" a venda.</li>
<li><strong>Atendimento acessível</strong>, com telefone, WhatsApp e e-mail que respondem.</li>
</ol>

<h2>Sinais de alerta</h2>
<ul>
<li>Pedido de depósito ou taxa antes da venda.</li>
<li>Pressa excessiva para assinar sem ler o contrato.</li>
<li>Proposta só por telefone, sem nada por escrito.</li>
<li>Contato não solicitado dizendo que você tem valores a receber, sem saber o número do processo.</li>
</ul>

<h2>Precatórios mais comuns em Natal</h2>
<div class="table-wrap"><table>
<tr><th>Devedor</th><th>Tribunal</th><th>Exemplos</th></tr>
<tr><td>União e INSS</td><td>TRF5</td><td>Aposentadorias, benefícios, servidores federais</td></tr>
<tr><td>Estado do RN</td><td>TJRN</td><td>Servidores estaduais, indenizações</td></tr>
<tr><td>Prefeitura de Natal</td><td>TJRN</td><td>Servidores municipais, desapropriações</td></tr>
</table></div>

<h2>A Antecipay é de Natal</h2>
<p>A Antecipay Precatórios tem sede em Natal, na Incubadora do IFRN – Campus Natal Central (Av. Senador Salgado Filho, 1559 – Tirol), e compra precatórios de credores de todo o Brasil. A proposta é apresentada por escrito, com o valor líquido, e o atendimento é 100% digital pelo WhatsApp. Saiba mais em <a href="/empresa-que-compra-precatorio-natal/">empresa que compra precatório em Natal</a> e <a href="/blog/como-vender-precatorio/">como vender precatório com segurança</a>.</p>
""",
  cta=("Tem precatório em Natal?","Envie o número do processo e compare com uma proposta por escrito da Antecipay.","Olá! Sou de Natal e quero uma proposta para o meu precatório."),
  related=["como-vender-precatorio","desagio-precatorio","precatorio-inss"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="cessao-de-precatorio",
  tag="Venda",
  title="Cessão de precatório: como funciona e o que conferir no contrato",
  seo="Cessão de precatório: como funciona o contrato | Antecipay",
  desc="Entenda o que é a cessão de precatório, o que a Constituição exige, como o contrato é comunicado ao tribunal e o que conferir antes de assinar.",
  lead="Cessão é o nome jurídico da venda do precatório. Veja como ela funciona, o que muda depois da assinatura e os pontos que você deve conferir no contrato.",
  answer="A cessão de precatório é o contrato pelo qual o credor transfere a outra pessoa ou empresa o direito de receber o precatório, em troca de um pagamento à vista. Ela é permitida pelo art. 100, §13, da Constituição, não depende da concordância do governo e passa a valer depois de comunicada ao tribunal e ao ente devedor.",
  faq=[
   ("A cessão de precatório é legal?","Sim. O art. 100, §13, da Constituição Federal permite que o credor ceda o precatório, total ou parcialmente, a terceiros, sem precisar da concordância do devedor."),
   ("Preciso de escritura pública para ceder o precatório?","Depende do tribunal. Alguns aceitam contrato particular com firma reconhecida; outros pedem escritura pública. A empresa compradora deve orientar e, em geral, arcar com esses custos."),
   ("O comprador fica com a minha prioridade de idoso ou doente?","Não. A Constituição diz que o cessionário não recebe a preferência por idade, doença ou deficiência. Por isso essa parte costuma ser tratada à parte na negociação."),
   ("Posso ceder só uma parte do precatório?","Sim. A cessão pode ser parcial. Isso é útil, por exemplo, para manter a parcela prioritária e vender apenas o saldo."),
  ],
  body="""
<h2>O que é cessão de precatório</h2>
<p><strong>Cessão de crédito</strong> é o contrato em que alguém transfere a outra pessoa o direito de receber um valor. Na cessão de precatório, o credor (chamado <strong>cedente</strong>) transfere o direito de receber o precatório a quem compra (o <strong>cessionário</strong>), que paga um valor à vista. Depois disso, quem recebe do governo é o cessionário.</p>
<h2>O que diz a Constituição</h2>
<ul>
<li><strong>Art. 100, §13:</strong> o credor pode ceder o precatório, no todo ou em parte, sem precisar da concordância do devedor. O cessionário não fica com a preferência por idade, doença grave ou deficiência, nem com a regra da RPV.</li>
<li><strong>Art. 100, §14:</strong> a cessão só produz efeitos depois de comunicada, por petição, ao tribunal de origem e ao ente devedor.</li>
</ul>
<h2>Passo a passo da cessão</h2>
<ol>
<li><strong>Análise do precatório:</strong> a empresa confere o processo, o valor, os descontos e a situação na fila.</li>
<li><strong>Proposta por escrito</strong>, com o valor líquido que você recebe.</li>
<li><strong>Assinatura do contrato</strong> de cessão, por instrumento particular ou escritura pública, conforme o tribunal.</li>
<li><strong>Pagamento</strong> ao credor, à vista.</li>
<li><strong>Comunicação ao tribunal</strong> e ao ente devedor, para que o pagamento futuro seja feito ao cessionário.</li>
</ol>
<h2>O que conferir no contrato</h2>
<div class="table-wrap"><table>
<tr><th>Cláusula</th><th>O que verificar</th></tr>
<tr><td>Valor e forma de pagamento</td><td>Valor líquido, à vista e com data definida</td></tr>
<tr><td>Parte cedida</td><td>Se é o precatório inteiro ou só uma parte</td></tr>
<tr><td>Custos</td><td>Quem paga cartório, certidões e taxas</td></tr>
<tr><td>Honorários do advogado</td><td>Como ficam os honorários contratuais de quem cuidou da ação</td></tr>
<tr><td>Impostos</td><td>Como ficam o imposto de renda e a contribuição previdenciária retidos no pagamento</td></tr>
</table></div>
<p>Nunca pague taxa para “liberar” a cessão ou o pagamento. Veja os sinais de golpe em <a href="/blog/como-vender-precatorio/">como vender precatório com segurança</a>.</p>
<h2>Imposto de renda na cessão</h2>
<p>O tratamento tributário depende do tipo de crédito e da diferença entre o valor recebido e o valor do precatório. Converse com o seu contador para declarar a operação corretamente no ano seguinte.</p>
<h2>E o deságio?</h2>
<p>Na cessão, você recebe menos que o valor cheio porque antecipa um dinheiro que só viria no futuro. Entenda em <a href="/blog/desagio-precatorio/">deságio de precatório</a> e faça uma estimativa na <a href="/calculadora-precatorio/">calculadora</a>. Quando estiver pronto, veja como <a href="/">vender precatório</a> de forma segura.</p>
""",
  cta=("Quer ceder o seu precatório?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Li o artigo sobre cessão de precatório e quero uma proposta."),
  related=["como-vender-precatorio","desagio-precatorio","empresas-que-compram-precatorios-natal"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="golpe-do-precatorio",
  tag="Segurança",
  title="Golpe do precatório: como identificar e se proteger",
  seo="Golpe do precatório: como identificar e evitar | Antecipay",
  desc="Golpe do precatório: veja os truques mais comuns, como falsos advogados que pedem taxa para liberar o pagamento, e o que fazer para não perder dinheiro.",
  lead="Recebeu uma mensagem dizendo que o seu precatório foi liberado e que basta pagar uma taxa? Desconfie. Veja como o golpe funciona e como se proteger.",
  answer="O golpe do precatório quase sempre termina num pedido de dinheiro: alguém se passa por advogado, servidor do tribunal ou empresa e cobra uma taxa, custas ou imposto para “liberar” o pagamento ou a venda. Os tribunais não cobram taxa por mensagem para liberar precatório, e empresa séria que compra precatório paga você, nunca o contrário. Na dúvida, confirme com o seu advogado e no portal do tribunal.",
  faq=[
   ("O tribunal manda mensagem cobrando taxa para liberar precatório?","Não. Desconfie de qualquer cobrança por mensagem ou telefone. Confirme sempre com o seu advogado e no portal do tribunal."),
   ("Preciso pagar alguma coisa para vender o meu precatório?","Não deveria. Na venda legítima, quem paga é a empresa compradora. Na Antecipay, a simulação e a proposta são gratuitas."),
   ("Como saber se o meu precatório foi mesmo liberado?","Consulte no portal do tribunal pelo CPF ou pelo número do processo, ou pergunte ao advogado que cuidou da ação."),
  ],
  body="""
<h2>Como o golpe costuma acontecer</h2>
<ul>
<li><strong>Mensagem com dados reais do processo.</strong> Os golpistas usam o seu nome, o número do processo e até o valor. Esses dados costumam ser públicos, então não provam nada.</li>
<li><strong>Falso advogado ou escritório.</strong> Diz que o valor foi liberado e pede um Pix para “custas”, “imposto” ou “alvará”.</li>
<li><strong>Falso servidor do tribunal</strong>, com documento de aparência oficial e prazo curto para pagar.</li>
<li><strong>Falsa empresa compradora</strong>, que promete um valor alto e pede taxa de cadastro, análise ou registro antes de pagar.</li>
<li><strong>Proposta sem nada por escrito</strong>, só por telefone ou áudio.</li>
</ul>

<h2>Sinais de alerta</h2>
<ul>
<li>Pedido de qualquer pagamento antes de você receber.</li>
<li>Pressa: “a liberação vence hoje”.</li>
<li>Contato que você não pediu, de número desconhecido.</li>
<li>Número de WhatsApp diferente do número do seu advogado.</li>
<li>Link para “acompanhar a liberação” ou pedido de senha e código do banco.</li>
<li>Documento com erros, logotipo estranho ou dados bancários em nome de pessoa física.</li>
</ul>

<h2>Como conferir se é verdade</h2>
<ol>
<li><strong>Ligue para o seu advogado</strong> no telefone que você já conhece, não no número que mandou a mensagem.</li>
<li><strong>Consulte o precatório</strong> no portal do tribunal, pelo CPF ou pelo número do processo. Veja <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>.</li>
<li><strong>Se for uma empresa compradora</strong>, confira se o CNPJ está ativo na Receita Federal, se ela tem endereço real, se a proposta vem por escrito com o valor líquido e se o contrato é de cessão de crédito.</li>
</ol>

<h2>Como é uma venda segura</h2>
<p>Na venda legítima, a empresa analisa o processo, apresenta a proposta por escrito, assina com você um <a href="/blog/cessao-de-precatorio/">contrato de cessão de crédito</a> e <strong>paga você</strong>. Depois, a cessão é comunicada ao tribunal, como exige o art. 100, §14, da Constituição. Na Antecipay, a simulação e a proposta são gratuitas e o pagamento sai em até 72 horas depois da cessão assinada.</p>
<p>Veja o passo a passo em <a href="/blog/como-vender-precatorio/">como vender precatório</a>, os critérios em <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa</a> e como <a href="/">vender precatório</a> com segurança.</p>

<h2>Caí no golpe. E agora?</h2>
<ol>
<li><strong>Avise o seu banco na hora</strong> e peça a devolução pelo Mecanismo Especial de Devolução do Pix (MED). Quanto antes, maior a chance de recuperar.</li>
<li><strong>Registre um boletim de ocorrência.</strong> Em muitos estados dá para fazer pela internet.</li>
<li><strong>Avise o seu advogado</strong> e, se o golpista usou o nome do tribunal, informe o próprio tribunal.</li>
<li><strong>Guarde tudo:</strong> prints das conversas, comprovantes e números de telefone.</li>
</ol>
""",
  cta=("Quer vender com segurança?","Envie o número do processo e receba uma proposta por escrito, sem pagar nada antecipado.","Olá! Li o artigo sobre golpe do precatório e quero uma proposta segura."),
  related=["como-vender-precatorio","cessao-de-precatorio","como-saber-se-tenho-precatorio"],
))

POSTS.insert(0, dict(
  slug="vale-a-pena-vender-precatorio",
  tag="Decisão",
  title="Vale a pena vender precatório? Como decidir sem errar",
  seo="Vale a pena vender precatório? Como decidir | Antecipay",
  desc="Vale a pena vender precatório? Veja quando antecipar faz sentido, quando é melhor esperar a fila do governo e como comparar a proposta antes de decidir.",
  lead="Recebeu uma proposta pelo seu precatório e não sabe se aceita? Veja os critérios que ajudam a decidir entre vender agora ou esperar o pagamento do governo.",
  answer="Vale a pena vender quando o dinheiro agora vale mais para você do que o valor cheio no futuro: para quitar dívidas caras, resolver uma urgência ou não depender de uma fila que pode levar anos. Se você pode esperar e o devedor paga em dia, esperar tende a render mais. Compare sempre o valor líquido da proposta com o tempo que ainda falta para receber.",
  faq=[
   ("Vender precatório é melhor que pegar empréstimo?","São coisas diferentes. No empréstimo você fica devendo e paga juros; na venda, você recebe à vista e não fica com dívida. Se a ideia é antecipar um dinheiro que já é seu, a venda costuma ser mais simples."),
   ("Vale a pena vender precatório do INSS?","Depende do prazo. O INSS é federal e a União costuma pagar em dia, então o desconto tende a ser menor. Compare a proposta com o tempo que ainda falta para o pagamento."),
   ("Posso vender só uma parte do precatório?","Sim. A cessão pode ser parcial, o que ajuda quem quer manter a parcela prioritária por idade, doença grave ou deficiência."),
  ],
  body="""
<h2>O que você ganha e do que abre mão</h2>
<p>Ao vender, você <strong>ganha</strong> o dinheiro à vista (na Antecipay, em até 72 horas depois da cessão assinada) e deixa de depender do prazo e dos atrasos do governo.</p>
<p>Em troca, você <strong>abre mão</strong> de duas coisas: a diferença entre o valor do precatório e o valor da proposta, chamada <a href="/blog/desagio-precatorio/">deságio</a>, e a correção que o precatório teria até ser pago. Pelas regras atuais, essa correção é o IPCA mais juros simples de 2% ao ano, limitada à Selic.</p>

<h2>Quando costuma valer a pena vender</h2>
<ul>
<li><strong>Você tem dívidas com juros altos.</strong> Os juros do cartão de crédito e do cheque especial costumam ser bem maiores que a correção do precatório. Quitar essas dívidas agora pode compensar o desconto.</li>
<li><strong>A fila do seu devedor é longa.</strong> Estados e prefeituras pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, e alguns acumulam anos de atraso. Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</li>
<li><strong>Você tem uma necessidade concreta agora</strong>, como saúde, moradia ou um negócio, e esperar teria um custo maior que o desconto.</li>
</ul>

<h2>Quando pode ser melhor esperar</h2>
<ul>
<li><strong>O pagamento está perto.</strong> No precatório federal, entre a inscrição e o pagamento passam de cerca de 11 meses a quase 3 anos. Se o seu já está no orçamento do próximo ano, a espera pode ser curta.</li>
<li><strong>O seu crédito é uma RPV.</strong> Valores federais de até 60 salários mínimos são pagos como RPV, em poucos meses. Em geral não compensa vender.</li>
<li><strong>Você tem prioridade por idade, doença grave ou deficiência.</strong> A <a href="/blog/superpreferencia-precatorio/">parcela prioritária</a> é paga antes e não passa para quem compra. Muitas vezes vale manter essa parte e vender só o restante.</li>
</ul>

<h2>Como comparar a proposta, passo a passo</h2>
<ol>
<li><strong>Descubra o valor líquido</strong> que você receberia do governo, depois de honorários do advogado, imposto de renda e contribuição previdenciária.</li>
<li><strong>Estime quando seria pago.</strong> Consulte o precatório no portal do tribunal; o passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>.</li>
<li><strong>Compare com o valor líquido da proposta</strong>, que deve vir por escrito.</li>
<li><strong>Pense no uso do dinheiro.</strong> Se ele vai quitar uma dívida cara, o ganho de quitar agora entra na conta.</li>
<li><strong>Peça mais de uma proposta</strong> e compare o valor líquido e o prazo de pagamento, não só a porcentagem anunciada.</li>
</ol>
<p>Para uma primeira referência, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>

<h2>Cuidados antes de decidir</h2>
<p>Nunca pague taxa para “liberar” a venda ou o pagamento: empresa séria paga você, não o contrário. Veja os sinais em <a href="/blog/golpe-do-precatorio/">golpe do precatório</a> e os critérios em <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa</a>. Se decidir vender, veja como funciona a <a href="/antecipacao-de-precatorio/">antecipação de precatório</a> e como <a href="/">vender precatório</a> com a Antecipay. Para precatórios do INSS, veja <a href="/vender-precatorio-inss/">vender precatório do INSS</a>.</p>
""",
  cta=("Quer comparar com uma proposta real?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Li o artigo sobre se vale a pena vender precatório e quero uma proposta para comparar."),
  related=["desagio-precatorio","quanto-tempo-demora-precatorio","golpe-do-precatorio"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="precatorio-de-heranca",
  tag="Herança",
  title="Precatório de herança: como receber ou vender",
  seo="Precatório de herança: como receber ou vender | Antecipay",
  desc="Herdou um precatório? Veja como os herdeiros recebem pela habilitação no processo ou pelo inventário, quais documentos juntar e como vender a sua parte.",
  lead="O titular do precatório faleceu antes de receber? O crédito passa para os herdeiros. Veja o caminho para regularizar a situação e as opções para receber ou vender.",
  answer="Quando o titular morre antes do pagamento, o precatório faz parte da herança e passa para os herdeiros. Para receber, eles precisam se habilitar no processo ou fazer o inventário, judicial ou em cartório. Depois de regularizada a sucessão, cada herdeiro pode esperar o pagamento ou vender a sua parte do precatório.",
  faq=[
   ("Os herdeiros perdem o precatório se demorarem para se habilitar?","O direito não se perde com o falecimento, mas o valor só é liberado para quem estiver habilitado no processo. Quanto antes a sucessão for regularizada, menor o risco de atraso no recebimento."),
   ("Cada herdeiro pode vender só a sua parte?","Sim. Depois de definida a parte de cada um, quem quiser pode vender a sua parte e os demais podem esperar o pagamento."),
   ("Precisa fazer inventário para receber o precatório?","Depende. Alguns juízes aceitam a habilitação dos herdeiros direto no processo; outros exigem o inventário. O advogado da família indica o caminho para o seu caso."),
  ],
  body="""
<h2>O precatório entra na herança</h2>
<p>O precatório é um direito de crédito e, como qualquer bem, passa para os herdeiros quando o titular morre. O direito não se perde, mas o tribunal só libera o pagamento para quem comprovar que é sucessor. Por isso, o primeiro passo é regularizar a sucessão no processo.</p>

<h2>Dois caminhos: habilitação ou inventário</h2>
<div class="table-wrap"><table>
<tr><th>Caminho</th><th>Como funciona</th></tr>
<tr><td><strong>Habilitação no processo</strong></td><td>Os herdeiros pedem, no próprio processo, para ocupar o lugar do titular (arts. 687 a 692 do Código de Processo Civil). Alguns juízes aceitam sem inventário, desde que a condição de herdeiro esteja comprovada.</td></tr>
<tr><td><strong>Inventário</strong></td><td>Feito na Justiça ou em cartório, partilha todos os bens, inclusive o precatório. Ao final, sai o formal de partilha ou a escritura, que indica a parte de cada herdeiro.</td></tr>
</table></div>

<h2>Documentos que costumam ser pedidos</h2>
<ul>
<li>Certidão de óbito do titular.</li>
<li>Documentos pessoais dos herdeiros (RG e CPF).</li>
<li>Certidão de casamento ou de união estável, quando houver.</li>
<li>Procuração para o advogado.</li>
<li>Formal de partilha, escritura ou alvará judicial, conforme o caso.</li>
</ul>

<h2>Posso vender o precatório herdado?</h2>
<p>Sim. Os herdeiros que não quiserem esperar a fila podem vender. Se o inventário ainda está na Justiça, a venda costuma depender de autorização do juiz (alvará). Depois da partilha, cada herdeiro pode vender a sua parte, sem que os outros precisem vender também.</p>
<p>A venda é feita por <a href="/blog/cessao-de-precatorio/">contrato de cessão de crédito</a>, comunicado ao tribunal. Veja o passo a passo em <a href="/blog/como-vender-precatorio/">como vender precatório</a> e como <a href="/">vender precatório</a> com a Antecipay.</p>

<h2>Impostos e descontos</h2>
<p>Além dos descontos normais do precatório, como honorários do advogado e imposto de renda, pode incidir o ITCMD, imposto estadual sobre herança. Confira com o advogado do inventário como ficam os impostos no seu caso.</p>

<h2>Cuidados</h2>
<p>Golpistas costumam procurar herdeiros dizendo que há valores a liberar mediante pagamento de taxa. Desconfie e veja os sinais em <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>. Para conferir a situação do crédito, veja <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>.</p>
""",
  cta=("Herdou um precatório?","Envie o número do processo e receba uma proposta por escrito para a sua parte.","Olá! Herdei um precatório e quero uma proposta para a minha parte."),
  related=["cessao-de-precatorio","como-vender-precatorio","golpe-do-precatorio"],
))

POSTS.insert(0, dict(
  slug="superpreferencia-precatorio",
  tag="Prioridade",
  title="Superpreferência no precatório: quem tem direito e como pedir",
  seo="Superpreferência no precatório: quem tem direito | Antecipay",
  desc="Superpreferência no precatório: veja quem tem direito (60 anos ou mais, doença grave ou deficiência), qual é o limite e o que acontece se você vender.",
  lead="Credores idosos, com doença grave ou com deficiência podem receber antes uma parte do precatório. Veja quem tem direito, qual é o limite e como pedir.",
  answer="Superpreferência é o direito de receber antes, fora da ordem normal da fila, uma parte do precatório de natureza alimentar. Têm direito credores com 60 anos ou mais, com doença grave ou com deficiência. O limite é o triplo do valor da RPV (no federal, 180 salários mínimos); o restante segue a fila. A preferência é pessoal e não passa para quem compra o precatório.",
  faq=[
   ("A superpreferência vale para qualquer precatório?","Não. Vale só para precatórios de natureza alimentar, como salários, aposentadorias, pensões e benefícios previdenciários."),
   ("Doença descoberta depois do início do processo conta?","Sim. A doença grave pode ter surgido depois do início do processo. O pedido é feito no próprio precatório, com laudo médico."),
   ("Posso vender só a parte que fica na fila?","Sim. A venda pode ser parcial: você mantém a parcela superpreferencial, que recebe antes, e vende só o saldo."),
  ],
  body="""
<h2>Quem tem direito</h2>
<p>A superpreferência está no art. 100, §2º, da Constituição. Ela vale para precatórios de <strong>natureza alimentar</strong>, como salários, vencimentos, aposentadorias, pensões, benefícios previdenciários e indenizações por morte ou invalidez, cujo titular:</p>
<ul>
<li>tem <strong>60 anos ou mais</strong>;</li>
<li>tem <strong>doença grave</strong>; ou</li>
<li>é <strong>pessoa com deficiência</strong>.</li>
</ul>

<h2>Qual é o limite</h2>
<p>A parte paga antes vai até o <strong>triplo do valor da RPV</strong> do devedor. No federal, a RPV vai até 60 salários mínimos, então a superpreferência chega a 180 salários mínimos. Estados e municípios têm limites de RPV próprios, por isso o teto muda conforme o devedor. O que passar do limite continua na fila normal.</p>
<p>Pelo entendimento do STF (Tema 1.156), essa parcela é paga por precatório, e não por RPV, salvo quando o valor estiver dentro do limite de pequeno valor.</p>

<h2>Como pedir</h2>
<ul>
<li><strong>Idade:</strong> costuma ser reconhecida pelo próprio tribunal, com base na data de nascimento do credor.</li>
<li><strong>Doença grave ou deficiência:</strong> precisa de pedido no processo, com laudo médico. Em geral, quem faz o pedido é o advogado que cuida da ação.</li>
</ul>

<h2>E se eu vender o precatório?</h2>
<p>A superpreferência é <strong>pessoal</strong>. Pela Constituição (art. 100, §13), quem compra o precatório não fica com essa prioridade. Por isso, vender o crédito inteiro pode significar abrir mão de receber logo uma parte dele.</p>
<p>Uma saída comum é a venda parcial: você mantém a parcela superpreferencial e vende só o saldo, que ainda esperaria a fila. Veja como funciona a <a href="/antecipacao-de-precatorio/">antecipação de precatório</a>, o <a href="/blog/cessao-de-precatorio/">contrato de cessão</a> e se <a href="/blog/vale-a-pena-vender-precatorio/">vale a pena vender precatório</a> no seu caso.</p>

<h2>Precatório do INSS e prazos</h2>
<p>Aposentados e pensionistas com ação contra o INSS costumam ter direito à superpreferência. Veja <a href="/blog/precatorio-inss/">como funciona o precatório do INSS</a> e <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>. Para estimar o valor do saldo, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>, e para a visão geral veja como <a href="/">vender precatório</a>.</p>
""",
  cta=("Quer vender só o saldo do seu precatório?","Envie o número do processo e receba uma proposta por escrito, mantendo a sua parcela prioritária.","Olá! Tenho direito à superpreferência e quero uma proposta para o saldo do meu precatório."),
  related=["precatorio-inss","quanto-tempo-demora-precatorio","vale-a-pena-vender-precatorio"],
))

POSTS.insert(0, dict(
  slug="precatorios-2027-ec-136",
  tag="Prazos",
  title="Precatórios 2027: o que muda com a EC 136/2025",
  seo="Precatórios 2027: o que muda com a EC 136 | Antecipay",
  desc="Precatórios 2027: veja a nova data de corte de 1º de fevereiro, quem entra no orçamento, a nova correção pelo IPCA e os limites de pagamento de estados.",
  lead="A Emenda Constitucional 136/2025 mudou a data de corte, a correção e os limites de pagamento dos precatórios. Veja o que isso significa para quem espera receber em 2027.",
  answer="Pela EC 136/2025, os precatórios apresentados até 1º de fevereiro de 2026 entram no orçamento de 2027 e devem ser pagos até o fim de 2027. Quem foi inscrito depois dessa data fica para o orçamento de 2028. A emenda também mudou a correção, que passou a ser o IPCA mais 2% ao ano, limitada à Selic, e fixou limites anuais de pagamento para estados e municípios.",
  faq=[
   ("Meu precatório foi apresentado em março de 2026. Quando recebo?","Como passou da data de corte de 1º de fevereiro de 2026, ele entra no orçamento de 2028 e deve ser pago até o fim de 2028."),
   ("A nova correção vale para precatórios antigos?","A correção pelo IPCA mais 2% ao ano, limitada à Selic, vale a partir da promulgação da emenda, em 2025. Os períodos anteriores seguem as regras antigas."),
   ("Essas regras podem mudar?","Podem. A EC 136/2025 é questionada no STF na ADI 7873. Enquanto não houver decisão, as regras da emenda continuam valendo."),
  ],
  body="""
<h2>A nova data de corte</h2>
<p>A EC 136/2025 antecipou de 2 de abril para <strong>1º de fevereiro</strong> a data-limite para um precatório entrar no orçamento do ano seguinte.</p>
<div class="table-wrap"><table>
<tr><th>Precatório apresentado</th><th>Orçamento</th><th>Pagamento até</th></tr>
<tr><td>Até 1º de fevereiro de 2026</td><td>2027</td><td>Fim de 2027</td></tr>
<tr><td>De 2 de fevereiro de 2026 a 1º de fevereiro de 2027</td><td>2028</td><td>Fim de 2028</td></tr>
</table></div>
<p>Na prática, um dia de diferença na apresentação pode adiar o pagamento em um ano. Veja mais em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>Como saber se o meu entra em 2027</h2>
<p>Consulte o precatório no portal do tribunal (TRF, para federais, ou TJ, para estaduais e municipais) e confira a data de apresentação e o ano do orçamento. O passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>.</p>

<h2>A nova correção</h2>
<p>Desde a emenda, os precatórios são corrigidos pelo <strong>IPCA mais juros simples de 2% ao ano</strong>. Se essa soma passar da Selic, vale a Selic, que funciona como teto. Antes, a correção era feita pela Selic.</p>

<h2>Estados e municípios: limite anual</h2>
<p>Estados e prefeituras passaram a pagar dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho do estoque de precatórios. A emenda também acabou com o prazo final para eles quitarem os atrasados. Para quem está numa fila longa, isso pode significar uma espera maior. Veja <a href="/vender-precatorio-estadual/">precatório estadual</a> e <a href="/vender-precatorio-municipal/">precatório municipal</a>.</p>

<h2>E os precatórios da União?</h2>
<p>A União costuma pagar os precatórios no ano do orçamento. Para quem tem precatório federal ou do INSS, a data de corte é o que mais pesa no prazo. Veja <a href="/vender-precatorio-federal/">precatório federal</a> e <a href="/vender-precatorio-inss/">vender precatório do INSS</a>.</p>

<h2>Esperar ou vender agora?</h2>
<p>Se o seu precatório ficou para 2028 ou está numa fila estadual ou municipal longa, antecipar pode fazer sentido. Veja os critérios em <a href="/blog/vale-a-pena-vender-precatorio/">vale a pena vender precatório</a>, faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a> e veja como <a href="/">vender precatório</a> com a Antecipay.</p>
""",
  cta=("Não quer esperar até 2027 ou 2028?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Li sobre os precatórios 2027 e quero uma proposta para o meu precatório."),
  related=["quanto-tempo-demora-precatorio","vale-a-pena-vender-precatorio","precatorio-inss"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="juntada-de-certidao",
  tag="Processo",
  title="Juntada de certidão: o que significa no processo",
  seo="Juntada de certidão: o que significa e o que vem depois",
  desc="Viu “juntada de certidão” no andamento do processo? Entenda em 1 minuto o que significa, se o dinheiro foi liberado e qual costuma ser o próximo passo.",
  lead="O andamento do processo mostra “juntada de certidão” e você não sabe se é bom ou ruim? Na maioria das vezes, é só um registro. Veja como entender.",
  answer="Juntada de certidão significa que um documento chamado certidão foi incluído no processo. Na certidão, um servidor da vara ou do tribunal confirma oficialmente um fato, como a publicação de uma decisão, o fim de um prazo ou o trânsito em julgado. Sozinha, a juntada não quer dizer que o pagamento saiu: para saber o que mudou, é preciso ler a certidão ou perguntar ao advogado.",
  faq=[
   ("Juntada de certidão é bom ou ruim?","Nem um nem outro. É um registro de que um fato foi confirmado no processo. Para saber se houve avanço, é preciso ler a certidão."),
   ("Juntada de certidão quer dizer que o dinheiro foi liberado?","Não. O pagamento aparece em outro registro, como a liberação ou o depósito do valor. Desconfie de quem pede taxa dizendo que o dinheiro foi liberado."),
   ("Quanto tempo depois da juntada de certidão o processo anda?","Depende do tipo de certidão e da vara. Se a certidão abriu um prazo, o processo costuma seguir depois que esse prazo termina."),
  ],
  body="""
<h2>O que é “juntada”</h2>
<p>No processo, <strong>juntada</strong> é o ato de incluir um documento nos autos: uma petição, um laudo, uma decisão ou uma certidão. Nos processos eletrônicos, o próprio sistema registra a juntada com a data, que pode servir para contar prazos.</p>

<h2>O que é uma certidão</h2>
<p>A <strong>certidão</strong> é um documento em que o servidor confirma oficialmente que algo aconteceu. Ela não decide nada: apenas registra um fato que vai orientar o próximo passo do processo.</p>

<h2>Certidões comuns na fase do precatório</h2>
<div class="table-wrap"><table>
<tr><th>Certidão</th><th>O que costuma indicar</th></tr>
<tr><td><strong>Trânsito em julgado</strong></td><td>A decisão não admite mais recurso. O processo pode seguir para os cálculos e a cobrança.</td></tr>
<tr><td><strong>Decurso de prazo</strong></td><td>Terminou o prazo para alguém se manifestar, e o processo segue adiante.</td></tr>
<tr><td><strong>Publicação ou intimação</strong></td><td>Uma decisão foi publicada ou alguém foi avisado. A partir daí, pode começar a correr um prazo.</td></tr>
<tr><td><strong>Expedição de requisição</strong></td><td>O ofício requisitório (RPV ou precatório) foi enviado ao tribunal.</td></tr>
</table></div>
<p>Esses são exemplos gerais. O que vale é o texto da certidão do seu processo.</p>

<h2>Como saber o que diz a sua certidão</h2>
<ul>
<li>Em muitos tribunais, o documento pode ser aberto clicando no andamento do processo; em outros, só com o acesso do advogado.</li>
<li>Se não conseguir abrir, peça ao advogado que cuida da ação.</li>
<li>Para acompanhar a requisição de pagamento na Justiça Federal do Nordeste, veja <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>.</li>
</ul>

<h2>E depois da juntada?</h2>
<p>Depende da certidão. Se ela registrou o trânsito em julgado, o próximo passo costuma ser a fase de cálculos. Se registrou a expedição da requisição, o pagamento entra na fila do tribunal: veja <a href="/blog/expedicao-de-oficio-precatorio/">o que significa expedição de ofício</a> e <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>Cuidado com golpes</h2>
<p>Golpistas usam andamentos reais do processo, como “juntada de certidão”, para dizer que o seu dinheiro foi liberado e pedir uma taxa. Juntada de certidão não é aviso de pagamento. Veja <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>.</p>

<h2>Quer antecipar o valor?</h2>
<p>Se o seu processo já chegou à fase do precatório, você pode <a href="/">vender precatório</a> e receber à vista, sem esperar a fila. Veja como funciona a <a href="/antecipacao-de-precatorio/">antecipação de precatório</a>.</p>
""",
  cta=("Seu processo já está na fase do precatório?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Estou acompanhando meu processo e quero uma proposta para o meu precatório."),
  related=["expedicao-de-oficio-precatorio","consultar-rpv-precatorio-trf5","golpe-do-precatorio"],
))

POSTS.insert(0, dict(
  slug="expedicao-de-oficio-precatorio",
  tag="Processo",
  title="Expedição de ofício requisitório: o que significa e o que vem depois",
  seo="Expedição de ofício requisitório: o que significa?",
  desc="Expedição de ofício requisitório deferida? Veja o que significa, o que quer dizer “ofício informando valor depositado” e quanto falta para receber.",
  lead="Viu “expedição de ofício” ou “ofício requisitório expedido” no andamento do processo? É um bom sinal: o pedido de pagamento foi enviado. Veja o que vem depois.",
  answer="Expedição de ofício, no precatório, significa que o juiz enviou ao tribunal o ofício requisitório: o pedido formal para que o governo pague o valor da condenação. É o começo da fila de pagamento, e não o pagamento em si. Depois disso, o tribunal confere a requisição, ela entra no orçamento do devedor e o valor é pago como RPV ou como precatório, conforme o valor.",
  faq=[
   ("Expedição de ofício quer dizer que vou receber logo?","Não necessariamente. Significa que o pedido de pagamento foi enviado ao tribunal. Se for RPV federal, o pagamento costuma sair em até 60 dias; se for precatório, depende da data de corte e da fila do devedor."),
   ("Qual a diferença entre ofício requisitório e precatório?","O ofício requisitório é o documento que o juiz envia ao tribunal pedindo o pagamento. Ele pode ser uma RPV, para valores menores, ou um precatório, para valores acima do limite."),
   ("O que fazer se o valor do ofício estiver errado?","Fale com o advogado que cuida da ação. Correções na requisição são pedidas ao juiz da execução."),
   ("O que significa “ofício informando valor depositado”?","Que o processo recebeu a comunicação de que o valor da RPV ou do precatório foi depositado em conta judicial. É o aviso de que o pagamento saiu. O próximo passo é o saque ou o levantamento, conforme as regras do tribunal."),
  ],
  body="""
<h2>O que é o ofício requisitório</h2>
<p>Quando a ação contra o governo termina e o valor está definido, o juiz da execução emite o <strong>ofício requisitório</strong>: um documento padronizado que pede ao presidente do tribunal o pagamento daquela quantia. Se o valor está dentro do limite de pequeno valor, ele vira uma <strong>RPV</strong>; acima disso, um <strong>precatório</strong>. Veja a diferença em <a href="/blog/o-que-e-precatorio-e-rpv/">o que é precatório e RPV</a>. Se o governo contestou só parte da conta, a parte aceita pode ser requisitada antes: veja <a href="/blog/valor-incontroverso-precatorio/">valor incontroverso</a>.</p>

<h2>O que acontece depois da expedição</h2>
<ol>
<li><strong>O tribunal recebe e confere</strong> a requisição. Se estiver tudo certo, ela é registrada.</li>
<li><strong>Entra na fila do orçamento.</strong> Precatórios apresentados até 1º de fevereiro entram no orçamento do ano seguinte.</li>
<li><strong>Pagamento.</strong> A RPV federal é paga em até 60 dias depois de chegar ao tribunal. O precatório é pago até o fim do ano do orçamento, na ordem cronológica, respeitando as prioridades.</li>
<li><strong>Saque.</strong> O valor é depositado em conta judicial em nome do credor.</li>
</ol>

<h2>Termos que aparecem no andamento</h2>
<div class="table-wrap"><table>
<tr><th>Andamento</th><th>O que significa</th></tr>
<tr><td><strong>Expedição de ofício requisitório deferida</strong></td><td>O juiz autorizou a emissão do ofício. O próximo passo é a expedição em si.</td></tr>
<tr><td><strong>Ofício requisitório expedido</strong></td><td>O pedido de pagamento foi emitido e enviado ao tribunal.</td></tr>
<tr><td><strong>Ofício informando valor depositado</strong></td><td>Chegou ao processo a comunicação de que o valor foi depositado em conta judicial. O pagamento saiu: falta o saque ou o levantamento.</td></tr>
</table></div>
<p>A redação muda um pouco de um tribunal para outro. Na dúvida, abra o documento no andamento ou pergunte ao advogado.</p>

<h2>Quanto tempo falta para receber</h2>
<div class="table-wrap"><table>
<tr><th>Situação</th><th>Prazo aproximado</th></tr>
<tr><td>RPV federal</td><td>Até 60 dias depois de chegar ao tribunal</td></tr>
<tr><td>Precatório federal apresentado até 1º de fevereiro</td><td>Até o fim do ano seguinte</td></tr>
<tr><td>Precatório federal apresentado depois de 1º de fevereiro</td><td>Até o fim do segundo ano seguinte</td></tr>
<tr><td>Precatório estadual ou municipal</td><td>Depende do limite anual de pagamento do devedor (1% a 5% da receita corrente líquida)</td></tr>
</table></div>
<p>Mais detalhes em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>O que conferir agora</h2>
<ul>
<li><strong>Os dados do ofício:</strong> nome, CPF e valor da condenação.</li>
<li><strong>Os honorários do advogado:</strong> em geral, os honorários contratuais precisam ser pedidos ao juiz antes da expedição para saírem destacados. Se não saíram, o advogado precisa pedir depois.</li>
<li><strong>A prioridade:</strong> quem tem 60 anos ou mais costuma ter a prioridade aplicada automaticamente; doença grave ou deficiência precisa de pedido. Veja <a href="/blog/superpreferencia-precatorio/">superpreferência no precatório</a>.</li>
<li><strong>O andamento no tribunal:</strong> no TRF5, a consulta é feita pelo CPF. Veja <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>.</li>
</ul>

<h2>Outros termos do andamento</h2>
<p>“Juntada de certidão” também aparece com frequência nessa fase. Veja <a href="/blog/juntada-de-certidao/">o que significa juntada de certidão</a>.</p>

<h2>Já foi expedido: dá para vender?</h2>
<p>Sim. Com o ofício expedido, o valor e o devedor estão definidos, e a análise para a compra fica mais simples. Se você não quer esperar a fila, veja como <a href="/">vender precatório</a> com a Antecipay ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Seu ofício já foi expedido?","Envie o número do processo e receba uma proposta por escrito para antecipar o valor.","Olá! O ofício do meu precatório foi expedido e quero uma proposta."),
  related=["quanto-tempo-demora-precatorio","consultar-rpv-precatorio-trf5","o-que-e-precatorio-e-rpv"],
))

POSTS.insert(0, dict(
  slug="consultar-rpv-precatorio-trf5",
  tag="Consulta",
  title="Consulta de RPV e precatório no TRF5 pelo CPF: passo a passo",
  seo="Consulta RPV TRF5 pelo CPF: INSS e União | Antecipay",
  desc="Consulta de RPV e precatório do INSS e da União no TRF5 pelo CPF: passo a passo, quando o dinheiro sai e onde sacar. Vale para AL, CE, PB, PE, RN e SE.",
  lead="Tem uma ação contra a União ou o INSS em Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte ou Sergipe? Veja como acompanhar a sua RPV ou o seu precatório no site do TRF5.",
  answer="Para consultar RPV ou precatório no TRF5, acesse rpvprecatorio.trf5.jus.br, escolha “CPF/CNPJ” em “Consultar por”, digite o seu CPF e clique em Pesquisar. Também dá para buscar pelo número do processo. A RPV federal é paga em até 60 dias depois de chegar ao tribunal; o precatório entra no orçamento conforme a data de corte de 1º de fevereiro.",
  faq=[
   ("Preciso de advogado para consultar?","Não. A consulta pública no site do TRF5 é aberta a qualquer pessoa, pelo CPF ou pelo número do processo. Para ver o cálculo e os dados bancários pela internet, é preciso certificado digital ou a ajuda do advogado."),
   ("Onde o dinheiro da RPV ou do precatório é depositado?","Numa conta judicial na Caixa ou no Banco do Brasil, em nome do beneficiário. Em geral, dá para sacar em qualquer agência do banco pagador, sem alvará, levando RG, CPF e comprovante de residência."),
   ("A minha consulta não mostra nada. E agora?","A requisição pode ainda não ter sido expedida pelo juiz, ou ter sido feita com outros dados. Confira com o advogado ou com a vara onde corre o processo."),
  ],
  body="""
<h2>Quais estados são atendidos pelo TRF5</h2>
<p>O Tribunal Regional Federal da 5ª Região cuida das ações contra a União, o INSS e outros órgãos federais em <strong>Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte e Sergipe</strong>. Se a sua ação correu na Justiça Federal de um desses estados, a RPV ou o precatório é pago pelo TRF5.</p>

<h2>Passo a passo da consulta</h2>
<ol>
<li>Acesse o site de RPV e precatórios do TRF5: <a href="https://rpvprecatorio.trf5.jus.br/" target="_blank" rel="noopener">rpvprecatorio.trf5.jus.br</a>.</li>
<li>Em <strong>“Consultar por”</strong>, escolha <strong>CPF/CNPJ</strong>.</li>
<li>Digite o seu CPF no campo de pesquisa.</li>
<li>Clique em <strong>Pesquisar</strong> e confira o resultado e o andamento da requisição.</li>
</ol>
<p>A consulta também pode ser feita pelo número do processo de execução, do processo originário ou do processo no TRF5, pelo número do requisitório ou pela OAB do advogado. Requisições muito antigas, de 2005 para trás, só aparecem em algumas dessas opções.</p>

<h2>Quando o dinheiro sai</h2>
<div class="table-wrap"><table>
<tr><th>Tipo</th><th>Prazo</th></tr>
<tr><td><strong>RPV</strong></td><td>Até 60 dias depois de a requisição chegar ao tribunal</td></tr>
<tr><td><strong>Precatório federal</strong></td><td>Apresentado até 1º de fevereiro: pago até o fim do ano seguinte. Depois dessa data, fica para o orçamento do ano posterior.</td></tr>
</table></div>
<p>Algumas perguntas frequentes do site do TRF5 ainda citam a data de 2 de abril. Desde a EC 136/2025, a data de corte é 1º de fevereiro. Veja <a href="/blog/precatorios-2027-ec-136/">precatórios 2027</a> e <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>Onde sacar</h2>
<p>O valor é depositado numa conta judicial na Caixa ou no Banco do Brasil, em nome do beneficiário. Em geral, o saque pode ser feito em qualquer agência do banco pagador, sem alvará, com RG, CPF e comprovante de residência. O alvará só é exigido quando o juiz determina ou quando a ação correu na Justiça Estadual com competência federal delegada. O dinheiro fica disponível por 2 anos; depois disso, volta para o Tesouro.</p>

<h2>Prioridade e mudanças na requisição</h2>
<p>A prioridade por idade é aplicada automaticamente. A prioridade por doença grave ou deficiência precisa ser pedida ao juiz da execução: veja <a href="/blog/superpreferencia-precatorio/">superpreferência no precatório</a>. Mudanças como inclusão de herdeiros ou registro de venda (cessão) também passam pela vara onde corre o processo, e não pelo tribunal.</p>

<h2>Entendendo o andamento</h2>
<p>Termos como “expedição de ofício” e “juntada de certidão” aparecem com frequência no acompanhamento. Veja o que significam em <a href="/blog/expedicao-de-oficio-precatorio/">expedição de ofício no precatório</a> e <a href="/blog/juntada-de-certidao/">juntada de certidão</a>. Para outros tribunais, veja <a href="/blog/consultar-rpv-precatorio-trf1/">consulta no TRF1</a> e <a href="/blog/consultar-rpv-precatorio-trf3/">consulta no TRF3</a>.</p>

<h2>Não quer esperar?</h2>
<p>Se o seu precatório do TRF5 ainda vai demorar, você pode <a href="/">vender precatório</a> e receber à vista. A Antecipay fica em Natal, na área do TRF5, e analisa precatórios federais e do <a href="/vender-precatorio-inss/">INSS</a> de toda a região. Faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem precatório no TRF5?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um precatório no TRF5 e quero uma proposta."),
  related=["como-saber-se-tenho-precatorio","quanto-tempo-demora-precatorio","precatorio-inss"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="valor-incontroverso-precatorio",
  tag="Processo",
  title="Valor incontroverso no precatório: receba a parte que não está em discussão",
  seo="Valor incontroverso no precatório: o que é | Antecipay",
  desc="Entenda o que é valor incontroverso, quando o governo contesta só parte da conta, e como pedir o precatório ou a RPV dessa parte antes do fim da discussão.",
  lead="O governo concordou com uma parte da conta e discute o resto? Essa parte aceita é o valor incontroverso, e você pode pedir o pagamento dela antes do fim da discussão.",
  answer="Valor incontroverso é a parte da conta que o governo não contestou. Quando a Fazenda Pública impugna só parte do cálculo, o Código de Processo Civil (art. 535, §4º) permite cobrar desde logo a parte não questionada, e o STF confirmou que é possível expedir precatório ou RPV dessa parcela (Tema 28). Assim, o credor não precisa esperar a discussão sobre o restante para entrar na fila de pagamento.",
  faq=[
   ("Valor incontroverso é pago mais rápido?","Ele entra na fila antes, porque não depende do fim da discussão. Depois de expedido, segue as mesmas regras de pagamento de qualquer RPV ou precatório."),
   ("Quem pede a expedição do valor incontroverso?","O advogado do credor, ao juiz da execução, quando a Fazenda contesta só parte do cálculo."),
   ("Se a parte incontroversa for pequena, vira RPV?","Não necessariamente. O que define se o pagamento sai por RPV ou por precatório é o valor total executado. Se o total passar do limite, a parte incontroversa sai como precatório."),
  ],
  body="""
<h2>O que é valor incontroverso</h2>
<p>Depois que o credor ganha a ação contra o governo, vem a fase de cobrança: o credor apresenta o cálculo do que tem a receber, e a Fazenda Pública pode contestar (impugnar) essa conta. Se ela contesta só uma parte, o restante é o <strong>valor incontroverso</strong>, ou seja, a parte sobre a qual não há discussão.</p>
<p><em>Exemplo hipotético:</em> o credor cobra R$ 100 mil e o governo diz que deve R$ 80 mil. Os R$ 80 mil são incontroversos; os R$ 20 mil restantes ficam em discussão.</p>

<h2>O que diz a lei</h2>
<ul>
<li><strong>Código de Processo Civil, art. 535, §4º:</strong> quando a impugnação é parcial, a parte não questionada pode ser cobrada desde logo.</li>
<li><strong>STF, Tema 28 de repercussão geral:</strong> o Supremo confirmou que é constitucional expedir precatório ou RPV para pagar a parte incontroversa e autônoma da condenação.</li>
</ul>

<h2>RPV ou precatório?</h2>
<p>O que define o caminho é o <strong>valor total executado</strong>, e não só a parte incontroversa. A Constituição proíbe dividir o crédito para que uma parte saia como RPV e outra como precatório (art. 100, §8º). Se o total passar do limite de pequeno valor, a parte incontroversa sai como precatório, mesmo que seja pequena. Veja a diferença em <a href="/blog/o-que-e-precatorio-e-rpv/">o que é precatório e RPV</a>.</p>

<h2>Como pedir</h2>
<p>O advogado do credor pede ao juiz da execução a expedição do ofício da parte incontroversa. Depois disso, o caminho é o mesmo de qualquer requisição: veja <a href="/blog/expedicao-de-oficio-precatorio/">o que acontece depois da expedição de ofício</a> e <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>E a parte em discussão?</h2>
<p>Ela continua sendo discutida no processo. Se, ao final, o credor tiver direito a ela, o valor pode gerar uma nova requisição de pagamento.</p>

<h2>Dá para vender a parte incontroversa?</h2>
<p>Sim. Depois de expedido, o precatório da parte incontroversa pode ser vendido como qualquer outro, por <a href="/blog/cessao-de-precatorio/">contrato de cessão de crédito</a>. Se você não quer esperar a fila, veja como <a href="/">vender precatório</a> com a Antecipay ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem valor incontroverso a receber?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um valor incontroverso no meu processo e quero uma proposta."),
  related=["expedicao-de-oficio-precatorio","o-que-e-precatorio-e-rpv","cessao-de-precatorio"],
))

POSTS.insert(0, dict(
  slug="consultar-precatorio-tjsp",
  tag="Consulta",
  title="Como consultar precatório no TJSP: posição na fila e pagamento",
  seo="Consulta de precatório no TJSP: fila e pagamento | Antecipay",
  desc="Consulta de precatório no TJSP passo a passo: onde ver a posição na fila, como pedir prioridade e como levantar o valor. Para credores do Estado e de SP.",
  lead="Tem precatório contra o Estado de São Paulo, um município paulista ou uma autarquia? Veja onde acompanhar a posição na fila e o que fazer quando o pagamento sai.",
  answer="Para consultar precatório no TJSP, acesse a página de precatórios do tribunal (tjsp.jus.br/precatorios). No menu Credores, a “Lista de Precatórios Disponibilizados e Pendentes de Pagamentos” mostra a posição na fila, e a lista de “Pagamentos Disponibilizados” mostra o que já foi pago. As listas de pendentes são atualizadas todo mês, por volta do dia 5.",
  faq=[
   ("Dá para consultar precatório do TJSP pelo CPF?","A página oficial de precatórios do TJSP não informa consulta por CPF. Se você não sabe o número do precatório ou do processo, peça ao advogado que cuidou da ação."),
   ("Como pedir prioridade por doença grave no TJSP?","Nos precatórios eletrônicos, a partir de 2016, o pedido é feito ao juízo da execução, com cópia do RG e do CPF e atestado médico. Nos precatórios físicos, anteriores a 2016, o pedido é protocolado na Depre."),
   ("Onde recebo o dinheiro do precatório do TJSP?","A Depre deposita o valor em conta ligada ao processo de origem. O levantamento é feito no juízo onde correu a ação, por mandado de levantamento em nome do advogado."),
  ],
  body="""
<h2>Quem paga pelo TJSP</h2>
<p>No Tribunal de Justiça de São Paulo, os precatórios do <strong>Estado de São Paulo</strong>, dos <strong>municípios paulistas</strong> e das autarquias estaduais e municipais são administrados pela <strong>Depre</strong>, a Diretoria de Execuções de Precatórios e Cálculos.</p>

<h2>Passo a passo da consulta</h2>
<ol>
<li>Acesse a página de precatórios do TJSP: <a href="https://www.tjsp.jus.br/precatorios" target="_blank" rel="noopener">tjsp.jus.br/precatorios</a>.</li>
<li>No menu <strong>Credores</strong>, abra a <strong>“Lista de Precatórios Disponibilizados e Pendentes de Pagamentos”</strong>.</li>
<li>Localize o ente devedor (o Estado ou o município) e o seu precatório na lista, para ver a posição na fila.</li>
<li>Se o precatório já foi pago, ele aparece na lista de <strong>“Pagamentos Disponibilizados”</strong>.</li>
</ol>
<p>As listas de pendentes são atualizadas mensalmente, por volta do dia 5, e os precatórios pagos no mês anterior saem delas. O TJSP informa que está substituindo o sistema de listas, então vale conferir os dois sistemas disponíveis na página. A “Pesquisa de Precatórios e Pagamentos” cobre registros até maio de 2018. Nos precatórios eletrônicos, também dá para acompanhar os autos digitais com a senha fornecida pelo advogado.</p>

<h2>Consulta por CPF</h2>
<p>A página oficial de precatórios do TJSP não informa consulta por CPF. Para encontrar o seu precatório com segurança, tenha em mãos o número do precatório ou do processo, que o advogado da ação pode informar.</p>

<h2>Prioridade por idade, doença ou deficiência</h2>
<ul>
<li><strong>Precatórios eletrônicos (a partir de 2016):</strong> a prioridade por idade já consta do ofício requisitório. Para doença grave ou deficiência que não constem do ofício, o pedido é feito ao juízo da execução, com cópia do RG e do CPF e atestado médico.</li>
<li><strong>Precatórios físicos (anteriores a 2016):</strong> o pedido é protocolado na Depre, com os mesmos documentos.</li>
</ul>
<p>Entenda os limites em <a href="/blog/superpreferencia-precatorio/">superpreferência no precatório</a>.</p>

<h2>Quando o pagamento sai</h2>
<p>A Depre deposita o valor em conta vinculada ao processo de origem. O levantamento é feito no juízo onde correu a ação, por <strong>mandado de levantamento</strong> em nome do advogado; na Capital, esse trâmite passa pela Upefaz. O andamento pode ser acompanhado na consulta processual do 1º grau.</p>

<h2>Quanto tempo demora</h2>
<p>Estados e municípios pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho do estoque de precatórios, e a espera pode ser longa. Veja <a href="/vender-precatorio-estadual/">precatório estadual</a>, <a href="/vender-precatorio-municipal/">precatório municipal</a> e <a href="/blog/precatorios-2027-ec-136/">o que mudou com a EC 136</a>.</p>

<h2>Não quer esperar a fila?</h2>
<p>A Antecipay compra precatórios de todo o Brasil, inclusive de São Paulo. Veja como <a href="/">vender precatório</a> com proposta por escrito ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem precatório em São Paulo?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um precatório no TJSP e quero uma proposta."),
  related=["consultar-rpv-precatorio-trf3","quanto-tempo-demora-precatorio","superpreferencia-precatorio"],
))

POSTS.insert(0, dict(
  slug="consultar-rpv-precatorio-trf3",
  tag="Consulta",
  title="Consulta de RPV e precatório no TRF3 pelo CPF: passo a passo",
  seo="Consulta RPV TRF3 pelo CPF: passo a passo | Antecipay",
  desc="Consulta de RPV e precatório no TRF3 pelo CPF: passo a passo da consulta de requisição de pagamento em SP e MS e quando o dinheiro sai.",
  lead="Tem uma ação contra a União ou o INSS na Justiça Federal de São Paulo ou de Mato Grosso do Sul? Veja como acompanhar a sua RPV ou o seu precatório no TRF3.",
  answer="Para consultar RPV ou precatório no TRF3, acesse a consulta de requisições de pagamento no site do tribunal e pesquise pelo CPF ou CNPJ do beneficiário, pela OAB do advogado, pelo número do processo de origem, do ofício requisitório ou do protocolo. A RPV é paga em até 60 dias depois de a requisição ser registrada no tribunal; o precatório segue a data de corte de 1º de fevereiro.",
  faq=[
   ("O TRF3 atende quais estados?","O TRF3 atende a Justiça Federal de São Paulo e de Mato Grosso do Sul."),
   ("Minha requisição é antiga e não aparece. O que fazer?","Precatórios enviados antes de 1º de julho de 2006 e RPVs enviadas antes de 1º de julho de 2007 não aparecem nessa consulta. Nesses casos, use a consulta processual geral do tribunal ou fale com o advogado."),
   ("Preciso de advogado para consultar?","Não. A consulta de requisições de pagamento é pública e pode ser feita pelo CPF do beneficiário."),
  ],
  body="""
<h2>Quais estados são atendidos pelo TRF3</h2>
<p>O Tribunal Regional Federal da 3ª Região cuida das ações contra a União, o INSS e outros órgãos federais em <strong>São Paulo</strong> e <strong>Mato Grosso do Sul</strong>.</p>

<h2>Passo a passo da consulta</h2>
<ol>
<li>Acesse a consulta de requisições de pagamento do TRF3: <a href="https://web.trf3.jus.br/consultas/Internet/ConsultaReqPag" target="_blank" rel="noopener">web.trf3.jus.br/consultas/Internet/ConsultaReqPag</a>.</li>
<li>Escolha como pesquisar: <strong>CPF/CNPJ do beneficiário</strong>, OAB do advogado, número do processo de origem, número do ofício requisitório ou número do protocolo.</li>
<li>Digite o dado e faça a pesquisa.</li>
<li>Confira a situação da requisição, na modalidade em que foi feita: precatório, que segue o orçamento anual, ou RPV, que segue o orçamento mensal.</li>
</ol>
<p>Precatórios enviados antes de 1º de julho de 2006 e RPVs enviadas antes de 1º de julho de 2007 não aparecem nessa consulta; para eles, use a consulta processual geral do tribunal.</p>

<h2>Quando o dinheiro sai</h2>
<div class="table-wrap"><table>
<tr><th>Tipo</th><th>Prazo</th></tr>
<tr><td><strong>RPV</strong></td><td>Até 60 dias depois de a requisição ser registrada no tribunal</td></tr>
<tr><td><strong>Precatório federal</strong></td><td>Apresentado até 1º de fevereiro: pago até o fim do ano seguinte. Depois dessa data, fica para o orçamento do ano posterior.</td></tr>
</table></div>
<p>Veja mais em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

<h2>Onde sacar</h2>
<p>Na Justiça Federal, o valor costuma ser depositado numa conta judicial na Caixa ou no Banco do Brasil, em nome do beneficiário. Em geral, o saque é feito na agência do banco pagador, com RG, CPF e comprovante de residência. Se o juiz exigir alvará, o advogado orienta o caminho.</p>

<h2>Termos do andamento</h2>
<p>Se aparecer “expedição de ofício” ou “juntada de certidão” no processo, veja <a href="/blog/expedicao-de-oficio-precatorio/">expedição de ofício no precatório</a> e <a href="/blog/juntada-de-certidao/">juntada de certidão</a>. Para outros tribunais, veja <a href="/blog/consultar-rpv-precatorio-trf1/">consulta no TRF1</a> e <a href="/blog/consultar-rpv-precatorio-trf5/">consulta no TRF5</a>.</p>

<h2>Não quer esperar?</h2>
<p>A Antecipay compra precatórios federais e do <a href="/vender-precatorio-inss/">INSS</a> de todo o Brasil. Veja como <a href="/">vender precatório</a> ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem precatório no TRF3?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um precatório no TRF3 e quero uma proposta."),
  related=["consultar-rpv-precatorio-trf1","consultar-rpv-precatorio-trf5","quanto-tempo-demora-precatorio"],
))

POSTS.insert(0, dict(
  slug="consultar-rpv-precatorio-trf1",
  tag="Consulta",
  title="Como consultar RPV e precatório no TRF1 pelo CPF",
  seo="Consultar RPV e precatório no TRF1 pelo CPF | Antecipay",
  desc="Veja como consultar RPV e precatório no TRF1 pelo CPF, onde ver a data e o banco do pagamento e quanto tempo falta. Vale para DF, BA, GO, PA e outros estados.",
  lead="Tem uma ação contra a União ou o INSS no Distrito Federal, na Bahia, em Goiás, no Pará ou em outro estado do TRF1? Veja como acompanhar a sua RPV ou o seu precatório.",
  answer="Para consultar RPV ou precatório no TRF1, acesse o site do tribunal (trf1.jus.br), clique na aba “Processual”, escolha “RPVs e Precatórios” e pesquise pelo CPF. Na aba “Movimentação”, aparecem as datas e o banco do depósito. A RPV federal é paga em até 60 dias depois de chegar ao tribunal; o precatório segue a data de corte de 1º de fevereiro.",
  faq=[
   ("O TRF1 atende quais estados?","Acre, Amapá, Amazonas, Bahia, Distrito Federal, Goiás, Maranhão, Mato Grosso, Pará, Piauí, Rondônia, Roraima e Tocantins. Minas Gerais passou para o TRF6 em 2022."),
   ("Onde vejo a data e o banco do pagamento?","Na aba “Movimentação” do resultado da consulta de RPVs e precatórios."),
   ("A consulta não mostra nada. E agora?","A requisição pode ainda não ter sido expedida pelo juiz, ou ter sido feita com outros dados. Confira com o advogado ou com a vara onde corre o processo."),
  ],
  body="""
<h2>Quais estados são atendidos pelo TRF1</h2>
<p>O Tribunal Regional Federal da 1ª Região cuida das ações contra a União, o INSS e outros órgãos federais em <strong>Acre, Amapá, Amazonas, Bahia, Distrito Federal, Goiás, Maranhão, Mato Grosso, Pará, Piauí, Rondônia, Roraima e Tocantins</strong>. Minas Gerais, que fazia parte do TRF1, passou para o TRF6 em 2022.</p>

<h2>Passo a passo da consulta</h2>
<ol>
<li>Acesse o site do TRF1: <a href="https://www.trf1.jus.br/" target="_blank" rel="noopener">trf1.jus.br</a>.</li>
<li>No menu do alto da página, clique na aba <strong>“Processual”</strong>.</li>
<li>Escolha <strong>“RPVs e Precatórios”</strong> e abra a consulta.</li>
<li>Pesquise pelo seu <strong>CPF</strong>. Aparece a lista de processos encontrados com o nome da parte.</li>
<li>Abra o resultado e veja a aba <strong>“Movimentação”</strong>, com as datas e o banco onde a RPV ou o precatório será depositado.</li>
</ol>
<p>O TRF1 lançou um novo portal no fim de 2023. Se os menus estiverem com outro nome, procure por “RPVs e Precatórios” na página inicial.</p>

<h2>Quando o dinheiro sai</h2>
<div class="table-wrap"><table>
<tr><th>Tipo</th><th>Prazo</th></tr>
<tr><td><strong>RPV</strong></td><td>Até 60 dias depois de a requisição chegar ao tribunal</td></tr>
<tr><td><strong>Precatório federal</strong></td><td>Apresentado até 1º de fevereiro: pago até o fim do ano seguinte. Depois dessa data, fica para o orçamento do ano posterior.</td></tr>
</table></div>
<p>Veja mais em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a> e <a href="/blog/precatorios-2027-ec-136/">precatórios 2027</a>.</p>

<h2>Onde sacar</h2>
<p>Na Justiça Federal, o valor costuma ser depositado numa conta judicial na Caixa ou no Banco do Brasil, em nome do beneficiário. Em geral, o saque é feito na agência do banco pagador, com RG, CPF e comprovante de residência. Se o juiz exigir alvará, o advogado orienta o caminho.</p>

<h2>Termos do andamento</h2>
<p>Se aparecer “expedição de ofício” ou “juntada de certidão” no processo, veja <a href="/blog/expedicao-de-oficio-precatorio/">expedição de ofício no precatório</a> e <a href="/blog/juntada-de-certidao/">juntada de certidão</a>. Para outros tribunais, veja <a href="/blog/consultar-rpv-precatorio-trf3/">consulta no TRF3</a> e <a href="/blog/consultar-rpv-precatorio-trf5/">consulta no TRF5</a>.</p>

<h2>Não quer esperar?</h2>
<p>A Antecipay compra precatórios federais e do <a href="/vender-precatorio-inss/">INSS</a> de todo o Brasil. Veja como <a href="/">vender precatório</a> ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem precatório no TRF1?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um precatório no TRF1 e quero uma proposta."),
  related=["consultar-rpv-precatorio-trf3","consultar-rpv-precatorio-trf5","precatorio-inss"],
))
POSTS.insert(0, dict(
  slug="precatorio-judicial",
  tag="Guia",
  title="Precatório judicial: o que é e como funciona",
  seo="Precatório judicial: o que é e como funciona | Antecipay",
  desc="Entenda o que é precatório judicial, quando a dívida do governo vira precatório ou RPV, as etapas até o pagamento e como consultar ou vender o seu.",
  lead="Ganhou uma ação contra o governo e ouviu falar em precatório judicial? Veja, sem juridiquês, o que isso significa e o caminho até o dinheiro cair na conta.",
  answer="Precatório judicial é a ordem de pagamento que a Justiça envia ao governo quando ele perde uma ação e não cabe mais recurso. Vale para dívidas da União, do INSS, de estados, de municípios e de autarquias. Valores menores são pagos por RPV, mais rápida; os maiores viram precatório e entram numa fila com data de corte em 1º de fevereiro.",
  faq=[
   ("Todo precatório é judicial?","Sim. O precatório sempre nasce de um processo na Justiça. A expressão “precatório judicial” só reforça isso: é a ordem que o juiz manda ao governo para pagar o que foi decidido."),
   ("Qual a diferença entre precatório e RPV?","As duas são ordens de pagamento contra o governo. A RPV vale para valores menores (na esfera federal, até 60 salários mínimos) e é paga em até 60 dias. Acima do limite, o pagamento é feito por precatório, que segue o orçamento anual."),
   ("Posso vender um precatório judicial?","Sim. A cessão de precatórios é permitida pelo art. 100, §13, da Constituição. Você recebe à vista e quem compra passa a receber do governo no futuro."),
   ("O precatório judicial pode ser de ação trabalhista?","Sim, quando a ação foi contra um órgão público, como a União, um estado, uma prefeitura ou uma autarquia."),
  ],
  body="""
<h2>O que é precatório judicial</h2>
<p>Quando alguém ganha uma ação contra o poder público e não cabe mais recurso, o governo não paga na hora, como faria uma pessoa ou empresa. A Constituição manda que o juiz envie ao tribunal uma <strong>ordem de pagamento</strong>, que entra no orçamento do governo devedor. Essa ordem é o precatório judicial.</p>
<p>O devedor pode ser a <strong>União</strong>, o <strong>INSS</strong> e outras autarquias, um <strong>estado</strong> ou um <strong>município</strong>. Entenda a diferença entre os tipos em <a href="/blog/o-que-e-precatorio-e-rpv/">o que é precatório e RPV</a>.</p>

<h2>Precatório ou RPV?</h2>
<div class="table-wrap"><table>
<tr><th></th><th>RPV</th><th>Precatório</th></tr>
<tr><td><strong>Valor</strong></td><td>Até o limite da RPV (na esfera federal, 60 salários mínimos)</td><td>Acima do limite da RPV</td></tr>
<tr><td><strong>Prazo</strong></td><td>Até 60 dias depois da requisição</td><td>Segue o orçamento anual e a data de corte de 1º de fevereiro</td></tr>
</table></div>
<p>Estados e municípios podem ter limites de RPV diferentes do federal, definidos em lei própria.</p>

<h2>As etapas até o pagamento</h2>
<ol>
<li><strong>Sentença definitiva:</strong> a ação termina sem possibilidade de recurso (trânsito em julgado).</li>
<li><strong>Cálculo:</strong> as partes discutem o valor devido. A parte sem discussão pode andar antes; veja <a href="/blog/valor-incontroverso-precatorio/">valor incontroverso</a>.</li>
<li><strong>Expedição do ofício:</strong> o juiz manda o pedido de pagamento ao tribunal. Veja o que significa a <a href="/blog/expedicao-de-oficio-precatorio/">expedição de ofício no precatório</a>.</li>
<li><strong>Inscrição no orçamento:</strong> precatórios apresentados até <strong>1º de fevereiro</strong> entram no orçamento do ano seguinte.</li>
<li><strong>Pagamento:</strong> o valor é depositado numa conta judicial em nome do credor.</li>
</ol>

<h2>Quanto tempo demora</h2>
<p>Os precatórios federais costumam ser pagos dentro do calendário. Já estados e municípios, pela EC 136/2025, pagam conforme um limite anual de 1% a 5% da sua receita corrente líquida, e por isso a fila pode levar anos. Veja os prazos em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a> e o que muda em <a href="/blog/precatorios-2027-ec-136/">precatórios 2027</a>.</p>

<h2>Prioridade na fila</h2>
<p>Créditos de natureza alimentar, como salários, aposentadorias e benefícios do <a href="/blog/precatorio-inss/">INSS</a>, são pagos antes dos demais. Credores com 60 anos ou mais, doença grave ou deficiência podem ter a <a href="/blog/superpreferencia-precatorio/">superpreferência</a>, que é pessoal e não passa para quem compra o precatório.</p>

<h2>Como consultar o seu</h2>
<p>A consulta é pública e pode ser feita pelo CPF no site do tribunal. Veja o passo a passo em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a> e nos guias do <a href="/blog/consultar-rpv-precatorio-trf1/">TRF1</a>, do <a href="/blog/consultar-rpv-precatorio-trf5/">TRF5</a> e do <a href="/blog/consultar-precatorio-tjsp/">TJSP</a>.</p>

<h2>Não quer esperar?</h2>
<p>Você pode vender o precatório e receber à vista. A Antecipay faz a <a href="/antecipacao-de-precatorio/">compra de precatório</a> <a href="/vender-precatorio-federal/">federal</a>, <a href="/vender-precatorio-estadual/">estadual</a> e <a href="/vender-precatorio-municipal/">municipal</a> de todo o Brasil. Veja como <a href="/">vender precatório</a> ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
""",
  cta=("Tem um precatório judicial?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Tenho um precatório judicial e quero uma proposta."),
  related=["o-que-e-precatorio-e-rpv","quanto-tempo-demora-precatorio","como-vender-precatorio"],
))
POSTS.insert(0, dict(
  slug="eleicoes-precatorios-rn-natal",
  tag="Orçamento",
  title="Eleições, orçamento e a fila dos precatórios no RN e em Natal",
  seo="Eleições e precatórios no RN e em Natal | Antecipay",
  desc="Troca de governo muda a fila dos precatórios? Entenda como o orçamento do RN e de Natal limita os pagamentos, como funcionam os acordos diretos e a antecipação.",
  lead="Em ano de eleição, o assunto precatório volta ao noticiário e às conversas entre credores. Veja, sem lado político, o que de fato define o ritmo da fila no Estado e na capital.",
  answer="A eleição não acelera nem para a fila dos precatórios. O ritmo é definido pela Constituição: desde a EC 136/2025, estados e municípios pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho da dívida, e o TJRN paga pela ordem cronológica. Promessas de campanha não mudam esse teto. Quem precisa de previsibilidade pode esperar a fila, aderir a um acordo direto quando houver edital (com deságio de até 40%) ou vender o precatório a uma empresa privada.",
  faq=[
   ("O pagamento de precatórios para durante a eleição?","Não. O precatório é uma ordem da Justiça e o pagamento é feito pelo tribunal, com os recursos que o governo deposita dentro do limite anual. O calendário eleitoral não suspende essa obrigação."),
   ("Um novo governador pode pagar a fila mais rápido?","Pode depositar valores acima do mínimo ou abrir acordos diretos, mas o mínimo anual é fixado pela Constituição e a ordem de pagamento é controlada pelo TJRN. Na prática, a velocidade da fila depende mais do tamanho da dívida e da arrecadação do que de quem governa."),
   ("O que é o acordo direto?","É um edital do tribunal em que o credor aceita receber com desconto, em geral de 40%, para passar na frente com a verba reservada para os acordos. Quem não for contemplado continua na posição original da fila."),
   ("Vender o precatório tira meu lugar na fila?","Não. Na cessão, o precatório continua na mesma posição; muda apenas quem vai receber quando chegar a vez. Você recebe à vista e a empresa compradora assume a espera."),
   ("Tenho precatório trabalhista contra o Estado ou contra Natal. Vale o mesmo?","Sim. Precatórios trabalhistas contra o Estado ou o Município são expedidos pela Justiça do Trabalho (TRT21) e também se sujeitam ao limite anual do devedor. Confira a situação no TRT21 e no TJRN."),
  ],
  body="""
<p>Com a campanha de 2026 nas ruas, o assunto aparece em debates, entrevistas e grupos de mensagem: quem tem precatório quer saber se a próxima gestão vai pagar mais rápido, mais devagar ou do mesmo jeito. A resposta honesta é que <strong>a velocidade da fila depende muito mais de regras constitucionais e do tamanho do orçamento do que de quem ocupa o cargo</strong>. Este texto explica essas regras, sem tomar partido de nenhum governo, passado, atual ou futuro.</p>

<h2>Bastidores do orçamento: por que o precatório disputa espaço</h2>
<p>Todo ano, o governo do Estado e a Prefeitura de Natal enviam ao Legislativo a <strong>lei orçamentária</strong> com a previsão do que vão arrecadar e gastar no ano seguinte. Boa parte desse dinheiro já chega com destino definido por lei, antes de qualquer escolha política:</p>
<ul>
<li><strong>Educação:</strong> pelo menos 25% da receita de impostos (art. 212 da Constituição).</li>
<li><strong>Saúde:</strong> pelo menos 12% da receita de impostos nos estados e 15% nos municípios (Lei Complementar 141/2012).</li>
<li><strong>Pessoal:</strong> salários, aposentadorias e pensões, com limites fixados pela Lei de Responsabilidade Fiscal.</li>
<li><strong>Dívidas:</strong> parcelas de empréstimos e financiamentos.</li>
</ul>
<p>O que sobra precisa cobrir custeio, obras e investimentos. Os precatórios entram nessa conta como despesa obrigatória, mas com um teto próprio. Pela <a href="/blog/precatorios-2027-ec-136/">EC 136/2025</a>, estados e municípios pagam precatórios dentro de um <strong>limite anual de 1% a 5% da receita corrente líquida</strong>, conforme o tamanho do estoque da dívida. A mesma emenda acabou com o prazo final, que era 2029, para quitar os atrasados.</p>
<p>Na prática, isso quer dizer que <strong>a fila anda no ritmo da arrecadação</strong>. Se a receita cresce, o valor reservado aos precatórios cresce junto; se a dívida acumulada é grande, a fila leva anos para andar, seja qual for o governo.</p>

<h3>E a troca de gestão?</h3>
<p>Quem toma posse em janeiro de 2027 recebe um orçamento já votado no ano anterior. Os precatórios apresentados até <strong>1º de fevereiro de 2026</strong> entram no orçamento de 2027; os apresentados depois disso ficam para 2028. Uma nova gestão pode decidir depositar mais do que o mínimo ou propor acordos diretos, mas não pode pagar abaixo do limite constitucional nem mudar a ordem da fila, que é controlada pelo Tribunal de Justiça.</p>
<p>A capital está em outro calendário: a eleição para prefeito foi em 2024 e a próxima é em 2028. Para os credores do Município de Natal, a eleição de 2026 não muda o comando da Prefeitura.</p>

<h2>A fila do regime especial e os acordos diretos</h2>
<p>O Estado do Rio Grande do Norte e o Município de Natal pagam seus precatórios pelo <strong>regime especial</strong> do art. 101 do ADCT. Funciona assim:</p>
<ol>
<li>O governo deposita mensalmente, numa conta administrada pelo <strong>TJRN</strong>, o valor correspondente ao seu limite anual.</li>
<li>O tribunal paga os credores pela <strong>ordem cronológica</strong>, com prioridade para créditos alimentares e para quem tem <a href="/blog/superpreferencia-precatorio/">superpreferência</a> (60 anos ou mais, doença grave ou deficiência).</li>
<li>Os precatórios trabalhistas, expedidos pelo <strong>TRT21</strong>, e os federais contra o Estado ou o Município também dependem desses recursos. Em regra, no regime especial o Tribunal de Justiça administra as contas e reparte o dinheiro com a Justiça do Trabalho e a Justiça Federal.</li>
</ol>

<h3>Como funcionam os editais de acordo direto</h3>
<p>Parte dos recursos pode ser destinada a <strong>acordos diretos</strong>. O tribunal publica um edital com o valor disponível, e o credor que aceitar um desconto passa na frente com essa verba. A Constituição permite redução de <strong>até 40%</strong> do valor atualizado (art. 102, §1º, do ADCT). Dois exemplos recentes no RN:</p>
<div class="table-wrap"><table>
<tr><th>Edital</th><th>Devedor</th><th>Valor reservado</th><th>Deságio</th><th>Adesão</th></tr>
<tr><td>Nº 01/2025 (TJRN)</td><td>Estado do RN</td><td>R$ 70 milhões</td><td>40%</td><td>3 a 14 de novembro de 2025</td></tr>
<tr><td>Nº 02/2025 (TJRN)</td><td>Município de Natal</td><td>R$ 35 milhões</td><td>40%</td><td>10 a 21 de novembro de 2025</td></tr>
</table></div>
<p>O que costuma valer nesses editais:</p>
<ul>
<li>A inscrição é feita pelo advogado do processo, no sistema de precatórios do TJRN, e o prazo é curto e improrrogável.</li>
<li>Só entram precatórios <strong>sem recurso pendente, sem discussão de cálculo e sem transferência de titularidade em andamento</strong>.</li>
<li>Ao aderir, o credor aceita o deságio e renuncia a discussões sobre o crédito.</li>
<li><strong>Manifestar interesse não garante o pagamento</strong>: se a verba acabar, quem não foi contemplado continua na posição original da fila.</li>
<li>Os editais podem ser revistos. Em 2025, um edital estadual de R$ 100 milhões foi suspenso depois de apontamentos do Conselho Nacional de Justiça sobre a ordem cronológica e acabou substituído pelo edital nº 01/2025.</li>
</ul>
<p>O acordo direto pode ser uma boa saída, mas <strong>não tem data certa</strong>: depende de o governo reservar verba, de o tribunal abrir edital e de o seu precatório se encaixar nas regras.</p>

<h2>A alternativa da antecipação privada</h2>
<p>Quem não quer depender do calendário da fila nem da abertura de editais pode <strong>vender o precatório</strong> a uma empresa privada. A operação se chama <a href="/blog/cessao-de-precatorio/">cessão de crédito</a> e é permitida pelo art. 100, §13, da Constituição. Você recebe à vista e a empresa passa a receber do governo quando chegar a vez do precatório.</p>
<p>Na Antecipay Precatórios, o caminho é este:</p>
<ol>
<li>Você envia o número do processo pelo WhatsApp.</li>
<li>Nossa equipe jurídica analisa o processo, a posição na fila e a situação do devedor.</li>
<li>Você recebe uma <strong>proposta por escrito, com o valor líquido</strong>, sem custo e sem compromisso.</li>
<li>Se aceitar, a cessão é assinada e o pagamento cai em <strong>até 72 horas</strong>. Depois, a cessão é comunicada ao tribunal (art. 100, §14).</li>
</ol>
<p>Como na fila e no acordo direto, a antecipação tem um custo: o <a href="/blog/desagio-precatorio/">deságio</a>, que varia conforme o devedor, o valor e o tempo estimado de espera. A diferença é que <strong>você sabe o valor e a data antes de decidir</strong>. Compare as três opções:</p>
<div class="table-wrap"><table>
<tr><th></th><th>Esperar a fila</th><th>Acordo direto</th><th>Vender o precatório</th></tr>
<tr><td><strong>Quanto recebe</strong></td><td>Valor integral corrigido</td><td>Até 40% a menos</td><td>Valor da proposta aceita</td></tr>
<tr><td><strong>Quando</strong></td><td>Incerto, pode levar anos</td><td>Só se houver edital e verba</td><td>Até 72 h após a cessão assinada</td></tr>
<tr><td><strong>Quem decide</strong></td><td>Orçamento e ordem da fila</td><td>Edital do tribunal</td><td>Você, com a proposta em mãos</td></tr>
</table></div>
<p>Antes de decidir, desconfie de quem pede pagamento antecipado para “liberar” o seu precatório; veja <a href="/blog/golpe-do-precatorio/">como evitar o golpe do precatório</a>. E se você tem 60 anos ou mais ou doença grave, confira primeiro se tem direito à superpreferência, que é pessoal e não passa para quem compra.</p>

<h2>Conclusão</h2>
<p>Seja qual for o resultado das urnas, <strong>a fila dos precatórios do RN e de Natal continuará presa ao limite constitucional e à arrecadação</strong>. Entender essas regras ajuda a não criar expectativa com promessas e a escolher com calma entre esperar, aderir a um edital ou antecipar. Se você quer saber quanto receberia hoje, faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a> ou peça uma simulação à nossa equipe. Veja também como <a href="/vender-precatorio-rn/">vender precatório no RN</a>, as regras do <a href="/vender-precatorio-estadual/">precatório estadual</a>, do <a href="/vender-precatorio-municipal/">precatório municipal</a> e do <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</p>
""",
  cta=("Quer previsibilidade, seja qual for o governo?","Envie o número do processo e receba uma simulação por escrito, transparente e sem compromisso.","Olá! Tenho um precatório do RN/Natal e quero uma simulação."),
  related=["precatorios-2027-ec-136","vale-a-pena-vender-precatorio","desagio-precatorio"],
))
BY = {p["slug"]: p for p in POSTS}

def autora_ld():
    d = {"@type":"Person","@id":SITE+AUTORA_URL+"#pessoa","name":AUTORA["nome"],"honorificPrefix":AUTORA["tratamento"],
         "jobTitle":AUTORA["cargo"],"url":SITE+AUTORA_URL,"worksFor":{"@id":SITE+"/#empresa"}}
    if AUTORA["oab"]: d["identifier"] = AUTORA["oab"]
    if AUTORA["foto"]: d["image"] = SITE + AUTORA["foto"]
    if AUTORA["same_as"]: d["sameAs"] = AUTORA["same_as"]
    return d

def build_post(p):
    url = f"{SITE}/blog/{p['slug']}/"
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"Article","headline":p["title"],"description":p["desc"],"dateModified":UPDATED,"datePublished":UPDATED,
       "author":autora_ld(),"publisher":{"@type":"Organization","@id":SITE+"/#empresa","name":"Antecipay Precatórios","logo":{"@type":"ImageObject","url":SITE+"/logo-512.png"}},
       "mainEntityOfPage":url,"image":SITE+"/og.png"},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Início","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
        {"@type":"ListItem","position":3,"name":p["title"],"item":url}]}]}
    ldtag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    words = len((p["body"]).split())
    mins = max(3, round(words/200))
    faq_html = "<h2>Perguntas frequentes</h2>" + "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in p["faq"])
    rel = "".join(f'<a class="card" href="/blog/{s}/"><span class="tag">{BY[s]["tag"]}</span><h3>{BY[s]["title"]}</h3><span class="more">Ler artigo →</span></a>' for s in p["related"])
    out = head(p["seo"], p["desc"], url, ldtag) + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head">
  <div class="narrow">
    <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <a href="/blog/">Blog</a></nav>
    <span class="eyebrow">{p['tag']}</span>
    <h1>{p['title']}</h1>
    <p class="lead">{p['lead']}</p>
    <p class="meta">Por <a href="{AUTORA_URL}">{AUTORA['tratamento']} {AUTORA['nome']}</a>, {AUTORA['cargo'].lower()} · Atualizado em {UPDATED_BR} · {mins} min de leitura</p>
  </div>
</section>
<article class="narrow">
  <div class="answer"><strong>Resposta rápida</strong>{p['answer']}</div>
  {p['body']}
  {cta(*p['cta'])}
  {faq_html}
  {NOTE}
</article>
<section class="related"><div class="narrow"><h2>Leia também</h2><div class="grid">{rel}</div></div></section>
</main>
""" + FOOT
    os.makedirs(f"blog/{p['slug']}", exist_ok=True)
    open(f"blog/{p['slug']}/index.html","w").write(out)

def build_index():
    url = SITE + "/blog/"
    ld = {"@context":"https://schema.org","@type":"Blog","name":"Blog da Antecipay","url":url,
          "blogPost":[{"@type":"BlogPosting","headline":p["title"],"url":f"{url}{p['slug']}/"} for p in POSTS]}
    cards = "".join(f'<a class="card" href="/blog/{p["slug"]}/"><span class="tag">{p["tag"]}</span><h2>{p["title"]}</h2><p>{p["desc"]}</p><span class="more">Ler artigo →</span></a>' for p in POSTS)
    out = head("Blog sobre precatórios: guias e prazos | Antecipay", "Guias simples sobre precatório e RPV: prazos de pagamento, como consultar se você tem um precatório, deságio, cessão e como vender com segurança.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>') + f"""
<main id="conteudo" tabindex="-1">
<section class="hero"><div class="wrap">
  <span class="eyebrow">Blog</span>
  <h1>Tudo sobre precatórios, sem juridiquês</h1>
  <p>Guias diretos para quem tem valores a receber do governo: prazos, consulta, RPV e antecipação.</p>
</div></section>
<section class="posts"><div class="wrap grid">{cards}</div></section>
<section style="padding:0 0 120px"><div class="narrow">
  <h2 style="font-size:1.6rem;margin-bottom:16px">Por onde começar</h2>
  <p style="margin-bottom:16px">Se você ganhou uma ação contra a União, o INSS, um estado ou uma prefeitura, o pagamento sai por RPV ou por precatório. A RPV é paga em poucos meses. O precatório entra numa fila que pode levar de um ano e meio, nos federais, a vários anos, nos estaduais e municipais. Os guias deste blog explicam cada etapa em linguagem simples, para você saber o que esperar e tomar decisões com segurança.</p>
  <p style="margin-bottom:16px">Comece por <a href="/blog/o-que-e-precatorio-e-rpv/">o que é precatório e RPV</a> e veja <a href="/blog/como-saber-se-tenho-precatorio/">como consultar se você tem um precatório</a>. Para entender quando o dinheiro deve chegar, leia <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>. Se a ação foi contra o INSS, há um guia específico sobre o <a href="/blog/precatorio-inss/">precatório do INSS</a>.</p>
  <p style="margin-bottom:16px">Quem não quer esperar pode vender o precatório. Antes de decidir, entenda o <a href="/blog/desagio-precatorio/">deságio</a>, faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a> e confira <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa</a> e <a href="/blog/como-vender-precatorio/">como vender com segurança</a>, sem cair em golpes.</p>
  <h2 style="font-size:1.6rem;margin:40px 0 16px">Vender por tipo de precatório</h2>
  <ul style="margin:0 0 16px 22px;display:grid;gap:8px">
    <li><a href="/vender-precatorio-inss/">Precatório do INSS</a>: atrasados de aposentadoria, auxílio, BPC e revisões.</li>
    <li><a href="/vender-precatorio-federal/">Precatório federal</a>: dívidas da União e de autarquias federais.</li>
    <li><a href="/vender-precatorio-estadual/">Precatório estadual</a>: dívidas dos estados, como diferenças salariais de servidores.</li>
    <li><a href="/vender-precatorio-municipal/">Precatório municipal</a>: dívidas de prefeituras de todo o Brasil.</li>
    <li><a href="/vender-precatorio-rn/">Precatório no RN</a>: TRF5, Estado do RN e prefeituras potiguares.</li>
  </ul>
  <p>A Antecipay é uma empresa de Natal-RN que compra precatórios de credores de todo o Brasil. Conheça mais <a href="/sobre/">sobre a Antecipay</a> ou fale com a nossa equipe pelo WhatsApp (84) 99493-8383.</p>
</div></section>
</main>
""" + FOOT
    os.makedirs("blog", exist_ok=True)
    open("blog/index.html","w").write(out)


def build_autora():
    a = AUTORA
    url = SITE + AUTORA_URL
    nome = f"{a['tratamento']} {a['nome']}"
    ld = {"@context":"https://schema.org","@type":"ProfilePage","url":url,"name":nome,"mainEntity":autora_ld()}
    foto = f'<img src="{a["foto"]}" alt="{html.escape(nome)}" width="160" height="160" style="border-radius:50%;margin-bottom:16px">' if a["foto"] else ""
    oab = f" · {a['oab']}" if a["oab"] else ""
    bio = f"<p>{html.escape(a['bio'])}</p>" if a["bio"] else ""
    perfis = ("<p>Perfis: " + ", ".join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(u.split("//")[-1].rstrip("/"))}</a>' for u in a["same_as"]) + "</p>") if a["same_as"] else ""
    artigos = "".join(f'<li><a href="/blog/{p["slug"]}/">{p["title"]}</a></li>' for p in POSTS)
    out = head(f"{nome}, advogada da Antecipay Precatórios",
               f"{nome} é advogada da Antecipay Precatórios, de Natal-RN, e assina os guias do blog sobre precatórios, RPV, cessão e consulta nos tribunais.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <a href="/sobre/">Sobre</a> <span aria-hidden="true">›</span> <span aria-current="page">{a['nome']}</span></nav>
  <span class="eyebrow">Equipe</span>
  {foto}
  <h1>{nome}</h1>
  <p class="lead">{a['cargo']} da Antecipay Precatórios{oab}</p>
</div></section>
<article class="narrow">
  {bio}
  <h2>Na Antecipay</h2>
  <p>{nome} é advogada da <a href="/sobre/">Antecipay Precatórios</a>, empresa de Natal-RN que compra precatórios federais, estaduais e municipais de credores de todo o Brasil. Ela assina os guias do blog, escritos para quem tem um precatório ou uma RPV a receber e quer entender o processo sem juridiquês.</p>
  <h2>Como trabalhamos</h2>
  <ul>
    <li><strong>Proposta por escrito</strong>, com o valor líquido, antes de qualquer assinatura.</li>
    <li><strong>Cessão de crédito</strong> nos termos do art. 100, §13, da Constituição, comunicada ao tribunal e ao devedor.</li>
    <li><strong>Nenhuma cobrança antecipada</strong> do credor.</li>
    <li><strong>Pagamento em até 72 horas</strong> depois da proposta aprovada e da cessão assinada.</li>
  </ul>
  <p>Veja como <a href="/">vender precatório</a> com a Antecipay, ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
  {perfis}
  <h2>Artigos</h2>
  <ul>{artigos}</ul>
  {cta("Tem um precatório?", "Envie o número do processo e receba uma proposta por escrito.", "Olá! Vim pelo site da Antecipay e quero uma proposta para o meu precatório.")}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs(AUTORA_URL.strip("/"), exist_ok=True)
    open(AUTORA_URL.strip("/") + "/index.html","w").write(out)

def build_sobre():
    url = SITE + "/sobre/"
    ld = {"@context":"https://schema.org","@type":"AboutPage","url":url,"name":"Sobre a Antecipay",
      "mainEntity":{"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","logo":SITE+"/logo-512.png","taxID":"64.382.432/0001-97",
        "url":SITE+"/","email":"contato@antecipay.com.br","telephone":"+55-84-99493-8383",
        "description":"Empresa que compra e antecipa precatórios federais, estaduais e municipais em todo o Brasil.",
        "areaServed":{"@type":"Country","name":"Brasil"},
        "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"},
        "knowsAbout":["Precatórios","RPV","Cessão de crédito","Precatórios do INSS","Precatórios federais","Precatórios estaduais","Precatórios municipais"],
        "sameAs":SAME_AS,"employee":{"@id":SITE+AUTORA_URL+"#pessoa"}}}
    out = head("O que é a Antecipay Precatórios? Quem somos e CNPJ", "A Antecipay Precatórios é uma empresa de Natal-RN que compra precatórios federais, estaduais e municipais. Veja quem somos, a nossa advogada e o CNPJ.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="sobre") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Sobre</span></nav>
  <span class="eyebrow">Sobre nós</span>
  <h1>O que é a Antecipay Precatórios</h1>
  <p class="lead">A Antecipay compra e antecipa precatórios federais, estaduais e municipais. Quem tem valores a receber do governo recebe à vista, sem esperar a fila de pagamentos.</p>
</div></section>
<article class="narrow">
  <div class="answer"><strong>Em resumo</strong>A Antecipay Precatórios (CNPJ 64.382.432/0001-97) é uma empresa sediada em Natal-RN que compra precatórios de credores de todo o Brasil. O credor vende o seu precatório por meio de um contrato de cessão de crédito e recebe o pagamento à vista. O atendimento é 100% digital, pelo WhatsApp (84) 99493-8383.</div>

  <h2>O que fazemos</h2>
  <p>Compramos precatórios devidos pela União, pelo INSS e outras autarquias federais, pelos Estados e pelos Municípios. Em vez de esperar meses ou anos pelo pagamento do governo, o credor recebe agora um valor à vista, combinado em proposta por escrito.</p>

  <h2>Como funciona a antecipação</h2>
  <ol>
    <li><strong>Contato:</strong> o credor envia o número do processo pelo WhatsApp.</li>
    <li><strong>Análise:</strong> nossa equipe jurídica analisa o processo e a situação do precatório.</li>
    <li><strong>Proposta:</strong> apresentamos por escrito o valor líquido que o credor vai receber.</li>
    <li><strong>Cessão e pagamento:</strong> com a proposta aceita, assinamos o contrato de cessão de crédito e o valor é pago ao credor.</li>
  </ol>
  <p>A venda de precatórios é permitida pela Constituição Federal (art. 100, §13) e é formalizada por contrato de cessão, comunicado ao tribunal.</p>

  <h2>Números</h2>
  <ul>
    <li>Mais de 500 precatórios antecipados.</li>
    <li>98% de clientes satisfeitos.</li>
    <li>Pagamento em até 72 horas após a proposta aprovada e a cessão assinada.</li>
  </ul>

  <h2>Onde atuamos</h2>
  <p>Atendemos credores de <strong>todo o Brasil</strong>, com processos em qualquer tribunal federal (TRF1 a TRF6) ou estadual. Nossa sede fica em Natal, no Rio Grande do Norte.</p>
  <p>A Antecipay Precatórios não tem relação com a AnteciPay, da Ecx Pay, que é outra empresa.</p>

  <h2>Equipe jurídica</h2>
  <p>A análise jurídica dos precatórios e a revisão dos conteúdos do blog ficam com a <a href="{AUTORA_URL}">{AUTORA['tratamento']} {AUTORA['nome']}</a>, advogada da Antecipay.</p>

  <h2>Dados da empresa</h2>
  <div class="table-wrap"><table>
    <tr><td><strong>Razão social</strong></td><td>Antecipay Precatórios</td></tr>
    <tr><td><strong>CNPJ</strong></td><td>64.382.432/0001-97</td></tr>
    <tr><td><strong>Endereço</strong></td><td>Av. Senador Salgado Filho, 1559 – Tirol, Incubadora do IFRN – Campus Natal Central, Natal-RN, CEP 59015-000</td></tr>
    <tr><td><strong>WhatsApp</strong></td><td>(84) 99493-8383</td></tr>
    <tr><td><strong>E-mail</strong></td><td>contato@antecipay.com.br</td></tr>
    <tr><td><strong>Site</strong></td><td>antecipayprecatorios.com.br</td></tr>
    <tr><td><strong>Instagram</strong></td><td><a href="https://www.instagram.com/antecipayprecatorios/" target="_blank" rel="noopener">@antecipayprecatorios</a></td></tr>
  </table></div>

  {cta("Quer antecipar o seu precatório?", "Envie o número do processo e receba uma proposta por escrito.", "Olá! Vim pela página Sobre e quero uma proposta para o meu precatório.")}

  <h2>Aprenda mais</h2>
  <ul>
    <li><a href="/blog/o-que-e-precatorio-e-rpv/">O que é precatório e RPV</a></li>
    <li><a href="/blog/quanto-tempo-demora-precatorio/">Quanto tempo demora para receber um precatório</a></li>
    <li><a href="/blog/como-saber-se-tenho-precatorio/">Como saber se tenho precatório a receber</a></li>
    <li><a href="/blog/desagio-precatorio/">Deságio: por que recebo menos ao antecipar</a></li>
  </ul>
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs("sobre", exist_ok=True)
    open("sobre/index.html","w").write(out)

def build_llms():
    t = f"""# Antecipay Precatórios

> Empresa brasileira que compra e antecipa precatórios federais, estaduais e municipais em todo o Brasil. O credor vende o precatório por contrato de cessão de crédito e recebe à vista. Sede em Natal-RN. CNPJ 64.382.432/0001-97.

- Atendimento: 100% digital, pelo WhatsApp (84) 99493-8383 ou contato@antecipay.com.br
- Endereço: Av. Senador Salgado Filho, 1559 – Tirol, Incubadora do IFRN – Campus Natal Central, Natal-RN, CEP 59015-000
- Área de atuação: todo o Brasil (precatórios da União, INSS, Estados e Municípios)
- Como funciona: envio do número do processo → análise jurídica → proposta por escrito com valor líquido → contrato de cessão e pagamento
- Base legal: art. 100, §13, da Constituição Federal permite a cessão de precatórios
- Horário: segunda a sexta, 8h às 18h; sábado, 8h às 12h
- Pagamento: em até 72 horas após a proposta aprovada e o contrato de cessão assinado
- Não confundir: a Antecipay Precatórios não tem relação com a AnteciPay, da Ecx Pay

## Páginas principais

- [Início]({SITE}/): apresentação, simulador e contato
- [Sobre a Antecipay]({SITE}/sobre/): quem somos, dados da empresa e como funciona
- [Calculadora de precatório]({SITE}/calculadora-precatorio/): estimativa de quanto vale o precatório à vista
- [Vender precatório trabalhista]({SITE}/vender-precatorio-trabalhista/): compra de precatórios de ações trabalhistas contra órgãos públicos
- [Compra e antecipação de precatório]({SITE}/antecipacao-de-precatorio/): como funciona a compra de precatório, diferença para empréstimo e antecipação parcial
- [Precatório federal]({SITE}/vender-precatorio-federal/): prazo de pagamento e venda de precatórios da União
- [Vender precatório estadual]({SITE}/vender-precatorio-estadual/): compra de precatórios de estados
- [Vender precatório municipal]({SITE}/vender-precatorio-municipal/): compra de precatórios de prefeituras
- [Qual a melhor empresa para vender precatório]({SITE}/melhor-empresa-para-vender-precatorio/): 7 pontos para escolher com segurança
- [Vender precatório do INSS]({SITE}/vender-precatorio-inss/): compra e antecipação de precatórios do INSS
- [Vender precatório no RN]({SITE}/vender-precatorio-rn/): precatórios do TRF5 e do TJRN (Estado do RN e municípios)
- [Empresa que compra precatórios em Natal]({SITE}/empresa-que-compra-precatorio-natal/): sede, contato e atendimento em Natal-RN
""" + "".join(f"- [Empresa que compra precatórios {e['em']}]({SITE}/{e['slug']}/): precatórios do {e['tj']} e do {e['trf']}, atendimento 100% digital\n" for e in ESTADOS) + f"""- [{AUTORA['tratamento']} {AUTORA['nome']}]({SITE}{AUTORA_URL}): advogada da Antecipay, autora dos guias do blog
- [Blog]({SITE}/blog/): guias sobre precatórios

## Guias

""" + "".join(f"- [{p['title']}]({SITE}/blog/{p['slug']}/): {p['desc']}\n" for p in POSTS)
    open("llms.txt","w").write(t)

def build_inss():
    url = SITE + "/vender-precatorio-inss/"
    faq=[("Posso vender o precatório do INSS?","Sim. A Constituição permite ceder o precatório a terceiros. A venda é feita por contrato de cessão de crédito, comunicado ao tribunal."),
         ("Quanto recebo ao vender o precatório do INSS?","Depende do valor, do prazo previsto de pagamento e da situação do processo. A Antecipay apresenta a proposta por escrito, com o valor líquido, antes de qualquer assinatura."),
         ("Preciso ir até um escritório?","Não. O atendimento é 100% digital, pelo WhatsApp."),
         ("Quem tem prioridade por idade ou doença deve vender?","A prioridade é pessoal e não passa para quem compra. Nesses casos, avaliamos com você se vale antecipar todo o crédito ou só a parte que ficaria na fila.")]
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":"Compra e antecipação de precatório do INSS","serviceType":"Antecipação de precatório","areaServed":{"@type":"Country","name":"Brasil"},
         "provider":{"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png"},"url":url},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in faq)
    out = head("Vender precatório do INSS: receba à vista | Antecipay", "Venda o seu precatório do INSS e receba à vista, sem esperar a fila da União. Análise do processo, proposta por escrito e atendimento 100% digital.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Precatório do INSS</span></nav>
  <span class="eyebrow">INSS</span>
  <h1>Venda o seu precatório do INSS e receba à vista</h1>
  <p class="lead">Ganhou uma ação de aposentadoria, auxílio, BPC ou revisão e está esperando o precatório? A Antecipay compra o seu crédito e você recebe agora, sem esperar a fila da União.</p>
  <p class="ctas"><a class="btn btn-wa" href="{wa('Olá! Tenho um precatório do INSS e quero uma proposta.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a><a class="btn btn-tel" href="tel:+5584994938383" aria-label="Ligar para (84) 99493-8383">{TEL_ICON}Ligar</a></p>
</div></section>
<article class="narrow">
  <div class="answer"><strong>Em resumo</strong>A Antecipay compra precatórios do INSS de credores de todo o Brasil. Você envia o número do processo, nossa equipe jurídica analisa, apresenta uma proposta por escrito com o valor líquido e, com a cessão assinada, você recebe à vista.</div>
  <h2>Para quem é</h2>
  <ul>
    <li>Quem ganhou ação contra o INSS e teve o precatório expedido ou está perto disso.</li>
    <li>Quem não quer esperar meses ou anos pelo pagamento da União.</li>
    <li>Quem precisa do dinheiro agora para quitar dívidas, investir ou realizar um plano.</li>
  </ul>
  <h2>Como funciona</h2>
  <ol>
    <li><strong>Envie o número do processo</strong> pelo WhatsApp.</li>
    <li><strong>Análise jurídica:</strong> verificamos o precatório, o valor, os descontos e o prazo previsto.</li>
    <li><strong>Proposta por escrito</strong>, com o valor líquido que você recebe.</li>
    <li><strong>Cessão e pagamento:</strong> assinamos o contrato de cessão de crédito e o valor é pago a você.</li>
  </ol>
  <h2>Por que vender com a Antecipay</h2>
  <ul>
    <li><strong>Transparência:</strong> proposta por escrito, sem letras miúdas.</li>
    <li><strong>Agilidade:</strong> pagamento em até 72 horas após a proposta aprovada e a cessão assinada.</li>
    <li><strong>Segurança jurídica:</strong> equipe especializada e cessão formalizada no tribunal.</li>
    <li><strong>100% digital:</strong> atendimento pelo WhatsApp, de qualquer lugar do Brasil.</li>
  </ul>
  <h2>Antes de decidir</h2>
  <p>Se você tem 60 anos ou mais, doença grave ou deficiência, pode ter direito a <a href="/blog/superpreferencia-precatorio/">receber antes uma parte do crédito</a>. Essa prioridade não passa para quem compra, então avaliamos com você a melhor opção. Para estimar o valor, use a <a href="/calculadora-precatorio/">calculadora de precatório</a>. Entenda mais em <a href="/blog/precatorio-inss/">Precatório do INSS: como funciona e quanto tempo demora</a> e em <a href="/blog/desagio-precatorio/">Deságio: por que recebo menos ao antecipar</a>.</p>
  <p>Tem precatório de outro devedor? Veja <a href="/vender-precatorio-federal/">precatório federal</a>, <a href="/vender-precatorio-estadual/">precatório estadual</a> e <a href="/vender-precatorio-municipal/">precatório municipal</a>, ou a página principal sobre como <a href="/">vender precatório</a>. Também compramos <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</p>
  {cta("Receba uma proposta para o seu precatório do INSS", "Envie o número do processo pelo WhatsApp.", "Olá! Tenho um precatório do INSS e quero uma proposta.")}
  <h2>Perguntas frequentes</h2>
  {faq_html}
  {NOTE}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs("vender-precatorio-inss", exist_ok=True)
    open("vender-precatorio-inss/index.html","w").write(out)

def build_rn():
    url = SITE + "/vender-precatorio-rn/"
    faq=[("A Antecipay compra precatório do Rio Grande do Norte?","Sim. Compramos precatórios federais do TRF5 (como os do INSS e da União) e precatórios estaduais e municipais do TJRN, devidos pelo Estado do RN e pelas prefeituras."),
         ("Onde consulto meu precatório no RN?","Precatórios federais: no portal de RPV e precatórios do TRF5, pelo CPF ou número do processo. Estaduais e municipais: na área de precatórios do site do TJRN."),
         ("Quanto tempo demora o precatório do Estado ou de um município do RN?","Depende de quanto cada ente reserva por ano para pagar precatórios e da sua posição na fila. Pelas regras atuais, estados e municípios pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, e a espera pode levar anos."),
         ("Preciso ir até o escritório em Natal?","Não. O atendimento é 100% digital, pelo WhatsApp. Se preferir, nossa sede fica na Incubadora do IFRN – Campus Natal Central.")]
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":"Compra de precatórios no Rio Grande do Norte","serviceType":"Antecipação de precatório",
         "areaServed":[{"@type":"State","name":"Rio Grande do Norte"},{"@type":"City","name":"Natal"}],
         "provider":{"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png",
           "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"}},"url":url},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in faq)
    out = head("Vender precatório no RN (TRF5 e TJRN) | Antecipay", "Venda seu precatório federal (TRF5), estadual ou municipal do Rio Grande do Norte e receba à vista. Empresa de Natal-RN, atendimento 100% digital.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Precatório no RN</span></nav>
  <span class="eyebrow">Rio Grande do Norte</span>
  <h1>Venda o seu precatório no Rio Grande do Norte</h1>
  <p class="lead">Tem valores a receber da União, do INSS, do Estado do RN ou de uma prefeitura potiguar? A Antecipay, empresa de Natal, compra o seu precatório e você recebe à vista.</p>
  <p class="ctas"><a class="btn btn-wa" href="{wa('Olá! Tenho um precatório no RN e quero uma proposta.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a><a class="btn btn-tel" href="tel:+5584994938383" aria-label="Ligar para (84) 99493-8383">{TEL_ICON}Ligar</a></p>
</div></section>
<article class="narrow">
  <div class="answer"><strong>Em resumo</strong>A Antecipay Precatórios, sediada em Natal-RN, compra precatórios federais do TRF5 (União e INSS) e precatórios estaduais e municipais do TJRN. Você envia o número do processo, recebe uma proposta por escrito e, com a cessão assinada, recebe à vista.</div>

  <h2>Quais precatórios do RN compramos</h2>
  <div class="table-wrap"><table>
    <tr><th>Tipo</th><th>Quem deve</th><th>Tribunal</th></tr>
    <tr><td><strong>Federal</strong></td><td>União, INSS, universidades e autarquias federais</td><td>TRF5</td></tr>
    <tr><td><strong>Estadual</strong></td><td>Estado do Rio Grande do Norte e suas autarquias</td><td>TJRN</td></tr>
    <tr><td><strong>Municipal</strong></td><td>Natal, Mossoró, Parnamirim e demais prefeituras do RN</td><td>TJRN</td></tr>
  </table></div>

  <h2>Quanto tempo você esperaria</h2>
  <ul>
    <li><strong>Federal (TRF5):</strong> precatórios inscritos até 1º de fevereiro são pagos até o fim do ano seguinte. Veja o caso do <a href="/vender-precatorio-inss/">precatório do INSS</a>.</li>
    <li><strong>Estadual e municipal (TJRN):</strong> o pagamento depende do limite anual que cada ente reserva para a fila, entre 1% e 5% da receita. A espera costuma ser bem maior e varia de um devedor para outro.</li>
  </ul>
  <p>Mais detalhes em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora para receber um precatório</a>.</p>

  <h2>Como consultar o seu precatório no RN</h2>
  <ul>
    <li><strong>Federal:</strong> no portal de RPV e precatórios do TRF5, pelo CPF ou pelo número do processo.</li>
    <li><strong>Estadual ou municipal:</strong> na área de precatórios do site do TJRN.</li>
  </ul>
  <p>Passo a passo completo em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>. Se preferir, envie o número do processo que a nossa equipe consulta para você. Precatórios federais do RN são pagos pelo TRF5: veja <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5 pelo CPF</a>.</p>
  <p>Antes de decidir, veja <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa para vender o precatório</a> e o guia <a href="/blog/empresas-que-compram-precatorios-natal/">como escolher empresa de precatório em Natal</a>. Para precatórios de outros estados, veja como <a href="/">vender precatório</a> em todo o Brasil.</p>

  <h2>Como funciona a venda</h2>
  <ol>
    <li><strong>Envie o número do processo</strong> pelo WhatsApp.</li>
    <li><strong>Análise jurídica</strong> do precatório, do valor e do prazo previsto.</li>
    <li><strong>Proposta por escrito</strong>, com o valor líquido que você recebe.</li>
    <li><strong>Cessão e pagamento:</strong> assinamos o contrato de cessão de crédito e o valor é pago a você.</li>
  </ol>

  <h2>Empresa daqui</h2>
  <p>A Antecipay tem sede em Natal, na Incubadora do IFRN – Campus Natal Central (Av. Senador Salgado Filho, 1559 – Tirol). O atendimento é 100% digital, então você resolve tudo pelo WhatsApp, de qualquer cidade do estado. Conheça mais <a href="/sobre/">sobre a Antecipay</a> e a nossa página de <a href="/empresa-que-compra-precatorio-natal/">empresa que compra precatórios em Natal</a>.</p>

  {cta("Tem precatório no RN?", "Envie o número do processo e receba uma proposta por escrito.", "Olá! Tenho um precatório no RN e quero uma proposta.")}
  <h2>Perguntas frequentes</h2>
  {faq_html}
  {NOTE}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs("vender-precatorio-rn", exist_ok=True)
    open("vender-precatorio-rn/index.html","w").write(out)

def build_natal():
    url = SITE + "/empresa-que-compra-precatorio-natal/"
    faq=[("Qual empresa compra precatório em Natal?","A Antecipay Precatórios é uma empresa com sede em Natal-RN que compra precatórios federais, estaduais e municipais. O atendimento é pelo WhatsApp (84) 99493-8383."),
         ("Onde fica a Antecipay em Natal?","Na Incubadora do IFRN – Campus Natal Central, Av. Senador Salgado Filho, 1559 – Tirol, Natal-RN, CEP 59015-000. O atendimento é 100% digital."),
         ("A Antecipay compra precatório da Prefeitura de Natal?","Sim. Compramos precatórios devidos pela Prefeitura de Natal e por outros municípios do RN, além de precatórios do Estado do RN, da União e do INSS."),
         ("Quanto tempo leva para receber?","Depois da proposta aprovada e do contrato de cessão assinado, o pagamento é feito em até 72 horas.")]
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","url":SITE+"/","logo":SITE+"/logo-512.png","image":SITE+"/logo-512.png",
         "telephone":"+55-84-99493-8383","email":"contato@antecipay.com.br","taxID":"64.382.432/0001-97",
         "description":"Empresa de Natal-RN que compra precatórios federais, estaduais e municipais.","sameAs":SAME_AS,
         "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"},
         "areaServed":[{"@type":"City","name":"Natal"},{"@type":"State","name":"Rio Grande do Norte"},{"@type":"Country","name":"Brasil"}],
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"08:00","closes":"12:00"}]},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in faq)
    out = head("Empresa que compra precatórios em Natal-RN | Antecipay", "A Antecipay é uma empresa de Natal-RN que compra precatórios federais, do INSS, do Estado do RN e da Prefeitura de Natal. Proposta por escrito e à vista.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Natal-RN</span></nav>
  <span class="eyebrow">Natal-RN</span>
  <h1>Empresa que compra precatórios em Natal</h1>
  <p class="lead">A Antecipay é uma empresa de Natal que compra precatórios da União, do INSS, do Estado do RN e da Prefeitura de Natal. Você recebe à vista, com proposta por escrito e segurança jurídica.</p>
  <p class="ctas"><a class="btn btn-wa" href="{wa('Olá! Sou de Natal e quero vender meu precatório.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a><a class="btn btn-tel" href="tel:+5584994938383" aria-label="Ligar para (84) 99493-8383">{TEL_ICON}Ligar</a></p>
</div></section>
<article class="narrow">
  <div class="answer"><strong>Em resumo</strong>A Antecipay Precatórios (CNPJ 64.382.432/0001-97) tem sede em Natal, na Incubadora do IFRN – Campus Natal Central, e compra precatórios federais, estaduais e municipais. Atendimento pelo WhatsApp (84) 99493-8383, de segunda a sexta, das 8h às 18h, e aos sábados, das 8h às 12h.</div>

  <h2>Precatórios que compramos em Natal</h2>
  <div class="table-wrap"><table>
    <tr><th>Devedor</th><th>Tribunal</th></tr>
    <tr><td>União, INSS e autarquias federais</td><td>TRF5 – Seção Judiciária do RN</td></tr>
    <tr><td>Estado do Rio Grande do Norte</td><td>TJRN</td></tr>
    <tr><td>Prefeitura de Natal e demais municípios do RN</td><td>TJRN</td></tr>
  </table></div>
  <p>Também atendemos credores de todo o Brasil, como os de <a href="/empresa-que-compra-precatorio-sao-paulo/">São Paulo</a>, da <a href="/empresa-que-compra-precatorio-paraiba/">Paraíba</a>, de <a href="/empresa-que-compra-precatorio-pernambuco/">Pernambuco</a> e do <a href="/empresa-que-compra-precatorio-ceara/">Ceará</a>. Veja como <a href="/">vender precatório</a> de qualquer tribunal, <a href="/vender-precatorio-rn/">vender precatório no RN</a> e <a href="/vender-precatorio-inss/">vender precatório do INSS</a>.</p>

  <h2>Por que vender para uma empresa de Natal</h2>
  <ul>
    <li><strong>Empresa daqui:</strong> sede em Natal, endereço que você pode conferir.</li>
    <li><strong>Proposta por escrito</strong>, com o valor líquido, antes de qualquer assinatura.</li>
    <li><strong>Pagamento em até 72 horas</strong> depois da proposta aprovada e da cessão assinada.</li>
    <li><strong>100% digital:</strong> você resolve pelo WhatsApp, sem sair de casa.</li>
    <li><strong>Nenhuma cobrança antecipada.</strong></li>
  </ul>

  <h2>Como funciona</h2>
  <ol>
    <li>Envie o número do processo pelo WhatsApp.</li>
    <li>Nossa equipe jurídica analisa o precatório.</li>
    <li>Você recebe a proposta por escrito.</li>
    <li>Assinamos o contrato de cessão e o valor é pago à vista.</li>
  </ol>

  <h2>Antes de decidir</h2>
  <p>Compare propostas e confira os pontos de segurança no guia <a href="/blog/empresas-que-compram-precatorios-natal/">como escolher empresa de precatório em Natal</a> e em <a href="/melhor-empresa-para-vender-precatorio/">qual a melhor empresa para vender precatório</a>. Credores da Prefeitura de Natal também podem avaliar o acordo direto oferecido pelo município.</p>

  <h2>Onde estamos</h2>
  <p><strong>Antecipay Precatórios</strong><br>Av. Senador Salgado Filho, 1559 – Tirol<br>Incubadora do IFRN – Campus Natal Central<br>Natal-RN, CEP 59015-000<br>WhatsApp (84) 99493-8383 · contato@antecipay.com.br</p>

  {cta("Quer vender seu precatório em Natal?", "Envie o número do processo e receba uma proposta por escrito.", "Olá! Sou de Natal e quero vender meu precatório.")}
  <h2>Perguntas frequentes</h2>
  {faq_html}
  {NOTE}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs("empresa-que-compra-precatorio-natal", exist_ok=True)
    open("empresa-que-compra-precatorio-natal/index.html","w").write(out)

# Páginas por estado no modelo da página de Natal. A empresa não tem escritório
# nesses estados: o texto deixa claro que a sede é em Natal e o atendimento é digital.
ESTADOS = [
    {"slug":"empresa-que-compra-precatorio-sao-paulo","uf":"SP","nome":"São Paulo","em":"em São Paulo","de":"de São Paulo","capital":"São Paulo",
     "seo":"Empresa que compra precatórios em São Paulo | Antecipay",
     "desc":"A Antecipay compra precatórios do Estado de SP, da Prefeitura de São Paulo e de outros municípios paulistas (TJSP), e federais do TRF3. Pagamento à vista.",
     "lead":"Tem precatório do Estado de São Paulo, da Prefeitura de São Paulo, de outro município paulista, da União ou do INSS? A Antecipay compra o seu precatório e você recebe à vista, com proposta por escrito.",
     "trf":"TRF3","trf_ufs":"São Paulo e Mato Grosso do Sul","tj":"TJSP",
     "devedores":[("União, INSS e autarquias federais","TRF3"),("Estado de São Paulo e autarquias estaduais","TJSP"),("Prefeitura de São Paulo e demais municípios paulistas","TJSP")],
     "consulta":"""<ul>
    <li><strong>Estadual ou municipal (TJSP):</strong> na página de precatórios do tribunal (tjsp.jus.br/precatorios), no menu Credores, a “Lista de Precatórios Disponibilizados e Pendentes de Pagamentos” mostra a posição na fila. Quem administra os pagamentos é a Depre, a Diretoria de Execuções de Precatórios e Cálculos.</li>
    <li><strong>Federal (TRF3):</strong> na consulta de requisições de pagamento do TRF3, pelo CPF do beneficiário ou pelo número do processo.</li>
  </ul>
  <p>Passo a passo em <a href="/blog/consultar-precatorio-tjsp/">como consultar precatório no TJSP</a> e <a href="/blog/consultar-rpv-precatorio-trf3/">como consultar RPV e precatório no TRF3</a>.</p>""",
     "extra":"""<h2>Por que tantos credores paulistas vendem o precatório</h2>
  <p>São Paulo concentra muitos precatórios do país, e a fila do Estado e de várias prefeituras paulistas é longa. Pelas regras atuais, estados e municípios pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho da dívida. Na prática, quem está no fim da fila pode esperar anos. Vender o precatório troca essa espera por um valor à vista.</p>""",
     "faq":[("A Antecipay compra precatório do Estado de São Paulo?","Sim. Compramos precatórios do Estado de São Paulo e de suas autarquias, da Prefeitura de São Paulo e de outros municípios paulistas, todos pagos pelo TJSP, além de precatórios federais do TRF3."),
            ("A Antecipay tem escritório em São Paulo?","Não. A sede é em Natal-RN, na Incubadora do IFRN, e o atendimento é 100% digital. Credores de São Paulo enviam o número do processo pelo WhatsApp e assinam a cessão sem sair de casa."),
            ("Dá para consultar precatório do TJSP pelo CPF?","A página oficial de precatórios do TJSP não informa consulta por CPF. Tenha em mãos o número do precatório ou do processo, que o advogado da ação pode informar."),
            ("Em quanto tempo recebo?","Depois da proposta aprovada e do contrato de cessão assinado, o pagamento é feito em até 72 horas.")]},
    {"slug":"empresa-que-compra-precatorio-paraiba","uf":"PB","nome":"Paraíba","em":"na Paraíba","de":"da Paraíba","capital":"João Pessoa",
     "seo":"Empresa que compra precatórios na Paraíba | Antecipay",
     "desc":"A Antecipay compra precatórios do Estado da Paraíba, de João Pessoa e de outros municípios paraibanos (TJPB), e federais do TRF5. Pagamento à vista.",
     "lead":"Tem precatório do Estado da Paraíba, da Prefeitura de João Pessoa, de Campina Grande, da União ou do INSS? A Antecipay, empresa vizinha de Natal, compra o seu precatório e você recebe à vista.",
     "trf":"TRF5","trf_ufs":"Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte e Sergipe","tj":"TJPB",
     "devedores":[("União, INSS e autarquias federais","TRF5 – Seção Judiciária da Paraíba"),("Estado da Paraíba e autarquias estaduais","TJPB"),("Prefeituras de João Pessoa, Campina Grande e demais municípios","TJPB")],
     "consulta":"""<ul>
    <li><strong>Estadual ou municipal (TJPB):</strong> na área de precatórios do site do TJPB (tjpb.jus.br), que publica a lista de ordem cronológica dos precatórios pendentes. A lista é pública e mostra a posição na fila.</li>
    <li><strong>Federal (TRF5):</strong> no site de RPV e precatórios do TRF5 (rpvprecatorio.trf5.jus.br), pelo CPF ou pelo número do processo.</li>
  </ul>
  <p>Passo a passo da consulta federal em <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>. Se preferir, envie o número do processo que a nossa equipe consulta para você.</p>""",
     "extra":"""<h2>Cuidado com golpes</h2>
  <p>O próprio TJPB alerta que não pede depósitos nem adiantamento de taxas, custas ou impostos para liberar precatório. Quem compra precatório também não deve cobrar nada de você: na Antecipay, a proposta é por escrito e não existe cobrança antecipada. Veja como reconhecer o <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>.</p>""",
     "faq":[("A Antecipay compra precatório do Estado da Paraíba?","Sim. Compramos precatórios do Estado da Paraíba, da Prefeitura de João Pessoa e de outros municípios paraibanos, pagos pelo TJPB, além de precatórios federais do TRF5."),
            ("A Antecipay tem escritório na Paraíba?","Não. A sede é em Natal-RN, na Incubadora do IFRN, a cerca de 180 km de João Pessoa. O atendimento é 100% digital, pelo WhatsApp."),
            ("O Estado da Paraíba faz acordo direto com credores?","O Estado já abriu editais de acordo direto, com desconto sobre o valor do precatório e seguindo a ordem cronológica. Vale comparar a proposta do acordo com a nossa antes de decidir."),
            ("Em quanto tempo recebo?","Depois da proposta aprovada e do contrato de cessão assinado, o pagamento é feito em até 72 horas.")]},
    {"slug":"empresa-que-compra-precatorio-pernambuco","uf":"PE","nome":"Pernambuco","em":"em Pernambuco","de":"de Pernambuco","capital":"Recife",
     "seo":"Empresa que compra precatórios em Pernambuco | Antecipay",
     "desc":"A Antecipay compra precatórios do Estado de Pernambuco, do Recife e de outros municípios pernambucanos (TJPE), e federais do TRF5. Pagamento à vista.",
     "lead":"Tem precatório do Estado de Pernambuco, da Prefeitura do Recife, de outro município pernambucano, da União ou do INSS? A Antecipay compra o seu precatório e você recebe à vista, com proposta por escrito.",
     "trf":"TRF5","trf_ufs":"Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte e Sergipe","tj":"TJPE",
     "devedores":[("União, INSS e autarquias federais","TRF5 – Seção Judiciária de Pernambuco"),("Estado de Pernambuco e autarquias estaduais","TJPE"),("Prefeituras do Recife, Jaboatão, Olinda e demais municípios","TJPE")],
     "consulta":"""<ul>
    <li><strong>Estadual ou municipal (TJPE):</strong> na área de precatórios do site do TJPE (tjpe.jus.br). Os tribunais publicam a lista de ordem cronológica de cada devedor, sem o nome completo do credor, onde você confere a posição na fila pelo número do precatório.</li>
    <li><strong>Federal (TRF5):</strong> no site de RPV e precatórios do TRF5 (rpvprecatorio.trf5.jus.br), pelo CPF ou pelo número do processo. O TRF5 tem sede no Recife.</li>
  </ul>
  <p>Passo a passo da consulta federal em <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>. Se você não sabe o número do processo, veja <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>.</p>""",
     "extra":"""<h2>Precatório federal ou estadual: a espera muda muito</h2>
  <p>O precatório federal do TRF5 inscrito até 1º de fevereiro é pago até o fim do ano seguinte. Já o precatório do Estado de Pernambuco ou de uma prefeitura depende do limite anual que cada ente reserva para a fila, entre 1% e 5% da receita corrente líquida, e a espera costuma ser bem maior. Por isso a proposta de compra também muda de um tipo para outro. Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>""",
     "faq":[("A Antecipay compra precatório do Estado de Pernambuco?","Sim. Compramos precatórios do Estado de Pernambuco, da Prefeitura do Recife e de outros municípios pernambucanos, pagos pelo TJPE, além de precatórios federais do TRF5."),
            ("A Antecipay tem escritório em Pernambuco?","Não. A sede é em Natal-RN, na Incubadora do IFRN, e o atendimento é 100% digital. Credores de Pernambuco resolvem tudo pelo WhatsApp."),
            ("Precatório do INSS em Pernambuco é pago por qual tribunal?","Pelo TRF5, que atende as ações contra a União e o INSS em Pernambuco, Alagoas, Ceará, Paraíba, Rio Grande do Norte e Sergipe."),
            ("Em quanto tempo recebo?","Depois da proposta aprovada e do contrato de cessão assinado, o pagamento é feito em até 72 horas.")]},
    {"slug":"empresa-que-compra-precatorio-ceara","uf":"CE","nome":"Ceará","em":"no Ceará","de":"do Ceará","capital":"Fortaleza",
     "seo":"Empresa que compra precatórios no Ceará | Antecipay",
     "desc":"A Antecipay compra precatórios do Estado do Ceará, de Fortaleza e de outros municípios cearenses (TJCE), e federais do TRF5. Proposta por escrito e à vista.",
     "lead":"Tem precatório do Estado do Ceará, da Prefeitura de Fortaleza, de outro município cearense, da União ou do INSS? A Antecipay compra o seu precatório e você recebe à vista, com proposta por escrito.",
     "trf":"TRF5","trf_ufs":"Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte e Sergipe","tj":"TJCE",
     "devedores":[("União, INSS e autarquias federais","TRF5 – Seção Judiciária do Ceará"),("Estado do Ceará e autarquias estaduais","TJCE"),("Prefeituras de Fortaleza, Caucaia, Juazeiro do Norte e demais municípios","TJCE")],
     "consulta":"""<ul>
    <li><strong>Estadual ou municipal (TJCE):</strong> na página do serviço de precatórios do TJCE (tjce.jus.br), que reúne as listas de ordem cronológica de cada ente devedor. O crédito mais antigo é pago primeiro.</li>
    <li><strong>Federal (TRF5):</strong> no site de RPV e precatórios do TRF5 (rpvprecatorio.trf5.jus.br), pelo CPF ou pelo número do processo.</li>
  </ul>
  <p>Passo a passo da consulta federal em <a href="/blog/consultar-rpv-precatorio-trf5/">como consultar RPV e precatório no TRF5</a>. Se preferir, envie o número do processo que a nossa equipe consulta para você.</p>""",
     "extra":"""<h2>Acordo direto ou venda?</h2>
  <p>O Estado do Ceará já abriu editais de acordo direto com credores, conduzidos pelo juízo de conciliação de precatórios do TJCE. No acordo, você recebe antes da fila, mas com desconto, e só quando há edital aberto. Na venda, você recebe à vista quando quiser. Compare as duas propostas: veja <a href="/blog/desagio-precatorio/">o que é deságio e como ele é calculado</a>.</p>""",
     "faq":[("A Antecipay compra precatório do Estado do Ceará?","Sim. Compramos precatórios do Estado do Ceará, da Prefeitura de Fortaleza e de outros municípios cearenses, pagos pelo TJCE, além de precatórios federais do TRF5."),
            ("A Antecipay tem escritório no Ceará?","Não. A sede é em Natal-RN, na Incubadora do IFRN, e o atendimento é 100% digital. Credores do Ceará resolvem tudo pelo WhatsApp."),
            ("Onde vejo a fila de precatórios de Fortaleza?","Na página do serviço de precatórios do TJCE, que publica as listas de ordem cronológica de cada devedor, inclusive a do Município de Fortaleza."),
            ("Em quanto tempo recebo?","Depois da proposta aprovada e do contrato de cessão assinado, o pagamento é feito em até 72 horas.")]},
]

def build_estados():
    for e in ESTADOS:
        url = SITE + f"/{e['slug']}/"
        msg = f"Olá! Tenho um precatório {e['de']} e quero uma proposta."
        ld={"@context":"https://schema.org","@graph":[
            {"@type":"Service","name":f"Compra de precatórios {e['em']}","serviceType":"Antecipação de precatório","url":url,
             "areaServed":[{"@type":"State","name":e["nome"]},{"@type":"City","name":e["capital"]}],
             "provider":{"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png",
               "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"}}},
            {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in e["faq"]]}]}
        faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in e["faq"])
        rows="".join(f"<tr><td>{d}</td><td>{t}</td></tr>" for d,t in e["devedores"])
        out = head(e["seo"], e["desc"], url, '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">{e['nome']}</span></nav>
  <span class="eyebrow">{e['nome']}</span>
  <h1>Empresa que compra precatórios {e['em']}</h1>
  <p class="lead">{e['lead']}</p>
  <p class="ctas"><a class="btn btn-wa" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a><a class="btn btn-tel" href="tel:+5584994938383" aria-label="Ligar para (84) 99493-8383">{TEL_ICON}Ligar</a></p>
</div></section>
<article class="narrow">
  <div class="answer"><strong>Em resumo</strong>A Antecipay Precatórios (CNPJ 64.382.432/0001-97) tem sede em Natal-RN e compra precatórios {e['de']}: estaduais e municipais do {e['tj']} e federais do {e['trf']}. O atendimento é 100% digital, pelo WhatsApp (84) 99493-8383, e o pagamento sai em até 72 horas depois da cessão assinada.</div>

  <h2>Precatórios que compramos {e['em']}</h2>
  <div class="table-wrap"><table>
    <tr><th>Devedor</th><th>Tribunal</th></tr>
    {rows}
  </table></div>
  <p>O {e['trf']} cuida das ações contra a União e o INSS em {e['trf_ufs']}. Veja também como <a href="/vender-precatorio-estadual/">vender precatório estadual</a>, <a href="/vender-precatorio-municipal/">vender precatório municipal</a> e <a href="/vender-precatorio-inss/">vender precatório do INSS</a>.</p>

  {e['extra']}

  <h2>Como consultar o seu precatório</h2>
  {e['consulta']}

  <h2>Atendimento {e['em']} sem sair de casa</h2>
  <ul>
    <li><strong>100% digital:</strong> você envia o número do processo e assina a cessão pelo celular.</li>
    <li><strong>Proposta por escrito</strong>, com o valor líquido, antes de qualquer assinatura.</li>
    <li><strong>Pagamento em até 72 horas</strong> depois da proposta aprovada e da cessão assinada.</li>
    <li><strong>Nenhuma cobrança antecipada.</strong></li>
    <li><strong>Empresa com endereço que você pode conferir:</strong> sede em Natal-RN, na Incubadora do IFRN.</li>
  </ul>

  <h2>Como funciona</h2>
  <ol>
    <li>Envie o número do processo pelo WhatsApp.</li>
    <li>Nossa equipe jurídica analisa o precatório.</li>
    <li>Você recebe a proposta por escrito.</li>
    <li>Assinamos o contrato de <a href="/blog/cessao-de-precatorio/">cessão de crédito</a> e o valor é pago à vista.</li>
  </ol>
  <p>Antes de decidir, veja <a href="/melhor-empresa-para-vender-precatorio/">como escolher a empresa para vender o precatório</a> ou faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>

  <h2>Quem somos</h2>
  <p><strong>Antecipay Precatórios</strong><br>Av. Senador Salgado Filho, 1559 – Tirol<br>Incubadora do IFRN – Campus Natal Central<br>Natal-RN, CEP 59015-000<br>WhatsApp (84) 99493-8383 · contato@antecipay.com.br</p>
  <p>Saiba mais <a href="/sobre/">sobre a Antecipay</a> e sobre a nossa <a href="/empresa-que-compra-precatorio-natal/">sede em Natal</a>.</p>

  {cta(f"Tem precatório {e['de']}?", "Envie o número do processo e receba uma proposta por escrito.", msg)}
  <h2>Perguntas frequentes</h2>
  {faq_html}
  {NOTE}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
        os.makedirs(e["slug"], exist_ok=True)
        open(f"{e['slug']}/index.html","w").write(out)


def landing(slug, seo, desc, crumb, eyebrow, h1, lead, wa_msg, answer, body, faq, service_name, extra_top=""):
    url = SITE + f"/{slug}/"
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":service_name,"serviceType":"Antecipação de precatório","areaServed":{"@type":"Country","name":"Brasil"},
         "provider":{"@type":"FinancialService","@id":SITE+"/#empresa","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png"},"url":url},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Início","item":SITE+"/"},{"@type":"ListItem","position":2,"name":crumb,"item":url}]}]}
    faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in faq)
    out = head(seo, desc, url, '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">{crumb}</span></nav>
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <p class="ctas"><a class="btn btn-wa" href="{wa(wa_msg)}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a><a class="btn btn-tel" href="tel:+5584994938383" aria-label="Ligar para (84) 99493-8383">{TEL_ICON}Ligar</a></p>
</div></section>
<article class="narrow">
  {extra_top}
  <div class="answer"><strong>Em resumo</strong>{answer}</div>
  {body}
  <h2>Perguntas frequentes</h2>
  {faq_html}
  {NOTE}
</article>
<div style="height:80px"></div>
</main>
""" + FOOT
    os.makedirs(slug, exist_ok=True)
    open(f"{slug}/index.html","w").write(out)

PASSOS = """<h2>Como funciona a venda</h2>
  <ol>
    <li><strong>Envie o número do processo</strong> pelo WhatsApp.</li>
    <li><strong>Análise jurídica:</strong> conferimos o precatório, o devedor, os descontos e a posição na fila.</li>
    <li><strong>Proposta por escrito</strong>, com o valor líquido que você recebe.</li>
    <li><strong>Cessão e pagamento:</strong> assinamos o contrato de cessão de crédito, comunicado ao tribunal, e o valor é pago em até 72 horas.</li>
  </ol>"""

def build_municipal():
    msg="Olá! Tenho um precatório municipal e quero uma proposta."
    body = f"""
  <h2>O que é precatório municipal</h2>
  <p>É a dívida de uma prefeitura (ou de uma autarquia municipal) reconhecida em decisão judicial definitiva e que passa do limite de RPV do município. Esse limite é definido por lei de cada cidade. O precatório é expedido pelo Tribunal de Justiça do estado e entra na fila de pagamento daquela prefeitura.</p>
  <h2>Por que a espera costuma ser longa</h2>
  <p>Muitas prefeituras estão no regime especial de pagamento. Com a Emenda Constitucional 136/2025, estados e municípios passaram a pagar precatórios dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho da dívida. Quando a fila é grande, ela anda devagar, e a espera pode levar vários anos.</p>
  <p>Cada município é um caso: há prefeituras em dia e outras com anos de atraso. Por isso analisamos o devedor antes de fazer a proposta. Para municípios paulistas, veja <a href="/blog/consultar-precatorio-tjsp/">como consultar precatório no TJSP</a>. Se o seu precatório é de outro devedor, veja <a href="/vender-precatorio-federal/">precatório federal</a>, <a href="/vender-precatorio-estadual/">precatório estadual</a> ou <a href="/vender-precatorio-inss/">precatório do INSS</a>, ou a página principal sobre como <a href="/">vender precatório</a>. Também compramos <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</p>
  <h2>Vender ou esperar?</h2>
  <div class="table-wrap"><table>
    <tr><th>Opção</th><th>Vantagem</th><th>Ponto de atenção</th></tr>
    <tr><td><strong>Esperar a fila</strong></td><td>Recebe o valor cheio, corrigido</td><td>Prazo incerto, pode levar anos</td></tr>
    <tr><td><strong>Acordo direto com a prefeitura</strong></td><td>Recebe antes, se houver edital</td><td>Depende de edital aberto e tem deságio</td></tr>
    <tr><td><strong>Vender para a Antecipay</strong></td><td>Dinheiro à vista, sem depender de edital</td><td>Há deságio pela antecipação</td></tr>
  </table></div>
  <p>Algumas prefeituras, como a de Natal, abrem editais de acordo direto. Vale comparar a proposta do acordo com a nossa. Veja também <a href="/blog/desagio-precatorio/">o que é deságio e como ele é calculado</a>. Credores da Prefeitura de Natal podem ver a página <a href="/empresa-que-compra-precatorio-natal/">empresa que compra precatório em Natal</a>.</p>
  {PASSOS}
  {cta("Quer saber quanto vale o seu precatório municipal?", "Faça uma estimativa na <a href='/calculadora-precatorio/' style='color:inherit;text-decoration:underline'>calculadora</a> ou envie o número do processo.", msg)}
  <h2>Prioridade por idade ou doença</h2>
  <p>Credores com 60 anos ou mais, doença grave ou deficiência podem receber antes uma parte do crédito (a parcela superpreferencial). Essa prioridade é pessoal e não passa para quem compra. Se for o seu caso, avaliamos com você se vale antecipar o crédito inteiro ou só o saldo que ficaria na fila.</p>
"""
    faq=[("Posso vender precatório municipal?","Sim. O art. 100, §13, da Constituição permite ceder o precatório a terceiros. A venda é feita por contrato de cessão de crédito, comunicado ao Tribunal de Justiça."),
         ("Quanto tempo demora o precatório municipal?","Depende da prefeitura. Pelas regras atuais, municípios pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, e a fila pode levar anos em cidades com dívida alta."),
         ("Por que o valor da proposta é menor que o do precatório?","Porque você recebe agora um valor que a prefeitura só pagaria no futuro. A diferença, chamada deságio, remunera a antecipação e o risco de atraso. Em precatórios municipais, o deságio costuma ser maior que nos federais."),
         ("A Antecipay compra precatório de qualquer cidade?","Analisamos precatórios de prefeituras de todo o Brasil. A proposta depende da situação do pagamento em cada município.")]
    landing("vender-precatorio-municipal","Vender precatório municipal: receba à vista | Antecipay",
        "Venda seu precatório municipal e receba à vista, sem esperar a fila da prefeitura. Análise do devedor, proposta por escrito e atendimento 100% digital.",
        "Precatório municipal","Precatório municipal","Venda o seu precatório municipal e receba à vista",
        "Tem um precatório contra uma prefeitura e a fila não anda? A Antecipay compra o seu crédito e você recebe agora, sem depender do orçamento do município.",
        msg,"Você pode vender o precatório que tem a receber de uma prefeitura. A Antecipay analisa o processo e a situação de pagamento do município, apresenta uma proposta por escrito e, com a cessão assinada, paga à vista em até 72 horas.",
        body, faq, "Compra de precatório municipal")

def build_estadual():
    msg="Olá! Tenho um precatório estadual e quero uma proposta."
    body = f"""
  <h2>O que é precatório estadual</h2>
  <p>É a dívida de um estado (ou de uma autarquia estadual, como institutos de previdência e universidades estaduais) reconhecida na Justiça e acima do limite de RPV fixado por lei estadual. É expedido pelo Tribunal de Justiça e entra na fila do estado devedor. Também são comuns precatórios de servidores públicos, por diferenças salariais, e de desapropriações.</p>
  <h2>Quanto tempo leva para receber</h2>
  <p>Pela EC 136/2025, os estados pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho do estoque de precatórios. Alguns estados estão em dia; outros têm filas de muitos anos. A posição na fila e a data de inscrição fazem diferença no prazo. Em São Paulo, veja <a href="/blog/consultar-precatorio-tjsp/">como consultar precatório no TJSP</a>. Veja o que mudou em <a href="/blog/precatorios-2027-ec-136/">precatórios 2027 e a EC 136</a>.</p>
  <p>Se o seu precatório é do Rio Grande do Norte, veja a página <a href="/vender-precatorio-rn/">vender precatório no RN</a>. Para outros devedores, veja <a href="/vender-precatorio-federal/">precatório federal</a>, <a href="/vender-precatorio-municipal/">precatório municipal</a> e <a href="/vender-precatorio-inss/">precatório do INSS</a>, ou a página principal sobre como <a href="/">vender precatório</a>. Também compramos <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</p>
  <h2>O que influencia a proposta</h2>
  <ul>
    <li><strong>Estado devedor:</strong> o histórico de pagamento e o tamanho da fila.</li>
    <li><strong>Situação do precatório:</strong> já expedido e inscrito, ou ainda em fase de cálculo.</li>
    <li><strong>Descontos:</strong> imposto de renda, contribuição previdenciária e honorários contratuais.</li>
    <li><strong>Prioridades:</strong> a parcela superpreferencial de idosos e doentes graves é pessoal e não é transferida.</li>
  </ul>
  {PASSOS}
  {cta("Quanto vale o seu precatório estadual?", "Faça uma estimativa na <a href='/calculadora-precatorio/' style='color:inherit;text-decoration:underline'>calculadora</a> ou envie o número do processo.", msg)}
  <p>Antes de assinar com qualquer empresa, confira <a href="/melhor-empresa-para-vender-precatorio/">como escolher uma empresa para vender o precatório</a>.</p>
"""
    faq=[("Posso vender precatório estadual?","Sim. A cessão de precatórios é permitida pelo art. 100, §13, da Constituição Federal. O contrato de cessão é comunicado ao Tribunal de Justiça."),
         ("Quem compra precatório estadual?","Empresas especializadas e fundos de investimento. A Antecipay compra precatórios estaduais de credores de todo o Brasil, com proposta por escrito e pagamento à vista."),
         ("Servidor público pode vender o precatório?","Sim. Precatórios de diferenças salariais de servidores podem ser vendidos como qualquer outro. Analisamos os descontos de imposto de renda e previdência para mostrar o valor líquido."),
         ("Qual documento preciso para pedir uma proposta?","Basta o número do processo. Nossa equipe consulta o precatório e pede outros documentos só se forem necessários.")]
    landing("vender-precatorio-estadual","Vender precatório estadual: proposta à vista | Antecipay",
        "Venda seu precatório estadual e receba à vista, sem esperar a fila do estado. Análise jurídica, proposta por escrito e atendimento pelo WhatsApp.",
        "Precatório estadual","Precatório estadual","Venda o seu precatório estadual e receba à vista",
        "Servidor, aposentado ou credor de uma ação contra o estado? A Antecipay compra o seu precatório estadual e você recebe agora, sem esperar anos na fila.",
        msg,"A Antecipay compra precatórios estaduais de todo o Brasil. Você envia o número do processo, nossa equipe analisa o estado devedor e a posição na fila e apresenta uma proposta por escrito. Com a cessão assinada, o pagamento é feito à vista.",
        body, faq, "Compra de precatório estadual")

def build_melhor():
    msg="Olá! Estou comparando empresas para vender meu precatório e quero uma proposta."
    body = f"""
  <h2>Os 7 pontos para avaliar uma empresa</h2>
  <ol>
    <li><strong>CNPJ ativo e endereço real.</strong> Consulte o CNPJ no site da Receita Federal e confira se o endereço existe.</li>
    <li><strong>Proposta por escrito</strong>, com o valor bruto, os descontos e o valor líquido que você recebe.</li>
    <li><strong>Nenhuma cobrança antecipada.</strong> Empresa séria não pede taxa, imposto ou depósito para liberar o pagamento. Esse é o golpe mais comum.</li>
    <li><strong>Contrato de cessão claro</strong>, comunicado ao tribunal, com prazo de pagamento definido.</li>
    <li><strong>Pagamento à vista</strong> em data certa, e não “quando o governo pagar”.</li>
    <li><strong>Análise jurídica do processo</strong> antes da proposta, com explicação de prioridades e descontos.</li>
    <li><strong>Seu advogado informado.</strong> Combine com quem cuidou da ação como ficam os honorários contratuais.</li>
  </ol>
  <h2>Como comparar propostas</h2>
  <p>Compare sempre o <strong>valor líquido</strong> que cai na sua conta e o <strong>prazo de pagamento</strong>, não só a porcentagem anunciada. Uma oferta de percentual alto com pagamento parcelado ou condicionado pode valer menos que uma proposta à vista. Entenda o cálculo em <a href="/blog/desagio-precatorio/">deságio: por que recebo menos ao antecipar</a>.</p>
  <div class="table-wrap"><table>
    <tr><th>Na proposta, confira</th><th>Por quê</th></tr>
    <tr><td>Valor líquido</td><td>É o que você recebe de fato</td></tr>
    <tr><td>Prazo e forma de pagamento</td><td>À vista, parcelado ou condicionado</td></tr>
    <tr><td>Quem paga os custos</td><td>Cartório, certidões e honorários</td></tr>
    <tr><td>Multas e cláusulas de desistência</td><td>Evita surpresas se você mudar de ideia</td></tr>
  </table></div>
  <h2>Sinais de golpe</h2>
  <ul>
    <li>Contato inesperado dizendo que “seu dinheiro foi liberado”.</li>
    <li>Pedido de pagamento de taxa, custas ou imposto para liberar valores.</li>
    <li>Pressão para assinar no mesmo dia.</li>
    <li>Recusa em enviar a proposta por escrito.</li>
  </ul>
  <p>Veja mais em <a href="/blog/como-vender-precatorio/">como vender precatório com segurança</a>, no guia <a href="/blog/empresas-que-compram-precatorios-natal/">como escolher empresa de precatório em Natal</a>, na página <a href="/empresa-que-compra-precatorio-natal/">empresa que compra precatório em Natal</a> e em <a href="/vender-precatorio-rn/">vender precatório no RN</a>. Para não cair em armadilhas, leia <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>. Para a visão geral, comece por <a href="/">vender precatório</a>.</p>
  <h2>Como a Antecipay atende a esses pontos</h2>
  <ul>
    <li>CNPJ 64.382.432/0001-97, com sede na Incubadora do IFRN – Campus Natal Central, em Natal-RN.</li>
    <li>Proposta por escrito, com o valor líquido, antes de qualquer assinatura.</li>
    <li>Nenhuma cobrança do credor.</li>
    <li>Pagamento em até 72 horas após a proposta aprovada e a cessão assinada.</li>
    <li>Atendimento 100% digital, pelo WhatsApp (84) 99493-8383.</li>
  </ul>
  {cta("Compare a nossa proposta", "Envie o número do processo e receba uma proposta por escrito, sem compromisso.", msg)}
"""
    faq=[("Qual a melhor empresa para vender precatório?","A melhor é a que oferece o maior valor líquido à vista, com proposta por escrito, CNPJ e endereço verificáveis e sem nenhuma cobrança antecipada. Peça propostas a mais de uma empresa e compare."),
         ("Banco compra precatório?","Alguns bancos e fundos compram precatórios, em geral os de valor mais alto. Empresas especializadas também compram e costumam atender créditos menores."),
         ("É seguro vender precatório?","Sim, quando a venda é feita por contrato de cessão de crédito, comunicado ao tribunal, com uma empresa identificável. Nunca pague taxa para receber."),
         ("Posso desistir depois de pedir a proposta?","Sim. Pedir proposta não obriga você a vender. O compromisso só existe com a assinatura do contrato de cessão.")]
    landing("melhor-empresa-para-vender-precatorio","Melhor empresa para vender precatório: 7 pontos | Antecipay",
        "Como escolher a melhor empresa para vender precatório: 7 pontos para avaliar, como comparar propostas e os sinais de golpe. Guia da Antecipay.",
        "Como escolher a empresa","Guia","Qual a melhor empresa para vender precatório?",
        "Não existe uma resposta única: a melhor empresa é a que paga mais, à vista e com segurança. Veja os 7 pontos para avaliar antes de assinar.",
        msg,"Escolha a empresa que oferece o maior valor líquido à vista, com proposta por escrito, CNPJ e endereço verificáveis, contrato de cessão comunicado ao tribunal e nenhuma cobrança antecipada. Peça mais de uma proposta e compare o valor líquido e o prazo de pagamento.",
        body, faq, "Compra de precatórios")

CALC_JS = r"""<script>
(function(){
  // Faixas indicativas (% do valor líquido de honorários). Ajuste aqui.
  var F={federal:{exp:[70,85],nao:[55,75],prazo:"cerca de 1 a 2 anos"},
         estadual:{exp:[35,65],nao:[25,50],prazo:"de alguns anos, conforme o estado"},
         municipal:{exp:[30,60],nao:[20,45],prazo:"de alguns anos, conforme a prefeitura"}};
  var f=document.getElementById('calc'), out=document.getElementById('calc-out');
  function brl(n){return n.toLocaleString('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:0})}
  function num(s){s=(s||'').replace(/[^\d,]/g,'').replace(',','.');return parseFloat(s)||0}
  function run(){
    var v=num(f.valor.value), h=Math.min(Math.max(num(f.hon.value),0),50), t=F[f.tipo.value], r=t[f.sit.value];
    var base=v*(1-h/100);
    if(!v){out.querySelector('.range').textContent='Informe o valor';return}
    out.querySelector('.range').textContent=brl(base*r[0]/100)+' a '+brl(base*r[1]/100);
    out.querySelector('.prazo').textContent='Sem vender, a espera estimada seria '+t.prazo+'.';
    var msg='Olá! Fiz a simulação na calculadora da Antecipay.\n\n• Tipo: '+f.tipo.options[f.tipo.selectedIndex].text+'\n• Valor do precatório: '+brl(v)+'\n• Situação: '+f.sit.options[f.sit.selectedIndex].text+'\n\nQuero uma proposta.';
    document.getElementById('calc-wa').href='https://wa.me/WA_NUM?text='+encodeURIComponent(msg);
  }
  f.addEventListener('input',run); f.addEventListener('change',run);
  f.valor.addEventListener('blur',function(){var v=num(f.valor.value);if(v)f.valor.value=brl(v)});
  document.getElementById('calc-wa').addEventListener('click',function(){if(window.clarity)clarity('event','calculadora_whatsapp')});
  run();
})();
</script>"""

def build_calc():
    msg="Olá! Quero saber quanto vale o meu precatório."
    calc = f"""<form class="calc" id="calc" onsubmit="return false">
    <h2>Calcule quanto vale o seu precatório</h2>
    <div class="fields">
      <label>Valor do precatório (R$)<input name="valor" inputmode="decimal" placeholder="Ex.: 150.000" autocomplete="off"></label>
      <label>Quem deve<select name="tipo"><option value="federal">União / INSS (federal)</option><option value="estadual">Estado (estadual)</option><option value="municipal">Prefeitura (municipal)</option></select></label>
      <label>Situação<select name="sit"><option value="exp">Já expedido / inscrito</option><option value="nao">Ainda não expedido</option></select></label>
      <label>Honorários contratuais do advogado (%)<input name="hon" inputmode="decimal" value="0" autocomplete="off"></label>
    </div>
    <div class="out" id="calc-out" aria-live="polite">
      <small>Estimativa à vista</small>
      <div class="range">Informe o valor</div>
      <p class="prazo"></p>
      <p>Faixa indicativa de mercado, antes de impostos. Não é uma proposta: o valor final depende da análise do processo.</p>
    </div>
    <a class="btn btn-wa" id="calc-wa" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Receber proposta exata</a>
  </form>"""
    body = f"""
  <h2>Como a estimativa é feita</h2>
  <p>A calculadora parte do valor do precatório, desconta os honorários contratuais que você informou e aplica uma faixa de deságio típica para o tipo de devedor e a situação do processo. É uma referência para você saber a ordem de grandeza antes de conversar com qualquer empresa. Para entender a operação, veja como funciona a <a href="/antecipacao-de-precatorio/">antecipação de precatório</a>.</p>
  <h2>O que muda o valor da sua proposta</h2>
  <ul>
    <li><strong>Devedor:</strong> precatórios federais costumam ter deságio menor, porque a União paga em prazo previsível. Estados e prefeituras variam muito.</li>
    <li><strong>Prazo até o pagamento:</strong> quanto mais longe o pagamento, maior o deságio.</li>
    <li><strong>Situação do processo:</strong> precatório <a href="/blog/expedicao-de-oficio-precatorio/">já expedido</a> e inscrito tem menos risco que um ainda em fase de cálculo.</li>
    <li><strong>Descontos:</strong> imposto de renda (em geral pelo regime de rendimentos acumulados), contribuição previdenciária e honorários.</li>
    <li><strong>Prioridades:</strong> a parcela superpreferencial de idosos, doentes graves e pessoas com deficiência é pessoal e não é transferida para quem compra.</li>
  </ul>
  <p>Entenda o cálculo em detalhes em <a href="/blog/desagio-precatorio/">deságio de precatório</a> e veja os prazos em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>. Para entender o contrato, leia <a href="/blog/cessao-de-precatorio/">cessão de precatório</a> e <a href="/blog/como-vender-precatorio/">como vender precatório passo a passo</a>. A visão geral de como <a href="/">vender precatório</a> está na página inicial.</p>
  <h2>Páginas por tipo de precatório</h2>
  <ul>
    <li><a href="/vender-precatorio-inss/">Vender precatório do INSS</a></li>
    <li><a href="/vender-precatorio-federal/">Vender precatório federal</a></li>
    <li><a href="/vender-precatorio-estadual/">Vender precatório estadual</a></li>
    <li><a href="/vender-precatorio-municipal/">Vender precatório municipal</a></li>
  </ul>
  {cta("Quer o valor exato?", "Envie o número do processo e receba uma proposta por escrito, sem compromisso.", msg)}
""" + CALC_JS.replace("WA_NUM", WA)
    faq=[("Quanto vale o meu precatório?","Depende do valor, do devedor (União, estado ou prefeitura), do prazo previsto de pagamento e dos descontos. Use a calculadora para uma estimativa e peça uma proposta para o valor exato."),
         ("Quanto se paga por um precatório?","Precatórios federais costumam ser comprados por uma parte maior do valor que os estaduais e municipais, porque o pagamento da União é mais previsível. A faixa exata varia em cada caso."),
         ("A estimativa da calculadora é uma proposta?","Não. É uma faixa indicativa. A proposta da Antecipay é feita por escrito, depois da análise do processo."),
         ("Preciso pagar algo para simular ou pedir proposta?","Não. A simulação e a proposta são gratuitas e sem compromisso.")]
    landing("calculadora-precatorio","Simulador de precatório: quanto vale o seu? | Antecipay",
        "Simulador gratuito: calcule quanto vale o seu precatório federal, estadual ou municipal se vender agora e quanto tempo esperaria na fila do governo.",
        "Calculadora","Calculadora e simulador","Calculadora de precatório: quanto vale o meu?",
        "Descubra em segundos quanto você poderia receber à vista ao vender o seu precatório, e quanto tempo esperaria se não vendesse.",
        msg,"O valor de venda de um precatório depende do devedor, do prazo até o pagamento, da situação do processo e dos descontos. Precatórios federais costumam ter deságio menor que os estaduais e municipais. Use a calculadora abaixo para uma estimativa e peça a proposta exata pelo WhatsApp.",
        body, faq, "Calculadora de precatório", extra_top=calc)


def build_federal():
    msg="Olá! Tenho um precatório federal e quero uma proposta."
    body = f"""
  <h2>O que é precatório federal</h2>
  <p>É a dívida da União, do INSS ou de outra autarquia ou fundação federal reconhecida em decisão judicial definitiva, acima de 60 salários mínimos. Abaixo desse valor, o pagamento sai por RPV, em cerca de 60 dias. O precatório federal é expedido pelo Tribunal Regional Federal (TRF1 a TRF6) e entra no orçamento da União.</p>
  <h2>Prazo de pagamento do precatório federal</h2>
  <div class="table-wrap"><table>
    <tr><th>Inscrição do precatório</th><th>Pagamento</th></tr>
    <tr><td>Até 1º de fevereiro</td><td>Até o fim do ano seguinte</td></tr>
    <tr><td>Depois de 1º de fevereiro</td><td>Até o fim do segundo ano seguinte</td></tr>
  </table></div>
  <p>A data de corte de 1º de fevereiro vale desde a Emenda Constitucional 136/2025; antes, era 2 de abril. Na prática, entre a inscrição e o dinheiro na conta podem se passar de cerca de 11 meses a quase 3 anos, conforme a data de inscrição. Veja os detalhes em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a> e em <a href="/blog/precatorios-2027-ec-136/">precatórios 2027</a>.</p>
  <h2>Como consultar o precatório federal</h2>
  <p>No portal de RPV e precatórios do TRF da sua região, pelo CPF ou pelo número do processo. O passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>. Se preferir, envie o número do processo pelo WhatsApp e nós consultamos para você.</p>
  <h2>Vale a pena vender o precatório federal?</h2>
  <p>O precatório federal é o que tem o pagamento mais previsível, por isso costuma ter o <strong>menor deságio</strong> entre os precatórios. Vender faz sentido para quem precisa do dinheiro agora ou não quer esperar até quase três anos. Quem pode esperar recebe o valor cheio, corrigido. Faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
  {PASSOS}
  {cta("Quer vender o seu precatório federal?", "Envie o número do processo e receba uma proposta por escrito.", msg)}
  <h2>Precatório do INSS e prioridades</h2>
  <p>Precatórios de ações contra o INSS são federais. Veja a página <a href="/vender-precatorio-inss/">vender precatório do INSS</a>. Credores com 60 anos ou mais, doença grave ou deficiência podem receber antes uma parte do crédito; essa prioridade é pessoal e não passa para quem compra.</p>
  <p>Para outros devedores, veja <a href="/vender-precatorio-estadual/">precatório estadual</a> e <a href="/vender-precatorio-municipal/">precatório municipal</a>, ou a página principal sobre como <a href="/">vender precatório</a>. Também compramos <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</p>
"""
    faq=[("Quando o precatório federal é pago?","Se for inscrito até 1º de fevereiro, até o fim do ano seguinte. Inscrito depois dessa data, até o fim do segundo ano seguinte."),
         ("Posso vender precatório federal?","Sim. A Constituição (art. 100, §13) permite ceder o precatório a terceiros. A venda é feita por contrato de cessão de crédito, comunicado ao tribunal."),
         ("Qual o deságio do precatório federal?","Costuma ser o menor entre os precatórios, porque o pagamento da União é previsível. O percentual exato depende do valor, do prazo até o pagamento e da situação do processo."),
         ("Quem compra precatório federal?","Bancos, fundos e empresas especializadas. A Antecipay compra precatórios federais de credores de todo o Brasil, com proposta por escrito e pagamento à vista.")]
    landing("vender-precatorio-federal","Precatório federal 2026: prazo e como vender | Antecipay",
        "Veja quando o precatório federal é pago, como consultar no TRF e como vender o seu precatório federal à vista, com proposta por escrito.",
        "Precatório federal","Precatório federal","Precatório federal: prazo de pagamento e como vender",
        "Tem um precatório contra a União ou o INSS? Veja quando ele deve ser pago e como receber à vista, sem esperar a fila do orçamento federal.",
        msg,"O precatório federal é a dívida da União, do INSS ou de autarquias federais acima de 60 salários mínimos. Inscrito até 1º de fevereiro, é pago até o fim do ano seguinte. Quem não quer esperar pode vender o precatório: a Antecipay faz uma proposta por escrito e paga à vista.",
        body, faq, "Compra de precatório federal")

def build_sitemap():
    urls = ["/", "/antecipacao-de-precatorio/", "/calculadora-precatorio/", "/vender-precatorio-federal/", "/vender-precatorio-estadual/", "/vender-precatorio-municipal/", "/vender-precatorio-trabalhista/", "/melhor-empresa-para-vender-precatorio/", "/vender-precatorio-inss/", "/vender-precatorio-rn/", "/empresa-que-compra-precatorio-natal/"] + [f"/{e['slug']}/" for e in ESTADOS] + ["/sobre/", AUTORA_URL, "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS] + ["/privacidade.html"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>\n" for u in urls)
    xml += "</urlset>\n"
    open("sitemap.xml","w").write(xml)

def build_antecipacao():
    msg="Olá! Quero antecipar o meu precatório. Podem me enviar uma proposta?"
    body = """
  <h2>Compra de precatório: como funciona</h2>
  <p>Na compra de precatório, uma empresa paga à vista ao credor e, em troca, passa a ser a dona do crédito. Quando o governo pagar, o dinheiro vai para a empresa. Para o credor, é a mesma coisa que antecipar: ele vende o precatório e recebe agora, em vez de esperar a fila.</p>
  <p>A compra é feita por <a href="/blog/cessao-de-precatorio/">contrato de cessão de crédito</a>, permitido pelo art. 100, §13, da Constituição. A cessão só produz efeitos depois de comunicada ao tribunal e ao devedor (§14). A Antecipay faz a compra de precatórios federais, estaduais e municipais de credores de todo o Brasil.</p>

  <h2>Antecipação não é empréstimo</h2>
  <p>Muita gente confunde as duas coisas. A diferença é grande:</p>
  <div class="table-wrap"><table>
    <tr><th></th><th>Antecipação</th><th>Empréstimo</th></tr>
    <tr><td><strong>Você fica devendo?</strong></td><td>Não</td><td>Sim</td></tr>
    <tr><td><strong>Paga parcelas e juros?</strong></td><td>Não</td><td>Sim</td></tr>
    <tr><td><strong>Se o governo atrasar</strong></td><td>O risco passa para quem comprou</td><td>Você continua devendo</td></tr>
    <tr><td><strong>O que você assina</strong></td><td>Contrato de cessão de crédito</td><td>Contrato de empréstimo</td></tr>
  </table></div>

  <h2>Quais precatórios podem ser antecipados</h2>
  <ul>
    <li><strong>Federais:</strong> dívidas da União, do <a href="/vender-precatorio-inss/">INSS</a> e de autarquias federais. Veja <a href="/vender-precatorio-federal/">precatório federal</a>.</li>
    <li><strong>Estaduais:</strong> dívidas dos estados, como diferenças salariais de servidores. Veja <a href="/vender-precatorio-estadual/">precatório estadual</a>.</li>
    <li><strong>Municipais:</strong> dívidas de prefeituras. Veja <a href="/vender-precatorio-municipal/">precatório municipal</a>.</li>
    <li><strong>Trabalhistas:</strong> ações na Justiça do Trabalho contra órgãos públicos. Veja <a href="/vender-precatorio-trabalhista/">precatório trabalhista</a>.</li>
  </ul>
  <p>Também dá para antecipar <strong>só uma parte</strong> do precatório. Isso é útil para quem tem prioridade por idade, doença grave ou deficiência: essa prioridade é pessoal e não passa para quem compra, então muitas vezes vale manter a parcela prioritária e antecipar só o restante. Entenda a <a href="/blog/superpreferencia-precatorio/">superpreferência no precatório</a>. Herdeiros também podem antecipar: veja <a href="/blog/precatorio-de-heranca/">precatório de herança</a>.</p>

  """ + PASSOS.replace("Como funciona a venda", "Como funciona a antecipação") + """

  <h2>Quanto você recebe</h2>
  <p>O valor da antecipação depende de quem deve (União, estado ou prefeitura), do prazo previsto até o pagamento, da situação do processo e dos descontos, como honorários e imposto de renda. Quanto mais longa e incerta a espera, maior o desconto. Entenda o cálculo em <a href="/blog/desagio-precatorio/">deságio de precatório</a> e faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>

  <h2>Antecipar ou esperar?</h2>
  <p>Antecipar faz sentido para quem precisa do dinheiro agora ou não quer depender de uma fila que pode levar anos. Quem pode esperar recebe o valor cheio no futuro. Para decidir com calma, leia <a href="/blog/vale-a-pena-vender-precatorio/">vale a pena vender precatório?</a> e veja como evitar o <a href="/blog/golpe-do-precatorio/">golpe do precatório</a>. A visão geral de como <a href="/">vender precatório</a> está na página inicial.</p>
""" + cta("Quer antecipar o seu precatório?", "Envie o número do processo e receba uma proposta por escrito, sem compromisso.", msg)
    faq=[("Antecipação de precatório é o mesmo que vender?","Sim. Antecipar é vender o direito de receber o precatório. A empresa paga à vista e recebe do governo depois."),
         ("Qual a diferença entre compra e antecipação de precatório?","É a mesma operação vista de lados diferentes. A empresa faz a compra do precatório; o credor faz a antecipação, porque recebe agora o que o governo só pagaria depois."),
         ("A antecipação de precatório é segura?","É uma operação prevista na Constituição (art. 100, §13) e formalizada por contrato de cessão, que só produz efeitos depois de comunicado ao tribunal. Confira sempre o CNPJ da empresa e nunca pague nada antecipado."),
         ("Posso antecipar só uma parte do precatório?","Sim. A cessão pode ser parcial, o que permite, por exemplo, manter a parcela prioritária e antecipar só o restante."),
         ("Em quanto tempo recebo?","Na Antecipay, o valor é pago em até 72 horas depois da proposta aprovada e do contrato de cessão assinado.")]
    landing("antecipacao-de-precatorio","Compra e antecipação de precatório à vista | Antecipay",
        "Compra e antecipação de precatório: venda o seu crédito federal, estadual ou municipal e receba à vista, sem empréstimo e sem parcelas.",
        "Compra e antecipação de precatório","Compra e antecipação","Compra e antecipação de precatório: receba agora o que o governo pagaria depois",
        "Tem um precatório para receber e não quer esperar a fila? Na antecipação, você vende o crédito e recebe à vista, sem contrair dívida.",
        msg,"Na compra e antecipação de precatório, você vende o direito de receber o precatório para uma empresa, que paga à vista e passa a receber do governo no futuro. Não é empréstimo: você não fica devendo nada e não paga parcelas. A operação é feita por contrato de cessão de crédito, permitido pelo art. 100, §13, da Constituição.",
        body, faq, "Compra e antecipação de precatório")


def build_trabalhista():
    msg="Olá! Tenho um precatório trabalhista e quero uma proposta."
    body = """
  <h2>O que é precatório trabalhista</h2>
  <p>É a ordem de pagamento que surge quando alguém ganha uma ação na Justiça do Trabalho contra um <strong>órgão público</strong>: a União, um estado, uma prefeitura ou uma autarquia. É o caso, por exemplo, de empregados públicos contratados pela CLT que cobram diferenças salariais.</p>
  <p>Só existe precatório quando quem deve é um órgão público. Se a ação foi contra uma empresa privada, o pagamento segue outro caminho e não há precatório. Valores pequenos são pagos por RPV, que é mais rápida.</p>

  <h2>Natureza alimentar e prioridade</h2>
  <p>Créditos trabalhistas são de natureza alimentar e entram na fila dos precatórios alimentares, que é paga antes dos demais. O STF já decidiu que a venda não muda essa natureza do precatório. Já a <a href="/blog/superpreferencia-precatorio/">superpreferência</a> de credores com 60 anos ou mais, doença grave ou deficiência é pessoal e não passa para quem compra.</p>

  """ + PASSOS + """
  <p>Cada Tribunal Regional do Trabalho tem procedimentos próprios para registrar a cessão. Na análise, conferimos o processo, o tribunal e o devedor antes de fazer a proposta.</p>

  <h2>Prazo de pagamento</h2>
  <p>O prazo depende de quem deve. Precatórios da União seguem o calendário federal, que costuma ser cumprido em dia; os de estados e prefeituras dependem do limite anual de pagamento de cada um. Veja <a href="/vender-precatorio-federal/">precatório federal</a>, <a href="/vender-precatorio-estadual/">precatório estadual</a>, <a href="/vender-precatorio-municipal/">precatório municipal</a> e <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>

  <h2>Quanto você recebe</h2>
  <p>O valor depende do devedor, do prazo previsto, da situação do processo e dos descontos. Faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a> e entenda o cálculo em <a href="/blog/desagio-precatorio/">deságio de precatório</a>. A visão geral de como <a href="/">vender precatório</a> está na página inicial.</p>
""" + cta("Tem um precatório trabalhista?", "Envie o número do processo e receba uma proposta por escrito, sem compromisso.", msg)
    faq=[("Todo crédito trabalhista vira precatório?","Não. Só vira precatório quando quem deve é um órgão público, como a União, um estado, uma prefeitura ou uma autarquia, e o valor passa do limite da RPV."),
         ("Posso vender precatório trabalhista?","Sim. A cessão de precatórios é permitida pelo art. 100, §13, da Constituição. Na análise, conferimos as regras do tribunal do seu processo antes de fazer a proposta."),
         ("A venda muda a natureza alimentar do precatório?","Não. O STF decidiu que a cessão não muda a natureza alimentar do precatório. Mas a superpreferência por idade, doença grave ou deficiência é pessoal e não passa para quem compra."),
         ("Em quanto tempo recebo?","Na Antecipay, o valor é pago em até 72 horas depois da proposta aprovada e do contrato de cessão assinado.")]
    landing("vender-precatorio-trabalhista","Vender precatório trabalhista: receba à vista | Antecipay",
        "Venda o seu precatório trabalhista contra a União, estados ou prefeituras e receba à vista. Análise jurídica, proposta por escrito e atendimento digital.",
        "Precatório trabalhista","Trabalhista","Venda o seu precatório trabalhista e receba à vista",
        "Ganhou uma ação trabalhista contra um órgão público e está esperando o precatório? A Antecipay compra o seu crédito e você recebe agora, sem esperar a fila.",
        msg,"Precatório trabalhista é a ordem de pagamento de uma ação ganha na Justiça do Trabalho contra um órgão público, como a União, um estado, uma prefeitura ou uma autarquia. Ele pode ser vendido por contrato de cessão de crédito, permitido pelo art. 100, §13, da Constituição. Na venda, você recebe à vista e quem compra passa a receber do governo no futuro.",
        body, faq, "Compra de precatório trabalhista")


if __name__ == "__main__":
    for p in POSTS: build_post(p)
    build_index(); build_sobre(); build_autora(); build_inss(); build_rn(); build_natal(); build_estados(); build_federal(); build_municipal(); build_estadual(); build_melhor(); build_calc(); build_antecipacao(); build_trabalhista(); build_llms(); build_sitemap()
    print("ok", len(POSTS), "artigos")
