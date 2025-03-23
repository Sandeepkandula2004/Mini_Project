import React, { useState } from "react";
import { Link } from "react-router-dom";

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [detectedFaces, setDetectedFaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setProcessedImage(null);
    setDetectedFaces([]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      setError("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedImage);

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/api/process", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Something went wrong!");
      }

      setDetectedFaces(data.detected_face_ids || []);
      setProcessedImage(`http://localhost:5000/${data.processed_image}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Navbar */}
      <nav className="bg-gray-800 p-4 text-white">
        <div className="container mx-auto flex justify-between">
          <h1 className="text-xl font-semibold">Face Detection</h1>
          <div>
            <Link to="/" className="px-4 hover:underline">
              Home
            </Link>
            <Link to="/students" className="px-4 hover:underline">
              Students
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="p-4 max-w-lg mx-auto">
        <h2 className="text-2xl font-semibold mb-4 text-center">
          Upload Image for Processing
        </h2>

        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="mb-2 block w-full text-center"
        />

        {selectedImage && (
          <div className="my-4 text-center">
            <h3 className="text-lg font-semibold mb-2">Selected Image:</h3>
            <img
              src={URL.createObjectURL(selectedImage)}
              alt="Selected"
              className="w-auto max-w-full h-auto object-cover rounded border mx-auto"
            />
          </div>
        )}

        <button
          onClick={handleUpload}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 block w-full"
          disabled={loading}
        >
          {loading ? "Processing..." : "Upload & Detect"}
        </button>

        {error && <p className="text-red-500 mt-2 text-center">{error}</p>}

        {detectedFaces.length > 0 && (
          <div className="mt-4 p-2 border rounded text-center">
            <h3 className="text-lg font-semibold">Detected Face IDs:</h3>
            <ul className="list-disc pl-4 inline-block text-left">
              {detectedFaces.map((id, index) => (
                <li key={index}>{id}</li>
              ))}
            </ul>
          </div>
        )}

        {processedImage && (
          <div className="mt-4 text-center">
            <h3 className="text-lg font-semibold mb-2">Processed Image:</h3>
            <img
              src={processedImage}
              alt="Processed"
              className="w-auto max-w-full h-auto object-cover rounded border mx-auto"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
