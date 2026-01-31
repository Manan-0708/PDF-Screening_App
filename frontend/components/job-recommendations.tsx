"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Briefcase,
  Sparkles,
  Loader2,
  TrendingUp,
} from "lucide-react";
import { getJobRecommendations, JobRecommendation } from "../lib/api";

interface JobRecommendationsProps {
  filename: string;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5, // ✅ no ease → fully type-safe
    },
  },
};

export function JobRecommendations({ filename }: JobRecommendationsProps) {
  const [jobs, setJobs] = useState<JobRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const data = await getJobRecommendations(filename);
        setJobs(data);
      } catch {
        setError("Failed to load job recommendations");
      } finally {
        setIsLoading(false);
      }
    };

    fetchJobs();
  }, [filename]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-10 h-10 animate-spin text-primary" />
        <p className="mt-4 text-muted-foreground">
          Finding matching jobs...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center py-16"
      >
        <p className="text-destructive">{error}</p>
      </motion.div>
    );
  }

  const getMatchColor = (score: number) => {
    if (score >= 80) return "text-green-500";
    if (score >= 60) return "text-yellow-500";
    return "text-orange-500";
  };

  const getMatchBgColor = (score: number) => {
    if (score >= 80) return "bg-green-500/10 border-green-500/20";
    if (score >= 60) return "bg-yellow-500/10 border-yellow-500/20";
    return "bg-orange-500/10 border-orange-500/20";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-primary/10 mb-3">
          <Briefcase className="w-7 h-7 text-primary" />
        </div>
        <h2 className="text-2xl font-semibold">
          Job Recommendations
        </h2>
        <p className="text-muted-foreground mt-1">
          {jobs.length} jobs matched based on your resume
        </p>
      </motion.div>

      {/* Job Cards */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 lg:grid-cols-2 gap-4"
      >
        {jobs.map((job, index) => (
          <motion.div
            key={index}
            variants={cardVariants}
            whileHover={{ scale: 1.02, y: -4 }}
            transition={{ duration: 0.2 }}
            className="bg-card rounded-2xl border border-border p-6 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          >
            {/* Job Header */}
            <div className="flex items-start justify-between gap-4 mb-4">
              <h3 className="text-lg font-semibold">
                {job.job_title}
              </h3>

              <div
                className={`px-3 py-1.5 rounded-full border ${getMatchBgColor(
                  job.match_score
                )}`}
              >
                <div className="flex items-center gap-1.5">
                  <TrendingUp
                    className={`w-4 h-4 ${getMatchColor(
                      job.match_score
                    )}`}
                  />
                  <span
                    className={`text-sm font-semibold ${getMatchColor(
                      job.match_score
                    )}`}
                  >
                    {job.match_score}%
                  </span>
                </div>
              </div>
            </div>

            {/* Progress */}
            <div className="mb-4">
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${job.match_score}%` }}
                  transition={{
                    duration: 0.8,
                    delay: 0.3 + index * 0.1,
                  }}
                  className={`h-full rounded-full ${
                    job.match_score >= 80
                      ? "bg-green-500"
                      : job.match_score >= 60
                      ? "bg-yellow-500"
                      : "bg-orange-500"
                  }`}
                />
              </div>
            </div>

            {/* AI Insights */}
            <div className="pt-4 border-t border-border">
              <div className="flex items-center gap-1.5 mb-2">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-xs uppercase tracking-wide text-muted-foreground">
                  AI Job Insights
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                {job.ai_job_insights}
              </p>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
