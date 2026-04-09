import { useEffect, useMemo, useState } from 'react';
import Header from './components/Header';
import GameBoard from './components/GameBoard';
import QuestionModal from './components/QuestionModal';
import ResetButton from './components/ResetButton';
import ScoreBoard from './components/ScoreBoard';
import WinnerScreen from './components/WinnerScreen';
import { categories, initialTeams } from './data/gameData';
import { clearGameState, loadGameState, saveGameState } from './utils/storage';

const getQuestionById = (categoryId, questionId) => {
  const category = categories.find((item) => item.id === categoryId);
  if (!category) return null;
  return category.questions.find((item) => item.id === questionId) ?? null;
};

const getInitialState = () => {
  const stored = loadGameState();
  if (stored) {
    return {
      teams: stored.teams ?? initialTeams,
      playedMap: stored.playedMap ?? {},
      activeQuestion: null,
      showAnswer: false,
      completed: stored.completed ?? false
    };
  }

  return {
    teams: initialTeams,
    playedMap: {},
    activeQuestion: null,
    showAnswer: false,
    completed: false
  };
};

function App() {
  const [state, setState] = useState(getInitialState);

  useEffect(() => {
    const { teams, playedMap, completed } = state;
    saveGameState({ teams, playedMap, completed });
  }, [state]);

  const playedCount = useMemo(() => Object.keys(state.playedMap).length, [state.playedMap]);
  const totalQuestions = categories.reduce((sum, category) => sum + category.questions.length, 0);

  useEffect(() => {
    if (playedCount === totalQuestions && totalQuestions > 0 && !state.completed) {
      setState((prev) => ({ ...prev, completed: true, activeQuestion: null, showAnswer: false }));
    }
  }, [playedCount, totalQuestions, state.completed]);

  const winner = useMemo(() => {
    return [...state.teams].sort((a, b) => b.score - a.score)[0] ?? null;
  }, [state.teams]);

  const openQuestion = (categoryId, questionId) => {
    const question = getQuestionById(categoryId, questionId);
    if (!question) return;

    setState((prev) => ({
      ...prev,
      activeQuestion: question,
      showAnswer: false,
      playedMap: {
        ...prev.playedMap,
        [question.id]: true
      }
    }));
  };

  const closeQuestion = () => {
    setState((prev) => ({ ...prev, activeQuestion: null, showAnswer: false }));
  };

  const showAnswer = () => {
    setState((prev) => ({ ...prev, showAnswer: true }));
  };

  const changeScore = (teamId, delta) => {
    setState((prev) => ({
      ...prev,
      teams: prev.teams.map((team) => (team.id === teamId ? { ...team, score: team.score + delta } : team))
    }));
  };

  const resetGame = () => {
    clearGameState();
    setState({
      teams: initialTeams,
      playedMap: {},
      activeQuestion: null,
      showAnswer: false,
      completed: false
    });
  };

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-[1500px] flex-col gap-5 px-4 py-6 md:px-6 lg:px-8">
      <Header />

      <div className="flex items-center justify-between rounded-xl border border-slate-700/50 bg-slate-900/45 px-4 py-3 text-sm">
        <span className="text-slate-200">Сыграно вопросов: {playedCount} / {totalQuestions}</span>
        <ResetButton onReset={resetGame} />
      </div>

      <ScoreBoard teams={state.teams} onChangeScore={changeScore} />
      <GameBoard categories={categories} playedMap={state.playedMap} onOpenQuestion={openQuestion} />

      {state.completed && winner && <WinnerScreen winner={winner} onRestart={resetGame} />}

      <QuestionModal
        question={state.activeQuestion}
        showAnswer={state.showAnswer}
        onShowAnswer={showAnswer}
        onClose={closeQuestion}
      />
    </div>
  );
}

export default App;
