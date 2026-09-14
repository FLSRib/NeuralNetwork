#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chatbot de Atendimento a Trouble Tickets com Análise de Sentimento (Versão rev_V3)
Disciplina: Redes Neurais / MBA FGV
Melhorias rev_V3:
- Split por Frase-Base (Zero Vazamento por Quase-Duplicidade)
- Guardrail Determinístico para Linguagem Hostil / Termos Ofensivos pt-BR
- Calibração de Threshold de Probabilidade para Priorização de Recall
- Auditoria de Motivo de Escalonamento em CSV
"""

import os
import sys
import re
import random
import argparse
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Assegura suporte a utf-8 em terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RANDOM_STATE = 42
LOG_ARQUIVO_CSV = "registro_sentimentos_tickets.csv"

# Termos ofensivos pt-BR para Guardrail de crise
TERMOS_OFENSIVOS_PTBR = [
    "merda", "porra", "caralho", "bosta", "fudeu", "foder", "fudido",
    "puta", "puto", "pqp", "carai", "desgraca", "desgraça", "cacete",
    "vsf", "vtnc", "imbecil", "idiota", "palhacada", "palhaçada"
]

TICKETS_DATA = [
    {
        "ticket_id": "TK-1001",
        "cliente": "Banco Alfa S/A",
        "servico_afetado": "Link MPLS Dedicado - Matriz",
        "ultimo_status": "Tratativa em andamento",
        "detalhes": "Equipe de campo acionada para troca de porta óptica no switch de distribuição."
    },
    {
        "ticket_id": "TK-1002",
        "cliente": "Varejo Global Logística",
        "servico_afetado": "Roteador Core BGP - Filial Campinas",
        "ultimo_status": "Fechado",
        "detalhes": "Sessão BGP restabelecida após normalização de operadora parceira. Testes concluídos com sucesso."
    },
    {
        "ticket_id": "TK-1003",
        "cliente": "Hospital São Lucas",
        "servico_afetado": "Conexão VPN IPsec Site-to-Site",
        "ultimo_status": "Aguardando cliente",
        "detalhes": "Aguardando teste de ping do cliente e validação da chave pré-compartilhada (PSK)."
    },
    {
        "ticket_id": "TK-1004",
        "cliente": "Indústria MetalTech",
        "servico_afetado": "Firewall Principal - Cluster HA",
        "ultimo_status": "Aberto",
        "detalhes": "Chamado aberto via monitoramento automático de CPU acima de 95%."
    }
]

frases_negativas_base = [
    # 1. Falhas Físicas e Hardware
    "o link continua fora do ar e a empresa está parada",
    "o roteador travou de novo e estamos sem comunicação",
    "o conversor de mídia óptico apagou e não temos redundância",
    "rompimento de fibra óptica na rota e estamos isolados",
    "sem sinal óptico na porta giga do switch de borda",
    "o enlace principal caiu e a comutação automática falhou",
    "cabo de rede danificado na caixa de terminação e sem sinal",
    "porta wan do roteador cpe não sincroniza de jeito nenhum",
    "equipamento da operadora queimou após oscilação elétrica",
    "perda total de sinal na entrada óptica da filial",
    # 2. Problemas Lógicos e de Rede (BGP / MTU / Latência / DNS)
    "a lentidão na rede continua insuportável",
    "sessão bgp com a operadora parceira fica oscilando toda hora",
    "perda massiva de pacotes acima de quarenta por cento na rota",
    "latência no link dedicado saltou para mais de trezentos milissegundos",
    "problema de fragmentação mtu travando a comunicação com matriz",
    "servidor dns da operadora parou de responder consultas",
    "túnel vpn ipsec caindo a cada cinco minutos sem estabilidade",
    "tabela de roteamento corrompida gerando loop de pacotes",
    "jitter altíssimo inviabilizando qualquer chamada de voz sobre ip",
    "rota assimétrica causando descarte massivo de pacotes",
    # 3. SLA e Falhas de Suporte
    "estou muito insatisfeito com a demora no atendimento",
    "já faz horas que abri o chamado e ninguém resolveu",
    "o atendente não soube explicar o motivo da queda",
    "o problema voltou a acontecer pela terceira vez essa semana",
    "o sla de atendimento foi completamente estourado",
    "ninguém do noc entrou em contato até agora",
    "fiquei esperando horas no telefone e não tive retorno",
    "não gostei do atendimento que recebi do suporte técnico",
    "não foi uma boa tratativa infelizmente o problema persiste",
    "prazo de restauração contratual de quatro horas venceu sem retorno",
    "suporte de nível um despreparado não consegue abrir chamado pro n2",
    "atendente anterior encerrou o ticket sem o link estar funcionando",
    "estou há horas tentando contato no zero oitocentos e ninguém atende",
    "falta de transparência total da equipe técnica no relatório",
    "chamado aberto desde ontem à noite e continua sem técnico no local",
    # 4. Impacto Financeiro e Rescisão (Persona Negócios/Financeiro)
    "péssimo suporte técnico estamos com prejuízo na operação",
    "estou muito decepcionado com a estabilidade do link",
    "vou cancelar o contrato se não resolverem isso hoje",
    "achei péssimo o serviço não recomendo para ninguém",
    "operação da fábrica totalmente paralisada gerando prejuízo",
    "nossas lojas não conseguem processar vendas com o circuito fora",
    "prejuízo no faturamento por causa dessa instabilidade recorrente",
    "se o link não voltar vou acionar o departamento jurídico",
    "vamos reter o pagamento da fatura até normalizarem o circuito",
    "diretoria já solicitou cotação em outra operadora concorrente",
    "impacto crítico no fechamento contábil devido à queda do link",
    "impossível trabalhar dessa forma estamos perdendo clientes",
    # 5. Linguagem Informal, Abreviações de Chat e Gírias
    "o link ta caindo td hora vc precisa ver isso urgente",
    "n consigo logar na vpn de jeito nenhum da erro",
    "qdo vao resolver a internet ta mt lenta hj",
    "estou c prejuizo na operacao e ngm da retorno no chamado",
    "estou c/ mta lentidao no circuito principal qto tempo p resolver",
    "vou cancelar se n consertarem a rota do roteador hj",
    "estamos sem internet e o noc n atende o tel de jeito nenhum",
    "que demora p responder esse chamado o link ta instavel d+",
    "net caiu dnv na filial e n conseguimos faturar nada hj",
    "link down e ngm resolve nada aqui socorro",
    "roteador reiniciando sozinho a cada dez minutos um caos",
    # 6. Frases com Vocabulário Hostil / Baixo Calão pt-BR (Gatilho Crítico)
    "que serviço de merda o link caiu de novo",
    "puta que pariu já faz quatro horas que estamos sem internet",
    "atendimento bosta ninguém resolve essa porra de chamado",
    "sistema caralho todo dia essa palhaçada de link fora do ar",
    "estamos fudidos com a fábrica parada e ninguém atende o telefone",
    "que porra de suporte é esse que não dá um parecer pro cliente",
    "essa merda de operadora só sabe cobrar a fatura na hora",
]

frases_positivas_base = [
    # 1. Restabelecimento Técnico Rápido
    "o atendimento do noc foi excelente e rápido",
    "muito obrigado o link já foi restabelecido com sucesso",
    "a equipe técnica foi muito atenciosa e resolveu na hora",
    "parabéns pela agilidade na troca do equipamento",
    "fiquei muito satisfeito com a solução do problema",
    "o suporte técnico foi perfeito tudo voltou a funcionar",
    "recomendo muito o trabalho da equipe de redes",
    "tudo normalizado por aqui excelente trabalho",
    "atendimento rápido eficiente e muito profissional",
    "estou muito feliz com o retorno ágil da equipe",
    "não tenho nada a reclamar suporte de altíssima qualidade",
    "resolveram a rota bgp em poucos minutos parabéns",
    "não imaginava que seria tão rápido o conserto adorei",
    "nada a reclamar atendimento perfeito do plantão",
    "o técnico de campo foi super ágil e prestativo",
    "não é exagero dizer que o suporte foi nota dez",
    "troca do conversor de fibra efetuada com maestria obrigado",
    "sessão bgp normalizada e ping voltou para doze milissegundos",
    "link redundante assumiu de forma transparente sem impacto parabéns",
    "roteador reconfigurado e tráfego fluindo com capacidade máxima",
    # 2. Confirmação de Testes e Desempenho
    "testes de throughput concluídos e banda totalmente entregue",
    "validação de failover realizada com sucesso podem fechar o ticket",
    "tráfego normalizado e latência estável abaixo de vinte milissegundos",
    "todas as dez filiais voltaram a comunicar perfeitamente",
    "perda de pacotes zerada após a manutenção excelente trabalho",
    "circuito operando com cem por cento de disponibilidade muito bom",
    "roteamento corrigido e vpn conectando com máxima velocidade",
    "serviço entregue com rigor e dentro da janela programada",
    "relatório de testes recebido e assinado tudo em ordem",
    "desempenho da conexão após o reparo superou as expectativas",
    # 3. Elogio a Atendentes e Engenharia
    "o engenheiro do noc foi brilhante no diagnóstico do problema",
    "parabéns ao analista de plantão pela clareza nas explicações",
    "atendimento humano empático e focado na solução nota cem",
    "equipe de redes muito competente e comprometida com o cliente",
    "agradeço imensamente o esforço conjunto para restabelecer o link",
    "comunicação transparente do início ao fim do incidente",
    "parceria exemplar da operadora com o nosso time de ti",
    "suporte de prontidão mesmo durante a madrugada parabéns a todos",
    "excelente postura técnica de toda a equipe envolvida",
    "atendimento cordial e assertivo resolveram com rapidez",
    # 4. Linguagem Rápida e Informal de Chat
    "valeu pela ajuda vc resolveu mt rapido hj",
    "td funcionando dnv obg pelo suporte",
    "link restabelecido c sucesso mto obrigado",
    "o suporte foi nota 10 resolveu qdo precisei",
    "atendimento top d+ vlw pela agilidade",
    "vc salvou nossa filial mt prestativo o tecnico",
    "tudo certinho por aki link voando mt obrigado",
    "parabens pelo noc resolveram qdo o link caiu de madrugada",
    "show de bola suporte agil d+ vlw",
    "link 100% obg pelo atendimento impecavel",
    "tudo ok por aqui vlw galera do suporte",
    "equipe nota mil resolveram em cinco minutos",
    "parabens pelo profissionalismo link voando",
    "obrigado time noc salvou nossa operacao hj",
    "atendimento nota dez parabens a equipe",
    "valeu msm pela atencao link top",
    "muito agradecido pelo suporte rapido e eficaz",
    "obrigado pela presteza problema 100% resolvido",
    "parabens pela eficiencia e simpatia no chat",
    "atendimento nota mil sempre impecavel",
    "link estavel operacao voando obrigado",
    "vlw pelo retorno agil e pela solucao rapida",
    "excelente atendimento como sempre parabens",
    "suporte topissimo obrigado pelo empenho",
    "resolveram perfeitamente podem finalizar o chamado",
]

frases_neutras_base = [
    # 1. Parâmetros Técnicos e Endereçamento
    "gostaria de saber qual o ip de gateway configurado",
    "qual o bloco ip publico e mascara alocados para nossa empresa",
    "solicito os ips primario e secundario dos servidores dns",
    "qual o asn configurado na sessao bgp",
    "favor informar a community bgp configurada para o circuito",
    "qual o valor de mtu configurado na porta de entrega wan",
    "preciso do ip de loopback do roteador de borda",
    "qual o vlan id configurado na interface física do switch",
    "gostaria de confirmar se a criptografia da vpn é aes duzentos e cinquenta e seis",
    "favor validar se o protocolo lldp está habilitado na porta",
    # 2. Janelas de Manutenção e Governança
    "qual é a previsão de término da manutenção programada",
    "qual o procedimento para agendar uma janela de manutenção",
    "gostaria de saber os horários do plantão nível dois",
    "preciso alterar o e-mail de notificação do monitoramento",
    "preciso atualizar o contato do responsável técnico local",
    "solicito o cronograma da próxima janela preventiva no circuito",
    "qual o procedimento para alteração cadastral do titular do link",
    "preciso cadastrar um novo técnico autorizado a receber o plantão",
    "qual o processo formal para solicitar mudança de endereço da cpe",
    "solicito confirmação de recebimento da documentação técnica enviada",
    # 3. Relatórios, Documentações e SLA
    "como faço para solicitar um relatório de tráfego mrg",
    "vocês podem enviar o log do roteador por e-mail",
    "gostaria de mais informações sobre o link redundante",
    "qual o prazo padrão de atendimento para este tipo de falha",
    "como faço para abrir um chamado para outra filial",
    "preciso do relatório de causa raiz rca assinado pelo engenheiro",
    "solicito o relatório de disponibilidade contratual do mês anterior",
    "qual o sla estipulado em contrato para restabelecimento de hardware",
    "onde posso consultar o historico completo de tickets deste contrato",
    "favor enviar o grafico de consumo de largura de banda das ultimas semanas",
    # 4. Consultas Operacionais e Esclarecimentos
    "gostaria de saber se o roteador homologado suporta protocolo ospf",
    "o circuito redundante opera em modo ativo balanceado ou ativo reserva",
    "qual o modelo e versão de firmware do equipamento instalado no rack",
    "solicito verificar se há alarmes ativos na gerência remota do link",
    "favor confirmar se a rota estática padrão aponta para o ip do gateway",
    "preciso saber qual a porta física onde o cabo de fibra está conectado",
    "qual o tempo de retenção dos logs de tráfego no portal do cliente",
    "gostaria de saber o nome do gerente de contas responsável pelo contrato",
    "onde acesso a fatura detalhada com os circuitos ativos da nossa planta",
    "solicito informação sobre a viabilidade técnica de upgrade de banda",
    # 5. Linguagem Informal e Dúvidas Curtas
    "qual o gateway configurado p testar a rota aki",
    "qdo termina a manutencao programada do link",
    "como faco p abrir chamado p outra filial",
    "preciso atualizar o cel do responsavel tecnico local",
    "qual o asn da sessao bgp p configurar o roteador",
    "pode mandar o log do router p gente analisar",
    "preciso do mtr completo desse link p avaliar perda de pacotes",
    "favor alterar o ip de gerencia do roteador da filial",
    "qual o ip de gerencia p eu pingar da minha ponta",
    "qto tempo dura a janela de manutencao preventiva hj",
    "como faco p cadastrar meu novo email de alertas",
    "favor mandar a chave publica da vpn p teste",
    "qual a mascara de subrede da wan deste link",
    "preciso saber qtas portas estao disponiveis no switch",
    "qual o telefone direto do plantao n2 do noc",
    # 6. Complementos para fechar 65 frases
    "qual a latencia media aceitavel para o circuito segundo o contrato",
    "solicito a relacao de contatos atualizada do suporte de terceiro nivel",
    "favor confirmar se a interface optica esta em modo full duplex",
    "onde solicito a segunda via da fatura mensal do link dedicado",
    "qual o procedimento para solicitar um teste conjunto de perda de pacotes",
    "preciso confirmar se o endereco mac do roteador foi atualizado na base",
    "solicito a ativacao de uma vlan adicional na porta wan da filial",
    "qual a taxa de transferencia maxima contratada em horario de pico",
    "gostaria de saber como agendar a visita tecnica de vistoria na matriz",
    "favor reenviar o relatorio de metricas semanais de consumo de banda"
]


sujeitos = ["", "sinceramente, ", "olha, ", "na real, ", "por favor, ", "informo que ", "comunicamos que ", "prezados, "]
complementos = [
    "", " novamente", " hoje", " com urgência", " no nosso circuito principal",
    " na filial matriz", " com a equipe de redes", " no link dedicado", " no chamado aberto"
]

def gerar_amostras_por_frases_base(lista_frases_base, label, base_id_offset, variacoes_por_frase=4, rng=None):
    amostras = []
    for idx_base, frase_base in enumerate(lista_frases_base):
        frase_id = f"{label}_{base_id_offset + idx_base}"
        for _ in range(variacoes_por_frase):
            p = rng.choice(sujeitos)
            s = rng.choice(complementos)
            frase = (p + frase_base + s).strip()
            frase = frase[0].upper() + frase[1:] + "."
            amostras.append({
                "texto": frase,
                "sentimento": label,
                "frase_base": frase_base,
                "frase_base_id": frase_id
            })
    return amostras

def verificar_guardrail_ofensivo(texto):
    """Intercepta termos ofensivos pt-BR para escalonamento imediato."""
    texto_norm = texto.lower()
    for termo in TERMOS_OFENSIVOS_PTBR:
        if re.search(r'\b' + re.escape(termo) + r'\b', texto_norm):
            return True, termo
    return False, None

def treinar_modelo_sentimento():
    """Treina o modelo com divisão prévia de frases-base (zero vazamento)."""
    rng = random.Random(RANDOM_STATE)
    neg_train, neg_test = train_test_split(frases_negativas_base, test_size=0.25, random_state=RANDOM_STATE)
    pos_train, pos_test = train_test_split(frases_positivas_base, test_size=0.25, random_state=RANDOM_STATE)
    neu_train, neu_test = train_test_split(frases_neutras_base, test_size=0.25, random_state=RANDOM_STATE)

    train_samples = (
        gerar_amostras_por_frases_base(neg_train, "negativo", 0, 5, rng) +
        gerar_amostras_por_frases_base(pos_train, "positivo", 0, 5, rng) +
        gerar_amostras_por_frases_base(neu_train, "neutro", 0, 5, rng)
    )
    test_samples = (
        gerar_amostras_por_frases_base(neg_test, "negativo", 1000, 5, rng) +
        gerar_amostras_por_frases_base(pos_test, "positivo", 1000, 5, rng) +
        gerar_amostras_por_frases_base(neu_test, "neutro", 1000, 5, rng)
    )
    df_tr = pd.DataFrame(train_samples)
    df_te = pd.DataFrame(test_samples)

    vec = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X_tr = vec.fit_transform(df_tr["texto"])
    X_te = vec.transform(df_te["texto"])

    mlp = MLPClassifier(hidden_layer_sizes=(32,), activation="relu", max_iter=500, random_state=RANDOM_STATE)
    mlp.fit(X_tr, df_tr["sentimento"])
    acc = accuracy_score(df_te["sentimento"], mlp.predict(X_te))
    print(f"[Setup rev_V3] MLP treinado com acurácia no teste inédito: {acc*100:.1f}% (Zero Vazamento).")
    return vec, mlp, pd.DataFrame(TICKETS_DATA)

def consultar_ticket(t_id, df_tickets):
    clean_id = str(t_id).strip().upper()
    if not clean_id.startswith("TK-"):
        clean_id = f"TK-{clean_id[2:].strip('-')}" if clean_id.startswith("TK") else f"TK-{clean_id}"
    m = df_tickets[df_tickets["ticket_id"] == clean_id]
    return m.iloc[0].to_dict() if not m.empty else None

def classificar_sentimento_hibrido(texto, vec, mlp, threshold_neg=0.30):
    is_ofensivo, termo = verificar_guardrail_ofensivo(texto)
    if is_ofensivo:
        return "negativo", 1.0, f"Guardrail Crítico: Linguagem ofensiva ('{termo}')"
    v = vec.transform([texto])
    probs = mlp.predict_proba(v)[0]
    classes = list(mlp.classes_)
    idx_neg = classes.index("negativo")
    if probs[idx_neg] >= threshold_neg:
        return "negativo", probs[idx_neg], "IA: Calibração de Recall (Negativo >= 30%)"
    else:
        idx_max = probs.argmax()
        return classes[idx_max], probs[idx_max], "IA: Máxima Verossimilhança"

def registrar_em_arquivo_csv(ticket_id, status, msg, sent, conf, motivo, caminho_csv=LOG_ARQUIVO_CSV):
    reg = pd.DataFrame([{
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticket_id": ticket_id,
        "ultimo_status": status,
        "mensagem_cliente": msg,
        "sentimento_analisado": sent,
        "score_confianca": round(conf, 4),
        "motivo_classificacao": motivo
    }])
    header = not os.path.exists(caminho_csv)
    reg.to_csv(caminho_csv, mode="a", header=header, index=False, encoding="utf-8-sig")

def executar_atendimento(t_id, msg=None, df_tickets=None, vec=None, mlp=None, log_csv=LOG_ARQUIVO_CSV):
    print("=" * 75)
    print("[BOT]: Olá! Bem-vindo ao Autoatendimento de Suporte Técnico & NOC.")
    print(f"[CLIENTE]: [Ticket informado]: {t_id}")
    info = consultar_ticket(t_id, df_tickets)
    if not info:
        print(f"[BOT]: Não localizamos o Trouble Ticket '{t_id}' em nossa base.")
        print("=" * 75 + "\n")
        return
    print(f"[BOT]: Ticket {info['ticket_id']} localizado com sucesso!")
    print(f"   • Cliente: {info['cliente']} | Serviço: {info['servico_afetado']}")
    print(f"   • Status Atual: [{info['ultimo_status'].upper()}]")
    print(f"   • Detalhes: {info['detalhes']}")
    print("-" * 75)
    print("[BOT]: Deseja algo mais ou tem alguma observação sobre este ticket?")
    if msg and msg.strip():
        print(f"[CLIENTE]: \"{msg}\"")
        sent, conf, motivo = classificar_sentimento_hibrido(msg, vec, mlp)
        if sent == "negativo":
            print(f"[BOT]: Sentimos muito pelo transtorno! Identificamos criticidade na mensagem (Sentimento: NEGATIVO | Confiança: {conf*100:.1f}%).")
            print(f"       [ALERTA NOC N2]: Escalonamento prioritário ativado (Hypercare). Motivo: {motivo}.")
        elif sent == "positivo":
            print(f"[BOT]: Ficamos muito felizes com seu retorno positivo! (Sentimento: POSITIVO | Confiança: {conf*100:.1f}%).")
            print("       Agradecemos a parceria com o NOC!")
        else:
            print(f"[BOT]: Anotamos sua observação operacional (Sentimento: NEUTRO | Confiança: {conf*100:.1f}%).")
            print(f"       Sua solicitação foi anexada ao chamado {info['ticket_id']}.")
        registrar_em_arquivo_csv(info['ticket_id'], info['ultimo_status'], msg, sent, conf, motivo, log_csv)
    else:
        print("[CLIENTE]: [Sem mensagens adicionais]")
        print("[BOT]: Perfeito! Obrigado pelo contato. Atendimento finalizado.")
    print("=" * 75 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Chatbot de Trouble Tickets com Análise de Sentimento (rev_V3)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Inicia modo interativo via terminal")
    args = parser.parse_args()

    vec, mlp, df_tickets = treinar_modelo_sentimento()

    if args.interactive:
        print("\n=== MODO INTERATIVO DO CHATBOT (rev_V3) ===")
        while True:
            t_in = input("[BOT]: Informe o número do Ticket (ou 'sair'): ")
            if t_in.lower().strip() in ["sair", "exit", "q"]:
                break
            if not t_in.strip():
                continue
            info = consultar_ticket(t_in, df_tickets)
            if not info:
                print(f"[BOT]: Ticket '{t_in}' não encontrado.\n")
                continue
            msg = input("[BOT]: Deseja algo mais ou tem alguma observação? ")
            executar_atendimento(t_in, msg, df_tickets, vec, mlp)
    else:
        print("\n--- Executando Simulação de Casos de Uso (rev_V3) ---\n")
        # 1. Caso Normal Negativo (SLA)
        executar_atendimento("TK-1001", "O link continua fora do ar e a empresa está parada, prejuízo total!", df_tickets, vec, mlp)
        # 2. Caso com Guardrail de Palavrão pt-BR
        executar_atendimento("TK-1001", "Que serviço de bosta, link fora do ar de novo porra!", df_tickets, vec, mlp)
        # 3. Caso Positivo
        executar_atendimento("1002", "Muito obrigado pelo suporte, a equipe resolveu rápido e funcionou perfeitamente!", df_tickets, vec, mlp)
        # 4. Caso Neutro
        executar_atendimento("tk-1003", "Gostaria de saber qual o IP de gateway configurado para eu testar a rota aqui.", df_tickets, vec, mlp)
        # 5. Caso Sem Mensagem
        executar_atendimento("TK-1004", None, df_tickets, vec, mlp)

if __name__ == "__main__":
    main()
