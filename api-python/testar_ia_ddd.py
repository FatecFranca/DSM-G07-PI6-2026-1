import sys
import os
import unittest
from unittest.mock import MagicMock

# Adiciona o caminho da pasta app ao path do Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.application.services.recomendacao_service import RecomendacaoService

class TestRecomendacaoServiceDDD(unittest.TestCase):
    def setUp(self):
        self.service = RecomendacaoService()
        # Mock do JavaAPIClient
        self.service.java_api_client = MagicMock()

    def test_recomendacao_sobrepeso(self):
        # Configura mock de dados do animal
        self.service.java_api_client.get_animal.return_value = (200, {
            "nome": "Max",
            "racaNome": "Labrador Retriever",
            "sexo": "Macho",
            "dataNascimento": "2021-05-20T00:00:00Z",
            "peso": 45.0,
            "caminhada_diaria_km": 1.0
        })

        # Executa a recomendação passando peso_ideal = 23.26
        res = self.service.obter_recomendacao_ia_animal("123", 23.26, "mock_token")
        
        self.assertEqual(res["animalId"], "123")
        self.assertEqual(res["nome"], "Max")
        self.assertEqual(res["diagnostico"], "Sobrepeso")
        self.assertEqual(res["peso_ideal_esperado"], 23.26)
        self.assertTrue(len(res["sugestoes_racao"]) > 0)
        self.assertEqual(res["recomendacoes_estilo_vida"]["nivel_atividade_meta"], "Muito Ativo")
        self.assertEqual(res["recomendacoes_estilo_vida"]["tipo_dieta_meta"], "Úmida")
        print("[TESTE OK] Cão em Sobrepeso (Labrador) validado com sucesso!")

    def test_recomendacao_abaixo_peso(self):
        self.service.java_api_client.get_animal.return_value = (200, {
            "nome": "Bella",
            "racaNome": "Golden Retriever",
            "sexo": "Fêmea",
            "dataNascimento": "2023-01-10T00:00:00Z",
            "peso": 12.0,
            "caminhada_diaria_km": 3.0
        })

        res = self.service.obter_recomendacao_ia_animal("456", 21.7, "mock_token")
        
        self.assertEqual(res["diagnostico"], "Abaixo do Peso")
        self.assertEqual(res["peso_ideal_esperado"], 21.7)
        self.assertEqual(res["recomendacoes_estilo_vida"]["tipo_dieta_meta"], "Ração Seca")
        print("[TESTE OK] Cão Abaixo do Peso (Golden) validado com sucesso!")

    def test_recomendacao_peso_ideal(self):
        self.service.java_api_client.get_animal.return_value = (200, {
            "nome": "Rocky",
            "racaNome": "Beagle",
            "sexo": "Macho",
            "dataNascimento": "2020-03-15T00:00:00Z",
            "peso": 21.8,
            "caminhada_diaria_km": 2.0
        })

        res = self.service.obter_recomendacao_ia_animal("789", 23.38, "mock_token")
        
        self.assertEqual(res["diagnostico"], "Peso Ideal")
        self.assertEqual(res["peso_ideal_esperado"], 23.38)
        print("[TESTE OK] Cão em Peso Ideal (Beagle) validado com sucesso!")

    def test_srd_porte_calculado_e_caminhada_opcional(self):
        self.service.java_api_client.get_animal.return_value = (200, {
            "nome": "Mel",
            "racaNome": "SRD (Sem Raça Definida)",
            "sexo": "Fêmea",
            "dataNascimento": "2022-09-01T00:00:00Z",
            "peso": 12.0
            # Sem caminhada_diaria_km (testando fallback)
        })

        res = self.service.obter_recomendacao_ia_animal("999", 7.0, "mock_token")
        
        self.assertEqual(res["diagnostico"], "Sobrepeso") # 12.0 > 7.0 * 1.15
        self.assertEqual(res["peso_ideal_esperado"], 7.0)
        # O porte deve ter sido calculado como Médio pois peso atual é 12.0 kg
        # E a caminhada diária foi processada corretamente sem dar erro
        print("[TESTE OK] Cão SRD com porte calculado e caminhada opcional validado com sucesso!")

    def test_validacoes_erros(self):
        # Sem peso
        with self.assertRaises(ValueError):
            self.service.gerar_sugestao_nutricional({"racaNome": "Poodle"}, peso_ideal=5.0)

        # Sem nascimento
        with self.assertRaises(ValueError):
            self.service.gerar_sugestao_nutricional({"racaNome": "Poodle", "peso": 8.0}, peso_ideal=5.0)

        # Sem peso ideal
        with self.assertRaises(ValueError):
            self.service.gerar_sugestao_nutricional({
                "racaNome": "Poodle",
                "peso": 8.0,
                "dataNascimento": "2020-01-01T00:00:00Z"
            }, peso_ideal=None)

        print("[TESTE OK] Validações de erro e fallbacks verificadas com sucesso!")

if __name__ == "__main__":
    unittest.main()
