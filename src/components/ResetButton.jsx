const ResetButton = ({ onReset }) => {
  return (
    <button
      type="button"
      onClick={onReset}
      className="rounded-lg border border-slate-500/70 bg-slate-700/30 px-4 py-2 text-sm font-semibold text-slate-100 transition hover:-translate-y-0.5 hover:bg-slate-600/40"
    >
      Сбросить игру
    </button>
  );
};

export default ResetButton;
