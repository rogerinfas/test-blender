"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const LINKS = [
  { href: "/", label: "Inicio" },
  { href: "/tours", label: "Tours" },
  { href: "/nosotros", label: "Nosotros" },
  { href: "/contacto", label: "Contáctanos" },
  { href: "/teclado", label: "Tecla 3D" },
];

export default function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-black/[0.08] bg-white/70 backdrop-blur-xl backdrop-saturate-150 dark:border-white/[0.12] dark:bg-black/60">
      <nav className="mx-auto flex h-12 max-w-5xl items-center justify-between px-5">
        <Link
          href="/"
          className="text-[17px] font-semibold tracking-tight text-zinc-900 dark:text-white"
        >
          MAPI
        </Link>

        {/* Desktop */}
        <ul className="hidden items-center gap-8 md:flex">
          {LINKS.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                className={`text-[13px] font-normal tracking-wide transition-colors hover:text-zinc-900 dark:hover:text-white ${
                  pathname === l.href
                    ? "text-zinc-900 dark:text-white"
                    : "text-zinc-500 dark:text-zinc-400"
                }`}
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>

        <Link
          href="/contacto"
          className="hidden rounded-full bg-[#0071e3] px-4 py-1.5 text-[13px] font-medium text-white transition-colors hover:bg-[#0077ed] md:block"
        >
          Reservar
        </Link>

        {/* Mobile toggle */}
        <button
          onClick={() => setOpen(!open)}
          aria-label="Abrir menú"
          className="flex h-9 w-9 flex-col items-center justify-center gap-[5px] md:hidden"
        >
          <span
            className={`h-[1.5px] w-5 bg-zinc-800 transition-transform dark:bg-zinc-200 ${
              open ? "translate-y-[6.5px] rotate-45" : ""
            }`}
          />
          <span
            className={`h-[1.5px] w-5 bg-zinc-800 transition-opacity dark:bg-zinc-200 ${
              open ? "opacity-0" : ""
            }`}
          />
          <span
            className={`h-[1.5px] w-5 bg-zinc-800 transition-transform dark:bg-zinc-200 ${
              open ? "-translate-y-[6.5px] -rotate-45" : ""
            }`}
          />
        </button>
      </nav>

      {/* Mobile menu */}
      {open && (
        <ul className="border-t border-black/[0.08] bg-white/95 px-5 py-2 backdrop-blur-xl md:hidden dark:border-white/[0.12] dark:bg-black/95">
          {LINKS.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                onClick={() => setOpen(false)}
                className={`block border-b border-black/[0.06] py-3 text-[15px] last:border-0 dark:border-white/[0.08] ${
                  pathname === l.href
                    ? "font-medium text-zinc-900 dark:text-white"
                    : "text-zinc-600 dark:text-zinc-300"
                }`}
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}
