"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Brain,
  TrendingUp,
  TrendingDown,
  User,
  MessageSquare,
  Loader2,
} from "lucide-react";

import { extractText, ResumeInsights as ResumeInsightsType } from "../lib/api";

interface ResumeInsightsProps {
  filename: string;
}

export function ResumeInsights({ filename }: ResumeInsightsProps) {
  const [insights, setInsights] = useState<ResumeInsightsType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadInsights = async () => {
      try {
        const data = await extractText(filename);
        setInsights(data);
      } catch (err) {
        setError("Failed to load resume insights");
      } finally {
        setLoading(false);
      }
    };

    loadInsights();
  }, [filename]);

  if (loading) {
    return (
      <div className="flex flex-col items-center py-16">
        <Loader2 className="w-10 h-10 animate-spin text-primary" />
        <p className="mt-4 text-muted-foreground">
          Analyzing your resume...
        </p>
      </div>
    );
  }

  if (error || !insights) {
    return (
      <div className="text-center py-16 text-destructive">
        {error ?? "No insights available"}
      </div>
    );
  }

  const getColor = (score: number) => {
    if (score >= 70) return "bg-green-500";
    if (score >= 40) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-primary/10 mb-3">
          <Brain className="w-7 h-7 text-primary" />
        </div>
        <h2 className="text-2xl font-semibold">Resume Analysis</h2>
        <p className="text-muted-foreground">
          AI-powered insights about your resume
        </p>
      </div>

      {/* Overall Score */}
      <div className="bg-card border rounded-2xl p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium">Overall Score</h3>
          <span className="text-3xl font-bold">{insights.score}/100</span>
        </div>
        <div className="h-3 bg-muted rounded-full overflow-hidden">
          <div
            className={`h-full ${getColor(insights.score)}`}
            style={{ width: `${insights.score}%` }}
          />
        </div>
      </div>

      {/* Screening Breakdown */}
      <div className="bg-card border rounded-2xl p-6">
        <h3 className="text-lg font-medium mb-4">
          Screening Breakdown
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Object.entries(insights.screening_breakdown ?? {}).map(
            ([category, value]) => (
              <div
                key={category}
                className="bg-muted/50 rounded-xl p-4"
              >
                <p className="font-medium capitalize mb-2">
                  {category.replace("_", " ")}
                </p>

                <div className="flex items-center gap-3">
                  <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className={`h-full ${getColor(value)}`}
                      style={{ width: `${value}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {value}%
                  </span>
                </div>
              </div>
            )
          )}
        </div>
      </div>

      {/* AI Insights */}
      <div className="bg-card border rounded-2xl p-6 space-y-6">
        <h3 className="text-lg font-medium">AI Insights</h3>

        {/* Summary */}
        <div className="p-4 bg-primary/5 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <User className="w-5 h-5 text-primary" />
            <span className="font-medium">Profile Summary</span>
          </div>
          <p className="text-muted-foreground">
            {insights.ai_insights.profile_summary}
          </p>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-green-500/5 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span className="font-medium">Strengths</span>
            </div>
            <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
              {insights.ai_insights.strengths.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          <div className="p-4 bg-orange-500/5 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <TrendingDown className="w-5 h-5 text-orange-500" />
              <span className="font-medium">Areas to Improve</span>
            </div>
            <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
              {insights.ai_insights.weaknesses.map((w, i) => (
                <li key={i}>{w}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Chatbot Feedback */}
      <div className="bg-card border rounded-2xl p-6">
        <div className="flex items-center gap-2 mb-3">
          <MessageSquare className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-medium">AI Feedback</h3>
        </div>
        <p className="text-muted-foreground whitespace-pre-line">
          {insights.chatbot_feedback}
        </p>
      </div>
    </div>
  );
}
