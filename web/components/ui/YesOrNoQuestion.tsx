"use client";

import { FaCheck, FaTimes } from "react-icons/fa";

interface YesOrNoQuestionProps {
  questionText: string;
  descriptionQuestion?: string;
  initialValue?: boolean | null;
  onChanged: (value: boolean | null) => void;
}

export default function YesOrNoQuestion({
  questionText,
  descriptionQuestion,
  initialValue = null,
  onChanged,
}: YesOrNoQuestionProps) {
  const handleSelection = (isYes: boolean) => {
    // Se clicar no botão que já está selecionado, opcionalmente desmarca (ou mantém)
    // No Flutter, o checkbox alterna ou seleciona. Vamos apenas setar o valor diretamente:
    onChanged(isYes);
  };

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Container de Pergunta */}
      <div className="w-full py-5 px-8 bg-[var(--color-sand-900)] rounded-[24px] flex flex-col items-center gap-1.5 shadow-[0_2px_8px_rgba(117,72,25,0.05)]">
        <h3 className="text-center font-bold text-[16px] leading-snug text-[var(--color-orange-900)]">
          {questionText}
        </h3>
        {descriptionQuestion && (
          <p className="text-center text-[12px] leading-normal text-[var(--color-brown)] opacity-90">
            {descriptionQuestion}
          </p>
        )}
      </div>

      {/* Botões de Seleção */}
      <div className="flex justify-center gap-6">
        {/* Botão Sim */}
        <button
          onClick={() => handleSelection(true)}
          className={`
            flex items-center justify-center gap-2
            w-[130px] h-[48px] rounded-full
            font-semibold text-sm border-2
            transition-all duration-300 transform active:scale-95
            shadow-sm cursor-pointer
            ${
              initialValue === true
                ? "bg-[var(--color-primary)] border-[var(--color-primary)] text-white shadow-md hover:brightness-110"
                : "bg-white border-[var(--color-primary)] text-[var(--color-primary)] hover:bg-[var(--color-sand-100)] hover:scale-102"
            }
          `}
        >
          {initialValue === true && <FaCheck className="text-[12px]" />}
          <span>Sim</span>
        </button>

        {/* Botão Não */}
        <button
          onClick={() => handleSelection(false)}
          className={`
            flex items-center justify-center gap-2
            w-[130px] h-[48px] rounded-full
            font-semibold text-sm border-2
            transition-all duration-300 transform active:scale-95
            shadow-sm cursor-pointer
            ${
              initialValue === false
                ? "bg-[var(--color-primary)] border-[var(--color-primary)] text-white shadow-md hover:brightness-110"
                : "bg-white border-[var(--color-primary)] text-[var(--color-primary)] hover:bg-[var(--color-sand-100)] hover:scale-102"
            }
          `}
        >
          {initialValue === false && <FaTimes className="text-[12px]" />}
          <span>Não</span>
        </button>
      </div>
    </div>
  );
}
