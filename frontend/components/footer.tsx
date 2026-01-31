"use client";

import { motion } from "framer-motion";
import { Github, Linkedin, Instagram, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border mt-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">

          {/* Left Text */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-sm text-muted-foreground flex items-center gap-1"
          >
            Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> by
            <span className="font-medium text-foreground ml-1">
              Manan
            </span>
          </motion.p>

          {/* Social Links */}
          <div className="flex items-center gap-5">
            <motion.a
              href="https://github.com/Manan-0708"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.15 }}
              whileTap={{ scale: 0.95 }}
              className="text-muted-foreground hover:text-foreground transition"
            >
              <Github className="w-5 h-5" />
            </motion.a>

            <motion.a
              href="https://www.linkedin.com/in/manan-shukla-18b234299"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.15 }}
              whileTap={{ scale: 0.95 }}
              className="text-muted-foreground hover:text-blue-500 transition"
            >
              <Linkedin className="w-5 h-5" />
            </motion.a>

            <motion.a
              href="https://www.instagram.com/manan_0708/"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.15 }}
              whileTap={{ scale: 0.95 }}
              className="text-muted-foreground hover:text-pink-500 transition"
            >
              <Instagram className="w-5 h-5" />
            </motion.a>
          </div>

        </div>

        {/* Bottom Line */}
        <p className="text-center text-xs text-muted-foreground mt-6">
          Resume Intelligence & Job Recommendation System
        </p>
      </div>
    </footer>
  );
}
