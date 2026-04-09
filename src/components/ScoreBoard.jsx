import TeamScoreCard from './TeamScoreCard';

const ScoreBoard = ({ teams, onChangeScore }) => {
  return (
    <section className="rounded-2xl border border-slate-700/60 bg-slate-900/40 p-4 md:p-5">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Счёт команд</h2>
        <span className="text-xs uppercase tracking-[0.2em] text-slate-400">Ручное управление</span>
      </div>
      <div className="grid gap-3 lg:grid-cols-3 md:grid-cols-2">
        {teams.map((team) => (
          <TeamScoreCard key={team.id} team={team} onChangeScore={onChangeScore} />
        ))}
      </div>
    </section>
  );
};

export default ScoreBoard;
