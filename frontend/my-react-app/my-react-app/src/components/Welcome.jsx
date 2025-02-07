import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Welcome = () => {
  const navigate = useNavigate();

  const handleCam = (e) => {
    e.preventDefault();
    try {
      navigate("/webcam");
    } catch (err) {
      console.error("Navigation error:", err);
    }
  };

  const handleUpload = (e) => {
    e.preventDefault();
    try {
      navigate("/upload");
    } catch (err) {
      console.error("Navigation error:", err);
    }
  };

  return (
    <div className="container mt-5">
      {/* Header */}
      <header className="text-center mb-4">
        <h1 className="display-4">Welcome to Student Fine App</h1>
      </header>

      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light rounded mb-4">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            Student Fine App
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link active" aria-current="page" to="/">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/students">
                  Student Details
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/upload">
                  Upload
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/webcam">
                  Webcam
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Buttons */}
      <div className="d-flex justify-content-center">
        <button className="btn btn-primary mx-2" onClick={handleCam}>
          Webcam
        </button>
        <button className="btn btn-secondary mx-2" onClick={handleUpload}>
          Upload
        </button>
      </div>
    </div>
  );
};

export default Welcome;
