import CategoryColumn from './CategoryColumn';

const GameBoard = ({ categories, playedMap, onOpenQuestion }) => {
  return (
    <section>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Игровое поле</h2>
        <span className="text-xs uppercase tracking-[0.2em] text-slate-400">5×5 вопросов</span>
      </div>
      <div className="grid gap-3 lg:grid-cols-5 sm:grid-cols-2">
        {categories.map((category) => (
          <CategoryColumn
            key={category.id}
            category={category}
            playedMap={playedMap}
            onOpenQuestion={onOpenQuestion}
          />
        ))}
      </div>
    </section>
  );
};

export default GameBoard;
