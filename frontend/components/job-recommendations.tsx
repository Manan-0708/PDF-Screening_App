"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { 
  Briefcase, 
  Check, 
  X, 
  Sparkles,
  Loader2,
  TrendingUp
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
    transition: { duration: 0.5, ease: "easeOut" }
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
      } catch (err) {
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
        <p className="mt-4 text-muted-foreground">Finding matching jobs...</p>
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
        <h2 className="text-2xl font-semibold text-foreground">Job Recommendations</h2>
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
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-foreground leading-tight">
                  {job.job_title}
                </h3>
              </div>
              <div className={`px-3 py-1.5 rounded-full border ${getMatchBgColor(job.match_score)}`}>
                <div className="flex items-center gap-1.5">
                  <TrendingUp className={`w-4 h-4 ${getMatchColor(job.match_score)}`} />
                  <span className={`text-sm font-semibold ${getMatchColor(job.match_score)}`}>
                    {job.match_score}%
                  </span>
                </div>
              </div>
            </div>

            {/* Match Progress */}
            <div className="mb-4">
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${job.match_score}%` }}
                  transition={{ duration: 0.8, delay: 0.3 + index * 0.1 }}
                  className={`h-full rounded-full ${
                    job.match_score >= 80 ? "bg-green-500" :
                    job.match_score >= 60 ? "bg-yellow-500" : "bg-orange-500"
                  }`}
                />
              </div>
            </div>

            {/* Skills */}
            <div className="space-y-3 mb-4">
              {/* Matched Skills */}
              {job.matched_skills.length > 0 && (
                <div>
                  <div className="flex items-center gap-1.5 mb-2">
                    <Check className="w-4 h-4 text-green-500" />
                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                      Matched Skills
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {job.matched_skills.map((skill, idx) => (
                      <motion.span
                        key={idx}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.4 + idx * 0.05 }}
                        className="px-2.5 py-1 text-xs font-medium bg-green-500/10 text-green-600 rounded-md border border-green-500/20"
                      >
                        {skill}
                      </motion.span>
                    ))}
                  </div>
                </div>
              )}

              {/* Missing Skills */}
              {job.missing_skills.length > 0 && (
                <div>
                  <div className="flex items-center gap-1.5 mb-2">
                    <X className="w-4 h-4 text-orange-500" />
                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                      Skills to Develop
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {job.missing_skills.map((skill, idx) => (
                      <motion.span
                        key={idx}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5 + idx * 0.05 }}
                        className="px-2.5 py-1 text-xs font-medium bg-orange-500/10 text-orange-600 rounded-md border border-orange-500/20"
                      >
                        {skill}
                      </motion.span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* AI Insights */}
            <div className="pt-4 border-t border-border">
              <div className="flex items-center gap-1.5 mb-2">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                  AI Job Insights
                </span>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {job.ai_job_insights}
              </p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {jobs.length === 0 && !isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12 bg-card rounded-2xl border border-border"
        >
          <Briefcase className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <p className="text-muted-foreground">No job recommendations found</p>
        </motion.div>
      )}
    </div>
  );
}
