import React, { useState, useEffect, useRef } from 'react';
import { Terminal, ShieldAlert, Send, ShieldCheck, Flame, Cpu, Eye, Activity } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: "Core framework online. Standing by for operations." }
  ]);
  const [terminalLogs, setTerminalLogs] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const socketRef = useRef(null);
  const logEndRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket('ws://localhost:8000/ws/logs');

    socketRef.current.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      setTerminalLogs((prev) => [...prev, payload]);
    };

    return () => socketRef.current?.close();
  }, []);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [terminalLogs]);

  const handleExecute = async () => {
    if (!input.trim() || isLoading) return;
    const prompt = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: prompt }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { role: 'agent', content: data.reply }]);
    } catch (err) {
      setTerminalLogs((prev) => [...prev, { type: 'error', data: 'SYSTEM REJECTION: Backend interface unreachable.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen w-screen bg-[#050505] text-red-500 font-mono flex flex-col overflow-hidden select-none">
      <header className="border-b border-red-950 bg-[#0a0202] px-6 py-3 flex items-center justify-between shadow-2xl z-10">
        <div className="flex items-center gap-3">
          <Flame className="w-5 h-5 text-red-600 animate-pulse" />
          <h1 className="text-sm font-black tracking-[0.3em] text-red-600 uppercase">
            Threat Orchestration & Execution Hub
          </h1>
        </div>
        <div className="flex items-center gap-4 text-[10px] tracking-wider font-bold">
          <span className="flex items-center gap-1.5 text-emerald-500 bg-emerald-950/20 px-2 py-1 rounded border border-emerald-900/40">
            <Cpu className="w-3.5 h-3.5" /> CLAUDE CORE ONLINE
          </span>
          <span className="flex items-center gap-1.5 text-red-500 bg-red-950/20 px-2 py-1 rounded border border-red-900/40">
            <Activity className="w-3.5 h-3.5 animate-spin" /> ASYNC BROKER ACTIVE
          </span>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <section className="w-1/2 border-r border-red-950/60 flex flex-col bg-[#070202]">
          <div className="bg-[#0b0303] px-4 py-2 border-b border-red-950/40 text-[10px] text-red-700 tracking-widest uppercase flex items-center gap-2">
            <Eye className="w-3.5 h-3.5" /> Strategic Reasoning Stream
          </div>
          <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
            {messages.map((msg, i) => (
              <div key={i} className={`p-4 rounded border text-sm max-w-[90%] ${
                msg.role === 'user' ? 'bg-[#111] border-zinc-800 text-zinc-300 ml-auto' : 'bg-[#0e0404] border-red-950 text-red-400'
              }`}>
                <div className="text-[9px] uppercase tracking-widest font-black opacity-40 mb-1">
                  {msg.role === 'user' ? '// operator' : '// strategic engine'}
                </div>
                <p className="font-sans leading-relaxed tracking-wide">{msg.content}</p>
              </div>
            ))}
            {isLoading && (
              <div className="text-xs text-red-700 animate-pulse flex items-center gap-2 italic">
                <ShieldAlert className="w-4 h-4 animate-spin" /> Evaluating context rules...
              </div>
            )}
          </div>
        </section>

        <section className="w-1/2 flex flex-col bg-black">
          <div className="bg-[#090909] px-4 py-2 border-b border-zinc-900 text-[10px] text-zinc-500 tracking-widest uppercase flex items-center gap-2">
            <Terminal className="w-3.5 h-3.5 text-red-600" /> Live Terminal Pipeline Output
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-1 font-mono text-xs custom-scrollbar bg-[#020202]">
            {terminalLogs.map((log, i) => (
              <div key={i} className={
                log.type === 'error' ? 'text-rose-600 font-bold bg-rose-950/20 px-2 py-0.5 rounded' :
                log.type === 'system' ? 'text-amber-500 font-semibold italic' : 'text-zinc-400'
              }>
                {log.type === 'terminal' && <span className="text-zinc-700 select-none mr-2">$</span>}
                {log.data}
              </div>
            ))}
            <div ref={logEndRef} />
          </div>
        </section>
      </div>

      <footer className="p-4 bg-[#070202] border-t border-red-950">
        <div className="max-w-7xl mx-auto flex gap-3 relative items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleExecute()}
            placeholder="Issue directives to the autonomous framework..."
            className="flex-1 bg-black border border-red-950 text-red-500 px-4 py-3 rounded focus:outline-none focus:border-red-700 focus:ring-1 focus:ring-red-950 text-sm transition-all placeholder:text-red-950/60"
          />
          <button onClick={handleExecute} className="bg-red-950 border border-red-800 text-red-400 hover:bg-red-900 hover:text-black p-3 rounded transition-all">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;
