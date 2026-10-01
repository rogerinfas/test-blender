import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Navbar from "@/components/Navbar";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "MAPI — Tours a Machu Picchu",
  description: "Tours, nosotros y contacto de MAPI",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="es"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col bg-white font-sans text-zinc-900 dark:bg-black dark:text-zinc-100">
        <Navbar />
        <main className="flex flex-1 flex-col">{children}</main>
        <footer className="border-t border-black/[0.08] py-6 text-center text-[12px] text-zinc-500 dark:border-white/[0.12] dark:text-zinc-400">
          © 2026 MAPI — Todos los derechos reservados
        </footer>
      </body>
    </html>
  );
}
