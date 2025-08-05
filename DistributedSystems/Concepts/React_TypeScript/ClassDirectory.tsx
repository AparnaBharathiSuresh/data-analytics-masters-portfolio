import React, { useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useNavigate } from 'react-router-dom';
import './App.css';

const ClassDirectory: React.FC = () => {
  const [classes, setClasses] = useState<string[]>([]);
  const [newClassID, setNewClassID] = useState<string>('');
  const [selectedClassID, setSelectedClassID] = useState<string>('');
  const [newSemester, setNewSemester] = useState<string>(''); 
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchClasses = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get<string[]>('http://localhost:8081/api/classes');
        setClasses(response.data);
      } catch (error) {
        console.error('Error fetching classes:', error);
        setError('Failed to fetch classes. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchClasses();
  }, []);

  const handleClassClick = (classID: string) => {
    navigate(`/classes/${classID}`);
  };

  const handleAddClass = async () => {
    if (!newClassID) return;

    if (classes.includes(newClassID)) {
      alert('Class ID already exists. Please choose a different ID.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await axios.post('http://localhost:8081/api/classes', { classID: newClassID });
      setClasses([...classes, newClassID]);
      setNewClassID('');
      setSuccessMessage('Class added successfully.');
    } catch (error) {
    // Use a type guard to check if it's an Axios error
    if (axios.isAxiosError(error)) {
        console.error('Error adding semester:', error.response?.data.message);
        setError(`Error: ${error.response?.data.message}`);
    } else {
        console.error('Unexpected error:', error);
        setError('An unexpected error occurred');
    }
} finally {
    setLoading(false);
}
  };

  const handleAddSemester = async () => {
    if (!newSemester || !selectedClassID) return;

    setLoading(true);
    setError(null);
    try {
      await axios.post(`http://localhost:8081/api/classes/${selectedClassID}/semesters`, { semester: newSemester });
      setSuccessMessage('Semester added successfully.');
      setNewSemester('');
    } catch (error) {
    // Use a type guard to check if it's an Axios error
    if (axios.isAxiosError(error)) {
        console.error('Error adding semester:', error.response?.data.message);
        setError(`Error: ${error.response?.data.message}`);
    } else {
        console.error('Unexpected error:', error);
        setError('An unexpected error occurred');
    }
} finally {
    setLoading(false);
}
  };

  return (
    <div style={{ backgroundColor: 'lightyellow' }}>
      <h3 style={{color: 'Red', backgroundColor: 'white'}}>Classes</h3>
      {loading && <p>Loading...</p>}
      {error && <p className="text-danger">{error}</p>}
      {successMessage && <p className="text-success">{successMessage}</p>}
      <ul className="list-group">
        {classes.map(classID => (
          <li key={classID} className="list-group-item">
            <button className="btn btn-link" onClick={() => handleClassClick(classID)}>
              {classID}
            </button>
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          value={newClassID}
          onChange={(e) => setNewClassID(e.target.value)}
          placeholder="Add new class ID"
        />
        <button onClick={handleAddClass} disabled={!newClassID}>
          Add Class
        </button>
      </div>
      <h3>Add New Semester</h3>
      <div>
        <select onChange={(e) => setSelectedClassID(e.target.value)} value={selectedClassID}>
          <option value="">Select Class</option>
          {classes.map(classID => (
            <option key={classID} value={classID}>
              {classID}
            </option>
          ))}
        </select>
        <input
          type="text"
          value={newSemester}
          onChange={(e) => setNewSemester(e.target.value)}
          placeholder="New semester name"
        />
        <button onClick={handleAddSemester} disabled={!newSemester || !selectedClassID}>
          Add Semester
        </button>
      </div>
    </div>
  );
};

export default ClassDirectory;
