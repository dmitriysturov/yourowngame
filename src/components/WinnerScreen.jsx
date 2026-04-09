const WinnerScreen = ({ winner, onRestart }) => {
  return (
    <section className="animate-fadeInUp mt-6 rounded-2xl border border-amber-300/35 bg-gradient-to-br from-amber-500/15 to-sky-500/15 p-8 text-center shadow-accent">
      <p className="text-sm uppercase tracking-[0.3em] text-amber-200">Игра завершена</p>
      <h2 className="mt-3 text-3xl font-black text-white md:text-4xl">Победитель: {winner.name}</h2>
      <p className="mt-3 text-lg text-amber-100">Финальный счёт: {winner.score} очков</p>
      <button
        type="button"
        onClick={onRestart}
        className="mt-6 rounded-xl border border-amber-300/60 bg-amber-400/20 px-5 py-3 font-bold text-amber-100 transition hover:-translate-y-0.5 hover:bg-amber-400/35"
      >
        Начать новую игру
      </button>
    </section>
  );
};

export default WinnerScreen;
