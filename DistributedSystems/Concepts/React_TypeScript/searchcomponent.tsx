import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SearchComponent.css';

const SearchComponent: React.FC = () => {
    const [firstName, setFirstName] = useState<string>('');
    const [lastName, setLastName] = useState<string>('');
    const [studentID, setStudentID] = useState<string>(''); // Keep it as a string for consistent input handling
    const [email, setEmail] = useState<string>('');
    const [notFound, setNotFound] = useState<boolean>(false); 
    const [errorMessage, setErrorMessage] = useState<string>('');
    const navigate = useNavigate();

    const handleSearch = async () => {
        // Clear previous messages
        setErrorMessage('');
        setNotFound(false);

        // Validate input before making the API request
        if (!firstName && !lastName && !studentID && !email) {
            setErrorMessage('Please enter at least one search criterion.');
            return;
        }

        try {
            const response = await axios.get<any[]>(`http://localhost:8081/api/search`, {
                params: { firstName, lastName, studentID, email },
            });

            // If no results, set the "not found" message
            if (Array.isArray(response.data) && response.data.length === 0) {
                setNotFound(true); // No students found
            } else {
                setNotFound(false); // Reset "not found"
                navigate('/search-results', { state: { results: response.data } });
            }
        } catch (error: any) { // Use 'any' for the error type
            // Check if the error is due to no matching students (e.g., 404 status)
            if (error.response && error.response.status === 404) {
                setNotFound(true); // No student found
            } else {
                setErrorMessage('Error during search. Please try again.');
            }
            console.error('Error during search:', error);
        }
    };

    return (
        <div style={{ color: 'Red' }}>
            <h2>Search for Students</h2>
            <input
                type="text"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
            /><br />
            <input
                type="text"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
            /><br />
            <input
                type="text" // Keep it as a string for consistent input handling
                placeholder="Student ID"
                value={studentID}
                onChange={(e) => setStudentID(e.target.value)}
            /><br />
            <input
                type="text"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            /><br />
            <button onClick={handleSearch}>Search</button>
            
            {/* Show "not found" message */}
            {notFound && <p style={{ color: 'red' }}>Student not found in any class.</p>}

            {/* Show error message for other issues */}
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        </div>
    );
};

export default SearchComponent;
