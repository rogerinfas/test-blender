const STATS = [
  { num: "+12 años", label: "operando en Cusco" },
  { num: "+25 mil", label: "viajeros felices" },
  { num: "4.9/5", label: "calificación promedio" },
];

export default function Nosotros() {
  return (
    <section className="mx-auto w-full max-w-3xl px-5 py-14 text-center">
      <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
        Nosotros
      </h1>
      <p className="mx-auto mt-5 max-w-xl text-[17px] leading-relaxed text-zinc-500 dark:text-zinc-400">
        Somos MAPI, un equipo cusqueño apasionado por mostrar lo mejor de
        nuestra tierra. Operamos tours pequeños, con guías locales y cero
        letra chica: lo que ves es lo que viajas.
      </p>
      <div className="mt-10 grid grid-cols-3 gap-4">
        {STATS.map((s) => (
          <div
            key={s.label}
            className="rounded-2xl bg-zinc-100 px-4 py-6 dark:bg-zinc-900"
          >
            <p className="text-2xl font-semibold tracking-tight md:text-3xl">
              {s.num}
            </p>
            <p className="mt-1 text-[13px] text-zinc-500 dark:text-zinc-400">
              {s.label}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
