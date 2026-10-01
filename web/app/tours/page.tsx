import Link from "next/link";

const TOURS = [
  {
    titulo: "Machu Picchu Clásico",
    duracion: "1 día",
    precio: "$249",
    desc: "Tren ida y vuelta, bus a la ciudadela, guía profesional y entrada incluida.",
  },
  {
    titulo: "Valle Sagrado + Machu Picchu",
    duracion: "2 días",
    precio: "$429",
    desc: "Pisac, Ollantaytambo, noche en Aguas Calientes y amanecer en la ciudadela.",
  },
  {
    titulo: "Huayna Picchu Extremo",
    duracion: "1 día",
    precio: "$299",
    desc: "Circuito completo más ascenso a la montaña Huayna Picchu. Solo para valientes.",
  },
  {
    titulo: "Camino Inca Corto",
    duracion: "2 días",
    precio: "$549",
    desc: "Trekking por el Qhapaq Ñan, Wiñay Wayna y Puerta del Sol al amanecer.",
  },
];

export default function Tours() {
  return (
    <section className="mx-auto w-full max-w-5xl px-5 py-14">
      <h1 className="text-center text-4xl font-semibold tracking-tight md:text-5xl">
        Tours
      </h1>
      <p className="mx-auto mt-3 max-w-xl text-center text-[16px] text-zinc-500 dark:text-zinc-400">
        Elige tu aventura. Todos incluyen recojo, guía y entradas.
      </p>
      <div className="mt-10 grid gap-4 md:grid-cols-2">
        {TOURS.map((t) => (
          <div
            key={t.titulo}
            className="flex flex-col rounded-2xl bg-zinc-100 p-7 dark:bg-zinc-900"
          >
            <div className="flex items-baseline justify-between gap-3">
              <h2 className="text-[20px] font-semibold tracking-tight">
                {t.titulo}
              </h2>
              <span className="shrink-0 rounded-full bg-black/[0.06] px-3 py-1 text-[12px] font-medium dark:bg-white/[0.1]">
                {t.duracion}
              </span>
            </div>
            <p className="mt-2 flex-1 text-[14px] leading-relaxed text-zinc-500 dark:text-zinc-400">
              {t.desc}
            </p>
            <div className="mt-5 flex items-center justify-between">
              <p className="text-[17px] font-semibold">{t.precio}</p>
              <Link
                href="/contacto"
                className="rounded-full bg-[#0071e3] px-5 py-2 text-[14px] font-medium text-white transition-colors hover:bg-[#0077ed]"
              >
                Reservar
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
