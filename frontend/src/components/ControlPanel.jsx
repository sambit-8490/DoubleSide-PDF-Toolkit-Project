import React from 'react';
import { Settings, BookOpen, Layers, Scissors, Unlock, Lock } from 'lucide-react';

const ControlPanel = ({ mode, setMode, startPage, setStartPage, endPage, setEndPage, onProcess, isProcessing, disabled, password, setPassword, reverseOrder, setReverseOrder }) => {

    const modes = [
        { id: 'double', label: 'Double Sided', icon: Layers, desc: 'Split into Odd/Even for manual duplex' },
        { id: 'four', label: '2-in-1 (N-up)', icon: BookOpen, desc: 'Place 2 pages on 1 sheet (A4 Landscape)' },
        { id: 'book', label: 'Booklet', icon: BookOpen, desc: 'Arrange pages for folding into a booklet' },
        { id: 'split', label: 'Split / Extract', icon: Scissors, desc: 'Extract a range of pages' },
        { id: 'decrypt', label: 'Decrypt', icon: Unlock, desc: 'Remove password protection' },
        { id: 'encrypt', label: 'Encrypt', icon: Lock, desc: 'Add password protection' }
    ];

    const showPageRange = ['double', 'four', 'split', 'book'].includes(mode);
    const showPassword = ['decrypt', 'encrypt'].includes(mode);
    const showReverse = ['double', 'four', 'book'].includes(mode);

    return (
        <div className="glass-panel mt-8 text-left animate-fade-in">
            <div className="flex items-center gap-2 mb-6">
                <Settings className="text-blue-400" />
                <h2 className="text-xl font-bold">Configuration</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                {modes.map((m) => {
                    const Icon = m.icon;
                    const isSelected = mode === m.id;
                    return (
                        <div
                            key={m.id}
                            onClick={() => setMode(m.id)}
                            className={`p-4 rounded-lg border cursor-pointer transition-all duration-200
                ${isSelected
                                    ? 'bg-blue-600/20 border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.3)]'
                                    : 'bg-slate-800/50 border-slate-700 hover:border-slate-500 hover:bg-slate-800'
                                }
              `}
                        >
                            <div className="flex items-center gap-3 mb-2">
                                <Icon size={20} className={isSelected ? 'text-blue-400' : 'text-gray-400'} />
                                <span className={`font-semibold ${isSelected ? 'text-white' : 'text-gray-300'}`}>{m.label}</span>
                            </div>
                            <p className="text-xs text-gray-400">{m.desc}</p>
                        </div>
                    );
                })}
            </div>

            {showPageRange && (
                <div className="flex flex-wrap gap-6 mb-8 p-4 bg-slate-900/30 rounded-lg border border-slate-800">
                    <div className="flex flex-col gap-2">
                        <label className="text-sm text-gray-400">Start Page</label>
                        <input
                            type="number"
                            min="1"
                            value={startPage}
                            onChange={(e) => setStartPage(parseInt(e.target.value) || 1)}
                            className="w-32 bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors"
                        />
                    </div>
                    <div className="flex flex-col gap-2">
                        <label className="text-sm text-gray-400">End Page (0 for all)</label>
                        <input
                            type="number"
                            min="0"
                            value={endPage}
                            onChange={(e) => setEndPage(parseInt(e.target.value) || 0)}
                            className="w-32 bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors"
                        />
                    </div>
                </div>
            )}

            {showReverse && (
                <div className="mb-8 animate-fade-in">
                    <label className="flex items-center gap-3 cursor-pointer group">
                        <div className="relative">
                            <input
                                type="checkbox"
                                checked={reverseOrder}
                                onChange={(e) => setReverseOrder(e.target.checked)}
                                className="sr-only peer"
                            />
                            <div className="w-10 h-6 bg-slate-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </div>
                        <span className="text-gray-300 group-hover:text-white transition-colors">Upside Down Printer (Face-Up Output)</span>
                    </label>
                    <p className="text-xs text-gray-500 mt-2 ml-13">Check this if your printer outputs pages face-up (e.g., most inkjets).</p>
                </div>
            )}

            {showPassword && (
                <div className="mb-8 animate-fade-in">
                    <label className="block text-sm font-medium text-gray-400 mb-2">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder={mode === 'encrypt' ? 'Set a password' : 'Enter PDF password'}
                        className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors"
                    />
                </div>
            )}

            <button
                onClick={onProcess}
                disabled={disabled || isProcessing}
                className="w-full btn-primary py-4 text-lg flex items-center justify-center gap-2"
            >
                {isProcessing ? (
                    <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Processing...
                    </>
                ) : (
                    <>
                        <span>Start Processing</span>
                    </>
                )}
            </button>
        </div>
    );
};

export default ControlPanel;
