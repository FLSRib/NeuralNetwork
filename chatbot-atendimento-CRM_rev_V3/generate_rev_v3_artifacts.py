import os
import sys
import json
import random
import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GroupKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

RANDOM_STATE = 42
random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

scratch_dir = r"C:\Users\fribeiro\.gemini\antigravity\scratch\NeuralNetwork\chatbot-atendimento-CRM_rev_V3"
fgv_dir = r"C:\Users\fribeiro\FGV\NeuralNetwork\chatbot-atendimento-CRM_rev_V3"

os.makedirs(scratch_dir, exist_ok=True)
os.makedirs(fgv_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. CURADORIA DAS FRASES-BASE (65 POR CLASSE = 195 FRASES-BASE)
# -------------------------------------------------------------
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

print(f"Total de frases-base: Negativas={len(frases_negativas_base)}, Positivas={len(frases_positivas_base)}, Neutras={len(frases_neutras_base)}")
assert len(frases_negativas_base) >= 65
assert len(frases_positivas_base) >= 65
assert len(frases_neutras_base) >= 65

# -------------------------------------------------------------
# 2. DEFINIÇÃO DOS TERMOS OFENSIVOS (GUARDRAIL pt-BR)
# -------------------------------------------------------------
TERMOS_OFENSIVOS_PTBR = [
    "merda", "porra", "caralho", "bosta", "fudeu", "foder", "fudido",
    "puta", "puto", "pqp", "carai", "desgraca", "desgraça", "cacete",
    "vsf", "vtnc", "imbecil", "idiota", "palhacada", "palhaçada"
]

import re

def verificar_guardrail_ofensivo(texto):
    """Detecta termos ofensivos pt-BR para escalonamento imediato de crise."""
    texto_norm = texto.lower()
    for termo in TERMOS_OFENSIVOS_PTBR:
        if re.search(r'\b' + re.escape(termo) + r'\b', texto_norm):
            return True, termo
    return False, None

# -------------------------------------------------------------
# 3. GERAÇÃO DE DATASET SINTÉTICO COM ZERO VAZAMENTO
# -------------------------------------------------------------
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

rng = random.Random(RANDOM_STATE)

# A. Divisão RIGOROSA das FRASES-BASE antes de gerar variações (75% treino, 25% teste)
neg_base_train, neg_base_test = train_test_split(frases_negativas_base, test_size=0.25, random_state=RANDOM_STATE)
pos_base_train, pos_base_test = train_test_split(frases_positivas_base, test_size=0.25, random_state=RANDOM_STATE)
neu_base_train, neu_base_test = train_test_split(frases_neutras_base, test_size=0.25, random_state=RANDOM_STATE)

print(f"Frases-Base Treino: Neg={len(neg_base_train)}, Pos={len(pos_base_train)}, Neu={len(neu_base_train)}")
print(f"Frases-Base Teste:  Neg={len(neg_base_test)},  Pos={len(pos_base_test)},  Neu={len(neu_base_test)}")

# Gera variações sintéticas a partir de bases 100% disjuntas
train_samples = (
    gerar_amostras_por_frases_base(neg_base_train, "negativo", 0, variacoes_por_frase=5, rng=rng) +
    gerar_amostras_por_frases_base(pos_base_train, "positivo", 0, variacoes_por_frase=5, rng=rng) +
    gerar_amostras_por_frases_base(neu_base_train, "neutro", 0, variacoes_por_frase=5, rng=rng)
)

test_samples = (
    gerar_amostras_por_frases_base(neg_base_test, "negativo", 1000, variacoes_por_frase=5, rng=rng) +
    gerar_amostras_por_frases_base(pos_base_test, "positivo", 1000, variacoes_por_frase=5, rng=rng) +
    gerar_amostras_por_frases_base(neu_base_test, "neutro", 1000, variacoes_por_frase=5, rng=rng)
)

df_train = pd.DataFrame(train_samples).sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)
df_test = pd.DataFrame(test_samples).sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)

# Auditoria matemática de vazamento de frases-base
sobreposicao = set(df_test["frase_base"]).intersection(set(df_train["frase_base"]))
print(f"Sobreposição de frases-base entre Treino e Teste: {len(sobreposicao)} (ZERO VAZAMENTO GARANTIDO)")
assert len(sobreposicao) == 0

# -------------------------------------------------------------
# 4. TREINAMENTO E VALIDAÇÃO COM PIPELINE E GROUPKFOLD
# -------------------------------------------------------------
vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
mlp = MLPClassifier(hidden_layer_sizes=(32,), activation="relu", max_iter=500, random_state=RANDOM_STATE)
lr = LogisticRegression(max_iter=500, random_state=RANDOM_STATE)

X_train_raw = df_train["texto"]
y_train = df_train["sentimento"]
X_test_raw = df_test["texto"]
y_test = df_test["sentimento"]

X_train_vec = vectorizer.fit_transform(X_train_raw)
X_test_vec = vectorizer.transform(X_test_raw)

mlp.fit(X_train_vec, y_train)
lr.fit(X_train_vec, y_train)

y_pred_mlp = mlp.predict(X_test_vec)
y_pred_lr = lr.predict(X_test_vec)

acc_test_mlp = accuracy_score(y_test, y_pred_mlp)
acc_test_lr = accuracy_score(y_test, y_pred_lr)

print(f"\nAcurácia no Teste Inédito (Zero Vazamento):")
print(f" • MLP: {acc_test_mlp:.4f} ({acc_test_mlp*100:.1f}%)")
print(f" • Regressão Logística: {acc_test_lr:.4f} ({acc_test_lr*100:.1f}%)")

# Validação Cruzada RIGOROSA usando Pipeline e GroupKFold (agrupando por frase_base_id)
df_total = pd.concat([df_train, df_test], ignore_index=True)
X_all = df_total["texto"]
y_all = df_total["sentimento"]
groups = df_total["frase_base_id"]

pipe_mlp = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
    ("clf", MLPClassifier(hidden_layer_sizes=(32,), activation="relu", max_iter=500, random_state=RANDOM_STATE))
])

pipe_lr = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=500, random_state=RANDOM_STATE))
])

gkf = GroupKFold(n_splits=5)
cv_scores_mlp = cross_val_score(pipe_mlp, X_all, y_all, groups=groups, cv=gkf)
cv_scores_lr = cross_val_score(pipe_lr, X_all, y_all, groups=groups, cv=gkf)

print(f"\nValidação Cruzada Rigorosa (5-Fold GroupKFold com Pipeline):")
print(f" • MLP Média: {cv_scores_mlp.mean():.4f} (Desvio Padrão: {cv_scores_mlp.std():.4f})")
print(f" • Regressão Logística Média: {cv_scores_lr.mean():.4f} (Desvio Padrão: {cv_scores_lr.std():.4f})")

# -------------------------------------------------------------
# 5. TESTE DE ESTRESSE COMPLETO (TODAS AS FRASES)
# -------------------------------------------------------------
def classificar_sentimento_hibrido(texto, vec_model, clf_model, threshold_neg=0.30):
    is_ofensivo, termo = verificar_guardrail_ofensivo(texto)
    if is_ofensivo:
        return "negativo", 1.0, f"Guardrail Crítico: Termo ofensivo detectado ('{termo}')"
        
    vec = vec_model.transform([texto])
    probs = clf_model.predict_proba(vec)[0]
    classes = list(clf_model.classes_)
    
    idx_neg = classes.index("negativo")
    prob_neg = probs[idx_neg]
    
    if prob_neg >= threshold_neg:
        return "negativo", prob_neg, "IA: Limiar de Recall prioritário (Negativo >= 30%)"
    else:
        pred_idx = probs.argmax()
        return classes[pred_idx], probs[pred_idx], "IA: Predição padrão por máxima verossimilhança"

frases_estresse = [
    ("Parabéns pelo link maravilhoso que caiu pela décima vez hoje.", "negativo (irônico)"),
    ("O atendimento do técnico foi bom, mas o link continua instável.", "negativo/misto"),
    ("caiu dnv", "negativo"),
    ("Favor checar a latência no roteador core de Curitiba.", "neutro"),
    ("Não tivemos nenhum erro ou queda durante a manutenção, obrigado.", "positivo"),
    ("Vocês pretendem lançar suporte a IPv6 este ano?", "neutro"),
    ("Que serviço de bosta, link fora do ar de novo!", "negativo (com termo ofensivo)"),
]

print("\n=== EXECUÇÃO DO TESTE DE ESTRESSE (TODAS AS FRASES) ===")
for frase, esperado in frases_estresse:
    sent, conf, motivo = classificar_sentimento_hibrido(frase, vectorizer, mlp, threshold_neg=0.30)
    print(f"Mensagem: \"{frase}\"")
    print(f" • Esperado: [{esperado}]")
    print(f" • Predição: [{sent.upper()}] (Confiança: {conf*100:.1f}%) | Motivo: {motivo}")
    print("-" * 75)
