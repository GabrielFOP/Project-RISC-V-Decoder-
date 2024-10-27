from myhdl import Signal as signal, intbv
from math import log
from defs import (
    CPU_BITS, CPU_REGS, RTYPE, ITYPE, STYPE, BTYPE, UTYPE, SBTYPE,
    AND, OR, ADD, SLL, SLT, SLTU, SUB, XOR, SRL, SRA
)

# Funct3 e Funct7 para R-Type
FUNCT3_ADD_SUB = 0b000
FUNCT3_SLL     = 0b001
FUNCT3_SLT     = 0b010
FUNCT3_SLTU    = 0b011
FUNCT3_XOR     = 0b100
FUNCT3_SRL_SRA = 0b101
FUNCT3_OR      = 0b110
FUNCT3_AND     = 0b111

FUNCT7_SUB     = 0b0100000   #SUB e SRA
FUNCT7_ADD_SLL = 0b0000000   #ADD, SLL, SRL

def load_memory_data(filename):
    memory = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line:  # Verifica se a linha não está vazia
                try:
                    memory.append(signal(intbv(int(line, 2))[CPU_BITS:]))
                except ValueError:
                    print(f"Skipping invalid line: '{line}'")  
    return memory

# Carregando as instruções e dados
data_ram = load_memory_data('mc_data')
inst_ram = load_memory_data('mc_code')

# Inicializando os registros
registers = [signal(intbv(0)[CPU_BITS:]) for _ in range(CPU_REGS)]
for i in range(len(registers)):
    registers[i] = intbv(10 + i)[CPU_BITS:]  # Atribuição direta

def main():
    pc = signal(intbv(0)[CPU_BITS:])

    while True:
        print(f"Current PC: {int(pc)}")

        if int(pc) >= len(inst_ram):
            print("End of instruction memory.")
            break

        instruction = inst_ram[int(pc)]
        opcode = instruction[7:0]

        op_type = ''
        alu_op = None
        result = 0  # Inicializando o resultado da ALU

        # Decodifica o opcode
        if opcode == RTYPE:
            funct3 = instruction[15:12]
            funct7 = instruction[32:25]
            op_type = 'RTYPE'

            # Decodificação da operação ALU com base em funct3 e funct7
            if funct3 == FUNCT3_ADD_SUB:
                if funct7 == FUNCT7_ADD_SLL:
                    alu_op = ADD
                    print("Operation: ADD")
                elif funct7 == FUNCT7_SUB:
                    alu_op = SUB
                    print("Operation: SUB")
            elif funct3 == FUNCT3_SLL:
                alu_op = SLL
                print("Operation: SLL")
            elif funct3 == FUNCT3_SLT:
                alu_op = SLT
                print("Operation: SLT")
            elif funct3 == FUNCT3_SLTU:
                alu_op = SLTU
                print("Operation: SLTU")
            elif funct3 == FUNCT3_XOR:
                alu_op = XOR
                print("Operation: XOR")
            elif funct3 == FUNCT3_SRL_SRA:
                if funct7 == FUNCT7_ADD_SLL:  # SRL
                    alu_op = SRL
                    print("Operation: SRL")
                elif funct7 == FUNCT7_SUB:  # SRA
                    alu_op = SRA
                    print("Operation: SRA")
            elif funct3 == FUNCT3_OR:
                alu_op = OR
                print("Operation: OR")
            elif funct3 == FUNCT3_AND:
                alu_op = AND
                print("Operation: AND")
            else:
                print(f"Unknown funct3: {int(funct3)}")
        
        elif opcode == ITYPE:
            alu_op = ADD  
            op_type = 'ITYPE'
        elif opcode == STYPE:
            op_type = 'STYPE'
        elif opcode == SBTYPE:
            op_type = 'SBTYPE'
        else:
            print(f"Unknown opcode: {int(opcode)}")
            break

        print(f"Opcode: {int(opcode)}, OpType: {op_type}")

        # Processa instruções RTYPE
        if op_type == 'RTYPE':
            rda_index = int(instruction[20:15])
            rdx_index = int(instruction[25:20])
            rd_index = int(instruction[12:7])  # Índice do destino (rd)

            rda = registers[rda_index]
            rdx = registers[rdx_index]

            print(f"rda: {int(rda)}, rdx: {int(rdx)}")

            # Realiza a operação ALU
            if alu_op == ADD:
                result = int(rda) + int(rdx)
            elif alu_op == SUB:
                result = int(rda) - int(rdx)
            elif alu_op == AND:
                result = int(rda) & int(rdx)
            elif alu_op == OR:
                result = int(rda) | int(rdx)
            elif alu_op == XOR:
                result = int(rda) ^ int(rdx)
            elif alu_op == SLL:
                result = int(rda) << int(rdx)
            elif alu_op == SRL:
                result = int(rda) >> int(rdx)
            elif alu_op == SRA:
                result = int(rda) >> int(rdx)  # Shift aritmético (sign extend)
            elif alu_op == SLT:
                result = 1 if int(rda) < int(rdx) else 0
            elif alu_op == SLTU:
                result = 1 if int(rda) < int(rdx) else 0  # Comparação sem sinal

            registers[rd_index] = result  # Atribuição direta do resultado no registrador

        elif op_type == 'ITYPE':
            rda_index = int(instruction[20:15])
            imm = int(instruction[32:20])
            rda = registers[rda_index]

            result = int(rda) + imm
            rd_index = int(instruction[12:7])
            registers[rd_index] = result  # Atribuição direta do resultado no registrador

        elif op_type == 'STYPE':
            rda_index = int(instruction[20:15])
            rdx_index = int(instruction[25:20])
            imm = int(instruction[12:7])
            rda = registers[rda_index]
            rdx = registers[rdx_index]

            address = int(rda) + imm
            data_ram[address] = rdx  # Armazena o valor diretamente na memória

        elif op_type == 'SBTYPE':
            rda_index = int(instruction[20:15])
            rdx_index = int(instruction[25:20])
            rda = registers[rda_index]
            rdx = registers[rdx_index]

            # Condição de branch
            if int(rda) == 0:
                pc = int(pc) + int(instruction[31:20])  # Atualiza o PC com o deslocamento
            else:
                pc = int(pc) + 1  # Incrementa o PC se a condição não for satisfeita

        # Adiciona impressão de depuração
        print(f"Instr: {int(pc):02x}, Opcode: {int(instruction):08x}, "
              f"rs1: {int(rda):08x}, rs2: {int(rdx):08x}, result: {int(result):08x}")

        pc = int(pc) + 1  # Atualiza o PC diretamente (incremento)

if __name__ == '__main__':
    main()
