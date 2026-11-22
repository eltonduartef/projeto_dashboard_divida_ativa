vendedor1 = "Ana"
vendas1 = "15000"
ativo1 = "1"

vendedor1 = "Ana"
vendas1 = float("15000")
ativo1 = bool(int("1"))
valor_comissao = (vendas1*0.05)
print(f"A vendedora: {vendedor1}, ganhou de Comissao: R$ {valor_comissao:.2f} | Ativo:{ativo1}")

vendedor2 = "Bruno"
vendas2 = "23000"
ativo2 = "0"

vendedor2 = "Bruno"
vendas2 = float("23000")
ativo2 = bool(int("0"))
valor_comissao = (vendas2*0.05)
print(f"O vendedor: {vendedor2}, ganhou uma comissao: R$ {valor_comissao:.2f} | Ativo: {ativo2}.")

vendedor3 = "Clara"
vendas3 = "9500"
ativo3 = "1"

vendedor3 = "Clara"
vendas3 = float("9500")
ativo3 = bool(int("1"))
valor_comissao = (vendas3*0.05)
print(f"A vendedora: {vendedor3}, ganhou uma comissão: R$ {valor_comissao:.2f} | Ativo: {ativo3}.")




nome = input("Qual é o seu nome?")
vendas_total = float(input("Quanto você vendeu?"))
comissao = vendas_total*0.08
print("======== RELATÓRIO DE VENDAS ========")
print(f"Vendedor: {nome}")
print(f"Total vendido: R$ {vendas_total:.2f}")
print(f"Comissão (8%): R$ {comissao:.2f}")
print("======================================")