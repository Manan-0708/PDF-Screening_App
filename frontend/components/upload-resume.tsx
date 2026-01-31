"use client";

import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, FileText, Loader2, CheckCircle2 } from "lucide-react";
import { uploadResume } from "../lib/api";

interface UploadResumeProps {
  onUploadSuccess: (filename: string) => void;
}

export function UploadResume({ onUploadSuccess }: UploadResumeProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF file only");
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) return;

    if (droppedFile.type !== "application/pdf") {
      setError("Please upload a PDF file only");
      return;
    }

    setFile(droppedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(null);

    try {
      const result = await uploadResume(file);
      onUploadSuccess(result.filename);
    } catch {
      setError("Failed to upload resume. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-xl mx-auto"
    >
      {/* CARD */}
      <div className="
        bg-card
        rounded-2xl border border-border
        p-8 shadow-md
      ">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
            <FileText className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-2xl font-semibold">Upload Your Resume</h2>
          <p className="text-muted-foreground mt-2">
            Upload a PDF to get AI-powered insights & job matches
          </p>
        </div>

        {/* Drop Area */}
        <motion.div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragOver(true);
          }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
          className={`
            relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
            transition-colors duration-200
            ${
              isDragOver
                ? "border-primary bg-primary/5"
                : file
                ? "border-green-500 bg-green-500/5"
                : "border-border hover:border-primary/50 hover:bg-muted/40"
            }
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
          />

          {file ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center gap-3"
            >
              <CheckCircle2 className="w-10 h-10 text-green-500" />
              <div>
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-muted-foreground">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </motion.div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <Upload className="w-10 h-10 text-muted-foreground" />
              <div>
                <p className="font-medium">Drag & drop your resume here</p>
                <p className="text-sm text-muted-foreground">
                  or click to browse (PDF only)
                </p>
              </div>
            </div>
          )}
        </motion.div>

        {/* Error */}
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-destructive text-sm mt-4 text-center"
          >
            {error}
          </motion.p>
        )}

        {/* ✅ PRIMARY CTA (FIXED) */}
        <motion.button
          onClick={handleUpload}
          disabled={!file || isUploading}
          whileHover={file && !isUploading ? { scale: 1.04 } : {}}
          whileTap={file && !isUploading ? { scale: 0.97 } : {}}
          className={`
            w-full mt-6 py-3 px-6 rounded-xl font-semibold
            flex items-center justify-center gap-2
            transition-all duration-200
            ${
              !file || isUploading
                ? "bg-muted text-muted-foreground cursor-not-allowed"
                : "bg-primary/90 text-primary-foreground shadow-lg ring-1 ring-black/20 hover:bg-primary hover:shadow-xl"
            }
          `}
        >
          {isUploading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing Resume...
            </>
          ) : (
            <>
              <Upload className="w-5 h-5" />
              Analyze Resume
            </>
          )}
        </motion.button>
      </div>
    </motion.div>
  );
}
