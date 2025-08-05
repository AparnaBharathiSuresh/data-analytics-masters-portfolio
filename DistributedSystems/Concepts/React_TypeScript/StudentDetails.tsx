import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios, { AxiosError } from 'axios';
import './SearchResults.css';

// Define a type for the student object
interface Student {
    firstName: string;
    lastName: string;
    email: string;
    studentID: string;
}

const StudentDetails: React.FC = () => {
    const { semester, classID } = useParams<{ semester: string; classID: string }>();
    const [students, setStudents] = useState<Student[]>([]);
    const [newStudent, setNewStudent] = useState<{ firstName: string; lastName: string; email: string; studentID: string }>({
        firstName: '',
        lastName: '',
        email: '',
        studentID: ''
    });
    const [removeStudentID, setRemoveStudentID] = useState<string>(''); // For removing student
    const [editStudentID, setEditStudentID] = useState<string>(''); // For editing student
    const [editStudent, setEditStudent] = useState<{ firstName: string; lastName: string; email: string }>({
        firstName: '',
        lastName: '',
        email: ''
    });

    // Fetch student details based on semester and classID
    useEffect(() => {
        const fetchStudentDetails = async () => {
            try {
                const response = await axios.get<Student[]>(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students`);
                setStudents(response.data); // Assuming response.data is an array of student objects
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Error fetching student details:', error.response?.data?.message || error.message);
                } else {
                    console.error('Unexpected error:', error);
                }
            }
        };

        fetchStudentDetails();
    }, [semester, classID]);

    // Fetch students function
    const fetchStudents = async () => {
        try {
            const response = await axios.get<Student[]>(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students`);
            setStudents(response.data);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Error fetching students:', error.response?.data?.message || error.message);
            } else {
                console.error('Unexpected error:', error);
            }
        }
    };

    // Handle adding a new student
    const handleAddStudent = async () => {
        if (!newStudent.firstName || !newStudent.lastName || !newStudent.email || !newStudent.studentID) {
            alert('All fields are required');
            return;
        }

        console.log("Sending the following data to the server:", newStudent); // Log the data

        try {
            await axios.post(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students`, newStudent);
            alert('Student added successfully.');
            // Clear input fields
            setNewStudent({ firstName: '', lastName: '', email: '', studentID: '' });
            // Fetch students again to update the list
            await fetchStudents();
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Error adding student:', error.response?.data?.message || error.message);
                alert(`Error: ${error.response?.data?.message || error.message}`);
            } else {
                console.error('Unexpected error:', error);
                alert(`Unexpected error: ${error}`);
            }
        }
    };

    // Handle removing a student by studentID
    const handleRemoveStudent = async () => {
        if (!removeStudentID) {
            alert('Please enter a Student ID to remove.');
            return;
        }

        try {
            const response = await axios.delete(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students/${removeStudentID}`);
            alert(response.data.message); // Display success message
            // Refresh the student list after removal
            await fetchStudents();
            setRemoveStudentID(''); // Clear the input field
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Error removing student:', error.response?.data?.message || error.message);
                alert(`Error: ${error.response?.data?.message || error.message}`);
            } else {
                console.error('Unexpected error:', error);
                alert(`Unexpected error: ${error}`);
            }
        }
    };

    // Handle editing a student's information
    const handleEditStudent = async () => {
        if (!editStudentID || !editStudent.firstName || !editStudent.lastName || !editStudent.email) {
            alert('All fields are required for editing.');
            return;
        }

        try {
            await axios.put(`http://localhost:8081/api/classes/${classID}/semesters/${semester}/students/${editStudentID}`, editStudent);
            alert('Student information updated successfully.');
            // Clear input fields
            setEditStudentID('');
            setEditStudent({ firstName: '', lastName: '', email: '' });
            // Fetch students again to update the list
            await fetchStudents();
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Error updating student:', error.response?.data?.message || error.message);
                alert(`Error: ${error.response?.data?.message || error.message}`);
            } else {
                console.error('Unexpected error:', error);
                alert(`Unexpected error: ${error}`);
            }
        }
    };

    return (
        <div style={{ backgroundColor: 'lightgreen' }}>
            <h2>Student Details for {semester} in {classID}</h2>
            {students.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Student ID</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {students.map((student) => (
                            <tr key={student.studentID}>
                                <td>{student.firstName}</td>
                                <td>{student.lastName}</td>
                                <td>{student.studentID}</td>
                                <td>{student.email}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No students found.</p>
            )}

            <h3>Add New Student</h3>
            <input
                type="text"
                value={newStudent.firstName}
                onChange={(e) => setNewStudent({ ...newStudent, firstName: e.target.value })}
                placeholder="First Name"
            />
            <input
                type="text"
                value={newStudent.lastName}
                onChange={(e) => setNewStudent({ ...newStudent, lastName: e.target.value })}
                placeholder="Last Name"
            />
            <input
                type="email"
                value={newStudent.email}
                onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
                placeholder="Email"
            />
            <input
                type="text"
                value={newStudent.studentID}
                onChange={(e) => setNewStudent({ ...newStudent, studentID: e.target.value })}
                placeholder="Student ID"
            />
            <button onClick={handleAddStudent}>Add Student</button>
            
            <h3>Remove Student</h3>
            <input
                type="text"
                value={removeStudentID}
                onChange={(e) => setRemoveStudentID(e.target.value)}
                placeholder="Enter Student ID to Remove"
            />
            <button onClick={handleRemoveStudent}>Remove Student</button>
            
            <h3>Edit Student</h3>
            <input
                type="text"
                value={editStudentID}
                onChange={(e) => setEditStudentID(e.target.value)}
                placeholder="Enter Student ID to Edit"
            />
            <input
                type="text"
                value={editStudent.firstName}
                onChange={(e) => setEditStudent({ ...editStudent, firstName: e.target.value })}
                placeholder="New First Name"
            />
            <input
                type="text"
                value={editStudent.lastName}
                onChange={(e) => setEditStudent({ ...editStudent, lastName: e.target.value })}
                placeholder="New Last Name"
            />
            <input
                type="email"
                value={editStudent.email}
                onChange={(e) => setEditStudent({ ...editStudent, email: e.target.value })}
                placeholder="New Email"
            />
            <button onClick={handleEditStudent}>Edit Student</button>
        </div>
    );
};

export default StudentDetails;
