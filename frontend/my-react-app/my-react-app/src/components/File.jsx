import React, { useState } from "react";
import axios from "axios";

const File = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [detectedFaces, setDetectedFaces] = useState([]);
  const [uploading, setUploading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith("video/")) {
      setVideoFile(file);
      setPreviewUrl(URL.createObjectURL(file)); // Generate preview URL
    } else {
      alert("Please upload a valid video file.");
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!videoFile) {
      alert("No video file selected.");
      return;
    }
    
    setUploading(true);
    const formData = new FormData();
    formData.append("video", videoFile);
    
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/upload_video", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDetectedFaces(response.data.detected_faces);
      alert("Video processed successfully!");
    } catch (error) {
      alert("Error uploading video: " + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Upload Video File</h2>
      <div className="mb-3">
        <label htmlFor="videoInput" className="form-label">Select Video File:</label>
        <input
          type="file"
          className="form-control"
          id="videoInput"
          accept="video/*"
          onChange={handleFileChange}
        />
      </div>
      {previewUrl && (
        <div className="mt-3">
          <h5>Video Preview:</h5>
          <video src={previewUrl} controls style={{ width: "100%", maxHeight: "400px" }} />
        </div>
      )}
      <button className="btn btn-primary mt-3" onClick={handleUpload} disabled={!videoFile || uploading}>
        {uploading ? "Uploading..." : "Upload Video"}
      </button>
      {detectedFaces.length > 0 && (
        <div className="mt-4">
          <h5>Detected Face IDs:</h5>
          <ul>
            {detectedFaces.map((id, index) => (
              <li key={index}>{id}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default File;
