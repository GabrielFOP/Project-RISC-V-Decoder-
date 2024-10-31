# Python decoder RISC-V

Este projeto implementa um decodificador de instruções para o conjunto de instruções RISC-V em Python usando MyHDL para simulação de hardware. 
Ele carrega instruções e dados de arquivos externos, armazena-os em memória, e simula o comportamento de um processador RISC-V executando instruções básicas.

Estrutura e Funcionamento

Carregamento de Memória:
A função load_memory_data carrega instruções e dados de arquivos em listas que simulam a RAM. O código conta com uma estrutura que
lida com possíveis linhas inválidas nos arquivos de entrada, como linhas em branco por exemplo.

![image](https://github.com/user-attachments/assets/3e3339d9-ce88-4e17-8de1-b1878a2dcefb)

Decodificação e Execução: 
Os registros do myhdl são inicializados, a função main implementa um laço principal que simula o ciclo de execução do processador. 
Cada instrução é carregada, seu opcode é decodificado, e o tipo de operação (RTYPE, ITYPE, STYPE, SBTYPE) é identificado.

![image](https://github.com/user-attachments/assets/3c4bf5ae-7590-4e77-8ebd-f21e745373ba)
![image](https://github.com/user-attachments/assets/8bdc3a59-1bc8-43b4-a728-50fe1e71c348)
![image](https://github.com/user-attachments/assets/696c08e5-c053-41c0-b5a6-3c05da094584)

Operações ALU: Com base em funct3 e funct7 para o tipo RTYPE, o código realiza operações aritméticas e lógicas na ALU, como ADD, SUB, AND, OR, SHIFT, entre outras. 
O resultado é armazenado nos registradores ou memória. A mesma lógica segue para os outros opcode

![image](https://github.com/user-attachments/assets/f8ec4f3f-9eab-462a-82e7-c89baba2afa8)
![image](https://github.com/user-attachments/assets/9e6608a3-0df8-4960-9987-651b4abf4eb0)

Controle de Fluxo: 
O programa também implementa operações de branch (SBTYPE) para alterar o valor do contador de programa (pc), simulando saltos condicionais.

![image](https://github.com/user-attachments/assets/9535b576-a6b6-40c9-bb6a-99a46dcd3b19)

Depuração: 
Ao longo de todo o progama são incluídas mensagens de depuração que exibem o pc, opcode e resultados das operações, 
facilitando a visualização do comportamento da execução e deixando mais claro a decodificação.

![image](https://github.com/user-attachments/assets/39d2649c-e377-4b00-91ca-b0d691f54ffb)

Fim de execução:
Ao final de todo o processo o pc e incrementado passando assim a outra leitura da memoria 

![image](https://github.com/user-attachments/assets/5e964094-c641-4841-90a6-08c061ed9843)


!créditos ao uso do arquivos defs e das memorias mc_code e mc_data presentes na [matéria](https://medium.com/programmatic/how-to-design-a-risc-v-processor-12388e1163c)
e encontrados no [repositorio](https://github.com/shirishbahirat/cpu)


