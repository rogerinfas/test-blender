'use client';

import Link from 'next/link';
import MachuCanvas from '@/components/MachuCanvas';

const DESTACADOS = [
  {
    titulo: 'Machu Picchu Clásico',
    desc: 'La ciudadela inca en un día. Tren, guía y entradas incluidas.',
    precio: 'Desde $249',
  },
  {
    titulo: 'Valle Sagrado',
    desc: 'Pisac, Ollantaytambo y salineras de Maras en ruta completa.',
    precio: 'Desde $89',
  },
  {
    titulo: 'Huayna Picchu',
    desc: 'Sube la montaña detrás de la ciudadela. Vistas extremas.',
    precio: 'Desde $299',
  },
];

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero con el modelo 3D de fondo */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 h-[600px] md:h-[680px]">
          <MachuCanvas autoRotate interactive={false} />
          <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-white/60 via-white/10 to-white dark:from-black/70 dark:via-black/20 dark:to-black" />
        </div>

        <div className="relative mx-auto flex w-full max-w-5xl flex-col items-center px-5 pb-16 pt-20 text-center md:pt-28">
          <p className="mb-3 text-[14px] font-medium text-[#0071e3]">
            Tours a Machu Picchu
          </p>
          <h1 className="max-w-3xl text-5xl font-semibold leading-[1.05] tracking-tight drop-shadow-sm md:text-7xl">
            La maravilla del mundo, sin complicaciones.
          </h1>
          <p className="mt-5 max-w-xl text-[17px] leading-relaxed text-zinc-600 dark:text-zinc-300">
            Nosotros nos encargamos de trenes, entradas y guías. Tú solo
            preocúpate de la foto.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/tours"
              className="rounded-full bg-[#0071e3] px-6 py-2.5 text-[15px] font-medium text-white transition-colors hover:bg-[#0077ed]"
            >
              Ver tours
            </Link>
            <Link
              href="/modelo"
              className="rounded-full bg-white/70 px-6 py-2.5 text-[15px] font-medium text-zinc-900 backdrop-blur transition-colors hover:bg-white dark:bg-black/60 dark:text-white dark:hover:bg-black"
            >
              Ver modelo 3D
            </Link>
          </div>
        </div>
      </section>

      {/* Destacados */}
      <section className="mx-auto grid w-full max-w-5xl gap-4 px-5 pb-20">
        <div className="grid gap-4 md:grid-cols-3">
          {DESTACADOS.map((t) => (
            <div
              key={t.titulo}
              className="flex flex-col rounded-2xl bg-zinc-100 p-7 dark:bg-zinc-900"
            >
              <h2 className="text-[19px] font-semibold tracking-tight">
                {t.titulo}
              </h2>
              <p className="mt-2 flex-1 text-[14px] leading-relaxed text-zinc-500 dark:text-zinc-400">
                {t.desc}
              </p>
              <p className="mt-4 text-[15px] font-medium">{t.precio}</p>
              <Link
                href="/tours"
                className="mt-3 text-[14px] font-medium text-[#0071e3] hover:underline"
              >
                Más información →
              </Link>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
