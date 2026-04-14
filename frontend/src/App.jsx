import { useState, useRef } from 'react';
import { Play, RotateCcw, Upload, Image as ImageIcon, Settings } from 'lucide-react';
import CanvasVisualizer from './components/CanvasVisualizer';
import OutputPanel from './components/OutputPanel';

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [codelSize, setCodelSize] = useState(1);
  const [executionData, setExecutionData] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const fileInputRef = useRef(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setImageSrc(e.target.result);
      reader.readAsDataURL(file);
      setExecutionData(null);
      setCurrentStepIndex(0);
    }
  };

  const handleRun = async () => {
    if (!imageSrc || !fileInputRef.current?.files[0]) return;
    
    setIsRunning(true);
    setCurrentStepIndex(0);
    
    const formData = new FormData();
    formData.append('file', fileInputRef.current.files[0]);
    formData.append('codel_size', codelSize);

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/run`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.status === 'success') {
        setExecutionData(data);
      } else {
        console.error("Execution failed", data);
      }
    } catch (error) {
      console.error("Failed to run piet program", error);
    }
    
    setIsRunning(false);
  };

  const handleReset = () => {
    setCurrentStepIndex(0);
  };

  const currentTrace = executionData?.trace?.[currentStepIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white font-sans overflow-hidden">
      <header className="px-8 py-5 border-b border-indigo-500/30 bg-black/20 backdrop-blur-md flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-pink-500 via-purple-400 to-indigo-400">
            Piet Image Compiler
          </h1>
          <p className="text-sm text-slate-400 mt-1">Abstract Art to Executable Code</p>
        </div>
      </header>

      <main className="p-8 grid grid-cols-1 lg:grid-cols-12 gap-8 h-[calc(100vh-100px)]">
        
        {/* Left Panel: Controls & Visualizer */}
        <div className="lg:col-span-8 flex flex-col gap-6 h-full">
          {/* Controls Bar */}
          <div className="flex flex-wrap items-center gap-4 bg-slate-800/50 p-4 rounded-2xl border border-indigo-500/20 backdrop-blur-sm shadow-xl">
            <button 
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 transition-colors rounded-xl font-medium"
            >
              <Upload size={18} /> Upload Image
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleImageUpload} 
              accept="image/png, image/jpeg, image/gif" 
              className="hidden" 
            />

            <div className="flex items-center gap-3 ml-auto text-sm font-medium">
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-900/50 rounded-xl border border-slate-700">
                <Settings size={16} className="text-slate-400" />
                <span className="text-slate-300">Codel Size:</span>
                <input 
                  type="number" 
                  min="1" 
                  value={codelSize} 
                  onChange={(e) => setCodelSize(parseInt(e.target.value) || 1)}
                  className="w-16 bg-transparent border-none outline-none text-right font-mono"
                />
              </div>

              <button 
                onClick={handleRun}
                disabled={!imageSrc || isRunning}
                className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-400 hover:to-purple-400 disabled:opacity-50 transition-all shadow-lg shadow-purple-500/20 rounded-xl"
              >
                <Play size={18} /> {isRunning ? 'Compiling...' : 'Execute'}
              </button>

              <button 
                onClick={handleReset}
                disabled={!executionData}
                className="flex items-center gap-2 px-4 py-2.5 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 transition-colors rounded-xl"
              >
                <RotateCcw size={18} /> Reset
              </button>
            </div>
          </div>

          {/* Visualizer Canvas */}
          <div className="flex-1 bg-slate-900/40 rounded-3xl border border-indigo-500/30 overflow-hidden relative shadow-2xl backdrop-blur-sm flex items-center justify-center p-4">
            {imageSrc ? (
              <CanvasVisualizer 
                imageSrc={imageSrc} 
                trace={executionData?.trace} 
                currentStepIndex={currentStepIndex}
                onStepChange={setCurrentStepIndex}
                codelSize={codelSize}
              />
            ) : (
              <div className="flex flex-col items-center gap-4 text-slate-500">
                <ImageIcon size={64} className="opacity-20" />
                <p>Upload a Piet program to visualize execution</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel: Output & Trace */}
        <div className="lg:col-span-4 h-full">
          <OutputPanel 
             output={executionData?.output} 
             trace={executionData?.trace}
             currentStep={currentTrace}
          />
        </div>
      </main>
    </div>
  );
}

export default App;
