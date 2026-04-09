const QuestionCell = ({ question, played, onOpen }) => {
  const baseClasses =
    'h-20 rounded-xl border text-2xl font-black transition duration-200 md:h-24 md:text-3xl';

  if (played) {
    return (
      <div
        className={`${baseClasses} border-slate-600/60 bg-played text-slate-400 line-through grid place-items-center`}
        aria-label="Вопрос уже сыгран"
      >
        ✓
      </div>
    );
  }

  return (
    <button
      type="button"
      onClick={onOpen}
      className={`${baseClasses} grid place-items-center border-accent/35 bg-panel text-accent shadow-accent hover:-translate-y-1 hover:scale-[1.02] hover:border-accentBlue/70 hover:text-accentBlue active:scale-100`}
    >
      {question.value}
    </button>
  );
};

export default QuestionCell;
