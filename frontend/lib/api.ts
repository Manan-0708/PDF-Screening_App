const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!BASE_URL) {
  throw new Error("NEXT_PUBLIC_API_BASE_URL is not defined");
}

/* ------------ API CALLS ------------ */

export async function uploadResume(
  file: File
): Promise<{ filename: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to upload resume");
  }

  return response.json();
}

export async function extractText(filename: string) {
  const response = await fetch(`${BASE_URL}/extract-text/${filename}`);

  if (!response.ok) {
    throw new Error("Failed to extract resume");
  }

  return response.json();
}

export async function getJobRecommendations(filename: string) {
  const response = await fetch(`${BASE_URL}/recommend-jobs/${filename}`);

  if (!response.ok) {
    throw new Error("Failed to get job recommendations");
  }

  const data = await response.json();
  return data.job_recommendations;
}
