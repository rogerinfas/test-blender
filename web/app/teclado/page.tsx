'use client';

import { Suspense, useCallback, useEffect, useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Loader } from '@react-three/drei';
import { Model as Tecla } from '@/components/Tecla';

function clickSound() {
  const Ctx =
    window.AudioContext ||
    (window as unknown as { webkitAudioContext: typeof AudioContext })
      .webkitAudioContext;
  const ctx = new Ctx();
  if (ctx.state === 'suspended') void ctx.resume();
  const t = ctx.currentTime;
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(2200, t);
  osc.frequency.exponentialRampToValueAtTime(300, t + 0.03);
  g.gain.setValueAtTime(0.12, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.05);
  osc.connect(g).connect(ctx.destination);
  osc.start(t);
  osc.stop(t + 0.06);
}

export default function Teclado() {
  const pressRef = useRef(0);
  const [pulsada, setPulsada] = useState(false);
  const [contador, setContador] = useState(0);

  const down = useCallback(() => {
    pressRef.current = 1;
    setPulsada(true);
  }, []);
  const up = useCallback(() => {
    pressRef.current = 0;
    setPulsada(false);
  }, []);

  const onBottomOut = useCallback(() => {
    clickSound();
    setContador((c) => c + 1);
  }, []);

  useEffect(() => {
    const kd = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        e.preventDefault();
        down();
      }
    };
    const ku = (e: KeyboardEvent) => {
      if (e.code === 'Space') up();
    };
    window.addEventListener('keydown', kd);
    window.addEventListener('keyup', ku);
    return () => {
      window.removeEventListener('keydown', kd);
      window.removeEventListener('keyup', ku);
    };
  }, [down, up]);

  return (
    <section className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-5 py-10">
      <h1 className="text-center text-4xl font-semibold tracking-tight md:text-5xl">
        Tecla interactiva
      </h1>
      <p className="mt-3 text-center text-[16px] text-zinc-500 dark:text-zinc-400">
        Haz clic en la tecla o pulsa <kbd className="rounded-md border border-black/[0.12] px-2 py-0.5 font-mono text-[13px] dark:border-white/[0.16]">ESPACIO</kbd>
      </p>

      <div className="mt-6 h-[52vh] min-h-[380px] w-full overflow-hidden rounded-3xl border border-black/[0.08] dark:border-white/[0.12]">
        <Canvas camera={{ position: [4.6, 4.2, 6.0], fov: 50, near: 0.1, far: 100 }}>
          <color attach="background" args={['#e8ebee']} />
          <ambientLight intensity={0.7} />
          <hemisphereLight args={['#ffffff', '#8a94a0', 0.5]} />
          <directionalLight position={[5, 8, -3]} intensity={2.2} color="#fff2df" />
          <Suspense fallback={null}>
            <group
              onPointerDown={down}
              onPointerUp={up}
              onPointerLeave={up}
            >
              <Tecla pressRef={pressRef} onBottomOut={onBottomOut} />
            </group>
          </Suspense>
          <OrbitControls target={[0, 0.6, 0]} makeDefault maxDistance={30} minDistance={3} />
        </Canvas>
        <Loader />
      </div>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="rounded-2xl bg-zinc-100 px-4 py-5 text-center dark:bg-zinc-900">
          <p className="text-[13px] text-zinc-500 dark:text-zinc-400">Estado</p>
          <p className="mt-1 text-[17px] font-semibold">
            {pulsada ? '● Pulsada' : '○ Reposo'}
          </p>
        </div>
        <div className="rounded-2xl bg-zinc-100 px-4 py-5 text-center dark:bg-zinc-900">
          <p className="text-[13px] text-zinc-500 dark:text-zinc-400">Pulsaciones</p>
          <p className="mt-1 text-[17px] font-semibold">{contador}</p>
        </div>
        <div className="rounded-2xl bg-zinc-100 px-4 py-5 text-center dark:bg-zinc-900">
          <p className="text-[13px] text-zinc-500 dark:text-zinc-400">Recorrido</p>
          <p className="mt-1 text-[17px] font-semibold">4.0 mm</p>
        </div>
      </div>
    </section>
  );
}
