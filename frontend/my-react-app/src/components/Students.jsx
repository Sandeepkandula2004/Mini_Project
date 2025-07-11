import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const StudentDetail = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/students");
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        setStudents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) return <p>Loading students...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

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
      <div className="p-4">
        <h2 className="text-2xl font-semibold mb-4">Student Fine Records</h2>
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="border px-4 py-2 text-center">JNTU ID</th>
              <th className="border px-4 py-2 text-center">Fine Amount (₹)</th>
            </tr>
          </thead>
          <tbody>
            {students.length > 0 ? (
              students.map((student) => (
                <tr key={student.JNTU} className="border">
                  <td className="border px-4 py-2 text-center">{student.JNTU}</td>
                  <td className="border px-4 py-2 text-center">{student.fine_amount}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" className="text-center py-2">
                  No records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StudentDetail;
