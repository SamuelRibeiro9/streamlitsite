import streamlit as st

st.title(':blue[Samuel Ribeiro] :material/engineering:')
st.divider()

st.write('''Graduando em Engenharia Elétrica pela Uniube, com sólida experiência em manutenção industrial e análise de indicadores de desempenho (KPIs). 
         Experiente também no setor de suprimentos, atuando na análise de KPIs com foco em otimização de processos e melhoria contínua. 
         Competente em análises de processos industriais, automação e controle de processos, com a capacidade de aplicar ferramentas e 
         metodologias para aumentar a eficiência e gerar insights estratégicos que facilitam a tomada de decisões. 

Principais projetos:
- Automação de um sistema de conforto térmico para um galpão de espera (Rivelli S/A)
- Implementação de planos de manutenção e inspeção em motores elétricos (Rivelli S/A)
- Desenvolvimento de script em Python para identificação de materiais duplicados no sistema SAP (Rivelli S/A)
- Desenvolvimento de dashboards no Grafana com dados de processos industriais (iSystems)
- Desenvolvimento de software de simulação de sintonia de controle em malha fechada (iSystems)
''')

st.link_button('🖥️ Potfólio GitHub', 'https://github.com/SamuelRibeiro9')

col_esquerda, col_direita = st.columns(2)

col_esquerda.subheader(':blue[Softwares e Habilidades]')
col_esquerda.write('''
                   - Pacote Office
                   - Power BI
                   - Python (Pandas, Matplotlib, Pyplot, Streamlit, Seaborn, Numpy, Scikit-learn, Requests, Selenium)
                   - SQL
                   - Grafana
                   - SAP S4/HANA
                   - Metodologias ágeis
                   - Gerenciamento de projetos
                   - Perfil analítico
                   ''')

col_direita.subheader(':blue[Dasboards]')

dash_f1 = col_direita.button('🏎️ F1 Dashboard')
dash_energy = col_direita.button('🔋 Demanda de energia')


if dash_f1 == 1: 
    st.switch_page('views/formula_1.py')
elif dash_energy == 1: 
    st.switch_page('views/energy_case.py')
