"""Gera as páginas do blog da Antecipay (HTML estático).
Para adicionar um artigo: inclua um dict em POSTS e rode `python3 build_blog.py`."""
import json, os, urllib.parse, html

SITE = "https://antecipayprecatorios.com.br"
WA = "5584994938383"
UPDATED = "2026-10-07"
UPDATED_BR = "7 de outubro de 2026"

def wa(msg):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8a9.8 9.8 0 01-5-1.37l-.36-.21-3.72.97.99-3.63-.23-.37A9.8 9.8 0 012.2 12 9.85 9.85 0 0112.05 2.2c2.63 0 5.1 1.03 6.96 2.89A9.78 9.78 0 0121.9 12a9.86 9.86 0 01-9.85 9.8zm8.38-18.18A11.76 11.76 0 0012.05.15C5.5.15.16 5.48.16 12.03c0 2.1.55 4.14 1.59 5.94L.06 24l6.17-1.62a11.87 11.87 0 005.81 1.48c6.55 0 11.89-5.33 11.89-11.88 0-3.18-1.24-6.16-3.49-8.4z"/></svg>'

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/blog.css">
{extra_ld}
<!-- Microsoft Clarity -->
<script>
(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","yqi1puom0k");
document.addEventListener("click",function(e){{var a=e.target.closest&&e.target.closest('a[href*="wa.me"]');if(a&&window.clarity){{clarity("event","whatsapp_click");}}}});
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top">
  <div class="wrap nav">
    <a href="/" class="logo" translate="no">Antecipay</a>
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
      <div><a href="/" class="logo" translate="no">Antecipay</a><p style="margin-top:12px;max-width:340px">Sediada em Natal-RN, atendendo credores de todo o Brasil.</p></div>
      <ul><li><a href="/">Vender precatório</a></li><li><a href="/calculadora-precatorio/">Calculadora de precatório</a></li><li><a href="/vender-precatorio-federal/">Precatório federal</a></li><li><a href="/vender-precatorio-estadual/">Precatório estadual</a></li><li><a href="/vender-precatorio-municipal/">Precatório municipal</a></li><li><a href="/melhor-empresa-para-vender-precatorio/">Como escolher a empresa</a></li><li><a href="/sobre/">Sobre a Antecipay</a></li><li><a href="/vender-precatorio-inss/">Precatório do INSS</a></li><li><a href="/vender-precatorio-rn/">Precatório no RN</a></li><li><a href="/empresa-que-compra-precatorio-natal/">Empresa de precatórios em Natal</a></li><li><a href="/blog/">Blog</a></li><li><a href="/privacidade.html">Política de Privacidade</a></li></ul>
      <ul><li><a href="{wa('Olá! Vim pelo site da Antecipay.')}" target="_blank" rel="noopener">WhatsApp (84) 99493-8383</a></li><li><a href="mailto:contato@antecipay.com.br">contato@antecipay.com.br</a></li><li>Av. Senador Salgado Filho, 1559 – Tirol, Natal-RN</li></ul>
    </div>
    <div class="legal"><span>© 2026 Antecipay Precatórios</span><span>CNPJ 64.382.432/0001-97</span></div>
  </div>
</footer>
<a class="fab" href="{wa('Olá! Vim pelo blog e tenho um precatório para antecipar.')}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp"><svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8a9.8 9.8 0 01-5-1.37l-.36-.21-3.72.97.99-3.63-.23-.37A9.8 9.8 0 012.2 12 9.85 9.85 0 0112.05 2.2c2.63 0 5.1 1.03 6.96 2.89A9.78 9.78 0 0121.9 12a9.86 9.86 0 01-9.85 9.8zm8.38-18.18A11.76 11.76 0 0012.05.15C5.5.15.16 5.48.16 12.03c0 2.1.55 4.14 1.59 5.94L.06 24l6.17-1.62a11.87 11.87 0 005.81 1.48c6.55 0 11.89-5.33 11.89-11.88 0-3.18-1.24-6.16-3.49-8.4z"/></svg></a>
</body>
</html>
"""

NOTE = '<p class="note">Conteúdo informativo, atualizado em ' + UPDATED_BR + '. As regras de pagamento de precatórios mudam com frequência e cada processo tem particularidades. Para uma análise do seu caso, fale com a nossa equipe.</p>'

def cta(title, text, msg):
    return f'<div class="cta"><h2>{title}</h2><p>{text}</p><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Falar no WhatsApp</a></div>'

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
<p>Quem tem um crédito pouco acima do limite pode, em alguns casos, <strong>renunciar ao valor que excede</strong> para receber como RPV, bem mais rápido. É uma decisão que precisa ser feita no processo e vale a pena fazer as contas antes.</p>
<h2>E se eu não quiser esperar?</h2>
<p>O precatório é um direito de crédito e pode ser <strong>vendido (cedido)</strong> a terceiros, como a Antecipay. Você recebe um valor à vista agora e quem compra passa a receber do governo no futuro. Entenda como funciona no artigo <a href="/blog/desagio-precatorio/">Deságio: por que recebo menos ao antecipar</a>.</p>
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
<p>Essa data mudou com a <strong>Emenda Constitucional 136/2025</strong>. Até então, o corte era 2 de abril. Na prática, entre a inscrição e o dinheiro na conta podem se passar de 11 a quase 24 meses.</p>
<h2>Precatório estadual e municipal</h2>
<p>Aqui a espera costuma ser bem maior. Com a EC 136/2025, estados e municípios passaram a pagar os precatórios dentro de um <strong>limite anual de 1% a 5% da receita corrente líquida</strong>, conforme o tamanho da dívida de cada um. Quem deve muito paga uma parte por ano e a fila anda devagar.</p>
<p>Por isso, dois credores com o mesmo valor podem esperar tempos muito diferentes: tudo depende de <strong>qual estado ou município</strong> deve e da sua posição na fila.</p>
<h2>RPV: o caminho mais rápido</h2>
<p>Se o valor estiver dentro do limite de pequeno valor, o pagamento sai como RPV, em geral em até 60 dias. Veja os limites em <a href="/blog/o-que-e-precatorio-e-rpv/">O que é precatório e RPV</a>.</p>
<h2>Quem tem prioridade na fila</h2>
<p>A Constituição garante prioridade a credores com <strong>60 anos ou mais</strong>, com <strong>doença grave</strong> ou com <strong>deficiência</strong>. Eles podem receber antes uma parte do crédito, até um limite legal. O restante segue a fila normal.</p>
<h2>O valor é corrigido enquanto espero?</h2>
<p>Sim. Pelas regras atuais, o valor é atualizado pelo IPCA, com juros simples de 2% ao ano (ou pela Selic, se ela for maior). Ainda assim, esperar anos significa adiar planos, e é por isso que muitos credores preferem antecipar.</p>
""",
  cta=("Não quer esperar a fila?","A Antecipay compra o seu precatório e você recebe à vista.","Olá! Li o artigo sobre prazos e quero antecipar meu precatório."),
  related=["como-saber-se-tenho-precatorio","desagio-precatorio","o-que-e-precatorio-e-rpv"],
 ),
 dict(
  slug="como-saber-se-tenho-precatorio",
  tag="Consulta",
  title="Como saber se tenho precatório a receber",
  seo="Como saber se tenho precatório: consulta por CPF | Antecipay",
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
<tr><td>TRF1</td><td>DF, GO, TO, MT, BA, PI, MA, PA, AM, AC, RR, RO, AP</td></tr>
<tr><td>TRF2</td><td>RJ, ES</td></tr>
<tr><td>TRF3</td><td>SP, MS</td></tr>
<tr><td>TRF4</td><td>RS, PR, SC</td></tr>
<tr><td>TRF5</td><td>PE, CE, AL, SE, RN, PB</td></tr>
<tr><td>TRF6</td><td>MG</td></tr>
</table></div>
<h2>3. Faça a consulta</h2>
<ol>
<li>Entre no site do tribunal e procure a área <strong>"Precatórios e RPV"</strong> ou <strong>"Consulta de requisições"</strong>.</li>
<li>Pesquise pelo seu <strong>CPF</strong> (ou CNPJ) ou pelo <strong>número do processo</strong>.</li>
<li>Anote o número do precatório, o valor, o ano do orçamento e a situação (por exemplo, "inscrito", "pago" ou "aguardando pagamento").</li>
</ol>
<p>No Rio Grande do Norte, por exemplo, precatórios federais são consultados no portal do <strong>TRF5</strong>, e os estaduais e municipais no <strong>TJRN</strong>.</p>
<h2>4. Não encontrou nada?</h2>
<p>A ação pode ainda não ter chegado à fase de pagamento, ou o precatório pode ter sido expedido com outros dados. Nesse caso, fale com o advogado que cuidou da ação ou envie o número do processo para a nossa equipe, que fazemos a análise.</p>
<h2>Achei meu precatório. E agora?</h2>
<p>Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo ele deve levar para ser pago</a>. Se não quiser esperar, você pode antecipar: a Antecipay compra o precatório e você recebe à vista.</p>
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
<p>Quando você antecipa, a empresa que compra o precatório <strong>paga agora</strong> e só vai <strong>receber do governo depois</strong>, às vezes anos depois. Durante esse tempo, o dinheiro dela fica parado e ela assume riscos, como atrasos no pagamento e mudanças nas regras. O deságio é o que remunera essa espera e esses riscos.</p>
<h2>O que influencia o valor da proposta</h2>
<ul>
<li><strong>Quem deve:</strong> precatórios federais costumam ter prazo mais previsível. Estados e municípios com muita dívida pagam mais devagar.</li>
<li><strong>Prazo esperado:</strong> quanto mais perto do pagamento, menor tende a ser o deságio.</li>
<li><strong>Situação do processo:</strong> pendências, discussões sobre o valor ou falta de documentos aumentam o risco.</li>
<li><strong>Descontos no crédito:</strong> honorários contratuais, imposto de renda e contribuições podem ser descontados do valor final.</li>
</ul>
<h2>Vale a pena antecipar?</h2>
<p>Depende da sua necessidade. Se você pode esperar, receber o valor cheio do governo pode compensar. Se precisa do dinheiro agora, para quitar dívidas com juros altos, investir ou realizar um plano, antecipar pode fazer mais sentido. O ideal é comparar a proposta com o tempo que você ainda esperaria. Veja <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora cada tipo de precatório</a>.</p>
<h2>O que conferir antes de assinar</h2>
<ol>
<li><strong>Valor líquido:</strong> quanto cai na sua conta, já com todos os descontos.</li>
<li><strong>Prazo de pagamento</strong> depois da assinatura.</li>
<li><strong>Contrato de cessão</strong> claro, com a identificação do precatório e das partes.</li>
<li><strong>Comunicação ao tribunal</strong>, que é o que formaliza a troca de credor.</li>
<li><strong>Empresa séria:</strong> CNPJ ativo, endereço e canais de contato verdadeiros.</li>
</ol>
<p>Na Antecipay, a proposta é apresentada por escrito, com o valor líquido, antes de qualquer assinatura.</p>
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
<p>Na prática, entre a inscrição e o dinheiro na conta podem se passar de 11 meses a quase 2 anos. Veja mais em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora para receber um precatório</a>.</p>
<h2>Prioridade para idosos, doentes graves e pessoas com deficiência</h2>
<p>Os atrasados de benefício do INSS são de <strong>natureza alimentar</strong> e têm preferência na fila. Além disso, credores com <strong>60 anos ou mais</strong>, com <strong>doença grave</strong> ou com <strong>deficiência</strong> podem receber antes uma parte do crédito, até o triplo do limite da RPV (180 salários mínimos). O restante segue a fila normal.</p>
<p><strong>Atenção:</strong> essa prioridade é pessoal. Se o precatório for vendido, quem compra não aproveita a preferência. Por isso, quem tem direito a ela deve avaliar com calma se vale antecipar todo o crédito ou só a parte que ainda ficaria na fila.</p>
<h2>Tem imposto de renda?</h2>
<p>Em geral, sim. Os atrasados previdenciários são tributados pelo regime de <strong>rendimentos recebidos acumuladamente (RRA)</strong>, que divide o valor pelos meses de atraso e costuma resultar em imposto menor. Aposentados com doença grave prevista em lei podem ser isentos, e os juros de mora sobre verbas alimentares não são tributados.</p>
<h2>Como consultar o seu precatório do INSS</h2>
<p>Entre no portal do TRF da sua região e pesquise pelo CPF ou pelo número do processo. O passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>.</p>
<h2>Não quer esperar?</h2>
<p>O precatório do INSS pode ser vendido. Você recebe um valor à vista agora e quem compra passa a receber da União no futuro. Veja <a href="/vender-precatorio-inss/">como funciona a venda do precatório do INSS na Antecipay</a>.</p>
""",
  cta=("Tem precatório do INSS?","Envie o número do processo e receba uma proposta por escrito.","Olá! Li o artigo sobre precatório do INSS e quero uma proposta."),
  related=["quanto-tempo-demora-precatorio","como-saber-se-tenho-precatorio","desagio-precatorio"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="como-vender-precatorio",
  tag="Vender precatório",
  title="Como vender precatório com segurança: passo a passo",
  seo="Como vender precatório com segurança | Antecipay",
  desc="Veja como vender precatório passo a passo: quem pode vender, documentos, como é calculada a proposta, o contrato de cessão e os cuidados para não cair em golpe.",
  lead="Vender o precatório é a forma de receber agora um valor que o governo só pagaria no futuro. Veja como funciona a venda, do primeiro contato ao dinheiro na conta, e o que conferir para fazer isso com segurança.",
  answer="Para vender precatório, você envia o número do processo a uma empresa compradora, recebe uma proposta por escrito com o valor líquido e, se aceitar, assina um contrato de cessão de crédito, que é comunicado ao tribunal. O pagamento é feito à vista ao credor. A venda é permitida pela Constituição (art. 100, §13).",
  faq=[
   ("Quem pode vender precatório?","O titular do crédito, seja pessoa física ou empresa. Herdeiros também podem vender, depois de regularizada a sucessão no processo."),
   ("Preciso de advogado para vender precatório?","Não é obrigatório, mas é recomendado avisar o advogado que cuidou da ação, porque os honorários contratuais dele costumam ser descontados do crédito."),
   ("Onde vender precatório com segurança?","Com uma empresa que tenha CNPJ ativo, endereço e contatos verdadeiros, que apresente a proposta por escrito e formalize a cessão no tribunal. Desconfie de quem pede pagamento antecipado."),
   ("Quanto tempo leva para vender precatório?","Depende da análise do processo. Na Antecipay, depois da proposta aprovada e da cessão assinada, o pagamento é feito em até 72 horas."),
  ],
  body="""
<h2>Quem pode vender precatório</h2>
<p>Pode vender quem é o <strong>titular do crédito</strong>: a pessoa física ou empresa que ganhou a ação. Se o titular faleceu, os <strong>herdeiros</strong> podem vender depois de regularizar a sucessão no processo. Precatórios federais, do INSS, estaduais e municipais podem ser vendidos.</p>

<h2>Passo a passo para vender precatório</h2>
<ol>
<li><strong>Reúna o número do processo.</strong> Se não souber, veja <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>.</li>
<li><strong>Peça uma proposta.</strong> A empresa analisa o processo, o valor, os descontos e o prazo previsto de pagamento.</li>
<li><strong>Compare a proposta</strong> com o tempo que você ainda esperaria. Entenda o desconto em <a href="/blog/desagio-precatorio/">deságio de precatório</a>.</li>
<li><strong>Assine o contrato de cessão de crédito</strong>, que identifica o precatório, as partes e o valor pago.</li>
<li><strong>Receba à vista.</strong> A cessão é comunicada ao tribunal e quem comprou passa a receber do governo no futuro.</li>
</ol>

<h2>Documentos normalmente pedidos</h2>
<ul>
<li>Documento de identidade e CPF (ou CNPJ, se for empresa).</li>
<li>Número do processo e, se tiver, o ofício requisitório.</li>
<li>Comprovante de endereço e dados bancários para o pagamento.</li>
<li>Em caso de herança, documentos da sucessão.</li>
</ul>

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

<h2>Quando vale a pena vender</h2>
<p>Vender faz sentido para quem precisa do dinheiro agora, quer quitar dívidas com juros altos ou não quer esperar a fila do governo. Quem pode esperar recebe o valor cheio no futuro. Credores com 60 anos ou mais, doença grave ou deficiência devem considerar que a prioridade de pagamento deles é pessoal e não passa para quem compra.</p>
<p>Para precatórios do INSS, veja a página <a href="/vender-precatorio-inss/">vender precatório do INSS</a>. Para o Rio Grande do Norte, veja <a href="/vender-precatorio-rn/">vender precatório no RN</a>.</p>
""",
  cta=("Quer vender seu precatório?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Quero vender meu precatório. Podem me enviar uma proposta?"),
  related=["desagio-precatorio","quanto-tempo-demora-precatorio","precatorio-inss"],
))
BY = {p["slug"]: p for p in POSTS}

POSTS.insert(0, dict(
  slug="empresas-que-compram-precatorios-natal",
  tag="Natal-RN",
  title="Empresas que compram precatórios em Natal: como escolher com segurança",
  seo="Empresas que compram precatórios em Natal | Antecipay",
  desc="Procurando empresas que compram precatórios em Natal? Veja o que conferir antes de vender, os sinais de alerta e as opções para precatórios federais, estaduais e da Prefeitura de Natal.",
  lead="Quem tem um precatório a receber em Natal encontra várias empresas oferecendo compra. Veja como comparar as propostas e escolher com quem negociar com segurança.",
  answer="Para escolher uma empresa que compra precatórios em Natal, confira se ela tem CNPJ ativo e endereço real, se apresenta a proposta por escrito com o valor líquido, se formaliza a cessão de crédito no tribunal e se não cobra nada antecipado. Compare também o prazo de pagamento e a clareza do contrato.",
  faq=[
   ("Existe empresa que compra precatório em Natal?","Sim. Há empresas de todo o país que compram precatórios de credores de Natal, e algumas têm sede na própria cidade, como a Antecipay, na Incubadora do IFRN – Campus Natal Central."),
   ("A Prefeitura de Natal faz acordo para pagar precatório?","A Prefeitura de Natal mantém um portal de precatórios com edital de credenciamento para acordos diretos com credores, mediante deságio. Vale comparar essa opção com as propostas de empresas compradoras."),
   ("Vender para uma empresa de Natal é melhor?","Ter sede na cidade facilita o contato e a conferência de que a empresa existe. O mais importante, porém, é a transparência da proposta e do contrato."),
  ],
  body="""
<h2>Quem compra precatórios em Natal</h2>
<p>Credores de Natal costumam receber propostas de três tipos de compradores:</p>
<ul>
<li><strong>Empresas especializadas</strong> em compra de precatórios, nacionais ou com sede no RN.</li>
<li><strong>Bancos e fundos de investimento</strong> que atuam nesse mercado.</li>
<li><strong>O próprio ente devedor</strong>, por meio de acordo direto. A Prefeitura de Natal, por exemplo, mantém um portal de precatórios com edital de credenciamento para acordos com deságio.</li>
</ul>
<p>Cada opção tem prazo, desconto e burocracia diferentes. Vale pedir mais de uma proposta e comparar.</p>

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
<p>Na cessão, você recebe menos que o valor cheio porque antecipa um dinheiro que só viria no futuro. Entenda em <a href="/blog/desagio-precatorio/">deságio de precatório</a> e faça uma estimativa na <a href="/calculadora-precatorio/">calculadora</a>.</p>
""",
  cta=("Quer ceder o seu precatório?","Envie o número do processo e receba uma proposta por escrito, sem compromisso.","Olá! Li o artigo sobre cessão de precatório e quero uma proposta."),
  related=["como-vender-precatorio","desagio-precatorio","empresas-que-compram-precatorios-natal"],
))
BY = {p["slug"]: p for p in POSTS}

def build_post(p):
    url = f"{SITE}/blog/{p['slug']}/"
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"Article","headline":p["title"],"description":p["desc"],"dateModified":UPDATED,"datePublished":UPDATED,
       "author":{"@type":"Organization","name":"Antecipay"},"publisher":{"@type":"Organization","name":"Antecipay","logo":{"@type":"ImageObject","url":SITE+"/logo-512.png"}},
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
    <p class="meta">Equipe Antecipay · Atualizado em {UPDATED_BR} · {mins} min de leitura</p>
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
    out = head("Blog sobre precatórios: guias e prazos | Antecipay", "Guias simples sobre precatório e RPV: prazos de pagamento, como consultar, deságio e antecipação.", url,
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


def build_sobre():
    url = SITE + "/sobre/"
    ld = {"@context":"https://schema.org","@type":"AboutPage","url":url,"name":"Sobre a Antecipay",
      "mainEntity":{"@type":"FinancialService","name":"Antecipay Precatórios","logo":SITE+"/logo-512.png","legalName":"Antecipay Precatórios","taxID":"64.382.432/0001-97",
        "url":SITE+"/","email":"contato@antecipay.com.br","telephone":"+55-84-99493-8383",
        "description":"Empresa que compra e antecipa precatórios federais, estaduais e municipais em todo o Brasil.",
        "areaServed":{"@type":"Country","name":"Brasil"},
        "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol (Incubadora do IFRN – Campus Natal Central)","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"},
        "knowsAbout":["Precatórios","RPV","Cessão de crédito","Precatórios do INSS","Precatórios federais","Precatórios estaduais","Precatórios municipais"]}}
    out = head("Sobre a Antecipay | Compra e antecipação de precatórios", "Conheça a Antecipay: empresa de Natal-RN que compra e antecipa precatórios federais, estaduais e municipais em todo o Brasil. CNPJ 64.382.432/0001-97.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="sobre") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Sobre</span></nav>
  <span class="eyebrow">Sobre nós</span>
  <h1>Sobre a Antecipay</h1>
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

  <h2>Dados da empresa</h2>
  <div class="table-wrap"><table>
    <tr><td><strong>Razão social</strong></td><td>Antecipay Precatórios</td></tr>
    <tr><td><strong>CNPJ</strong></td><td>64.382.432/0001-97</td></tr>
    <tr><td><strong>Endereço</strong></td><td>Av. Senador Salgado Filho, 1559 – Tirol, Incubadora do IFRN – Campus Natal Central, Natal-RN, CEP 59015-000</td></tr>
    <tr><td><strong>WhatsApp</strong></td><td>(84) 99493-8383</td></tr>
    <tr><td><strong>E-mail</strong></td><td>contato@antecipay.com.br</td></tr>
    <tr><td><strong>Site</strong></td><td>antecipayprecatorios.com.br</td></tr>
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

## Páginas principais

- [Início]({SITE}/): apresentação, simulador e contato
- [Sobre a Antecipay]({SITE}/sobre/): quem somos, dados da empresa e como funciona
- [Calculadora de precatório]({SITE}/calculadora-precatorio/): estimativa de quanto vale o precatório à vista
- [Precatório federal]({SITE}/vender-precatorio-federal/): prazo de pagamento e venda de precatórios da União
- [Vender precatório estadual]({SITE}/vender-precatorio-estadual/): compra de precatórios de estados
- [Vender precatório municipal]({SITE}/vender-precatorio-municipal/): compra de precatórios de prefeituras
- [Qual a melhor empresa para vender precatório]({SITE}/melhor-empresa-para-vender-precatorio/): 7 pontos para escolher com segurança
- [Vender precatório do INSS]({SITE}/vender-precatorio-inss/): compra e antecipação de precatórios do INSS
- [Vender precatório no RN]({SITE}/vender-precatorio-rn/): precatórios do TRF5 e do TJRN (Estado do RN e municípios)
- [Empresa que compra precatórios em Natal]({SITE}/empresa-que-compra-precatorio-natal/): sede, contato e atendimento em Natal-RN
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
         "provider":{"@type":"FinancialService","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png"},"url":url},
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
  <p style="margin-top:28px"><a class="btn btn-wa" href="{wa('Olá! Tenho um precatório do INSS e quero uma proposta.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a></p>
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
  <p>Se você tem 60 anos ou mais, doença grave ou deficiência, pode ter direito a receber antes uma parte do crédito. Essa prioridade não passa para quem compra, então avaliamos com você a melhor opção. Entenda mais em <a href="/blog/precatorio-inss/">Precatório do INSS: como funciona e quanto tempo demora</a> e em <a href="/blog/desagio-precatorio/">Deságio: por que recebo menos ao antecipar</a>.</p>
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
         "provider":{"@type":"FinancialService","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png",
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
  <p style="margin-top:28px"><a class="btn btn-wa" href="{wa('Olá! Tenho um precatório no RN e quero uma proposta.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a></p>
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
  <p>Passo a passo completo em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório a receber</a>. Se preferir, envie o número do processo que a nossa equipe consulta para você.</p>

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
         "description":"Empresa de Natal-RN que compra precatórios federais, estaduais e municipais.",
         "address":{"@type":"PostalAddress","streetAddress":"Av. Senador Salgado Filho, 1559 – Tirol (Incubadora do IFRN – Campus Natal Central)","postalCode":"59015-000","addressLocality":"Natal","addressRegion":"RN","addressCountry":"BR"},
         "areaServed":[{"@type":"City","name":"Natal"},{"@type":"State","name":"Rio Grande do Norte"},{"@type":"Country","name":"Brasil"}],
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"08:00","closes":"12:00"}]},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    faq_html="".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in faq)
    out = head("Empresa que compra precatórios em Natal-RN | Antecipay", "A Antecipay é uma empresa de Natal-RN que compra precatórios federais, do INSS, do Estado do RN e da Prefeitura de Natal. Proposta por escrito e pagamento à vista.", url,
               '<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>', current="") + f"""
<main id="conteudo" tabindex="-1">
<section class="art-head"><div class="narrow">
  <nav class="crumbs" aria-label="Trilha de navegação"><a href="/">Início</a> <span aria-hidden="true">›</span> <span aria-current="page">Natal-RN</span></nav>
  <span class="eyebrow">Natal-RN</span>
  <h1>Empresa que compra precatórios em Natal</h1>
  <p class="lead">A Antecipay é uma empresa de Natal que compra precatórios da União, do INSS, do Estado do RN e da Prefeitura de Natal. Você recebe à vista, com proposta por escrito e segurança jurídica.</p>
  <p style="margin-top:28px"><a class="btn btn-wa" href="{wa('Olá! Sou de Natal e quero vender meu precatório.')}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a></p>
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
  <p>Também atendemos credores de todo o Brasil. Veja <a href="/vender-precatorio-rn/">vender precatório no RN</a> e <a href="/vender-precatorio-inss/">vender precatório do INSS</a>.</p>

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
  <p>Compare propostas e confira os pontos de segurança no guia <a href="/blog/empresas-que-compram-precatorios-natal/">empresas que compram precatórios em Natal: como escolher</a>. Credores da Prefeitura de Natal também podem avaliar o acordo direto oferecido pelo município.</p>

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


def landing(slug, seo, desc, crumb, eyebrow, h1, lead, wa_msg, answer, body, faq, service_name, extra_top=""):
    url = SITE + f"/{slug}/"
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":service_name,"serviceType":"Antecipação de precatório","areaServed":{"@type":"Country","name":"Brasil"},
         "provider":{"@type":"FinancialService","name":"Antecipay Precatórios","url":SITE+"/","telephone":"+55-84-99493-8383","logo":SITE+"/logo-512.png"},"url":url},
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
  <p style="margin-top:28px"><a class="btn btn-wa" href="{wa(wa_msg)}" target="_blank" rel="noopener">{WA_ICON}Quero uma proposta</a></p>
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
  <p>Cada município é um caso: há prefeituras em dia e outras com anos de atraso. Por isso analisamos o devedor antes de fazer a proposta.</p>
  <h2>Vender ou esperar?</h2>
  <div class="table-wrap"><table>
    <tr><th>Opção</th><th>Vantagem</th><th>Ponto de atenção</th></tr>
    <tr><td><strong>Esperar a fila</strong></td><td>Recebe o valor cheio, corrigido</td><td>Prazo incerto, pode levar anos</td></tr>
    <tr><td><strong>Acordo direto com a prefeitura</strong></td><td>Recebe antes, se houver edital</td><td>Depende de edital aberto e tem deságio</td></tr>
    <tr><td><strong>Vender para a Antecipay</strong></td><td>Dinheiro à vista, sem depender de edital</td><td>Há deságio pela antecipação</td></tr>
  </table></div>
  <p>Algumas prefeituras, como a de Natal, abrem editais de acordo direto. Vale comparar a proposta do acordo com a nossa. Veja também <a href="/blog/desagio-precatorio/">o que é deságio e como ele é calculado</a>.</p>
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
  <p>Pela EC 136/2025, os estados pagam dentro de um limite anual de 1% a 5% da receita corrente líquida, conforme o tamanho do estoque de precatórios. Alguns estados estão em dia; outros têm filas de muitos anos. A posição na fila e a data de inscrição fazem diferença no prazo.</p>
  <p>Se o seu precatório é do Rio Grande do Norte, veja a página <a href="/vender-precatorio-rn/">vender precatório no RN</a>.</p>
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
        "Venda seu precatório estadual e receba à vista, sem esperar a fila do estado. Análise jurídica, proposta por escrito e atendimento 100% digital pelo WhatsApp.",
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
  <p>Veja mais em <a href="/blog/como-vender-precatorio/">como vender precatório com segurança</a>.</p>
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
  <p>A calculadora parte do valor do precatório, desconta os honorários contratuais que você informou e aplica uma faixa de deságio típica para o tipo de devedor e a situação do processo. É uma referência para você saber a ordem de grandeza antes de conversar com qualquer empresa.</p>
  <h2>O que muda o valor da sua proposta</h2>
  <ul>
    <li><strong>Devedor:</strong> precatórios federais costumam ter deságio menor, porque a União paga em prazo previsível. Estados e prefeituras variam muito.</li>
    <li><strong>Prazo até o pagamento:</strong> quanto mais longe o pagamento, maior o deságio.</li>
    <li><strong>Situação do processo:</strong> precatório já expedido e inscrito tem menos risco que um ainda em fase de cálculo.</li>
    <li><strong>Descontos:</strong> imposto de renda (em geral pelo regime de rendimentos acumulados), contribuição previdenciária e honorários.</li>
    <li><strong>Prioridades:</strong> a parcela superpreferencial de idosos, doentes graves e pessoas com deficiência é pessoal e não é transferida para quem compra.</li>
  </ul>
  <p>Entenda o cálculo em detalhes em <a href="/blog/desagio-precatorio/">deságio de precatório</a> e veja os prazos em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>
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
    landing("calculadora-precatorio","Quanto vale meu precatório? Calculadora | Antecipay",
        "Calcule quanto vale o seu precatório federal, estadual ou municipal se vender agora. Estimativa gratuita e proposta por escrito pelo WhatsApp.",
        "Calculadora","Calculadora","Quanto vale o meu precatório?",
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
  <p>A data de corte de 1º de fevereiro vale desde a Emenda Constitucional 136/2025; antes, era 2 de abril. Na prática, entre a inscrição e o dinheiro na conta podem se passar de 11 a quase 24 meses. Veja os detalhes em <a href="/blog/quanto-tempo-demora-precatorio/">quanto tempo demora um precatório</a>.</p>
  <h2>Como consultar o precatório federal</h2>
  <p>No portal de RPV e precatórios do TRF da sua região, pelo CPF ou pelo número do processo. O passo a passo está em <a href="/blog/como-saber-se-tenho-precatorio/">como saber se tenho precatório</a>. Se preferir, envie o número do processo pelo WhatsApp e nós consultamos para você.</p>
  <h2>Vale a pena vender o precatório federal?</h2>
  <p>O precatório federal é o que tem o pagamento mais previsível, por isso costuma ter o <strong>menor deságio</strong> entre os precatórios. Vender faz sentido para quem precisa do dinheiro agora ou não quer esperar até dois anos. Quem pode esperar recebe o valor cheio, corrigido. Faça uma estimativa na <a href="/calculadora-precatorio/">calculadora de precatório</a>.</p>
  {PASSOS}
  {cta("Quer vender o seu precatório federal?", "Envie o número do processo e receba uma proposta por escrito.", msg)}
  <h2>Precatório do INSS e prioridades</h2>
  <p>Precatórios de ações contra o INSS são federais. Veja a página <a href="/vender-precatorio-inss/">vender precatório do INSS</a>. Credores com 60 anos ou mais, doença grave ou deficiência podem receber antes uma parte do crédito; essa prioridade é pessoal e não passa para quem compra.</p>
"""
    faq=[("Quando o precatório federal é pago?","Se for inscrito até 1º de fevereiro, até o fim do ano seguinte. Inscrito depois dessa data, até o fim do segundo ano seguinte."),
         ("Posso vender precatório federal?","Sim. A Constituição (art. 100, §13) permite ceder o precatório a terceiros. A venda é feita por contrato de cessão de crédito, comunicado ao tribunal."),
         ("Qual o deságio do precatório federal?","Costuma ser o menor entre os precatórios, porque o pagamento da União é previsível. O percentual exato depende do valor, do prazo até o pagamento e da situação do processo."),
         ("Quem compra precatório federal?","Bancos, fundos e empresas especializadas. A Antecipay compra precatórios federais de credores de todo o Brasil, com proposta por escrito e pagamento à vista.")]
    landing("vender-precatorio-federal","Precatório federal 2026: prazo e como vender | Antecipay",
        "Veja quando o precatório federal é pago, como consultar no TRF e como vender o seu precatório federal à vista, com proposta por escrito e atendimento digital.",
        "Precatório federal","Precatório federal","Precatório federal: prazo de pagamento e como vender",
        "Tem um precatório contra a União ou o INSS? Veja quando ele deve ser pago e como receber à vista, sem esperar a fila do orçamento federal.",
        msg,"O precatório federal é a dívida da União, do INSS ou de autarquias federais acima de 60 salários mínimos. Inscrito até 1º de fevereiro, é pago até o fim do ano seguinte. Quem não quer esperar pode vender o precatório: a Antecipay faz uma proposta por escrito e paga à vista.",
        body, faq, "Compra de precatório federal")

def build_sitemap():
    urls = ["/", "/calculadora-precatorio/", "/vender-precatorio-federal/", "/vender-precatorio-estadual/", "/vender-precatorio-municipal/", "/melhor-empresa-para-vender-precatorio/", "/vender-precatorio-inss/", "/vender-precatorio-rn/", "/empresa-que-compra-precatorio-natal/", "/sobre/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS] + ["/privacidade.html"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>\n" for u in urls)
    xml += "</urlset>\n"
    open("sitemap.xml","w").write(xml)

if __name__ == "__main__":
    for p in POSTS: build_post(p)
    build_index(); build_sobre(); build_inss(); build_rn(); build_natal(); build_federal(); build_municipal(); build_estadual(); build_melhor(); build_calc(); build_llms(); build_sitemap()
    print("ok", len(POSTS), "artigos")
