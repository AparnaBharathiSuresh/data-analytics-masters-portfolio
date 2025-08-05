import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './App.css';

interface Student {
    name: string;
}

const SemesterManagement: React.FC = () => {
    const { classID } = useParams<{ classID: string }>(); // Get the class ID from the URL
    const navigate = useNavigate(); // Initialize useNavigate
    const [semesters, setSemesters] = useState<string[]>([]); // State for semesters
    const [students, setStudents] = useState<Student[]>([]); // State for students in the selected semester
    const [studentName, setStudentName] = useState<string>(''); // State for student name
    const [selectedSemester, setSelectedSemester] = useState<string>(''); // State for selected semester

    // Fetch semesters for the selected class
    useEffect(() => {
        const fetchSemesters = async () => {
            try {
                const response = await axios.get<string[]>(`http://localhost:8081/api/classes/${classID}/semesters`);
                setSemesters(response.data);
            } catch (error) {
                console.error('Error fetching semesters:', error);
            }
        };

        fetchSemesters();
    }, [classID]);

    // Fetch students for the selected semester
    const fetchStudents = async (semester: string) => {
        try {
            const response = await axios.get<Student[]>(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students`);
            setStudents(response.data);
            setSelectedSemester(semester); // Set the selected semester
        } catch (error) {
            console.error('Error fetching students:', error);
        }
    };

    // Handle adding a new student to the selected semester
    const handleAddStudent = async () => {
        if (!studentName || !selectedSemester) return;

        try {
            await axios.post(`http://localhost:8081/api/classes/${classID}/semesters/${selectedSemester}/students`, { name: studentName });
            alert('Student added successfully.');
            setStudentName(''); // Clear input after adding
            // Fetch students again to update the list
            await fetchStudents(selectedSemester);
        } catch (error) {
            const axiosError = error as { response?: { data: { message: string } } };
            console.error('Error adding student:', axiosError.response?.data.message);
            alert(`Error: ${axiosError.response?.data.message}`);
        }
    };

    // Handle navigating to the StudentDetails page
    const handleSemesterClick = (semester: string) => {
        navigate(`/student/${semester}/${classID}`); // Navigate to StudentDetails
    };

    return (
        <div>
            <h2 style= {{ backgroundColor: 'white' , color : 'Purple'}}>{classID}</h2>

            <h4 style={{ backgroundColor: 'white' , color : 'Purple'}}>Semesters</h4>
            <ul className="list-group">
                {semesters.map((semester) => (
                    <li key={semester} className="list-group-item">
                        <button onClick={() => handleSemesterClick(semester)} className="btn btn-link">
                            {semester}
                        </button>
                    </li>
                ))}
            </ul>

            {selectedSemester && (
                <div>
                    <h4>Students in {selectedSemester}</h4>
                    <ul className="list-group">
                        {students.map((student, index) => (
                            <li key={index} className="list-group-item">{student.name}</li>
                        ))}
                    </ul>

                    <div>
                        <input
                            type="text"
                            value={studentName}
                            onChange={(e) => setStudentName(e.target.value)}
                            placeholder="Student Name"
                        />
                        <button onClick={handleAddStudent}>Add Student</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SemesterManagement;
