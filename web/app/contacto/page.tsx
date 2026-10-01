"use client";

import { useState } from "react";

export default function Contacto() {
  const [enviado, setEnviado] = useState(false);

  return (
    <section className="mx-auto w-full max-w-xl px-5 py-14">
      <h1 className="text-center text-4xl font-semibold tracking-tight md:text-5xl">
        Contáctanos
      </h1>
      <p className="mt-3 text-center text-[16px] text-zinc-500 dark:text-zinc-400">
        Respondemos en menos de 24 horas.
      </p>

      {enviado ? (
        <div className="mt-10 rounded-2xl bg-zinc-100 p-10 text-center dark:bg-zinc-900">
          <p className="text-[20px] font-semibold">¡Mensaje enviado! 🎉</p>
          <p className="mt-2 text-[15px] text-zinc-500 dark:text-zinc-400">
            Te escribiremos muy pronto.
          </p>
        </div>
      ) : (
        <form
          className="mt-10 flex flex-col gap-4"
          onSubmit={(e) => {
            e.preventDefault();
            setEnviado(true);
          }}
        >
          <input
            required
            placeholder="Nombre"
            className="rounded-xl border border-black/[0.12] bg-transparent px-4 py-3 text-[15px] outline-none placeholder:text-zinc-400 focus:border-[#0071e3] dark:border-white/[0.16]"
          />
          <input
            required
            type="email"
            placeholder="Email"
            className="rounded-xl border border-black/[0.12] bg-transparent px-4 py-3 text-[15px] outline-none placeholder:text-zinc-400 focus:border-[#0071e3] dark:border-white/[0.16]"
          />
          <textarea
            required
            rows={4}
            placeholder="¿Qué tour te interesa?"
            className="resize-none rounded-xl border border-black/[0.12] bg-transparent px-4 py-3 text-[15px] outline-none placeholder:text-zinc-400 focus:border-[#0071e3] dark:border-white/[0.16]"
          />
          <button
            type="submit"
            className="rounded-full bg-[#0071e3] py-3 text-[15px] font-medium text-white transition-colors hover:bg-[#0077ed]"
          >
            Enviar mensaje
          </button>
        </form>
      )}
    </section>
  );
}
