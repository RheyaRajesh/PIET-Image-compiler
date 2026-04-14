import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

function CanvasVisualizer({ imageSrc, trace, currentStepIndex, onStepChange, codelSize }) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (imageSrc) {
      const img = new Image();
      img.onload = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        // Disable image smoothing for pixel art
        ctx.imageSmoothingEnabled = false;
        
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        
        setDimensions({ width: img.width, height: img.height });
      };
      img.src = imageSrc;
    }
  }, [imageSrc]);

  // Handle animation playback
  useEffect(() => {
    if (trace && trace.length > 0 && currentStepIndex < trace.length - 1) {
      const timer = setTimeout(() => {
        onStepChange(currentStepIndex + 1);
      }, 500); // 500ms delay per step (could be configurable speed)
      return () => clearTimeout(timer);
    }
  }, [trace, currentStepIndex, onStepChange]);

  const currentTrace = trace?.[currentStepIndex];

  return (
    <div 
      ref={containerRef}
      className="relative flex items-center justify-center w-full h-full overflow-auto p-4"
    >
      <div 
        className="relative shadow-2xl overflow-hidden rounded-md border border-slate-700/50 bg-black"
        style={{
          width: dimensions.width || 'auto',
          height: dimensions.height || 'auto',
          // Simple scale to fit screen if large
          transform: `scale(${Math.min(1, Math.min(600 / (dimensions.width || 1), 600 / (dimensions.height || 1)))})`,
          transformOrigin: 'center'
        }}
      >
        <canvas 
          ref={canvasRef} 
          className="block"
        />

        {currentTrace && currentTrace.block && (
          <motion.div
             className="absolute bg-white/30 border-2 border-fuchsia-400 pointer-events-none"
             initial={false}
             animate={{
                left: Math.min(...currentTrace.block.map(b => b[0])) * codelSize,
                top: Math.min(...currentTrace.block.map(b => b[1])) * codelSize,
                width: (Math.max(...currentTrace.block.map(b => b[0])) - Math.min(...currentTrace.block.map(b => b[0])) + 1) * codelSize,
                height: (Math.max(...currentTrace.block.map(b => b[1])) - Math.min(...currentTrace.block.map(b => b[1])) + 1) * codelSize,
             }}
             transition={{ type: "spring", stiffness: 300, damping: 30 }}
          />
        )}
      </div>

      <div className="absolute bottom-4 left-4 bg-slate-900/80 backdrop-blur border border-slate-700 p-3 rounded-xl flex gap-4 text-xs font-mono">
         <div>DP: {currentTrace ? ['RIGHT','DOWN','LEFT','UP'][currentTrace.dp] : '-'}</div>
         <div>CC: {currentTrace ? ['LEFT','RIGHT'][currentTrace.cc] : '-'}</div>
      </div>
    </div>
  );
}

export default CanvasVisualizer;
