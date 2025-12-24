import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText } from 'lucide-react';

const UploadArea = ({ onFileSelect, selectedFile }) => {
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles?.length > 0) {
            onFileSelect(acceptedFiles[0]);
        }
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        multiple: false
    });

    return (
        <div
            {...getRootProps()}
            className={`glass-panel cursor-pointer transition-all duration-300 border-2 border-dashed 
        ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-gray-600 hover:border-gray-400'}
        ${selectedFile ? 'border-green-500/50' : ''}
      `}
            style={{ minHeight: '200px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}
        >
            <input {...getInputProps()} />

            {selectedFile ? (
                <div className="text-center animate-fade-in">
                    <FileText size={48} className="mx-auto text-green-400 mb-4" />
                    <p className="text-xl font-semibold text-green-400">{selectedFile.name}</p>
                    <p className="text-sm text-gray-400 mt-2">Click or drag to replace</p>
                </div>
            ) : (
                <div className="text-center">
                    <UploadCloud size={48} className={`mx-auto mb-4 ${isDragActive ? 'text-blue-400' : 'text-gray-400'}`} />
                    {isDragActive ? (
                        <p className="text-xl text-blue-400">Drop the PDF here...</p>
                    ) : (
                        <>
                            <p className="text-xl font-semibold mb-2">Drag & drop your PDF here</p>
                            <p className="text-sm text-gray-400">or click to select file</p>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default UploadArea;
