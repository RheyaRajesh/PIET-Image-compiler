import { Terminal, Layers, Activity } from 'lucide-react';

function OutputPanel({ output, trace, currentStep }) {
  return (
    <div className="flex flex-col gap-6 h-full">
      {/* Operation Log */}
      <div className="bg-slate-800/50 rounded-2xl border border-indigo-500/20 backdrop-blur-sm p-5 flex flex-col gap-3 shadow-xl">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-indigo-300">
          <Activity size={20} /> Current Operation
        </h2>
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-700 min-h-[80px] flex items-center justify-center">
          {currentStep ? (
            <span className="text-xl font-mono relative">
               {currentStep.error ? (
                 <span className="text-red-400">{currentStep.error}</span>
               ) : (
                 <span className="text-green-400 font-bold tracking-wider">{currentStep.op || 'slide / pass'}</span>
               )}
            </span>
          ) : (
            <span className="text-slate-600 font-mono italic">Waiting for execution...</span>
          )}
        </div>
      </div>

      {/* Stack State */}
      <div className="bg-slate-800/50 rounded-2xl border border-indigo-500/20 backdrop-blur-sm p-5 flex flex-col gap-3 shadow-xl flex-1 max-h-[40%]">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-purple-300">
          <Layers size={20} /> Stack
        </h2>
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-700 flex-1 overflow-y-auto flex flex-col-reverse gap-1">
          {currentStep?.stack ? (
            currentStep.stack.map((val, i) => (
              <div key={i} className="bg-slate-800 px-3 py-2 border border-slate-600 rounded text-center font-mono text-purple-200">
                {val}
              </div>
            ))
          ) : (
            <span className="text-slate-600 font-mono italic text-center">Stack empty</span>
          )}
        </div>
      </div>

      {/* Standard Output */}
      <div className="bg-slate-800/50 rounded-2xl border border-indigo-500/20 backdrop-blur-sm p-5 flex flex-col gap-3 shadow-xl flex-1 max-h-[35%]">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-pink-300">
          <Terminal size={20} /> Console Output
        </h2>
        <div className="bg-black p-4 rounded-xl border border-slate-700 flex-1 overflow-y-auto font-mono text-sm whitespace-pre-wrap text-emerald-400">
          {output !== undefined ? output : <span className="text-slate-700 italic">No output yet</span>}
        </div>
      </div>
    </div>
  );
}

export default OutputPanel;
