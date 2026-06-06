import pandas as pd
import joblib
import os
from fastapi import HTTPException
from app.application.dto.peso_dto import PesoIdealRequestDTO, PesoIdealResponseDTO
from app.domain.utils.utils import DomainUtils

class PesoService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PesoService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Carrega os modelos e CSVs na memória apenas uma vez."""
        # Caminho base: api-python
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        project_root = os.path.dirname(base_dir)
        models_dir = os.path.join(project_root, "models", "peso")

        try:
            # Modelos
            self.modelo_com_raca = joblib.load(os.path.join(models_dir, "modelo_com_raca.pkl"))
            self.modelo_srd = joblib.load(os.path.join(models_dir, "modelo_srd.pkl"))

            # CSVs com faixas saudáveis
            self.faixas_raca = pd.read_csv(os.path.join(models_dir, "faixas_por_raca.csv"))
            self.faixas_porte = pd.read_csv(os.path.join(models_dir, "faixas_por_porte.csv"))
        except Exception as e:
            print(f"[ERRO] Falha ao carregar modelos de peso: {e}")
            self.modelo_com_raca = None
            self.modelo_srd = None
            self.faixas_raca = None
            self.faixas_porte = None

    def analisar_peso_ideal(self, dados: PesoIdealRequestDTO) -> PesoIdealResponseDTO:
        if self.modelo_com_raca is None or self.modelo_srd is None:
            raise HTTPException(status_code=500, detail="Modelos de IA não carregados.")

        # Identificando se é SRD
        # Consideramos SRD se a raça for nula, vazia, ou "SRD (Sem Raça Definida)" (ignorando case)
        breed = dados.raca.strip() if dados.raca else ""
        is_srd = not breed or breed.upper() in ["SRD (SEM RAÇA DEFINIDA)", "SRD", "UNKNOWN", "MISTURA"]

        # Mapeando o porte de Português para Inglês para uso no modelo e CSV
        mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
        breed_size_en = mapa_porte.get(dados.porte, dados.porte)

        # Mapeando o Sexo (M -> MALE, F -> FEMALE)
        sex_en = "MALE" if dados.sexo.upper() == "M" else "FEMALE"

        # Mapeando Castrado (True -> NEUTERED/SPAYED, False -> INTACT)
        # O modelo pode usar NEUTERED para machos e SPAYED para fêmeas ou genérico.
        # Vamos assumir o padrão NEUTERED para castrados em geral, ou SPAYED para femeas
        spay_neuter_en = "INTACT"
        if dados.castrado:
            spay_neuter_en = "SPAYED" if sex_en == "FEMALE" else "NEUTERED"

        # Calculando a idade a partir da data de nascimento
        try:
            idade_calculada = DomainUtils.calcular_idade(dados.data_nascimento, retornar_float=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao calcular idade: {str(e)}")

        peso_minimo = 0.0
        peso_maximo = 0.0
        peso_ideal_calculado = 0.0

        if not is_srd:
            # Fluxo Com Raça
            df_input = pd.DataFrame([{
                "Breed": breed,
                "Breed Size": breed_size_en,
                "Sex": sex_en,
                "Age": idade_calculada,
                "Spay/Neuter Status": spay_neuter_en
            }])
            
            try:
                # O modelo .pkl já deve conter o pre-processing (Pipelines)
                peso_ideal_calculado = float(self.modelo_com_raca.predict(df_input)[0])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao predizer peso (Com Raça): {str(e)}")
            
            # Buscar faixas
            faixa = self.faixas_raca[self.faixas_raca["Breed"].str.contains(breed, case=False, na=False)]
            if not faixa.empty:
                peso_minimo = float(faixa["P10"].values[0])
                peso_maximo = float(faixa["P90"].values[0])
            else:
                # Fallback se a raça não for encontrada exatamente no CSV
                peso_minimo = max(0, peso_ideal_calculado * 0.85)
                peso_maximo = peso_ideal_calculado * 1.15
        else:
            # Fluxo SRD
            df_input = pd.DataFrame([{
                "Breed Size": breed_size_en,
                "Sex": sex_en,
                "Age": idade_calculada,
                "Spay/Neuter Status": spay_neuter_en
            }])
            
            try:
                peso_ideal_calculado = float(self.modelo_srd.predict(df_input)[0])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao predizer peso (SRD): {str(e)}")

            # Buscar faixas por porte
            faixa = self.faixas_porte[self.faixas_porte["Breed Size"].str.contains(breed_size_en, case=False, na=False)]
            if not faixa.empty:
                peso_minimo = float(faixa["P10"].values[0])
                peso_maximo = float(faixa["P90"].values[0])
            else:
                # Fallback se o porte não for encontrado
                peso_minimo = max(0, peso_ideal_calculado * 0.85)
                peso_maximo = peso_ideal_calculado * 1.15

        return PesoIdealResponseDTO(
            peso_ideal=round(peso_ideal_calculado, 2),
            peso_atual=dados.peso_atual,
            peso_minimo=round(peso_minimo, 2),
            peso_maximo=round(peso_maximo, 2)
        )
