import React from 'react';
import { useLocation } from 'react-router-dom';
import './SearchResults.css';

interface Student {
    classID: string;
    semester: string;
    studentFirstName: string;
    studentLastName: string;
    studentID: string;
    studentEmails: string[];
}

interface LocationState {
    results: Student[];
}

const SearchResults: React.FC = () => {
    const location = useLocation(); // Get location without type argument
    const results: Student[] = (location.state as LocationState)?.results || []; // Cast the state to LocationState

    return (
        <div style={{ backgroundColor: 'lightblue' }}>
            <h1 style={{color: 'Red', backgroundColor: 'white'}}>Search Results</h1>
            {results.length === 0 ? (
                <p>No results found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Class ID</th>
                            <th>Semester</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Student ID</th>
                            <th>Emails</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((student, index) => (
                            <tr key={index}>
                                <td>{student.classID}</td>
                                <td>{student.semester}</td>
                                <td>{student.studentFirstName}</td>
                                <td>{student.studentLastName}</td>
                                <td>{student.studentID}</td>
                                <td>{student.studentEmails.join(', ')}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default SearchResults;
