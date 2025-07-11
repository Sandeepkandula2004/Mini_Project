import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StudentDetail from "./routes/StudentDetail";
import Upload from "./routes/Upload";
const App = () => {
  return (
    <div className="container">
      <Router>
        <Routes>
          <Route path="/students" element={<StudentDetail />} />
          <Route path="/" element={<Upload/>}></Route>
        </Routes>
      </Router>
    </div>
  );
};

export default App;
