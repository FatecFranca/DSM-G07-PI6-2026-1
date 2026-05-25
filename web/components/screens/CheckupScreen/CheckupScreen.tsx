"use client";

import { useState, useRef } from "react";
import { authService } from "@/services/authService";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import YesOrNoQuestion from "@/components/ui/YesOrNoQuestion";
import DiseasePrediction from "@/components/ui/DiseasePrediction";
import { FaStethoscope, FaArrowLeft } from "react-icons/fa";

interface Props {
  animalId: string;
  animalName: string;
}

const INITIAL_RESPONTAS = {
  duracao: "" as string | number,
  perda_de_apetite: null as boolean | null,
  vomito: null as boolean | null,
  diarreia: null as boolean | null,
  tosse: null as boolean | null,
  dificuldade_para_respirar: null as boolean | null,
  dificuldade_para_locomover: null as boolean | null,
  problemas_na_pele: null as boolean | null,
  secrecao_nasal: null as boolean | null,
  secrecao_ocular: null as boolean | null,
  agitacao: null as boolean | null,
  andar_em_circulos: null as boolean | null,
  aumento_apetite: null as boolean | null,
  cera_excessiva_nas_orelhas: null as boolean | null,
  coceira: null as boolean | null,
  desidratacao: null as boolean | null,
  desmaio: null as boolean | null,
  dificuldade_para_urinar: null as boolean | null,
  dor: null as boolean | null,
  espamos_musculares: null as boolean | null,
  espirros: null as boolean | null,
  febre: null as boolean | null,
  fraqueza: null as boolean | null,
  inchaco: null as boolean | null,
  lambedura: null as boolean | null,
  letargia: null as boolean | null,
  lingua_azulada: null as boolean | null,
  perda_de_pelos: null as boolean | null,
  perda_de_peso: null as boolean | null,
  ranger_de_dentes: null as boolean | null,
  ronco: null as boolean | null,
  salivacao: null as boolean | null,
  suor_alterado: null as boolean | null,
};

export default function CheckupScreen({ animalId, animalName }: Props) {
  const [mostrouIntroducao, setMostrouIntroducao] = useState(false);
  const [etapaAtual, setEtapaAtual] = useState(0);
  const [enviando, setEnviando] = useState(false);
  const [mostrouResultado, setMostrouResultado] = useState(false);
  const [resultadoRotulo, setResultadoRotulo] = useState<string | null>(null);
  const [description, setDescription] = useState<string | null>(null);
  const [showWarning, setShowWarning] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const [respostas, setRespostas] = useState<Record<string, any>>(INITIAL_RESPONTAS);

  const containerRef = useRef<HTMLDivElement>(null);

  const resetarFluxo = () => {
    setRespostas({ ...INITIAL_RESPONTAS });
    setMostrouIntroducao(false);
    setEtapaAtual(0);
    setEnviando(false);
    setMostrouResultado(false);
    setResultadoRotulo(null);
    setDescription(null);
    setShowWarning(false);
    setApiError(null);
    scrollToTop();
  };

  const scrollToTop = () => {
    if (containerRef.current) {
      containerRef.current.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const mapResultadoParaRotulo = (resultado: string) => {
    switch (resultado) {
      case "gastrointestinal":
        return "Problemas gastrointestinais";
      case "respiratoria":
        return "Problemas respiratórios";
      case "cutanea":
        return "Problemas cutâneos";
      case "urogenital":
        return "Problemas urogenitais";
      case "neuro_musculoesqueletica":
        return "Problemas neuro-musculoesqueléticos";
      case "cardiovascular_hematologica":
        return "Problemas cardiovasculares/hematológicos";
      case "nenhuma":
      default:
        return `${animalName} está saudável`;
    }
  };

  const mapResultadoParaRotuloDescricao = (resultado: string) => {
    if (resultado === "nenhuma") {
      return "Não foi identificado nenhum problema de saúde de acordo com as respostas fornecidas.";
    }
    return null;
  };

  const atualizarResposta = (chave: string, valor: boolean | null) => {
    setRespostas((prev) => ({
      ...prev,
      [chave]: valor,
    }));
    setShowWarning(false);
  };

  const perguntasDaEtapa = (etapa: number): string[] => {
    switch (etapa) {
      case 0:
        return ["agitacao", "letargia", "fraqueza", "andar_em_circulos", "ranger_de_dentes", "lambedura"];
      case 1:
        return ["perda_de_apetite", "aumento_apetite", "vomito", "diarreia", "perda_de_peso", "desidratacao"];
      case 2:
        return ["tosse", "dificuldade_para_respirar", "ronco", "espirros", "lingua_azulada", "febre"];
      case 3:
        return ["dificuldade_para_locomover", "dor", "espamos_musculares", "desmaio", "inchaco"];
      case 4:
        return ["problemas_na_pele", "coceira", "perda_de_pelos", "cera_excessiva_nas_orelhas", "suor_alterado", "salivacao"];
      case 5:
        return ["secrecao_nasal", "secrecao_ocular", "dificuldade_para_urinar"];
      default:
        return [];
    }
  };

  const todasPerguntasRespondidas = (): boolean => {
    const perguntas = perguntasDaEtapa(etapaAtual);
    for (const chave of perguntas) {
      if (respostas[chave] === null) {
        return false;
      }
    }
    return true;
  };

  const enviarRespostas = async () => {
    const token = authService.getToken();
    if (!token) {
      setApiError("ID do pet ou Token não encontrado. Faça login novamente.");
      return;
    }

    setEnviando(true);
    setApiError(null);

    // Mapear booleanos para 1/0 para a API Python, mantendo 'duracao'
    const duracaoNum = parseInt(respostas.duracao?.toString() || "0", 10);
    const payload: Record<string, any> = {
      duracao: isNaN(duracaoNum) ? 0 : duracaoNum,
    };

    Object.keys(respostas).forEach((key) => {
      if (key !== "duracao") {
        const val = respostas[key];
        payload[key] = val === null ? null : val ? 1 : 0;
      }
    });

    try {
      console.log("[CheckupScreen] Enviando payload:", payload);

      const res = await fetch(`/api/checkup/${animalId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error("Falha ao processar o checkup no servidor.");
      }

      const data = await res.json();
      console.log("[CheckupScreen] Resposta da API:", data);

      const resultLabel = mapResultadoParaRotulo(data.resultado);
      const descLabel = mapResultadoParaRotuloDescricao(data.resultado);

      setResultadoRotulo(resultLabel);
      setDescription(descLabel);
      setMostrouResultado(true);
      scrollToTop();
    } catch (e: any) {
      console.error(e);
      setApiError(e.message || "Erro de rede ao submeter formulário.");
    } finally {
      setEnviando(false);
    }
  };

  const handleProximoBotao = () => {
    if (mostrouResultado) {
      resetarFluxo();
      return;
    }

    if (!todasPerguntasRespondidas()) {
      setShowWarning(true);
      scrollToTop();
      return;
    }

    if (etapaAtual < 5) {
      setEtapaAtual((prev) => prev + 1);
      scrollToTop();
    } else {
      enviarRespostas();
    }
  };

  const handleVoltarBotao = () => {
    setShowWarning(false);
    setApiError(null);
    if (etapaAtual === 0) {
      setMostrouIntroducao(false);
    } else {
      setEtapaAtual((prev) => prev - 1);
    }
    scrollToTop();
  };

  const getTituloEtapa = (etapa: number): string => {
    switch (etapa) {
      case 0:
        return "Comportamento e Rotina";
      case 1:
        return "Alimentação e Digestão";
      case 2:
        return "Respiração e Circulação";
      case 3:
        return "Movimento e Coordenação";
      case 4:
        return "Pele, Orelhas e Pelos";
      case 5:
        return "Sintomas Específicos";
      default:
        return "";
    }
  };

  return (
    <div
      ref={containerRef}
      className="w-full h-full overflow-y-auto bg-[var(--color-sand-100)] px-4 py-6 pb-[250px] scrollbar-hide flex flex-col items-center"
    >
      <div className="flex flex-col items-center max-w-md w-full mt-auto mb-auto">
        
        {/* TELA DE INTRODUÇÃO */}
        {!mostrouIntroducao && !mostrouResultado && (
          <div className="w-full flex flex-col items-center">
            {/* Título principal */}
            <div className="flex flex-col items-center gap-1.5 mb-6">
              <h2 className="text-[var(--color-primary)] text-[26px] font-black text-center tracking-tight">
                Checkup Inteligente
              </h2>
              <span className="text-[var(--color-orange-900)] font-bold text-[12px] uppercase tracking-wider text-center">
                Descubra o que o seu pet pode estar sentindo
              </span>
            </div>

            {/* Parágrafo explicativo */}
            <p className="text-center text-[14px] leading-relaxed text-[var(--color-brown)] font-medium mb-8 px-2">
              Responda algumas perguntas rápidas sobre os sintomas observados e deixe a inteligência da PetDex analisar os dados para identificar possíveis problemas de saúde de forma ágil e segura.
            </p>

            {/* Card Informativo com lista */}
            <div
              className="w-full p-6 rounded-[24px] mb-8"
              style={{
                backgroundColor: "var(--color-sand-900)",
              }}
            >
              <h4 className="font-bold text-sm text-[var(--color-orange-900)] mb-4">
                A nossa análise poderá indicar se há sinais relacionados a:
              </h4>
              <ul className="flex flex-col gap-2.5 text-[var(--color-brown)] font-semibold text-[13px]">
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Sistema cardiovascular e hematológico</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Problemas de pele (cutâneas)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Distúrbios gastrointestinais</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Problemas neurológicos ou musculoesqueléticos</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Alterações respiratórias</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[var(--color-brown)] font-black text-base leading-none">•</span>
                  <span>Condições do trato urinário ou genital</span>
                </li>
              </ul>

              <p className="text-center font-bold text-sm text-[var(--color-primary)] mt-4">
                Ou indicar que está tudo bem! 🐾
              </p>
            </div>

            {/* Iniciar Button */}
            <button
              onClick={() => {
                setMostrouIntroducao(true);
                scrollToTop();
              }}
              className="flex items-center justify-center gap-2 h-[50px] px-8 text-base bg-[var(--color-primary-active)] hover:brightness-110 active:scale-95 text-white font-semibold rounded-full cursor-pointer shadow-md transition-all duration-300 transform"
            >
              Iniciar
            </button>

            {/* Bottom Disclaimer */}
            <p className="text-center text-[11px] leading-snug text-[var(--color-brown)] opacity-60 font-medium mt-6 px-4">
              Essa análise tem caráter estritamente informativo e não substitui de forma alguma a avaliação de um médico veterinário.
            </p>
          </div>
        )}

        {/* FLUXO DE PERGUNTAS */}
        {mostrouIntroducao && !mostrouResultado && (
          <div className="w-full flex flex-col items-center gap-6">
            
            {/* Header da Etapa */}
            <div className="w-full flex flex-col items-center gap-1.5 mb-2">
              <h2 className="text-[var(--color-primary)] text-[22px] font-black text-center tracking-tight leading-tight">
                {getTituloEtapa(etapaAtual)}
              </h2>
              <span className="bg-[var(--color-sand-900)] text-[var(--color-brown)] px-3 py-1.5 rounded-full font-bold text-[11px] uppercase tracking-widest shadow-sm">
                Passo {etapaAtual + 1} de 6
              </span>
            </div>

            {/* Warning de validação se houver */}
            {showWarning && (
              <div className="w-full bg-[var(--color-primary-active)] text-white text-center font-semibold text-[13px] rounded-2xl py-3.5 px-5 shadow-[0_4px_12px_rgba(191,73,4,0.2)] transition-all duration-300 animate-pulse">
                ⚠️ Por favor, responda todas as perguntas antes de continuar.
              </div>
            )}

            {/* Erro de API */}
            {apiError && (
              <div className="w-full bg-[var(--color-red-200)] text-[var(--color-red-700)] text-center font-semibold text-[13px] rounded-2xl py-3.5 px-5 border border-[var(--color-red-700)] opacity-90">
                ❌ {apiError}
              </div>
            )}

            {/* Renderização condicional das etapas */}
            <div className="w-full flex flex-col gap-6">
              {etapaAtual === 0 && (
                <>
                  <YesOrNoQuestion
                    questionText={`${animalName} está agitado ou mais inquieto que o normal?`}
                    initialValue={respostas.agitacao}
                    onChanged={(v) => atualizarResposta("agitacao", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Você notou letargia?"
                    descriptionQuestion="Desânimo, cansaço ou dorme mais que o normal"
                    initialValue={respostas.letargia}
                    onChanged={(v) => atualizarResposta("letargia", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} demonstra fraqueza ou dificuldade em se levantar?`}
                    initialValue={respostas.fraqueza}
                    onChanged={(v) => atualizarResposta("fraqueza", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Está andando em círculos, sem motivo aparente?"
                    initialValue={respostas.andar_em_circulos}
                    onChanged={(v) => atualizarResposta("andar_em_circulos", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Está rangendo os dentes com frequência?"
                    initialValue={respostas.ranger_de_dentes}
                    onChanged={(v) => atualizarResposta("ranger_de_dentes", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Apresenta lambedura excessiva em alguma parte do corpo?"
                    initialValue={respostas.lambedura}
                    onChanged={(v) => atualizarResposta("lambedura", v)}
                  />
                </>
              )}

              {etapaAtual === 1 && (
                <>
                  <YesOrNoQuestion
                    questionText={`${animalName} perdeu o apetite recentemente?`}
                    initialValue={respostas.perda_de_apetite}
                    onChanged={(v) => atualizarResposta("perda_de_apetite", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Houve aumento no apetite, comendo mais que o normal?"
                    initialValue={respostas.aumento_apetite}
                    onChanged={(v) => atualizarResposta("aumento_apetite", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Está vomitando com frequência?"
                    initialValue={respostas.vomito}
                    onChanged={(v) => atualizarResposta("vomito", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Apresenta diarreia ou fezes muito moles?"
                    initialValue={respostas.diarreia}
                    onChanged={(v) => atualizarResposta("diarreia", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Você notou perda de peso sem motivo aparente?"
                    initialValue={respostas.perda_de_peso}
                    onChanged={(v) => atualizarResposta("perda_de_peso", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} está com sinais de desidratação?`}
                    descriptionQuestion="Boca, olhos ou nariz secos, urina escura e em menor quantidade, boca quente."
                    initialValue={respostas.desidratacao}
                    onChanged={(v) => atualizarResposta("desidratacao", v)}
                  />
                </>
              )}

              {etapaAtual === 2 && (
                <>
                  <YesOrNoQuestion
                    questionText={`${animalName} está com tosse?`}
                    initialValue={respostas.tosse}
                    onChanged={(v) => atualizarResposta("tosse", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Tem dificuldade para respirar ou respiração ofegante em repouso?"
                    initialValue={respostas.dificuldade_para_respirar}
                    onChanged={(v) => atualizarResposta("dificuldade_para_respirar", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Você notou roncos ou barulhos diferentes ao respirar?"
                    initialValue={respostas.ronco}
                    onChanged={(v) => atualizarResposta("ronco", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Está espirrando com frequência?"
                    initialValue={respostas.espirros}
                    onChanged={(v) => atualizarResposta("espirros", v)}
                  />
                  <YesOrNoQuestion
                    questionText="A língua ou gengivas estão azuladas?"
                    initialValue={respostas.lingua_azulada}
                    onChanged={(v) => atualizarResposta("lingua_azulada", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} parece ter febre?`}
                    descriptionQuestion="Aparenta estar com o corpo mais quente, especialmente as orelhas."
                    initialValue={respostas.febre}
                    onChanged={(v) => atualizarResposta("febre", v)}
                  />
                </>
              )}

              {etapaAtual === 3 && (
                <>
                  <YesOrNoQuestion
                    questionText={`${animalName} tem dificuldade para se locomover?`}
                    descriptionQuestion="Manca ou evita andar?"
                    initialValue={respostas.dificuldade_para_locomover}
                    onChanged={(v) => atualizarResposta("dificuldade_para_locomover", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Demonstra dor ao ser tocado ou ao se mover?"
                    initialValue={respostas.dor}
                    onChanged={(v) => atualizarResposta("dor", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Você percebeu espasmos musculares?"
                    descriptionQuestion="Tremores involuntários"
                    initialValue={respostas.espamos_musculares}
                    onChanged={(v) => atualizarResposta("espamos_musculares", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} já teve algum desmaio recentemente?`}
                    initialValue={respostas.desmaio}
                    onChanged={(v) => atualizarResposta("desmaio", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Há inchaços visíveis em alguma parte do corpo?"
                    initialValue={respostas.inchaco}
                    onChanged={(v) => atualizarResposta("inchaco", v)}
                  />
                </>
              )}

              {etapaAtual === 4 && (
                <>
                  <YesOrNoQuestion
                    questionText="Há problemas na pele, como feridas, irritações ou manchas?"
                    initialValue={respostas.problemas_na_pele}
                    onChanged={(v) => atualizarResposta("problemas_na_pele", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} está com coceira constante?`}
                    initialValue={respostas.coceira}
                    onChanged={(v) => atualizarResposta("coceira", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Há perda de pelos excessiva ou em áreas específicas?"
                    initialValue={respostas.perda_de_pelos}
                    onChanged={(v) => atualizarResposta("perda_de_pelos", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Há cera excessiva nas orelhas ou mau cheiro?"
                    initialValue={respostas.cera_excessiva_nas_orelhas}
                    onChanged={(v) => atualizarResposta("cera_excessiva_nas_orelhas", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Você notou suor alterado?"
                    descriptionQuestion="Áreas úmidas ou odor incomum"
                    initialValue={respostas.suor_alterado}
                    onChanged={(v) => atualizarResposta("suor_alterado", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Está com salivação maior que o normal?"
                    initialValue={respostas.salivacao}
                    onChanged={(v) => atualizarResposta("salivacao", v)}
                  />
                </>
              )}

              {etapaAtual === 5 && (
                <>
                  <YesOrNoQuestion
                    questionText="Há secreção nasal?"
                    descriptionQuestion="Corrimento pelo nariz"
                    initialValue={respostas.secrecao_nasal}
                    onChanged={(v) => atualizarResposta("secrecao_nasal", v)}
                  />
                  <YesOrNoQuestion
                    questionText="Há secreção ocular?"
                    descriptionQuestion="Olhos lacrimejando ou com crostas"
                    initialValue={respostas.secrecao_ocular}
                    onChanged={(v) => atualizarResposta("secrecao_ocular", v)}
                  />
                  <YesOrNoQuestion
                    questionText={`${animalName} demonstra dificuldade para urinar?`}
                    initialValue={respostas.dificuldade_para_urinar}
                    onChanged={(v) => atualizarResposta("dificuldade_para_urinar", v)}
                  />

                  {/* Campo de Duração dos Sintomas */}
                  <div className="w-full flex flex-col gap-4 mt-4">
                    <div className="w-full py-4 px-8 bg-[var(--color-sand-900)] rounded-[24px] flex flex-col items-center gap-1 shadow-sm">
                      <h4 className="font-bold text-[16px] text-[var(--color-orange-900)] text-center leading-snug">
                        Qual é a duração dos sintomas?
                      </h4>
                    </div>

                    <div className="w-full flex justify-center py-2">
                      <Input
                        hintText="Ex: 3"
                        type="number"
                        centerText={true}
                        suffixText=" dias"
                        textColor="text-[var(--color-brown)]"
                        value={respostas.duracao.toString()}
                        onChange={(text) => {
                          setRespostas((prev) => ({
                            ...prev,
                            duracao: text,
                          }));
                        }}
                      />
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Controles de Navegação */}
            <div className="w-full flex flex-col items-center gap-3 mt-4">
              <button
                onClick={enviando ? () => {} : handleProximoBotao}
                className="flex items-center justify-center gap-2 h-[50px] px-8 text-base bg-[var(--color-primary-active)] hover:brightness-110 active:scale-95 text-white font-semibold rounded-full cursor-pointer shadow-md transition-all duration-300 transform"
              >
                {enviando ? "Enviando..." : etapaAtual < 5 ? "Continuar" : "Enviar Respostas"}
              </button>

              {/* Botão Voltar */}
              <button
                onClick={handleVoltarBotao}
                className="flex items-center justify-center gap-2 py-2 px-6 rounded-full font-bold text-[14px] text-[var(--color-orange-900)] transition-all hover:bg-[var(--color-sand-900)] active:scale-95 cursor-pointer"
              >
                <FaArrowLeft size={12} />
                <span>Voltar</span>
              </button>
            </div>

            {/* Loading Indicator */}
            {enviando && (
              <div className="flex items-center justify-center w-full mt-4">
                <div className="w-8 h-8 border-4 border-[var(--color-orange-900)] border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </div>
        )}

        {/* TELA DE RESULTADO */}
        {mostrouResultado && (
          <div className="w-full flex flex-col items-center gap-6">
            
            {/* Header da Etapa */}
            <div className="w-full flex flex-col items-center gap-1 mb-2">
              <h2 className="text-[var(--color-primary)] text-[22px] font-black text-center tracking-tight leading-tight">
                Resultado da Análise
              </h2>
              <span className="bg-[var(--color-green-700)] text-white px-3 py-1.5 rounded-full font-bold text-[11px] uppercase tracking-widest shadow-sm">
                Concluído 🐾
              </span>
            </div>

            <DiseasePrediction
              diseaseText={resultadoRotulo || "Análise indisponível"}
              descriptionText={description}
            />

            {/* Botão Começar Novamente */}
             <button
               onClick={resetarFluxo}
               className="flex items-center justify-center gap-2 h-[50px] px-8 text-base bg-[var(--color-orange-900)] hover:brightness-110 active:scale-95 text-white font-semibold rounded-full cursor-pointer shadow-md transition-all duration-300 transform"
             >
               Começar Novamente
             </button>
          </div>
        )}
      </div>
    </div>
  );
}
