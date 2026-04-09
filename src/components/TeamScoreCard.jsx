const TeamScoreCard = ({ team, onChangeScore }) => {
  return (
    <article className="rounded-2xl border border-slate-700/60 bg-panel/60 p-4 shadow-glow">
      <h3 className="text-lg font-bold text-slate-100">{team.name}</h3>
      <p className="mt-2 text-3xl font-black text-accent">{team.score}</p>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onChangeScore(team.id, -100)}
          className="flex-1 rounded-lg border border-rose-400/40 bg-rose-500/20 px-3 py-2 font-semibold text-rose-100 transition hover:-translate-y-0.5 hover:bg-rose-500/35"
        >
          −100
        </button>
        <button
          type="button"
          onClick={() => onChangeScore(team.id, 100)}
          className="flex-1 rounded-lg border border-emerald-400/40 bg-emerald-500/20 px-3 py-2 font-semibold text-emerald-100 transition hover:-translate-y-0.5 hover:bg-emerald-500/35"
        >
          +100
        </button>
      </div>
    </article>
  );
};

export default TeamScoreCard;
