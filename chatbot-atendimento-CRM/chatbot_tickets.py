#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chatbot de Atendimento a Trouble Tickets com Análise de Sentimento (Rede Neural MLP)
Disciplina: Redes Neurais / MBA FGV
"""

import os
import random
import argparse
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

RANDOM_STATE = 42
LOG_ARQUIVO_CSV = "registro_sentimentos_tickets.csv"

# Base de Dados Sintética de Trouble Tickets
TICKETS_DATA = [
    {
        "ticket_id": "TK-1001",
        "cliente": "Banco Alfa S/A",
        "servico_afetado": "Link MPLS Dedicado - Matriz",
        "ultimo_status": "Tratativa em andamento",
        "data_abertura": "2026-08-23 09:15",
        "detalhes": "Equipe de campo acionada para troca de porta óptica no switch de distribuição."
    },
    {
        "ticket_id": "TK-1002",
        "cliente": "Varejo Global Logística",
        "servico_afetado": "Roteador Core BGP - Filial Campinas",
        "ultimo_status": "Fechado",
        "data_abertura": "2026-08-22 14:30",
        "detalhes": "Sessão BGP restabelecida após normalização de operadora parceira. Testes concluídos com sucesso."
    },
    {
        "ticket_id": "TK-1003",
        "cliente": "Hospital São Lucas",
        "servico_afetado": "Conexão VPN IPsec Site-to-Site",
        "ultimo_status": "Aguardando cliente",
        "data_abertura": "2026-08-23 11:00",
        "detalhes": "Aguardando teste de ping do cliente e validação da chave pré-compartilhada (PSK)."
    },
    {
        "ticket_id": "TK-1004",
        "cliente": "Indústria MetalTech",
        "servico_afetado": "Firewall Principal - Cluster HA",
        "ultimo_status": "Aberto",
        "data_abertura": "2026-08-23 16:45",
        "detalhes": "Chamado aberto via monitoramento automático de CPU acima de 95%."
    },
    {
        "ticket_id": "TK-1005",
        "cliente": "E-commerce Brasil",
        "servico_afetado": "Link de Internet Redundante",
        "ultimo_status": "Tratativa em andamento",
        "data_abertura": "2026-08-23 13:20",
        "detalhes": "Análise de perda de pacotes e latência intermitente pela equipe de NOC N2."
    },
    {
        "ticket_id": "TK-1006",
        "cliente": "TechFin Soluções",
        "servico_afetado": "Servidor DNS Primário",
        "ultimo_status": "Fechado",
        "data_abertura": "2026-08-21 08:00",
        "detalhes": "Configuração de zona DNS corrigida e sincronizada com servidores secundários."
    },
    {
        "ticket_id": "TK-1007",
        "cliente": "AgroExport Alimentos",
        "servico_afetado": "Circuito Satelital Filial MT",
        "ultimo_status": "Aguardando cliente",
        "data_abertura": "2026-08-22 17:10",
        "detalhes": "Solicitado reinício do modem satelital local pelo responsável técnico da unidade."
    },
    {
        "ticket_id": "TK-1008",
        "cliente": "Consultoria Prime",
        "servico_afetado": "Acesso Remoto VPN SSL",
        "ultimo_status": "Aberto",
        "data_abertura": "2026-08-23 17:30",
        "detalhes": "Usuários relatando lentidão na autenticação de dois fatores."
    }
]

def treinar_modelo_sentimento():
    """Gera corpus sintético e treina o pipeline TF-IDF + MLP."""
    frases_negativas = [
        "o link continua fora do ar e a empresa está parada",
        "estou muito insatisfeito com a demora no atendimento",
        "já faz horas que abri o chamado e ninguém resolveu",
        "o atendente não soube explicar o motivo da queda",
        "o problema voltou a acontecer pela terceira vez essa semana",
        "péssimo suporte técnico estamos com prejuízo na operação",
        "o sla de atendimento foi completamente estourado",
        "ninguém do noc entrou em contato até agora",
        "estou muito decepcionado com a estabilidade do link",
        "o roteador travou de novo e estamos sem comunicação",
        "vou cancelar o contrato se não resolverem isso hoje",
        "fiquei esperando horas no telefone e não tive retorno",
        "não gostei do atendimento que recebi do suporte técnico",
        "a lentidão na rede continua insuportável",
        "achei péssimo o serviço não recomendo para ninguém",
        "não foi uma boa tratativa infelizmente o problema persiste",
    ]
    frases_positivas = [
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
    ]
    frases_neutras = [
        "gostaria de saber qual o ip de gateway configurado",
        "qual é a previsão de término da manutenção programada",
        "preciso alterar o e-mail de notificação do monitoramento",
        "como faço para solicitar um relatório de tráfego mrg",
        "qual o procedimento para agendar uma janela de manutenção",
        "gostaria de saber os horários do plantão nível dois",
        "preciso atualizar o contato do responsável técnico local",
        "qual o asn configurado na sessão bgp",
        "vocês podem enviar o log do roteador por e-mail",
        "gostaria de mais informações sobre o link redundante",
        "qual o prazo padrão de atendimento para este tipo de falha",
        "como faço para abrir um chamado para outra filial",
    ]

    sujeitos = ["", "sinceramente, ", "olha, ", "na real, ", "por favor, ", "informo que ", "comunicamos que "]
    complementos = ["", " novamente", " hoje", " com urgência", " no nosso circuito principal", " na filial matriz", " com a equipe de redes", " no link dedicado"]

    def gerar_variacoes(base_list, n, rng):
        res = []
        while len(res) < n:
            b = rng.choice(base_list)
            p = rng.choice(sujeitos)
            s = rng.choice(complementos)
            frase = (p + b + s).strip()
            frase = frase[0].upper() + frase[1:] + "."
            res.append(frase)
        return res

    rng = random.Random(RANDOM_STATE)
    n = 120
    neg = gerar_variacoes(frases_negativas, n, rng)
    pos = gerar_variacoes(frases_positivas, n, rng)
    neu = gerar_variacoes(frases_neutras, n, rng)

    textos = neg + pos + neu
    rotulos = (["negativo"] * len(neg)) + (["positivo"] * len(pos)) + (["neutro"] * len(neu))
    df = pd.DataFrame({"texto": textos, "sentimento": rotulos}).sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(df["texto"], df["sentimento"], test_size=0.25, random_state=RANDOM_STATE, stratify=df["sentimento"])
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    mlp = MLPClassifier(hidden_layer_sizes=(32,), activation="relu", max_iter=500, random_state=RANDOM_STATE)
    mlp.fit(X_train_vec, y_train)
    acc = accuracy_score(y_test, mlp.predict(X_test_vec))
    print(f"[Setup] Modelo MLP treinado com acurácia de {acc*100:.1f}% no teste.")
    return vectorizer, mlp, pd.DataFrame(TICKETS_DATA)

def consultar_ticket(ticket_id_input, df_base_tickets):
    clean_id = str(ticket_id_input).strip().upper()
    if not clean_id.startswith("TK-"):
        clean_id = "TK-" + clean_id[2:].strip("-") if clean_id.startswith("TK") else f"TK-{clean_id}"
    match = df_base_tickets[df_base_tickets["ticket_id"] == clean_id]
    return match.iloc[0].to_dict() if not match.empty else None

def classificar_sentimento_texto(texto, vectorizer, mlp):
    vec = vectorizer.transform([texto])
    pred = mlp.predict(vec)[0]
    probs = mlp.predict_proba(vec)[0]
    confianca = probs[list(mlp.classes_).index(pred)]
    return pred, confianca

def registrar_em_arquivo_csv(ticket_id, status_ticket, mensagem_cliente, sentimento, confianca, caminho_csv=LOG_ARQUIVO_CSV):
    novo_registro = pd.DataFrame([{
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticket_id": ticket_id,
        "ultimo_status": status_ticket,
        "mensagem_cliente": mensagem_cliente,
        "sentimento_analisado": sentimento,
        "score_confianca": round(confianca, 4)
    }])
    header = not os.path.exists(caminho_csv)
    novo_registro.to_csv(caminho_csv, mode="a", header=header, index=False, encoding="utf-8-sig")

def executar_atendimento(ticket_id_input, mensagem_adicional=None, df_tickets=None, vectorizer=None, mlp=None, caminho_log=LOG_ARQUIVO_CSV):
    print("=" * 75)
    print("BOT: Ola! Bem-vindo ao Autoatendimento de Suporte Tecnico & NOC.")
    print(f"CLIENTE: [Ticket informado]: {ticket_id_input}")
    
    info = consultar_ticket(ticket_id_input, df_tickets)
    if not info:
        print(f"BOT: Nao localizamos o Trouble Ticket '{ticket_id_input}' em nossa base ativa.")
        print("BOT: Por favor, confira o numero do ticket ou entre em contato com o NOC Central.")
        print("=" * 75 + "\n")
        return
    
    t_id = info["ticket_id"]
    status = info["ultimo_status"]
    print(f"BOT: Ticket {t_id} localizado com sucesso!")
    print(f"   • Cliente: {info['cliente']}")
    print(f"   • Servico Afetado: {info['servico_afetado']}")
    print(f"   • ULTIMO STATUS: [{status.upper()}]")
    print(f"   • Detalhes da Tratativa: {info['detalhes']}")
    print("-" * 75)
    print("BOT: Deseja algo mais ou tem alguma observacao sobre este ticket?")
    
    if mensagem_adicional and mensagem_adicional.strip():
        print(f"CLIENTE: \"{mensagem_adicional}\"")
        sent, conf = classificar_sentimento_texto(mensagem_adicional, vectorizer, mlp)
        if sent == "negativo":
            print(f"BOT: Sentimos muito pelo transtorno! Identificamos criticidade na sua mensagem (Sentimento: {sent.upper()} | Confianca: {conf*100:.1f}%).")
            print("     [ALERTA NOC]: Registramos protocolo prioritario de ESCALONAMENTO para o NOC Nivel 2 agilizar a tratativa.")
        elif sent == "positivo":
            print(f"BOT: Ficamos muito felizes com seu retorno positivo! (Sentimento: {sent.upper()} | Confianca: {conf*100:.1f}%).")
            print("     Agradecemos a confianca no suporte tecnico. Conte sempre com a nossa equipe!")
        else:
            print(f"BOT: Anotamos sua observacao operacional (Sentimento: {sent.upper()} | Confianca: {conf*100:.1f}%).")
            print(f"     Sua solicitacao foi anexada ao historico do chamado {t_id}.")
        registrar_em_arquivo_csv(t_id, status, mensagem_adicional, sent, conf, caminho_log)
        print(f"\n[LOG AUDITORIA]: Interacao gravada em '{caminho_log}' (Ticket: {t_id} | Emocao: {sent})")
    else:
        print("CLIENTE: [Sem mensagens adicionais / Encerramento]")
        print("BOT: Perfeito! Obrigado por entrar em contato. Atendimento finalizado.")
    print("=" * 75 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Chatbot de Trouble Tickets com Analise de Sentimento (Rede Neural MLP)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Inicia o modo interativo via terminal")
    args = parser.parse_args()

    vectorizer, mlp, df_tickets = treinar_modelo_sentimento()

    if args.interactive:
        print("\n=== MODO INTERATIVO DO CHATBOT DE TROUBLE TICKETS ===")
        while True:
            t_in = input("BOT: Informe o numero do Trouble Ticket (ou 'sair' para encerrar): ")
            if t_in.lower().strip() in ["sair", "exit", "q"]:
                print("Atendimento encerrado.")
                break
            if not t_in.strip():
                continue
            info = consultar_ticket(t_in, df_tickets)
            if not info:
                print(f"BOT: Ticket '{t_in}' nao encontrado na base.\n")
                continue
            print(f"BOT: Ticket {info['ticket_id']} | Status: [{info['ultimo_status']}] | Servico: {info['servico_afetado']}")
            print(f"BOT: Detalhes: {info['detalhes']}")
            msg = input("BOT: Deseja algo mais ou tem alguma observacao? (Pressione Enter para encerrar): ")
            executar_atendimento(t_in, msg if msg.strip() else None, df_tickets, vectorizer, mlp)
    else:
        print("\n--- Executando Simulacao de Casos de Uso ---\n")
        executar_atendimento("TK-1001", "Ja faz horas que estamos com o link parado e com prejuizo na operacao, preciso de urgencia!", df_tickets, vectorizer, mlp)
        executar_atendimento("1002", "Muito obrigado pelo suporte, a equipe tecnica foi excelente e resolveu na hora!", df_tickets, vectorizer, mlp)
        executar_atendimento("tk-1003", "Gostaria de saber qual o IP de gateway configurado para eu testar a rota aqui.", df_tickets, vectorizer, mlp)
        executar_atendimento("TK-1004", None, df_tickets, vectorizer, mlp)
        executar_atendimento("TK-9999", "Alguem me ajuda?", df_tickets, vectorizer, mlp)

if __name__ == "__main__":
    main()
