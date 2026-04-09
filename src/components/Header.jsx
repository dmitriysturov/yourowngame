const Header = () => {
  return (
    <header className="rounded-2xl border border-sky-300/25 bg-panel/80 px-6 py-5 shadow-glow backdrop-blur">
      <p className="text-sm uppercase tracking-[0.35em] text-accentBlue/80">Телевизионная викторина</p>
      <h1 className="mt-2 text-3xl font-black leading-tight text-white md:text-4xl">Своя игра: Турнир знаний</h1>
      <p className="mt-2 text-sm text-slate-300 md:text-base">Открывайте вопросы, начисляйте или снимайте очки командам и определяйте победителя.</p>
    </header>
  );
};

export default Header;
