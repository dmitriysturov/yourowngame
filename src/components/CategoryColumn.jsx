import QuestionCell from './QuestionCell';

const CategoryColumn = ({ category, playedMap, onOpenQuestion }) => {
  return (
    <article className="animate-fadeInUp rounded-2xl border border-slate-700/70 bg-slate-900/40 p-3">
      <h3 className="mb-3 min-h-16 rounded-xl bg-panel px-2 py-3 text-center text-sm font-bold uppercase tracking-wide text-accentBlue md:text-base">
        {category.title}
      </h3>
      <div className="space-y-2">
        {category.questions.map((question) => {
          const played = Boolean(playedMap[question.id]);
          return (
            <QuestionCell
              key={question.id}
              question={question}
              played={played}
              onOpen={() => onOpenQuestion(category.id, question.id)}
            />
          );
        })}
      </div>
    </article>
  );
};

export default CategoryColumn;
