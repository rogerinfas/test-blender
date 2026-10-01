'use client';

import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Model as MachuPicchu } from '@/components/MachuPicchu';

type Props = {
  autoRotate?: boolean;
  interactive?: boolean;
};

export default function MachuCanvas({ autoRotate = false, interactive = true }: Props) {
  return (
    <Canvas camera={{ position: [28, 30, 98], fov: 53, near: 0.5, far: 3000 }}>
      <color attach="background" args={['#a8c4e0']} />
      {/* Si el modelo se ve negro: sube el ambientLight a 1.2 o el directional a 3 */}
      <ambientLight intensity={0.7} />
      <hemisphereLight args={['#bfd9ff', '#4a7c3a', 0.5]} />
      <directionalLight position={[100, 80, -60]} intensity={2.2} color="#fff2df" />
      <Suspense fallback={null}>
        {/* Si el modelo es invisible: revisa que la cámara far cubra la escena (aquí 3000) */}
        <MachuPicchu />
      </Suspense>
      <OrbitControls
        target={[14, 6, 2]}
        makeDefault
        maxDistance={600}
        autoRotate={autoRotate}
        autoRotateSpeed={0.6}
        enableZoom={interactive}
        enablePan={interactive}
      />
    </Canvas>
  );
}
