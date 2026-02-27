📊 Sistema de Controle Financeiro

📌 Objetivo
Desenvolver um sistema de controle financeiro em Python que permita registrar entradas e saídas em reais (R$), garantindo:
Precisão de duas casas decimais
Exibição de valores com vírgula como separador decimal
O sistema inclui autenticação de usuários, relatórios detalhados e cálculo automático de saldo.

⚙️ Funcionalidades
🔐 Autenticação
Tela de login com usuário e senha obrigatórios
Opção de cadastrar novo usuário
Cada usuário acessa apenas seus próprios registros (isolamento de dados)

💰 Registro de Entradas
Categorias: UBER, 99POP, INDRIVER, OUTROS
Campo obrigatório para valor (não negativo, digitado com vírgula)
Campo opcional para comentários

💸 Registro de Saídas
Categorias: COMBUSTÍVEL, ALIMENTAÇÃO, INVESTIMENTOS, DÍVIDAS, OUTROS
Campo obrigatório para valor (não negativo, digitado com vírgula)
Campo opcional para comentários

📝 Botão de Registro
Solicita dupla confirmação antes de salvar
Registra: categoria, valor, data (DD/MM/AAAA) e horário (HH:MM)

🖥️ Tela Principal
Exibe apenas o saldo total
Saldo positivo em verde
Saldo negativo em vermelho
Botão separado Relatório para abrir nova janela

📑 Relatório
Nova janela com tabela listando todos os registros
Opções de Editar e Excluir cada registro
Ambas as ações exigem dupla confirmação
Edição permite alterar valor (com vírgula) e comentário
Exclusão pede confirmação inicial e final antes de remover

📈 Consistência
Cálculos feitos com precisão usando Decimal
Exibição sempre com vírgula (ex.: R$ 10,50)
Fórmula: Entradas – Saídas = Saldo

🚀 Tecnologias Utilizadas
Python 3.x
Tkinter (interface gráfica)
Decimal (precisão nos cálculos)
