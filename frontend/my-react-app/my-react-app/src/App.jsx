import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./routes/Home";
import StudentDetail from "./routes/StudentDetail";
import Upload from "./routes/Upload";
import Webcam from "./routes/Webcam";

const App = () => {
  return (
    <div className="container">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/students" element={<StudentDetail />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/webcam" element={<Webcam />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
