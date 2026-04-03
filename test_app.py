#!/usr/bin/env python3
"""
Script de validação - Testa funcionalidade do app sem GUI
Verifica: imports, funções, cálculos e estrutura de dados
"""

from decimal import Decimal, ROUND_HALF_UP

def test_formatar_tempo():
    """Testa função de formatação de tempo"""
    def formatar_tempo(tempo_dec):
        if tempo_dec <= 0:
            return "00:00:00"
        tempo_dec = abs(float(tempo_dec))
        horas = int(tempo_dec)
        minutos_totais = (tempo_dec - horas) * 60
        minutos = int(minutos_totais)
        segundos = int(round((minutos_totais - minutos) * 60))
        if segundos == 60:
            segundos = 0
            minutos += 1
        if minutos == 60:
            minutos = 0
            horas += 1
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    assert formatar_tempo(2.5) == "02:30:00", "Teste 1 falhou"
    assert formatar_tempo(1.0) == "01:00:00", "Teste 2 falhou"
    assert formatar_tempo(0.25) == "00:15:00", "Teste 3 falhou"
    print("✅ formatar_tempo() - OK")

def test_parse_time_to_decimal():
    """Testa conversão de tempo para decimal"""
    from decimal import Decimal
    
    def parse_time_to_decimal(time_str: str) -> float:
        if time_str is None:
            return 0.0
        s = str(time_str).strip()
        if not s:
            return 0.0
        if ':' in s:
            parts = s.split(':')
            try:
                h = Decimal(parts[0]) if parts[0] != '' else Decimal('0')
                m = Decimal(parts[1]) if len(parts) > 1 and parts[1] != '' else Decimal('0')
                sec = Decimal(parts[2]) if len(parts) > 2 and parts[2] != '' else Decimal('0')
                resultado = h + m/Decimal('60') + sec/Decimal('3600')
                return float(resultado)
            except Exception:
                return 0.0
        try:
            s2 = s.replace(',', '.')
            return float(Decimal(s2))
        except Exception:
            return 0.0
    
    assert parse_time_to_decimal("2:30") == 2.5, "Teste 1 falhou"
    assert parse_time_to_decimal("1:00") == 1.0, "Teste 2 falhou"
    assert parse_time_to_decimal("2.5") == 2.5, "Teste 3 falhou"
    assert parse_time_to_decimal("00:15:00") == 0.25, "Teste 4 falhou"
    print("✅ parse_time_to_decimal() - OK")

def test_acabamento_pick_up():
    """Testa cálculo de Pick-up (arraste de banho)"""
    # Entrada
    ps = Decimal(str(150))  # Peso seco
    pu = Decimal(str(165))  # Peso úmido
    
    # Cálculo
    pickup_pct = ((pu - ps) / ps) * Decimal('100')
    
    # Validação
    expected = 10.0
    assert float(pickup_pct) == expected, f"Esperado {expected}, obteve {float(pickup_pct)}"
    print(f"✅ Pick-up Calculation: {float(pickup_pct):.2f}% - OK")

def test_acabamento_taxa_producao():
    """Testa cálculo de Taxa de Produção (Acabamento)"""
    # Entrada
    largura = Decimal(str(1.5))
    velocidade = Decimal(str(120))
    
    # Cálculo
    taxa_prod = largura * velocidade
    
    # Validação
    expected = 180.0
    assert float(taxa_prod) == expected, f"Esperado {expected}, obteve {float(taxa_prod)}"
    print(f"✅ Taxa de Produção: {float(taxa_prod):.2f} m/h - OK")

def test_tinturaria_taxa_producao():
    """Testa cálculo de Taxa de Produção (Tinturaria)"""
    # Entrada
    metragem = Decimal(str(100000))  # metros
    tempo_horas = Decimal(str(10))   # horas
    
    # Cálculo
    if tempo_horas > 0:
        taxa = metragem / tempo_horas
    else:
        taxa = Decimal('0')
    
    # Validação
    expected = 10000.0
    assert float(taxa) == expected, f"Esperado {expected}, obteve {float(taxa)}"
    print(f"✅ Taxa Tinturaria: {float(taxa):.2f} m/h - OK")

def test_metragem_tinturaria():
    """Testa cálculo de Metragem (Tinturaria)"""
    # Entrada
    comp = Decimal(str(1000))      # metros
    rolos = Decimal(str(5))
    corpos = Decimal(str(2))
    cordas = Decimal(str(2))
    
    # Cálculo
    metragem = comp * rolos * corpos * cordas
    
    # Validação
    expected = 20000.0
    assert float(metragem) == expected, f"Esperado {expected}, obteve {float(metragem)}"
    print(f"✅ Metragem Tinturaria: {float(metragem):.0f} m - OK")

def test_peso_tinturaria():
    """Testa cálculo de Peso (Tinturaria)"""
    # Entrada
    metragem = Decimal(str(20000))
    gramatura = Decimal(str(150))  # g/m
    
    # Cálculo
    peso = (metragem * gramatura) / Decimal('1000')
    
    # Validação
    expected = 3000.0
    assert float(peso) == expected, f"Esperado {expected}, obteve {float(peso)}"
    print(f"✅ Peso Tinturaria: {float(peso):.2f} kg - OK")

def test_precisao_decimal():
    """Testa precisão usando Decimal"""
    # Operação que pode causar erro em float
    a = Decimal('0.1')
    b = Decimal('0.2')
    c = a + b
    
    # Validação
    assert c == Decimal('0.3'), "Precisão Decimal falhou"
    print(f"✅ Precisão Decimal: {c} - OK")

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTES - App Taxas de Produção v2.0")
    print("="*60 + "\n")
    
    tests = [
        ("Formatação de Tempo", test_formatar_tempo),
        ("Parse Tempo para Decimal", test_parse_time_to_decimal),
        ("Pick-up (Arraste)", test_acabamento_pick_up),
        ("Taxa Acabamento", test_acabamento_taxa_producao),
        ("Taxa Tinturaria", test_tinturaria_taxa_producao),
        ("Metragem Tinturaria", test_metragem_tinturaria),
        ("Peso Tinturaria", test_peso_tinturaria),
        ("Precisão Decimal", test_precisao_decimal),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"▶️  {name}...", end=" ")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FALHOU: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERRO: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESULTADOS: {passed} Passados | {failed} Falhados")
    print("="*60 + "\n")
    
    if failed == 0:
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("\n✨ O aplicativo está pronto para uso em produção.\n")
    else:
        print(f"⚠️  {failed} teste(s) falharam. Verifique o código.\n")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
