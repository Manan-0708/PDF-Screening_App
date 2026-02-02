"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { UploadResume } from "../components/upload-resume";
import { ResumeInsights } from "../components/resume-insights";
import { JobRecommendations } from "../components/job-recommendations";
import { ThemeToggle } from "../components/theme-toggle";
import { Footer } from "../components/footer";

import {
  FileText,
  Sparkles,
  ArrowLeft,
  Download
} from "lucide-react";

export default function Home() {
  const [filename, setFilename] = useState<string | null>(null);

  const handleUploadSuccess = (uploadedFilename: string) => {
    setFilename(uploadedFilename);
  };

  const handleReset = () => {
    setFilename(null);
  };

  return (
    <main className="min-h-screen bg-background text-foreground">

      {/* ================= HEADER ================= */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between">

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
                <FileText className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-lg font-semibold">Resume Intelligence</h1>
                <p className="text-xs text-muted-foreground">
                  AI-Powered Resume Analysis
                </p>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-3">
              <ThemeToggle />

              {filename && (
                <motion.button
                  onClick={handleReset}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  className="flex items-center gap-2 px-4 py-2 text-sm rounded-lg
                             text-muted-foreground hover:text-foreground
                             hover:bg-muted transition"
                >
                  <ArrowLeft className="w-4 h-4" />
                  Upload New Resume
                </motion.button>
              )}
            </div>

          </div>
        </div>
      </motion.header>

      {/* ================= MAIN ================= */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <AnimatePresence mode="wait">

          {!filename ? (
            /* ================= UPLOAD VIEW ================= */
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, y: -20 }}
              className="py-12"
            >
              {/* Hero */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-12"
              >
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="inline-flex items-center gap-2 px-4 py-2
                             rounded-full bg-primary/10 text-primary
                             text-sm font-medium mb-6"
                >
                  <Sparkles className="w-4 h-4" />
                  Powered by AI
                </motion.div>

                <h2 className="text-3xl sm:text-4xl font-bold mb-4">
                  Get AI-Powered Resume Insights
                </h2>

                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Upload your resume to receive deep analysis, strengths,
                  improvement areas, and realistic job matches.
                </p>
              </motion.div>

              <UploadResume onUploadSuccess={handleUploadSuccess} />

              {/* Features */}
              <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6">
                {[
                  {
                    title: "Resume Analysis",
                    description: "Structured scoring across core technical areas",
                  },
                  {
                    title: "AI Insights",
                    description: "Clear strengths and improvement suggestions",
                  },
                  {
                    title: "Job Matching",
                    description: "Skill-based role recommendations",
                  },
                ].map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + index * 0.1 }}
                    className="text-center p-6 rounded-2xl bg-card border border-border"
                    whileHover={{ y: -4 }}
                  >
                    <h3 className="font-semibold mb-2">{feature.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ) : (
            /* ================= RESULTS VIEW ================= */
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-12 py-8"
            >
              {/* Resume Insights */}
              <ResumeInsights filename={filename} />

              {/* Download PDF */}
              <div className="flex justify-center">
                <motion.a
                  href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/download-analysis/${filename}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.97 }}
                  className="inline-flex items-center gap-2 px-6 py-3
                             rounded-xl bg-primary text-primary-foreground
                             font-medium shadow hover:shadow-md transition"
                >
                  <Download className="w-5 h-5" />
                  Download Resume Analysis (PDF)
                </motion.a>
              </div>

              {/* Divider */}
              <div className="flex items-center gap-4">
                <div className="flex-1 h-px bg-border" />
                <span className="text-sm text-muted-foreground">
                  Job Recommendations
                </span>
                <div className="flex-1 h-px bg-border" />
              </div>

              {/* Job Recommendations */}
              <JobRecommendations filename={filename} />
            </motion.div>
          )}

        </AnimatePresence>
      </div>

      {/* ================= FOOTER ================= */}
      <Footer />
    </main>
  );
}
