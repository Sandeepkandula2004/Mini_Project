import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
const WebcamCapture = () => {
  const [streaming, setStreaming] = useState(false);

  useEffect(() => {
    const processedVideo = document.getElementById("processed-video");
    if (streaming && processedVideo) {
      processedVideo.src = "http://localhost:5000/video_feed";
    } else if (processedVideo) {
      processedVideo.src = "";
    }
  }, [streaming]);

  const stopStreaming = async () => {
    setStreaming(false);
    try {
      await fetch("http://localhost:5000/api/stop_stream", { method: "POST" });
    } catch (error) {
      console.error("Error stopping stream:", error);
    }
  };

  return (
    <div>
      <h2>Processed Video Feed</h2>
      <button onClick={() => (streaming ? stopStreaming() : setStreaming(true))}>
        {streaming ? "Stop Streaming" : "Start Streaming"}
      </button>
      <br />
      {streaming && (
        <img id="processed-video" alt="Live video stream" width={640} height={480} />
      )}
    </div>
  );
};

export default WebcamCapture;