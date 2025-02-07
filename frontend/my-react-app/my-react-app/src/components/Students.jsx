import React, { useEffect, useState } from "react";
import axios from "axios";

const StudentDetails = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch student details from the backend
    const fetchStudents = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/students");
        setStudents(response.data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch student details");
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (error) {
    return <div className="text-center mt-5 text-danger">{error}</div>;
  }

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Student Details</h2>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>JNTU Number</th>
            <th>Fine Amount (₹)</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student, index) => (
            <tr key={index}>
              <td>{student.JNTU}</td>
              <td>{student.fine_amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentDetails;
