'use client';

import { Loader } from '@react-three/drei';
import MachuCanvas from '@/components/MachuCanvas';

export default function Modelo() {
  return (
    <section className="relative flex w-full flex-1 flex-col">
      <div className="pointer-events-none absolute left-0 right-0 top-0 z-10 mx-auto mt-6 max-w-5xl px-5 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900 drop-shadow-sm md:text-4xl">
          Machu Picchu en 3D
        </h1>
        <p className="mt-1 text-[14px] text-zinc-600">
          Arrastra para orbitar · scroll para zoom · clic derecho para mover
        </p>
      </div>

      <div className="h-[calc(100dvh-6.5rem)] min-h-[480px] w-full">
        <MachuCanvas />
        <Loader />
      </div>
    </section>
  );
}
