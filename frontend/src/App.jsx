import React, { useState } from 'react';
import axios from 'axios';
import UploadArea from './components/UploadArea';
import ControlPanel from './components/ControlPanel';
import { Download, AlertCircle, CheckCircle } from 'lucide-react';

// Read API base from Vite environment variable
const API_BASE = import.meta.env.VITE_API_BASE;

// Extract origin only (removes trailing /api if present)
const API_ORIGIN = API_BASE.replace(/\/api$/, '');

function App() {
  const [file, setFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState(null);
  const [mode, setMode] = useState('double');
  const [startPage, setStartPage] = useState(1);
  const [endPage, setEndPage] = useState(0);
  const [password, setPassword] = useState('');
  const [reverseOrder, setReverseOrder] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [downloadLinks, setDownloadLinks] = useState([]);
  const [error, setError] = useState(null);

  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    setDownloadLinks([]);
    setError(null);
    setUploadedFilename(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setUploadedFilename(res.data.filename);
    } catch (err) {
      console.error(err);
      setError('Failed to upload file.');
    }
  };

  const handleProcess = async () => {
    if (!uploadedFilename) return;

    setIsProcessing(true);
    setError(null);
    setDownloadLinks([]);

    try {
      const res = await axios.post(`${API_BASE}/process`, {
        filename: uploadedFilename,
        original_filename: file.name,
        mode,
        start_page: startPage,
        end_page: endPage,
        password: password,
        reverse_order: reverseOrder
      });

      setDownloadLinks(res.data.files);
    } catch (err) {
      console.error(err);
      setError('Processing failed. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen pb-20">
      <header className="mb-12 pt-8">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-2">
          DoubleSide
        </h1>
        <p className="text-gray-400">
          Advanced printing tools for single-sided printers
        </p>
      </header>

      <main className="max-w-4xl mx-auto">
        <UploadArea onFileSelect={handleFileSelect} selectedFile={file} />

        {file && (
          <ControlPanel
            mode={mode}
            setMode={setMode}
            startPage={startPage}
            setStartPage={setStartPage}
            endPage={endPage}
            setEndPage={setEndPage}
            password={password}
            setPassword={setPassword}
            reverseOrder={reverseOrder}
            setReverseOrder={setReverseOrder}
            onProcess={handleProcess}
            isProcessing={isProcessing}
            disabled={!uploadedFilename}
          />
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-3 text-red-200 animate-fade-in">
            <AlertCircle size={24} />
            <span>{error}</span>
          </div>
        )}

        {downloadLinks.length > 0 && (
          <div className="mt-8 glass-panel animate-fade-in">
            <div className="flex items-center gap-2 mb-6 text-green-400">
              <CheckCircle size={24} />
              <h2 className="text-xl font-bold">
                Processing Complete!
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {downloadLinks.map((linkObj, index) => {
                const url =
                  typeof linkObj === 'string'
                    ? linkObj
                    : linkObj.url;

                const name =
                  typeof linkObj === 'string'
                    ? linkObj.split('/').pop()
                    : linkObj.name;

                return (
                  <a
                    key={index}
                    href={`${API_ORIGIN}${url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg border border-slate-700 hover:bg-slate-800 hover:border-blue-500 transition-all group"
                  >
                    <span className="font-mono text-sm truncate mr-4">
                      {name}
                    </span>
                    <Download
                      size={20}
                      className="text-blue-400 group-hover:scale-110 transition-transform"
                    />
                  </a>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
