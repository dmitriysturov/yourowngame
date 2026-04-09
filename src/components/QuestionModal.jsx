const QuestionModal = ({ question, showAnswer, onShowAnswer, onClose }) => {
  if (!question) return null;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/80 p-4 backdrop-blur-sm">
      <div className="animate-fadeInUp w-full max-w-3xl rounded-2xl border border-accentBlue/35 bg-panel p-6 shadow-glow">
        <p className="text-sm uppercase tracking-[0.25em] text-accentBlue">Стоимость: {question.value}</p>
        <h2 className="mt-3 text-2xl font-black text-white md:text-3xl">{question.question}</h2>

        <div className="mt-6 min-h-24 rounded-xl border border-slate-700/60 bg-slate-900/45 p-4">
          {showAnswer ? (
            <p className="text-lg font-semibold text-accent">Ответ: {question.answer}</p>
          ) : (
            <p className="text-slate-400">Нажмите кнопку ниже, чтобы показать правильный ответ.</p>
          )}
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onShowAnswer}
            disabled={showAnswer}
            className="rounded-lg border border-accent/50 bg-accent/20 px-4 py-2 font-semibold text-accent transition hover:scale-[1.02] hover:bg-accent/30 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Показать ответ
          </button>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-sky-400/50 bg-sky-500/15 px-4 py-2 font-semibold text-sky-200 transition hover:scale-[1.02] hover:bg-sky-500/30"
          >
            Вернуться на поле
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuestionModal;
